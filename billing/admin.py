from django.contrib import admin

from billing.models import Bill, Line


class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at',)


class LineAdmin(admin.ModelAdmin):
    list_display = ('id', 'bill_id', 'procedure', 'price')


admin.site.register(Bill, BillAdmin)
admin.site.register(Line, LineAdmin)
