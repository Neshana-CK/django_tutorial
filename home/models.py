from django.db import models
from django.contrib.auth.models import User


class Departments(models.Model):
    dep_name = models.CharField(max_length=100)
    dep_description = models.TextField()

    def __str__(self):
        return self.dep_name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=100)
    doc_spec = models.CharField(max_length=100)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    doc_image = models.ImageField(upload_to='doctors/')

    def __str__(self):
        return self.doc_name

class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    booking_date = models.DateField()


    def __str__(self):
        return self.patient.username if self.patient else "No Patient"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ✅ FIXED REPORT MODEL
class Report(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_received")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_sent")
    report = models.FileField(upload_to='reports/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username}"