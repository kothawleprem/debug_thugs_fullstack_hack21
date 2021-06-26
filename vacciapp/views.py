from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from .filters import SlotFilter, PincodeFilter
from django.contrib.auth.decorators import login_required

import requests
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def HomeView(request):
    return render(request,'vacciapp/home.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            if request.user.is_staff:
                return redirect('adminViewPincode')
            else:
                return redirect('viewSlot')
    return render(request, 'vacciapp/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

def registerView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registered Successfully')
            user = form.save()
            return redirect('login')
    context = {
        'form' : form,
    }
    return render(request,'vacciapp/register.html',context)

@login_required(login_url='login')   
def profile(request):
    try:
        add = Customer.objects.filter(user=request.user)
    except:
        pass
    form = CustomerProfileForm()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            aadhar = form.cleaned_data['aadhar']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            vtaken = form.cleaned_data['vtaken']
            email = request.user.email
            customer_profile = Customer(user=usr,name=name,phone=phone,aadhar=aadhar,age=age,gender=gender,address=address,city=city,state=state,pincode=pincode,vtaken=vtaken,email=email)
            customer_profile.save()
            return redirect('viewSlot')
    context = {
        'form' : form,
        'add' : add
    }
    return render(request,'vacciapp/profile.html',context)

@login_required(login_url='login') 
def viewSlot(request):
    bs = Booking.objects.filter(user=request.user)
    pincodes = Customer.objects.filter(user=request.user).values('pincode')
    l = len(pincodes)
    if l>0:
        userPincode = pincodes[l-1].get('pincode')
        slots = Slot.objects.filter(pincode=userPincode)
        counts = Slot.objects.filter(count__gte=1).filter(pincode=userPincode)
        context = {
            'slots' : counts,

            }
        return render(request,'vacciapp/viewSlot.html',context)
    else:
        return redirect ('profile')
    

            
@login_required(login_url='login') 
def selectSlot(request,pk):
    user = request.user
    slot = Slot.objects.get(pk=pk)
    address_dict = Slot.objects.values('address').get(pk=pk)
    address = address_dict.get('address')
    city_dict = Slot.objects.values('city').get(pk=pk)
    city = city_dict.get('city')
    state_dict = Slot.objects.values('state').get(pk=pk)
    state = state_dict.get('state')
    
    al = address.split(" ")
    cl = city.split(" ")
    sl = state.split(" ")
    final = ""
    for a in al:
        final = final + a + "+"
    for c in cl:
        final = final + c + "+"
    for s in sl:
        final = final + s + "+"
    if "," in final:
        st = final.replace(",","")
        st = st + "India"
    else:
        st = final + "India"

    link = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBonEm9k9dZ4T9k6cZHWGzCYGupxNQgwBc&q="+st
 
    context = {
        'slot' : slot,
        'link' : link
    }
    return render(request,'vacciapp/selectSlot.html',context)

@login_required(login_url='login') 
def orderSlot(request,pk):
    add = Customer.objects.filter(user=request.user)
    usr = request.user
    slot = Slot.objects.get(pk=pk)
    address_dict = Slot.objects.values('address').get(pk=pk)
    address = address_dict.get('address')
    city_dict = Slot.objects.values('city').get(pk=pk)
    city = city_dict.get('city')
    state_dict = Slot.objects.values('state').get(pk=pk)
    state = state_dict.get('state')
    
    al = address.split(" ")
    cl = city.split(" ")
    sl = state.split(" ")
    final = ""
    for a in al:
        final = final + a + "+"
    for c in cl:
        final = final + c + "+"
    for s in sl:
        final = final + s + "+"
    if "," in final:
        st = final.replace(",","")
        st = st + "India"
    else:
        st = final + "India"

    link = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBonEm9k9dZ4T9k6cZHWGzCYGupxNQgwBc&q="+st
  
    if request.method == 'POST':
        custid = request.POST.get('custid')
        customer = Customer.objects.get(id=custid)     
        Booking(user=usr,customer=customer,slot=slot).save()
        count = Slot.objects.values('count').get(pk=pk)
        if count.get('count') - 1 == 0:
            slot.status = 'In Process'
        slot.count = count.get('count') - 1
        email_dict = Customer.objects.values('email').get(id=custid)
        email = email_dict.get('email')
        name_dict = Customer.objects.values('name').get(id=custid)
        name = name_dict.get('name')
        vtype_dict = Slot.objects.values('vtype').get(pk=pk)
        vtype = vtype_dict.get('vtype')
        date_dict = Slot.objects.values('date').get(pk=pk)
        date = date_dict.get('date')
        slot.save()
        toemail = email
        # print(date)
        if count.get('count') - 1 != 0:
            subject, from_email, to = 'Your Slot has been booked!!', settings.EMAIL_HOST_USER,toemail
            text_content = f"Hello {name},Your vaccination slot has been booked for {vtype} vaccine on {date}. The confirmation is currently pending as {count.get('count') - 1} more should book slot so that it can be confirmed. You will receive confirmation email regarding the same. Kindly visit http://127.0.0.1:8000/bookedSlot for more information."
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.send()
        if count.get('count') - 1 == 0:
            all_bk = Booking.objects.filter(slot=slot).values('customer')
            cust = []
            for i in all_bk:
                cust.append(i.get('customer'))
            cust_id = []
            for j in cust:
                if j in cust_id:
                    continue
                else:
                    cust_id.append(j)
            for ids in cust_id:
                email_dict = Customer.objects.values('email').get(id=ids)
                email = email_dict.get('email')
                name_dict = Customer.objects.values('name').get(id=ids)
                name = name_dict.get('name')
                toemail = email
                subject, from_email, to = 'Your Slot has been Confirmed!!', settings.EMAIL_HOST_USER,toemail
                text_content = f"Hello {name},Your vaccination slot has been Confirmed for {vtype} vaccine on {date}. Kindly visit http://127.0.0.1:8000/bookedSlot for more information."
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.send()
        return redirect ('bookedSlot')
    context = {
        'link':link,
        'slot' : slot,
        'add':add,
    }
    return render(request,'vacciapp/orderSlot.html',context)

@login_required(login_url='login') 
def bookedSlot(request):
    bs = Booking.objects.filter(user=request.user)
    try:
        pk_dict =  Booking.objects.filter(user=request.user).values('slot')
        p = pk_dict.values('slot_id')
        pk = p[0]['slot_id']
        address_dict = Slot.objects.values('address').get(pk=pk)
        address = address_dict.get('address')
        city_dict = Slot.objects.values('city').get(pk=pk)
        city = city_dict.get('city')
        state_dict = Slot.objects.values('state').get(pk=pk)
        state = state_dict.get('state')
        
        al = address.split(" ")
        cl = city.split(" ")
        sl = state.split(" ")
        final = ""
        for a in al:
            final = final + a + "+"
        for c in cl:
            final = final + c + "+"
        for s in sl:
            final = final + s + "+"
        if "," in final:
            st = final.replace(",","")
            st = st + "India"
        else:
            st = final + "India"

        link = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBonEm9k9dZ4T9k6cZHWGzCYGupxNQgwBc&q="+st
        print(link)
    except:
        link = 0
        pass
    context = {
        'bs' : bs,
        'link' : link
    }
    return render(request,'vacciapp/bookedSlot.html',context)

@login_required(login_url='login') 
def deleteBooking(request,pk):
    Booking.objects.get(id=pk).delete()
    return render(request,'vacciapp/deleteBooking.html')

@login_required(login_url='login') 
def adminViewPincode(request ):
    customers = Customer.objects.all()
    myPincodeFilter = PincodeFilter(request.GET,queryset=customers)
    customers = myPincodeFilter.qs
    pincodes = customers.values('pincode')
    pins = []
    count = []
    pincd = []
    for i in pincodes:
        pins.append(i.get('pincode'))
    
    done = []
    pin_dict = dict()
    for j in pins:
        if j in done:
            continue
        else:
            occ = pins.count(j)
            pin_dict[f'{j}'] = occ

    pin_sort = sorted(pin_dict.items(),key=lambda x: x[1], reverse=True)

    pincd = []
    count = []
    for k in pin_sort:
        pincd.append(k[0])
        count.append(k[1])

    slots = Slot.objects.all().order_by('-date_created')
    mySlotFilter = SlotFilter(request.GET,queryset=slots)
    slots = mySlotFilter.qs

    context = {
        'customers' : customers,
        'pincd' : pincd,
        'count' : count,
        'slots' : slots,
        'mySlotFilter' : mySlotFilter,
        'myPincodeFilter' : myPincodeFilter,
    }
    return render(request,'vacciapp/adminViewPincode.html',context)
    
@login_required(login_url='login') 
def adminCreateSlot(request):
    form = AdminCreateSlotForm()
    if request.method == 'POST':
        form = AdminCreateSlotForm(request.POST)
        if form.is_valid():
            vtype = form.cleaned_data['vtype']
            date = form.cleaned_data['date']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            count = form.cleaned_data['count']
            create_slot = Slot(vtype=vtype,date=date,address=address,city=city,state=state,pincode=pincode,count=count)
            create_slot.save()
            return redirect ('adminViewPincode')
    context = {
        'form' : form,
        
    }
    return render(request,'vacciapp/adminCreateSlot.html',context)

@login_required(login_url='login') 
def adminUpdateSlot(request,pk):
    slot = Slot.objects.get(id=pk)
    form = AdminCreateSlotForm(instance=slot)
    form = AdminCreateSlotForm()
    context = {
        'form' : form,
    }
    if request.method == 'POST':
        form = AdminCreateSlotForm(request.POST,instance=slot)
        if form.is_valid():
            form.save()
            return redirect('adminViewPincode')
    return render(request,'vacciapp/adminCreateSlot.html',context)

@login_required(login_url='login') 
def adminDeleteSlot(request,pk):
    try:
        Booking.objects.get(slot=pk).delete()
    except:
        pass
    Slot.objects.get(id=pk).delete()
    return render(request,'vacciapp/adminDeleteSlot.html')

@login_required(login_url='login') 
def adminCompletedSlot(request):
    
    slots = Slot.objects.filter(status='In Process')

    context = {
        'slots' : slots,
    }
    return render(request,'vacciapp/adminCompletedSlot.html',context)

@login_required(login_url='login') 
def adminUpdateStatus(request,pk):
    slot = Slot.objects.get(id=pk)
    slotn = Slot.objects.filter(id=pk)
    if request.method == 'POST':
        setstatus = request.POST.get('setstatus')
        status = setstatus
        slot.status = setstatus
        slot.save()
        return redirect ('/')
    context = {
        'slotn' : slotn
    }
    return render(request,'vacciapp/adminUpdateStatus.html',context)


