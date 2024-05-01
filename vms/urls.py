from django.urls import path,include
from . import views
urlpatterns = [
    path('api/vendors/', views.save_vendor, name='save_vendor'),
    path('api/vendors/list/', views.list_vendors, name='list_vendors'),
    path('api/vendors/<int:vendor_id>/', views.get_vendor_details, name='get_vendor_details'),
    path('edit_vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('vendor_details', views.vendor_details, name='vendor_details'),
]