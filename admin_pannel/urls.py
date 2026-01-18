from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_login,name='admin-login'),
    path('admin/', admin_main,name='admin'),
    path('dashboard/', dashboard,name='dashboard'),
    path('contacts/', contacts,name='contacts'),
    path("contacts/delete/<int:query_id>/", delete_contact, name="delete_contact"),
    path('jobs/', jobs, name='job'),
    path('add-job/', add_job,name='add_job'),
     path('edit-job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', delete_job, name='delete_job'),
    path('applications/', applications,name='applications'),
    path('applications/delete/<int:app_id>/', delete_application, name='delete_application'),
    
    
]
