# Generated by Django 4.0.3 on 2022-03-20 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_pro', models.BooleanField(default=False)),
                ('about', models.TextField()),
                ('night_mode', models.BooleanField(default=False)),
                ('github', models.CharField(max_length=30)),
                ('linkedin', models.CharField(max_length=60)),
                ('website', models.CharField(max_length=60)),
                ('is_public', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='')),
                ('last_lesson_url', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('notes', models.TextField()),
                ('description', models.TextField()),
                ('description_preview', models.TextField()),
                ('applied_on', models.DateField()),
                ('follow_up', models.DateField()),
                ('excitement', models.IntegerField()),
                ('keywords', models.CharField(max_length=100)),
                ('additional_details', models.TextField()),
                ('img_url', models.CharField(max_length=300)),
                ('color', models.CharField(max_length=100)),
                ('rank', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.account')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('notes', models.TextField(max_length=600)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.job')),
            ],
        ),
    ]
