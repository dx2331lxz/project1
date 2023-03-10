# Generated by Django 4.1.4 on 2022-12-28 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0015_remove_information_hobby_information_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.CharField(max_length=64, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='名字'),
        ),
    ]
