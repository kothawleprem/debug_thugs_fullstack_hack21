from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView,name='home'),
    path('register/',views.registerView,name='register'),
    path('login/',views.loginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('viewSlot',views.viewSlot,name='viewSlot'),
    path('selectSlot/<int:pk>',views.selectSlot,name='selectSlot'),
    path('orderSlot/<int:pk>',views.orderSlot,name='orderSlot'),
    path('deleteBooking/<int:pk>',views.deleteBooking,name='deleteBooking'),
    path('adminViewPincode',views.adminViewPincode,name='adminViewPincode'),
    path('bookedSlot',views.bookedSlot,name='bookedSlot'),
    path('adminCreateSlot/<str:pin>',views.adminCreateSlot,name='adminCreateSlot'),
    path('adminUpdateSlot/<str:pk>/',views.adminUpdateSlot,name ='adminUpdateSlot'),
    path('adminDeleteSlot/<str:pk>/',views.adminDeleteSlot,name ='adminDeleteSlot'),
    path('adminCompletedSlot',views.adminCompletedSlot,name='adminCompletedSlot'),
    path('adminUpdateStatus/<str:pk>/',views.adminUpdateStatus,name='adminUpdateStatus')


]
