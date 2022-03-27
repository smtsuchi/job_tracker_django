from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.getJobs, name='getJobs'),
    path('jobs/<int:job_id>/', views.getJob, name='getJob'),
    path('jobs/update/<int:job_id>/', views.updateJob, name='updateJob'),
    path('jobs/add/', views.addJob, name='addJob'),
    path('jobs/update/', views.updateJobs, name='updateJobs'),
    path('api/login/', obtain_auth_token, name='api-login'),
    path('api/register/', views.registerUser, name='api-register'),
    path('jobs/description/update/<int:job_id>/', views.updateJobDescription, name='updateJobDescription'),
    path('jobs/notes/update/<int:job_id>/', views.updateNotes, name='updateNotes'),
    path('jobs/contacts/get/<int:job_id>/', views.getJobContacts, name='getJobContacts'),
    path('jobs/contacts/add/<int:job_id>/', views.addContact, name='addContact'),
    path('jobs/contacts/update/<int:contact_id>/', views.updateContact, name='updateContact'),
]