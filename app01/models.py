from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(verbose_name='名字', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=64, unique=True)


class Information(models.Model):
    user = models.ForeignKey(verbose_name='关联用户id', to="UserInfo", to_field='id', on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    age = models.IntegerField(verbose_name='年龄')
    name = models.CharField(verbose_name='盲盒用户名', max_length=64)
    title = models.CharField(verbose_name="标题", max_length=100)
    call = models.CharField(verbose_name="联系方式", max_length=100)
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    school = models.ForeignKey(verbose_name='学校', to_field='school', to='School', on_delete=models.DO_NOTHING)
    content = RichTextUploadingField(config_name='default')
    # collect = models.ForeignKey(to_field='collection', to='Collection', on_delete=models.CASCADE, unique=True,
    #                             null=True, blank=True)


class School(models.Model):
    school = models.CharField(verbose_name='学校', max_length=64, unique=True)

    def __str__(self):
        return self.school


class Comment(models.Model):
    commenter = models.ForeignKey(to_field='name', to='UserInfo', on_delete=models.CASCADE, verbose_name='评论的人',
                                  null=True, blank=True)
    content = RichTextUploadingField(config_name='default')
    user = models.ForeignKey(to_field='id', to='Information', on_delete=models.CASCADE, verbose_name='被评论对象',
                             null=True, blank=True)

    class Meta:
        db_table = 'comment'
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return


class CommentReply(models.Model):
    user = models.ForeignKey(to_field='name', to='UserInfo', on_delete=models.CASCADE, verbose_name='评论者', null=True,
                             blank=True)
    reply_user = models.ForeignKey(to_field='id', to='Comment', on_delete=models.CASCADE,
                                   verbose_name='被评论回复的用户',
                                   null=True,
                                   blank=True)
    replyed_user = models.ForeignKey(to_field='id', to='Information', on_delete=models.CASCADE,
                                     verbose_name='被评论回复的盲盒',
                                     null=True,
                                     blank=True)
    content = RichTextUploadingField(config_name='default', null=True, blank=True)


class Collection(models.Model):
    collector = models.ForeignKey(to_field='id', to='UserInfo', on_delete=models.CASCADE, null=True, blank=True)
    # collection = models.ForeignKey(to_field='id', to='Information', on_delete=models.CASCADE, null=True, blank=True,
    #                                unique=True)
    collection = models.ForeignKey(to_field='id', to='Information', on_delete=models.CASCADE, null=True, blank=True)


class MainInformation(models.Model):
    user = models.ForeignKey(to_field='id', to='UserInfo', on_delete=models.CASCADE, verbose_name='关联的用户',
                             null=True, blank=True)
    signature = models.TextField(verbose_name='个性签名', max_length=520)
    skills = models.CharField(verbose_name='技能', max_length=520, null=True, blank=True)
    QQ = models.CharField(verbose_name='QQ号', max_length=64)
    Weixin = models.CharField(verbose_name='微信号', max_length=30)
    Blogger_URL = models.CharField(verbose_name='url', max_length=100)
    picture = models.ImageField(upload_to='avatar', default='avatar/default.jpg')
