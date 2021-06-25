from django.contrib import admin

from . models import *

@admin.register(Customer)
class CustomerModel(admin.ModelAdmin):
    list_display = ['id','user','name','phone','email','aadhar','age','gender','address','city','state','pincode','vtaken']

@admin.register(Slot)
class SlotModel(admin.ModelAdmin):
    list_display = ['id','vtype','date','address','city','state','pincode','date_created','addMap']

@admin.register(Booking)
class BookingModel(admin.ModelAdmin):
    list_display = ['id','user','customer','slot','date_booked','status']