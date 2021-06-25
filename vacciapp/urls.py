from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView,name='home'),
    path('register/',views.registerView,name='register'),
    path('login/',views.loginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('viewSlot',views.viewSlot,name='viewSlot'),
    path('selectSlot/<int:pk>',views.selectSlot,name='selectSlot')
]
