# Generated by Django 4.1.7 on 2023-03-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsrv', '0004_userinfo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='usrverified',
            field=models.CharField(default='False', max_length=16),
            preserve_default=False,
        ),
    ]
