from django.contrib import admin
from .models import Fisioterapist, Appointment
from user.models import User

admin.site.register(User)
admin.site.register(Fisioterapist)
admin.site.register(Appointment)


# Register your models here.
