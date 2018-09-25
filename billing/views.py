import csv

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from billing.models import Bill, Line
from billing.serializers import BillListSerializer, BillDetailSerializer, BillValidateSerializer
from claims_validation.custom_exception import InvalidParameter
from claims_validation.settings import EXCLUSION_RULES_FILE_PATH
from claims_validation.utils import get_object_by_pk


class ApiRoot(generics.GenericAPIView):

    def get(self, request):
        return Response({
            'bills': reverse('bill-list', request=request),
        })


class BillList(APIView):

    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillListSerializer(bills, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if 'lines' not in request.data:
            raise InvalidParameter("'lines' field is required")

        lines = request.data.get("lines")

        if lines:
            bill = Bill.objects.create()

            for line in lines:
                Line.objects.create(
                    bill=bill,
                    procedure=line["procedure"],
                    price=line["price"]
                )
        else:
            raise InvalidParameter("'lines' cannot be null or empty")

        serializer = BillListSerializer(bill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BillDetail(APIView):

    def get(self, request, pk):
        bill = get_object_by_pk(Bill, pk)
        serializer = BillDetailSerializer(bill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BillValidate(APIView):

    def get(self, request, pk):
        bill = get_object_by_pk(Bill, pk)
        serializer = BillValidateSerializer(bill, context={'request': request})
        data = serializer.data

        # Exclusion process
        exclusion_rules = self.get_exclusion_rules()
        data['lines'] = self.get_valid_lines(data['lines'], exclusion_rules)

        return Response(data, status=status.HTTP_200_OK)

    def get_exclusion_rules(self):
        with open(EXCLUSION_RULES_FILE_PATH) as fp:
            reader = csv.reader(fp, delimiter=",")
            return [(row[0].strip(), row[1].strip()) for row in reader]

    def get_valid_lines(self, lines, exclusion_rules):
        for first_procedure, second_procedure in exclusion_rules:

            # First procedure lines and max price
            first_procedure_lines = self.get_lines_by_procedure(lines, first_procedure)
            first_procedure_price = self.get_max_price(first_procedure_lines)

            # Second procedure lines and max price
            second_procedure_lines = self.get_lines_by_procedure(lines, second_procedure)
            second_procedure_price = self.get_max_price(second_procedure_lines)

            lines = self.exclusion(
                        lines,
                        first_procedure_lines,
                        second_procedure_lines,
                        first_procedure_price,
                        second_procedure_price
                    )

        return lines

    def get_lines_by_procedure(self, lines, procedure):
        return [line for line in lines if line['procedure'] == procedure]

    def get_max_price(self, lines):
        return max([line['price'] for line in lines], default='0')

    def exclusion(
        self,
        lines,
        first_procedure_lines,
        second_procedure_lines,
        first_procedure_price,
        second_procedure_price
    ):
        if len(first_procedure_lines):
            if first_procedure_price >= second_procedure_price:
                lines = self.exclude_lines(lines, second_procedure_lines)
            else:
                lines = self.exclude_lines(lines, first_procedure_lines)

        return lines

    def exclude_lines(self, lines, excluded_lines):
        return [line for line in lines if line not in excluded_lines]
