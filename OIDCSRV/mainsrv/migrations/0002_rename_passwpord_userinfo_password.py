# Generated by Django 4.1.7 on 2023-03-12 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsrv', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='passwpord',
            new_name='password',
        ),
    ]
