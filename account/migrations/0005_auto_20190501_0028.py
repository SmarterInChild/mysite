# Generated by Django 2.2 on 2019-04-30 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userinfo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photo/%Y%m%d'),
        ),
    ]
