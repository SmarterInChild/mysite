# Generated by Django 2.1.7 on 2019-04-30 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
