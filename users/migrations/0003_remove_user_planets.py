# Generated by Django 4.0.3 on 2022-03-18 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_planets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='planets',
        ),
    ]
