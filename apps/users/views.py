from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import check_password,make_password
from django.http import HttpResponse
from json import dumps


from .forms import *
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_sp_email, send_forget_email

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return  None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class RegiserView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html",{"register_form":register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg":"邮箱已经被注册","register_form": register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.is_active = False
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_sp_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, "register.html", {"register_form": register_form})

class LoginView(View):
    def get(self, request):
        return render(request, "login.html",{})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "project.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活!","login_form": login_form})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!","login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form":forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            user = UserProfile.objects.filter(email=email).last()
            if user != None:
                send_forget_email(email=email)
                return HttpResponse(dumps("{'status':'0','msg':'新密码已发送至您邮箱,请查收'}"), content_type='application/json')
            else:
                return HttpResponse(dumps("{'status':'-1', 'msg':'用户不存在,请检查邮箱是否正确'}"), content_type='application/json')
        else:
            return HttpResponse(dumps("{'status':'-1', 'msg':'邮箱格式不正确'}"), content_type='application/json')

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get("email", "")
            pass_word = request.POST.get("oldpassword", "")
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:

                return HttpResponse(dumps("{'status':'-1', 'msg':'两次密码不一致'}"), content_type='application/json')
            user = authenticate(email=email, password=pass_word)
            if user is not None:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return HttpResponse(dumps("{'status':'0','msg':'密码更改成功'}"), content_type='application/json')
            else:
                return HttpResponse(dumps("{'status':'-1', 'msg':'密码错误'}"), content_type='application/json')
        else:
            return HttpResponse(dumps("{'status':'-1', 'msg':'密码格式不正确'}"), content_type='application/json')

