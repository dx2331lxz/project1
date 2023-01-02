from django.contrib import admin
from .models import Comment, Information, UserInfo

admin.site.register(Comment)
admin.site.register(Information)
admin.site.register(UserInfo)
