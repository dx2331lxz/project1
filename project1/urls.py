from django.contrib import admin
from django.urls import path, include, re_path
from app01 import views
from django.views.static import serve
from .settings import MEDIA_ROOT
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', views.mainpage),
                  path('login/', views.login),
                  path('logout/', views.logout),
                  path('image/code/', views.image_code),  # 验证码图片
                  path('email/password/', views.get_password),
                  path('register/', views.register),
                  path('make_box/', views.make_box),
                  path('box_delete/<int:nid>/', views.box_delete),
                  path('show_box/<int:nid>/', views.show_box),
                  path('update_password/', views.update_password),
                  path('select_box/<int:gender>/', views.select_box),  # 抽取盲盒
                  path('collect/<int:user_id>/', views.collect),  # 收藏盲盒
                  path('delete_collect/<int:user_id>/', views.delete_collect),  # 取消收藏盲盒
                  path('collections/', views.collect_box),  # 收藏盲盒夹
                  path('personal_page/', views.personal_page),  # 个人主页
                  path('edit_personal_page/', views.edit_personal_page),  # 个人主页编辑
                  path('setting/', views.setting),  # 个人主页编辑
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
