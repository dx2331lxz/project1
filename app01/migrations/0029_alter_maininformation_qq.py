# Generated by Django 4.1.4 on 2023-01-01 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0028_alter_maininformation_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maininformation',
            name='QQ',
            field=models.CharField(max_length=64, verbose_name='QQ号'),
        ),
    ]