from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    aadhar = models.CharField(max_length=200,null=True)
    age = models.CharField(max_length=200,null=True)
    gender = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    vtaken = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

STATUS = (
        ('Pending','Pending'),
        ('In Process','In Process'),
        ('Completed','Completed'),
    )
class Slot(models.Model):
    
    vtype = models.CharField(max_length=200,null=True)
    date = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    addMap = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    count = models.IntegerField(null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS,default="Pending")

    # def setStatus(self):
    #     c = self.count
    #     if c == 0:
    #         status = 'In Process'
    #     return status
    
    # def save(self,*args,**kwargs):
    #     self.status = str(self.setSatus())
    #     super().save(*args, **kwargs)


    def __str__(self):
        return self.pincode

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    slot = models.ForeignKey(Slot, null=True, on_delete=models.SET_NULL)
    date_booked = models.DateTimeField(auto_now_add=True,null=True)
    

    # def setStatus(self):
    #     c = self.count
    #     if c == 0:
    #         status = 'In Process'
    #     return status
    
    # def save(self,*args,**kwargs):
    #     self.status = str(self.setSatus())
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.name