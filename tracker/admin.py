from django.contrib import admin
from .models import Account, Contact, Job

# Register your models here.
admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Job)