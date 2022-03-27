from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

# Create your models here.
class Account(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_pro = models.BooleanField(default=False)
    about = models.TextField()
    night_mode = models.BooleanField(default=False)
    github = models.CharField(max_length=30)
    linkedin = models.CharField(max_length=60)
    website = models.CharField(max_length=60)
    is_public = models.BooleanField(default=True)
    image = models.ImageField()
    last_lesson_url = models.CharField(max_length=100)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return f'{self.username}'
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

class Job(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=[('wishlist','wishlist'),('applied','applied'),('interviewing','interviewing'),('offer','offer')], default='wishlist')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    description = models.TextField(blank=True)
    description_preview = models.TextField(blank=True)
    applied_on = models.DateField(blank=True, null=True)
    follow_up = models.DateField(blank=True, null=True)
    excitement = models.IntegerField(blank=True, null=True)
    keywords = models.CharField(max_length=100, blank=True)
    additional_details = models.TextField( blank=True)
    img_url = models.CharField(max_length=300, blank=True)
    color = models.CharField(max_length=100, blank=True)
    rank = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f'{self.job_title} | {self.company}'
    def to_dict(self):
        return {
            'id': str(self.id),
            'jobTitle': self.job_title,
            'company': self.company,
            'location': self.location,
            'notes': self.notes,
            'description': self.description,
            'descriptionPreview': self.description_preview,
            'appliedOn': self.applied_on,
            'followUp': self.follow_up,
            'excitement': self.excitement,
            'keywords': self.keywords,
            'additionalDetails': self.additional_details,
            'imgUrl': self.img_url,
            'color': self.color,
            'rank': self.rank
        }

class Contact(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    notes = models.TextField(max_length=600, blank=True)
    def __str__(self):
        return f'{self.job} | {self.first_name}'