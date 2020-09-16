from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *
app_name='core'
urlpatterns = [
    path('', Home,name='home'),
    path('index', Index,name='index'),
    path('register/',CreateUser,name='register'),
    path('register_doctor/',RegisterDoctor,name='register_doctor'),
    path('register_receptionist/',RegisterReceptionist,name='register_receptionist'),
    path('adminhome/',AdminHome,name='adminhome'),
    path('receptionisthome/',ReceptionistHome,name='receptionisthome'),
    path('doctorhome/',DoctorHome,name='doctorhome'),
    path('login/',LoginView.as_view(template_name='core/login.html'),name='login'),
    path('logout/',LogOut,name='logout'),
    path('login_success/',LoginSuccess,name='login_success'),
    path('deleteappointment/<str:pk>/',AppointmentDelete,name='deleteappointment'),
    path('updateappointment/<str:pk>/',AppointmentUpdateView.as_view(),name='updateappointment'),
    path('addappointment/',AddAppointment,name='addappointment'),
    path('allappointment/',AllAppointments,name='allappointment'),
]