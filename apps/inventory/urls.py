from django.urls import path
from . import views

urlpatterns = [
    # Warehouses
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/add/', views.WarehouseCreateView.as_view(), name='warehouse_add'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouses/<int:pk>/edit/', views.WarehouseUpdateView.as_view(), name='warehouse_edit'),

    # Locations
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/add/', views.LocationCreateView.as_view(), name='location_add'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('locations/<int:pk>/edit/', views.LocationUpdateView.as_view(), name='location_edit'),

    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),

    # Inventory
    path('inventory/', views.InventoryListView.as_view(), name='inventory_list'),
    path('inventory/adjust/', views.InventoryAdjustView.as_view(), name='inventory_adjust'),

    # Suppliers
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', views.SupplierCreateView.as_view(), name='supplier_add'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_edit'),

    # Purchase Orders
    path('purchases/', views.PurchaseOrderListView.as_view(), name='purchase_list'),
    path('purchases/add/', views.PurchaseOrderCreateView.as_view(), name='purchase_add'),
    path('purchases/<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='purchase_detail'),
    path('purchases/<int:pk>/edit/', views.PurchaseOrderUpdateView.as_view(), name='purchase_edit'),
    path('purchases/<int:pk>/receive/', views.PurchaseReceiveView.as_view(), name='purchase_receive'),

    # Stock Movements
    path('movements/', views.StockMovementListView.as_view(), name='movement_list'),
    path('movements/<int:pk>/', views.StockMovementDetailView.as_view(), name='movement_detail'),

    # Transfers
    path('transfers/', views.TransferListView.as_view(), name='transfer_list'),
    path('transfers/add/', views.TransferCreateView.as_view(), name='transfer_add'),
    path('transfers/<int:pk>/', views.TransferDetailView.as_view(), name='transfer_detail'),
    path('transfers/<int:pk>/process/', views.TransferProcessView.as_view(), name='transfer_process'),
]