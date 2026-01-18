from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/',about,name="about"),
    # path('about/',apply_job,name="about"),
    path('services/', services, name="services"),
    path('contact/', contact,name='contact'),
    path('career/', career, name='career'),
    path('casestudy/', casestudy, name='casestudy'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('apply/<int:job_id>/', apply_job,name="apply_job"),
    path('logout/', user_logout, name='logout'),
    path('industry/',industry, name = 'industries'),
    path('forgot/',forgot, name = 'forgot'),
     path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),
]
