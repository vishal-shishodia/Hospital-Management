from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Receptionist)
admin.site.register(Appointment)

