import collections

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from app01.models import *
from app01 import models
from app01.utils.code import check_code
from django.core.mail import send_mail
from project1 import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from .forms import CommentForm, PassWord, CommentReplyForm, MAINInformation
from django.db.models import Q
import random
from django.utils.safestring import mark_safe


# 主页
def mainpage(request):
    search = request.GET.get("search")
    collection = Collection.objects.filter(collector_id=request.session["info"]["id"])
    collect_list = []
    for i in collection:
        collect_list.append(i.collection_id)
    if search:
        data_list_man = Information.objects.filter(
            Q(age__contains=search) | Q(name__contains=search) | Q(title__contains=search) | Q(
                school__school__contains=search) | Q(content__contains=search), gender=1)
        data_list_woman = Information.objects.filter(
            Q(age__contains=search) | Q(name__contains=search) | Q(title__contains=search) | Q(
                school__school__contains=search) | Q(content__contains=search), gender=2)
    else:
        kwargs_man = {"gender": 1}
        kwargs_woman = {"gender": 2}
        data_list_man = Information.objects.filter(**kwargs_man)
        data_list_woman = Information.objects.filter(**kwargs_woman)
    data_list = {"data_list_man": data_list_man, "data_list_woman": data_list_woman,
                 "collect_list": collect_list}
    return render(request, "mainpage.html", data_list)


# 注册
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=6,
                           widget=forms.TextInput(attrs={"class": "input_box", "placeholder": "姓名"}))
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(attrs={"class": "input_box", "placeholder": "密码"}))
    re_password = forms.CharField(min_length=6,
                                  widget=forms.PasswordInput(attrs={"class": "input_box", "placeholder": "确认密码"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "input_box", "placeholder": "邮箱"}))

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", 'email']
        # # 略显多余
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "input_box", "placeholder": "姓名"}),
        #     "password": forms.PasswordInput(attrs={"class": "input_box", "placeholder": "密码"})
        # }
        #


def register(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "register.html", {"form": form})
    form = UserModelForm(data=request.POST)

    name = request.POST.get("name")
    password = request.POST.get("password")
    re_password = request.POST.get("re_password")
    if not re_password:
        error = "密码不可以为空"
        return render(request, "register.html", {"form": form, "error": error})

    if re_password != password:
        error = "两次输入密码不一样"
        return render(request, "register.html", {"form": form, "error": error})

    for i in name:
        if u"\u4e00" < i < u"\u9fff" or not name.isalnum():
            error = "用户名只能包含字母和数字"
            return render(request, "register.html", {"form": form, "error": error})

    # 校验数据
    if UserInfo.objects.filter(name=name):
        form.add_error("name", "用户名已存在")
        return render(request, "register.html", {"form": form})
    if form.is_valid():
        form.save()
        return redirect("/login/")
    else:
        return render(request, "register.html", {"form": form})


class UserModelForm1(forms.ModelForm):
    name = forms.CharField(min_length=6,
                           widget=forms.TextInput(attrs={"class": "input_box", "placeholder": "用户名"}))
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(attrs={"class": "input_box", "placeholder": "密码"}))
    code = forms.CharField(widget=forms.TextInput(attrs={"class": "input_box", "placeholder": "图片验证码"}))

    class Meta:
        model = models.UserInfo
        fields = ["password", 'code']
        # # 略显多余
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "input_box", "placeholder": "姓名"}),
        #     "password": forms.PasswordInput(attrs={"class": "input_box", "placeholder": "密码"})
        # }


# 登陆
def login(request):
    if request.method == "GET":
        form = UserModelForm1()
        return render(request, "login.html", {"form": form})
    form = UserModelForm1(data=request.POST)

    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("code")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})
        obj = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not obj:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        request.session["info"] = {"id": obj.id, "name": obj.name}
        request.session.set_expiry(None)
        return redirect("/")
    else:
        return render(request, "login.html", {"form": form})


# 图片验证码

from io import BytesIO


def image_code(request):
    img, code_string = check_code()
    request.session["code"] = code_string
    request.session.set_expiry(60 * 60 * 24)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


# 找回密码

def get_password(request):
    if request.method == "GET":
        return render(request, "find_password.html")
    email = request.POST.get("email")
    if not UserInfo.objects.filter(email=email):
        return HttpResponse("该邮箱尚未注册，请返回重试。")
    code_out = str(random.randint(000000, 999999))
    request.session["code_out"] = code_out
    request.session["email"] = email
    user = UserInfo.objects.filter(email=email).first()
    subject = "找回密码"
    message = """找回密码，验证码为{}
            如果不是本人操作，请勿暴露验证码。""".format(code_out)
    email = user.email
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ])
    return redirect("/update_password/")


# 重置密码
def update_password(request):
    if request.method == "GET":
        form = PassWord()
        return render(request, "update_password.html", {"form": form})
    email = request.session.get("email")
    code_out = request.session.get("code_out")
    code_in = request.POST.get("code")
    password = request.POST.get("password")
    re_password = request.POST.get("re_password")
    form = PassWord(request.POST)
    if form.is_valid():
        if code_in != code_out:
            form.add_error("code", "验证码错误")
            return render(request, "update_password.html", {"form": form})
        elif password != re_password:
            form.add_error("re_password", "两次输入密码不一致")
            return render(request, "update_password.html", {"form": form})
        UserInfo.objects.filter(email=email).update(password=password)
        return redirect("/login/")
    else:
        return render(request, "update_password.html", {"form": form})


