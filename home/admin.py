from django.contrib import admin
from .models import Departments, Doctor, Booking,Profile, Report


admin.site.register(Departments)
admin.site.register(Doctor)
admin.site.register(Booking)
admin.site.register(Profile)
admin.site.register(Report)