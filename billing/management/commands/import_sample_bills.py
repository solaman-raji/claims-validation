import csv
from collections import defaultdict

from django.core.management.base import BaseCommand

from billing.models import Bill, Line
from claims_validation.settings import SAMPLE_BILLS_FILE_PATH


class Command(BaseCommand):
    help = 'Import sample bills'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to import...'))
        bills = self.merge_bill()
        self.create_bill(bills)
        self.stdout.write(self.style.SUCCESS('All bills successfully imported.'))

    def merge_bill(self):
        bills = defaultdict(list)

        for row in self.read_bill(SAMPLE_BILLS_FILE_PATH):
            self.stdout.write(self.style.SUCCESS(f'{row["billid"]}, {row["procedure"]}, {row["price"]}'))
            bills[row["billid"]].append(self.get_line(row))

        return bills

    def read_bill(self, filepath):
        try:
            with open(filepath) as fp:
                reader = csv.DictReader(fp)

                for row in reader:
                    yield self.cleanup_row(row)
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'{e}'))

    def cleanup_row(self, row):
        row = dict(row)

        for key, value in row.items():
            row[key.strip()] = value.strip()

        return row

    def get_line(self, row):
        return {
            "procedure": row['procedure'],
            "price": row['price']
        }

    def create_bill(self, bills):
        for lines in bills.values():
            bill = Bill.objects.create()

            for line in lines:
                Line.objects.create(
                    bill=bill,
                    procedure=line["procedure"],
                    price=line["price"]
                )

            self.stdout.write(self.style.SUCCESS(f'Created bill {bill.id}'))
