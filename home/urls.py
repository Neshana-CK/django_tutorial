from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # ✅ ADD THESE BACK
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('doctors/', views.doctors, name="doctors"),
    path('departments/', views.departments, name="departments"),
    path('booking/', views.booking, name="booking"),
    path('booking/success/', views.booking_success, name="booking_success"),

    # AUTH
    path('signup/patient/', views.patient_signup, name="patient_signup"),
    path('signup/doctor/', views.doctor_signup, name="doctor_signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # DASHBOARDS
    path('doctor/dashboard/', views.doctor_dashboard, name="doctor_dashboard"),


    path('my-reports/', views.my_reports, name='my_reports'),
    path('profile/', views.profile, name='profile'),
]
