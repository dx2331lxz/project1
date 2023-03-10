# Generated by Django 4.1.4 on 2022-12-25 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_rename_infomation_information'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=64, unique=True, verbose_name='学校')),
            ],
        ),
        migrations.AddField(
            model_name='information',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app01.school', to_field='school', verbose_name='学校'),
        ),
    ]
