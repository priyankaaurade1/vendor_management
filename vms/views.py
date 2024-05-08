from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from django.shortcuts import render,redirect
from .models import Vendor,PurchaseOrder,HistoricalPerformance
from django.contrib import messages
from .serializers import VendorSerializer,PurchaseOrderSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .forms import VendorForm,PurchaseOrderForm
import json
from rest_framework.views import APIView
from django.core.serializers import serialize
from django.db.models import Avg, F, ExpressionWrapper, fields
from django.utils import timezone


def index(request):
    return render(request, 'index.html')

# vendor logic
def save_vendor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_details = request.POST.get('contact_details')
        address = request.POST.get('address')
        vendor_code = request.POST.get('vendor_code')
        on_time_delivery_rate = request.POST.get('on_time_delivery_rate')
        quality_rating_avg = request.POST.get('quality_rating_avg')
        average_response_time = request.POST.get('average_response_time')
        fulfillment_rate = request.POST.get('fulfillment_rate')
        
        try:
            vendor = Vendor.objects.create(
                name=name,
                contact_details=contact_details,
                address=address,
                vendor_code=vendor_code,
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=quality_rating_avg,
                average_response_time=average_response_time,
                fulfillment_rate=fulfillment_rate
            )
            messages.success(request, 'Vendor details added successfully')
            return redirect('vendor_details') 
        except Exception as e:
            messages.error(request, str(e)) 
            return redirect('save_vendor')
    else:
        return render(request, 'vendor/create_vendor.html')

def list_vendors(request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_vendor_details(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    serializer = VendorSerializer(vendor)
    return JsonResponse(serializer.data)

def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor data updated successfully.')
            return redirect('edit_vendor', vendor_id=vendor_id)
    else:
        form = VendorForm(instance=vendor) 
    context = {
        'vendor_id': vendor_id,
        'vendor': vendor,
        'form': form,
    }
    return render(request, 'vendor/edit_vendor.html', context)
    
def vendor_details(request):
    data = Vendor.objects.all()
    context ={
        'data':data,
    }
    return render(request, 'vendor/view_vendor.html', context)

def delete_vendor(request, vendor_id):
    if request.method == 'POST':
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor.delete()
        return redirect('vendor_details')  
    else:
        pass

# purchase order logic
def create_purchase_order(request):
    vendors = Vendor.objects.all()
    if request.method=='POST':
        po_number = request.POST.get('po_number')
        vendor_id = request.POST.get('vendor')
        order_date = request.POST.get('order_date')
        delivery_date = request.POST.get('delivery_date')
        items = request.POST.get('items')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status')
        quality_rating = request.POST.get('quality_rating')
        issue_date = request.POST.get('issue_date')
        acknowledgment_date = request.POST.get('acknowledgment_date')

        try:
            Purchaseorder = PurchaseOrder.objects.create(
                po_number=po_number,
                vendor_id=vendor_id,
                order_date=order_date,
                delivery_date=delivery_date,
                items=items,
                quantity=quantity,
                status=status,
                quality_rating=quality_rating,
                issue_date=issue_date,
                acknowledgment_date=acknowledgment_date
            )
            messages.success(request, 'Purchase order created successfully')
            return redirect('create_purchase_order') 
        except Exception as e:
            messages.error(request, str(e)) 
            return render(request, 'order/create_purchase_order.html')
    else:
        return render(request, 'order/create_purchase_order.html', {'vendors': vendors})
    
def list_purchase_orders(request):
    vendor_id = request.GET.get('vendor')
    if vendor_id:
        purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    else:
        purchase_orders = PurchaseOrder.objects.all()

    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_purchase_order_details(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    serializer = PurchaseOrderSerializer(purchase_order)
    return JsonResponse(serializer.data)

def update_purchase_order(request, po_id):
    order = get_object_or_404(PurchaseOrder, pk=po_id)
    
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=order)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, 'Order data updated successfully.')
            return redirect('order_details') 
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = PurchaseOrderForm(instance=order) 

    vendors = Vendor.objects.all()  
    context = {
        'po_id': po_id,
        'order': order,
        'form': form,
        'vendors': vendors, 
    }
    return render(request, 'order/update_purchase_order.html', context)

def order_details(request):
    data = PurchaseOrder.objects.all()
    context ={
        'data':data,
    }
    return render(request, 'order/view_orders.html', context)

def delete_order(request, po_id):
    if request.method == 'POST':
        order = PurchaseOrder.objects.get(pk=po_id)
        order.delete()
        return redirect('order_details')  
    else:
        pass

def historical_details(request):
    data = HistoricalPerformance.objects.all()
    context ={
        'data':data,
    }
    return render(request, 'performance/view_performance.html', context)

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        
        # On-Time Delivery Rate Calculation
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = on_time_delivered_pos / total_completed_pos if total_completed_pos > 0 else 0
        
        # Quality Rating Average Calculation
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0
        
        # Average Response Time Calculation
        avg_response_time_timedelta = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(
            avg_response_time=ExpressionWrapper(
                Avg(F('acknowledgment_date') - F('issue_date')),
                output_field=fields.DurationField()
            )
        )['avg_response_time']

        # Convert avg_response_time_timedelta to seconds or set it to 0 if None
        avg_response_time_seconds = avg_response_time_timedelta.total_seconds() if avg_response_time_timedelta else 0

        # Fulfillment Rate Calculation
        total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        fulfillment_rate = fulfilled_pos / total_pos if total_pos > 0 else 0
        
        # Return performance metrics along with other data
        context = {
            'vendor': vendor,
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time_seconds,  # No need to call total_seconds() again
            'fulfillment_rate': fulfillment_rate,
        }
        
        return render(request, 'performance/performance.html', context)
