from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from .models import Departments, Doctor, Booking, Report, Profile
from .forms import (
    BookingForm,
    PatientSignupForm,
    DoctorSignupForm,
    LoginForm,
    ReportForm
)

# ================= BASIC PAGES =================

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='login')
def departments(request):
    return render(request, 'departments.html', {
        'dept': Departments.objects.all()
    })


@login_required(login_url='login')
def doctors(request):
    return render(request, 'doctors.html', {
        'doc': Doctor.objects.all()
    })


# ================= SIGNUP =================

def patient_signup(request):
    form = PatientSignupForm()

    if request.method == 'POST':
        form = PatientSignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # FIX: avoid duplicate profile
            profile, created = Profile.objects.get_or_create(user=user)

            profile.role = 'patient'
            profile.save()


            return redirect('login')

    return render(request, 'patient_signup.html', {'form': form})

def doctor_signup(request):
    form = DoctorSignupForm()

    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = 'doctor'
            profile.save()

            return redirect('login')

    return render(request, 'doctor_signup.html', {'form': form})

# ================= LOGIN =================

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)

                profile = Profile.objects.get(user=user)

                if profile.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif profile.role == 'patient':
                    return redirect('home')

            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Invalid username or password'
                })

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


# ================= BOOKING =================


@login_required(login_url='login')
def booking(request):

    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # attach logged-in user
            booking.patient = request.user
            booking.save()

            # EMAIL (safe + simple)
            if request.user.email:
                send_mail(
                    subject="Appointment Confirmed",
                    message=f"""
Hi {request.user.username},

Your appointment is confirmed.

Doctor: {booking.doctor.doc_name}
Department: {booking.department.dep_name}
Date: {booking.booking_date}

Thank you.
""",
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=True
                )

            return redirect('booking_success')

    return render(request, 'booking.html', {'form': form})


@login_required(login_url='login')
def booking_success(request):
    return render(request, 'bookingSuccess.html')


# ================= DOCTOR DASHBOARD =================
@login_required(login_url='login')
def doctor_dashboard(request):

    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'doctor':
        return redirect('home')

    doctor = Doctor.objects.filter(user=request.user).first()

    appointments = Booking.objects.all()
    patients = User.objects.filter(booking__doctor=doctor).distinct()

    # FIX: reports written by this doctor
    reports = Report.objects.filter(doctor=request.user)

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.doctor = request.user

            # IMPORTANT FIX (must exist in form OR assign manually)
            if hasattr(obj, "patient") and obj.patient is None:
                obj.patient = request.user

            obj.save()
            return redirect('doctor_dashboard')

    else:
        form = ReportForm()

    return render(request, 'doctor_dashboard.html', {
        'form': form,
        'appointments': appointments,
        'patients': patients,
        'reports': reports,
        'total_appointments': appointments.count(),
        'total_patients': patients.count(),
    })
# ================= REPORTS =================

@login_required(login_url='login')
def my_reports(request):
    reports = Report.objects.filter(patient=request.user)
    return render(request, 'my_reports.html', {'reports': reports})


@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'profile.html', {'profile': profile})



