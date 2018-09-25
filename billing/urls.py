from django.urls import path

from billing.views import BillList, BillDetail, BillValidate, ApiRoot

urlpatterns = [
    path('', ApiRoot.as_view()),
    path('bills/', BillList.as_view(), name='bill-list'),
    path('bills/<int:pk>/', BillDetail.as_view()),
    path('bills/<int:pk>/validate/', BillValidate.as_view()),
]
