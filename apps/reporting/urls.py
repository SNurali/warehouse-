from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    path('sales/', views.SalesReportView.as_view(), name='sales_report'),
    path('purchases/', views.PurchaseReportView.as_view(), name='purchase_report'),
    path('movements/', views.MovementReportView.as_view(), name='movement_report'),
    path('custom/', views.CustomReportView.as_view(), name='custom_report'),
]