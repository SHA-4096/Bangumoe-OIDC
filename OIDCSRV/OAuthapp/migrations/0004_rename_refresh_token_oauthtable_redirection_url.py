# Generated by Django 4.1.7 on 2023-03-14 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OAuthapp', '0003_oauthtable_refresh_token_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oauthtable',
            old_name='refresh_token',
            new_name='redirection_url',
        ),
    ]
