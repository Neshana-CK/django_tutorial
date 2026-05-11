from django import forms
from django.contrib.auth.models import User
from .models import Booking, Report, Departments


# ---------------- PATIENT SIGNUP ----------------
class PatientSignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )

    class Meta:

        model = User

        fields = ['username', 'email', 'password']

        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),

        }

# ---------------- DOCTOR SIGNUP ----------------
from django import forms
from django.contrib.auth.models import User
class DoctorSignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )

    class Meta:
        model = User

        fields = ['username', 'email', 'password']

        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),

        }

# ---------------- LOGIN ----------------
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# ---------------- BOOKING ----------------
class BookingForm(forms.ModelForm):

    booking_date = forms.DateField(

        widget=forms.DateInput(attrs={

            'type': 'date',

            'class': 'form-control'

        })

    )

    class Meta:

        model = Booking

        fields = ['department', 'doctor', 'booking_date']

        widgets = {

            'department': forms.Select(attrs={
                'class': 'form-control'
            }),

            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),

        }
# ---------------- REPORT (FIXED PROPERLY) ----------------
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['patient', 'description', 'report']