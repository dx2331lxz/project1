# Generated by Django 4.1.4 on 2022-12-28 06:57

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_alter_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='hobby',
        ),
        migrations.AddField(
            model_name='information',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=0),
            preserve_default=False,
        ),
    ]
