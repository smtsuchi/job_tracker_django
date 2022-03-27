from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Account, Job, Contact


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Passwords must match"})
        user.set_password(password)
        user.save()
        return user

@receiver(post_save, sender=Account)
def createAuthToken(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'job_title', 'company', 'location', 'notes', 'description',
            'description_preview', 'applied_on', 'follow_up', 'excitement',
            'keywords', 'additional_details', 'img_url', 'color', 'rank', 'status'
            ]

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['description']

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['notes']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'notes', 'id']