# 注销
def logout(request):
    request.session.clear()
    return redirect('/login/')


# 盲盒信息编辑

class InformationForm(forms.ModelForm):
    class Meta:
        model = models.Information
        fields = "__all__"
        exclude = ["user"]


#########盲盒


# 创建盲盒
def make_box(request):
    if request.method == "GET":
        form = InformationForm()
        return render(request, "makebox.html", {"form": form})
    form = InformationForm(data=request.POST)
    if form.is_valid():
        form.save()
        Information.objects.filter(**form.cleaned_data).update(user_id=request.session["info"]["id"])
        return redirect("/")
    else:
        return render(request, "makebox.html", {"form": form})


# 查看盲盒详情

def show_box(request, nid):
    if request.method == "GET":
        comment_id = request.GET.get("comment_id")  # 点击时候显示富文本框位置的切换
        if not comment_id:
            comment_id = 0
            form = CommentForm()
        else:
            comment_id = int(comment_id)  # 点击时候显示富文本框位置的切换
            form = CommentReplyForm()
        content = Comment.objects.filter(user_id=nid).order_by('-id')
        content_reply = CommentReply.objects.filter(replyed_user=nid).order_by('-id')
        data_box = Information.objects.filter(id=nid)
        avatar = MainInformation.objects.all()
        return render(request, "show_box.html",
                      {"data_box": data_box, 'form': form, 'content': content, 'content_reply': content_reply,
                       'comment_id': comment_id, 'avatar': avatar})
    else:
        content_id = int(request.GET.get("content_id"))  # 储存时候确定位置
        if content_id == 0:
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                Comment.objects.filter(**form.cleaned_data).update(user_id=nid,
                                                                   commenter=request.session['info']['name'])
                return redirect("/show_box/{}/".format(nid))
            else:
                data_box = Information.objects.filter(id=nid)
                return render(request, "show_box.html", {"data_box": data_box, 'form': form})
        else:
            form = CommentReplyForm(request.POST)
            if form.is_valid():
                form.save()
                CommentReply.objects.filter(**form.cleaned_data).update(user_id=request.session['info']['name'],
                                                                        reply_user=content_id, replyed_user=nid)
                return redirect("/show_box/{}/".format(nid))
            else:
                data_box = Information.objects.filter(id=nid)
                return render(request, "show_box.html", {"data_box": data_box, 'form': form})


# 删除盲盒

def box_delete(request, nid):
    Information.objects.filter(id=nid).delete()
    return redirect("/")


# 抽取盲盒

def select_box(request, gender):
    obj = Information.objects.filter(gender=gender).order_by("?")[0]
    return redirect("/show_box/{}/".format(obj.id))


# 收藏

def collect(request, user_id):
    nid = request.session["info"]["id"]
    Collection.objects.create(collector_id=nid, collection_id=user_id)
    return redirect("/")


# 取消收藏
def delete_collect(request, user_id):
    nid = request.session["info"]["id"]
    Collection.objects.filter(collector_id=nid, collection_id=user_id).delete()
    return redirect("/")


# 收藏夹

def collect_box(request):
    collection = Collection.objects.filter(collector_id=request.session["info"]["id"])
    collect_list = []
    for i in collection:
        collect_list.append(i.collection_id)
    data_list_man = Information.objects.filter(id__in=collect_list, gender=1)
    data_list_woman = Information.objects.filter(id__in=collect_list, gender=2)
    return render(request, 'collect_list.html', {"data_list_man": data_list_man, "data_list_woman": data_list_woman})


# 个人主页

def personal_page(request):
    form = MainInformation.objects.filter(user_id=request.session['info']['id'])[0]
    return render(request, 'personal_page.html', {"form": form})


# 编辑个人信息


def edit_personal_page(request):
    list1 = MainInformation.objects.filter(user_id=request.session["info"]["id"]).first()
    if request.method == "GET":
        if not list1:
            form = MAINInformation()
        else:
            form = MAINInformation(instance=list1)
        return render(request, "edit_personal_page.html", {"form": form})
    if not list1:
        picture = request.FILES.get("picture")
        form = MAINInformation(request.POST)
        if form.is_valid():
            form.save()
            MainInformation.objects.filter(**form.cleaned_data).update(user_id=request.session["info"]["id"])
            list2 = MainInformation.objects.filter(user_id=request.session["info"]["id"]).first()
            list2.picture = picture
            list2.save()
            return redirect("/personal_page/")
        else:
            return render(request, "edit_personal_page.html", {"form": form})
    else:
        form = MAINInformation(request.POST, instance=list1)
        picture = request.FILES.get("picture")
        if form.is_valid():
            list1.picture = picture
            list1.save()
            form.save()
            # MainInformation.objects.filter(user_id=request.session["info"]["id"]).update(picture=picture)
            return redirect("/personal_page/")
        else:
            return render(request, "edit_personal_page.html", {"form": form})


# 设置

def setting(request):
    return render(request, "setting.html")



