from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class M1(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in ["/login/", "/image/code/", "/register/", "/email/password/", "/update_password/"]:
            return
        info = request.session.get("info")
        if info:
            return
        else:
            return redirect("/login/")
