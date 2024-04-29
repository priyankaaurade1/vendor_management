from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50,unique=True)
    vendor_name = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    items = models.CharField(max_length=50)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()