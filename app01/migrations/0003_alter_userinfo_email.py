# Generated by Django 4.1.4 on 2022-12-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_userinfo_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.CharField(max_length=64, verbose_name='邮箱'),
        ),
    ]
