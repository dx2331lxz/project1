from django import forms
from ckeditor_uploader.fields import RichTextUploadingField

from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]


class PassWord(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "验证码"}))

    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(attrs={"class": "input_box", "placeholder": "密码"}))
    re_password = forms.CharField(min_length=6,
                                  widget=forms.PasswordInput(attrs={"class": "input_box", "placeholder": "确认密码"}))

    class Meta:
        model = UserInfo
        fields = ["password", ]


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['content', ]


class MAINInformation(forms.ModelForm):
    class Meta:
        model = MainInformation
        fields = "__all__"
        exclude = ['user']
