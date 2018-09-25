from rest_framework import serializers

from billing.models import Bill


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

    def get_line(self, obj):
        return {"procedure": obj.procedure, "price": f'{obj.price:.2f}'}

    def get_lines(self, obj):
        lines = obj.lines.all()
        return [self.get_line(line) for line in lines]

    def get_absolute_uri(self):
        request = self.context.get('request')
        return request.build_absolute_uri()

    def get_detail_url(self, obj):
        absolute_uri = self.get_absolute_uri()
        return f'{absolute_uri}{obj.id}/'

    def get_validate_url(self, obj):
        absolute_uri = self.get_absolute_uri()
        return f'{absolute_uri}{obj.id}/validate/'

    def get_validate_url_for_detail(self):
        absolute_uri = self.get_absolute_uri()
        return f'{absolute_uri}validate/'


class BillListSerializer(BillSerializer):
    def to_representation(self, obj):
        return {
            "id": obj.id,
            "lines": self.get_lines(obj),
            "created_at": obj.created_at.isoformat(),
            "_links": {
                "details": self.get_detail_url(obj),
                "validate": self.get_validate_url(obj),
            },
        }


class BillDetailSerializer(BillSerializer):
    def to_representation(self, obj):
        return {
            "id": obj.id,
            "lines": self.get_lines(obj),
            "created_at": obj.created_at.isoformat(),
            "_links": {
                "validate": self.get_validate_url_for_detail(),
            },
        }


class BillValidateSerializer(BillSerializer):
    def to_representation(self, obj):
        return {
            "id": obj.id,
            "lines": self.get_lines(obj),
            "created_at": obj.created_at.isoformat(),
        }
