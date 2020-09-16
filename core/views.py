from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView , DeleteView
from django.contrib.auth.decorators import login_required
from .models import *
from.forms import *

# Create your views here.
def Home(request):
	return render(request,'core/home.html')

@login_required
def Index(request):
	appointments = Appointment.objects.filter(user=request.user)
	return render(request, 'core/index.html', {'appointments': appointments})

@login_required
def AdminHome(request):
	return render(request, 'core/admin_home.html')

@login_required
def DoctorHome(request):
	user=request.user
	person=Person(user=user)
	doctor=Doctor.objects.get(person=person)
	appointments=Appointment.objects.filter(Doctor=doctor)
	return render(request,'core/doctorhome.html',{'appointments':appointments})

@login_required
def ReceptionistHome(request):
	user=request.user
	person=Person.objects.get(user=user)
	receptionist=Receptionist.objects.filter(person=person)
	appointments=Appointment.objects.all()
	return render(request,'core/receptionisthome.html',{'appointments':appointments})

def CreateUser(request):
	context={}
	if request.POST:
		u_form=UserForm(request.POST)
		p_form=PatientForm(request.POST)
		if u_form.is_valid() and p_form.is_valid():
			user=u_form.save(commit=False)
			username=u_form.cleaned_data['username']
			password=u_form.cleaned_data['password']
			user.set_password(password)
			user.save()
			person=Person(user=user)
			person.save()
			patient=p_form.save(commit=False)
			patient.person=Person.objects.get(user=user)
			patient.save()
			account=authenticate(username=username,password=password)
			if user:
				login(request,account)
				return redirect('core:index')
		else:
			context['u_form']=u_form
			context['p_form']=p_form
	else:
		u_form=UserForm()
		p_form=PatientForm()
		context['u_form']=u_form
		context['p_form']=p_form
	return render(request,'core/register.html',context)

def RegisterDoctor(request):
	context={}
	if request.POST:
		u_form=UserForm(request.POST)
		d_form=DoctorForm(request.POST)
		if u_form.is_valid() and d_form.is_valid():
			user=u_form.save(commit=False)
			username=u_form.cleaned_data['username']
			password=u_form.cleaned_data['password']
			user.set_password(password)
			user.save()
			person=Person(user=user)
			person.type=1
			person.save()
			doctor = d_form.save(commit=False)
			doctor.person=Person.objects.get(user=user)
			doctor.save()
			account=authenticate(username=username,password=password)
			if user:
				login(request,account)
				return redirect('core:adminhome')
		else:
			context['u_form']=u_form
			context['d_form']=d_form
	else:
		u_form=UserForm()
		d_form=DoctorForm()
		context['u_form']=u_form
		context['d_form']=d_form
	return render(request,'core/doctor_register.html',context)

def RegisterReceptionist(request):
	context={}
	if request.POST:
		u_form=UserForm(request.POST)
		d_form=ReceptionistForm(request.POST)
		if u_form.is_valid() and d_form.is_valid():
			user=u_form.save(commit=False)
			username=u_form.cleaned_data['username']
			password=u_form.cleaned_data['password']
			user.set_password(password)
			user.save()
			person=Person(user=user)
			person.type=2
			person.save()
			receptionist = d_form.save(commit=False)
			receptionist.person=Person.objects.get(user=user)
			receptionist.save()
			account=authenticate(username=username,password=password)
			if user:
				login(request,account)
				return redirect('core:adminhome')
		else:
			context['u_form']=u_form
			context['d_form']=d_form
	else:
		u_form=UserForm()
		d_form=ReceptionistForm()
		context['u_form']=u_form
		context['d_form']=d_form
	return render(request,'core/doctor_register.html',context)

@login_required
def AddAppointment(request):
	if not request.user.is_authenticated:
		return render(request, 'core/login.html')
	else:
		if request.POST:
			form = AppointmentForm(request.POST or None)
			if form.is_valid():
				appointment = form.save(commit=False)
				appointment.user = request.user
				appointment.save()
				appointments = Appointment.objects.filter(user=request.user)
				return render(request, 'core/index.html', {'appointments': appointments})
			context = {"form": form}
		else:
			form = AppointmentForm()
			context = {"form": form}
	return render(request, 'core/appointment_form.html', context)


def AppointmentDelete(request,pk):
	appointment=Appointment.objects.get(id=pk)
	if request.POST:
		appointment.delete()
		return redirect('core:index')
	return render(request,'core/delete.html',{'appointment':appointment})


class AppointmentUpdateView(UpdateView):
	model = Appointment
	pk_url_kwargs='pk'
	fields = ['user', 'Doctor', 'Date', 'status']
	success_url = reverse_lazy('core:receptionisthome')

@login_required
def LoginSuccess(request):
	if request.user.is_superuser:
		return redirect("core:adminhome")
	person=Person.objects.get(user=request.user)
	if person.type == 1:
		return redirect("core:doctorhome")
	if person.type == 2:
		return redirect("core:receptionisthome")
	else:
		return redirect("core:index")

def LogOut(request):
	logout(request)
	return redirect('core:home')

def AllAppointments(request):
	appointments = Appointment.objects.all()
	return render(request, 'core/all_appointments.html', {'appointments': appointments})