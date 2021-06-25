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
            return render(request,'vacciapp/register.html',context)
    context = {
        'form' : form,
    }
    return render(request,'vacciapp/register.html',context)

def viewSlot(request):
    userPincode = '410206'
    slots = Slot.objects.filter(pincode=userPincode)
    vtype = Slot.objects.values('vtype')
    print(vtype)
    context = {
        'slots' : slots,
    }
    return render(request,'vacciapp/viewSlot.html',context)

def selectSlot(request,pk):
    slot = Slot.objects.get(pk=pk)
    context = {
        'slot' : slot,
    }
    return render(request,'vacciapp/selectSlot.html',context)
    

def bookedSlot(request):
    pass

def viewPincode(request):
    pass

def createSlot(request):
    pass

def completedSlot(request):
    pass

