from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django .forms import ModelForm
from .models import *

class CreateUserForm(UserCreationForm):
    # name =  forms.CharField(max_length=100)
    # phone = forms.CharField(max_length=100)
    # aadhar = forms.CharField(max_length=100)
    # age = forms.CharField(max_length=100)
    # gender = forms.CharField(max_length=100)
    # address = forms.CharField(max_length=100)
    # city = forms.CharField(max_length=100)
    # state = forms.CharField(max_length=100)
    # pincode = forms.CharField(max_length=100)
    # vtaken = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        # 'name','phone','aadhar','age','gender','address','city','state','pincode','vtaken'

class PassChangeForm(PasswordChangeForm):
    pass

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','phone','aadhar','age','gender','address','city','state','pincode','vtaken']
        widgets = {'name':forms.TextInput(),'phone':forms.TextInput(),'aadhar':forms.TextInput(),'age':forms.TextInput(),'gender':forms.TextInput(),'address':forms.TextInput(),'city':forms.TextInput(),'state':forms.TextInput(),'pincode':forms.TextInput(),'vtaken':forms.TextInput()}

class AdminCreateSlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['vtype','date','address','city','state','pincode','addMap']

class AdminCreateSlotFormPin(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['vtype','date','address','city','state','addMap']
