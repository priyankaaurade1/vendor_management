from django.urls import path,include
from . import views
urlpatterns = [
    # Vendor Profile Management:
    path('', views.index, name='index'),
    path('api/vendors/', views.save_vendor, name='save_vendor'),
    path('api/vendors/list/', views.list_vendors, name='list_vendors'),
    path('vendor_details', views.vendor_details, name='vendor_details'),
    path('api/vendors/<int:vendor_id>/', views.get_vendor_details, name='get_vendor_details'),
    path('edit_vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('vendor/<int:vendor_id>/delete/', views.delete_vendor, name='delete_vendor'),

    # Purchase Order Tracking
    path('api/purchase_orders/', views.create_purchase_order, name='create_purchase_order'),
    path('api/purchase_orders/list/', views.list_purchase_orders, name='list_purchase_orders'),
    path('api/purchase_orders/<int:po_id>/', views.get_purchase_order_details, name='get_purchase_order_details'),
    path('edit_orders/<int:po_id>/', views.update_purchase_order, name='update_purchase_order'),
    path('order/<int:po_id>/delete/', views.delete_order, name='delete_order'),
    path('order_details', views.order_details, name='order_details'),
    path('historical_details', views.historical_details, name='historical_details'),
    path('api/vendors/<int:vendor_id>/performance', views.VendorPerformanceView.as_view()),

]