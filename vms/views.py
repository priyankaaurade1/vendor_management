from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import render,redirect
from .models import Vendor
from django.contrib import messages
from .serializers import VendorSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import VendorForm

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
        messages.success(request, 'Vendor data saved successfully.')
        return redirect('/api/vendors/')
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
            print(form.errors) 
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