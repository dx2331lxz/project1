# Generated by Django 4.1.4 on 2022-12-30 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0024_alter_comment_commenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreply',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.userinfo', to_field='name', verbose_name='评论者'),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='reply_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.comment', verbose_name='被评论回复的用户'),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='replyed_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.information', verbose_name='被评论回复的盲盒'),
        ),
    ]
