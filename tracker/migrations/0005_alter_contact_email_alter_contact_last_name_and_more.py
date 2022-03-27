# Generated by Django 4.0.3 on 2022-03-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_alter_job_applied_on_alter_job_follow_up'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='notes',
            field=models.TextField(blank=True, max_length=600),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='excitement',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
