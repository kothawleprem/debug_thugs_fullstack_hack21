from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout

def HomeView(request):
    return render(request,'vacciapp/home.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
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
            return render(request,'vacciapp/login.html')
    context = {
        'form' : form,
    }
    return render(request,'vacciapp/register.html',context)

    
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
            msg = "Profile Updated!!!"
            customer_profile.save()
    context = {
        'form' : form,
        'add' : add
    }
    return render(request,'vacciapp/profile.html',context)

def viewSlot(request):
    pincodes = Customer.objects.filter(user=request.user).values('pincode')
    l = len(pincodes)
    if l>0:
        userPincode = pincodes[l-1].get('pincode')
        slots = Slot.objects.filter(pincode=userPincode)
        vtype = Slot.objects.values('vtype')
        context = {
            'slots' : slots,
        }
        return render(request,'vacciapp/viewSlot.html',context)
    else:
        return redirect ('profile')

def selectSlot(request,pk):
    user = request.user
    slot = Slot.objects.get(pk=pk)
    context = {
        'slot' : slot,
    }
    return render(request,'vacciapp/selectSlot.html',context)

def bookedSlot(request):
    pass

def adminViewPincode(request):
    pass

def adminCreateSlot(request):
    pass

def adminCompletedSlot(request):
    pass

