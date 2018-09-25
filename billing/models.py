from django.db import models


class Bill(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class Line(models.Model):
    bill = models.ForeignKey(
        Bill,
        related_name='lines',
        on_delete=models.CASCADE
    )
    procedure = models.CharField(max_length=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)
