# Generated by Django 5.0.6 on 2024-05-16 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_roles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlogs',
            old_name='User',
            new_name='user',
        ),
    ]