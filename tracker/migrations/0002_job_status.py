# Generated by Django 4.0.3 on 2022-03-20 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('wishlist', 'wishlist'), ('applied', 'applied'), ('interviewing', 'interviewing'), ('offer', 'offer')], default='wishlist', max_length=12),
        ),
    ]
