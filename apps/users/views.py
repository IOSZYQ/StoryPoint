from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import check_password,make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from json import dumps


from .forms import *
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_sp_email, send_forget_email
from group.models import Group

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

class DeleteUserView(View):
    def post(self,request):
        user_id = request.POST.get('userid',0)
        user = UserProfile.objects.filter(id=user_id).last()
        if user != None:
            user.delete()
        result = {'status': 0}
        return HttpResponse(dumps(result), content_type='application/json')

class AddUserView(View):
    def post(self, request):
        user_id = request.POST.get('userid', '')
        user_name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        if user_name == '':
            return HttpResponse(dumps({'status': -1, 'msg': '名字不能为空'}), content_type="application/json")
        groupid = request.POST.get('groupid', '')
        group = Group.objects.get(pk=groupid)
        leaderid = request.POST.get('leader', '')
        if int(user_id) != 0:
            user = UserProfile.objects.get(pk=user_id)
            user.username = user_name
            user.email = email
            user.save()
            if leaderid == 'true':
                group.leader = user
                group.save()
            else:
                if group.leader == user:
                    group.leader = None
                    group.save()
        else:
            if UserProfile.objects.filter(username=user_name):
                return HttpResponse(dumps({'status': -1, 'msg': '名字已经存在,请更换名字'}), content_type="application/json")
            if email != '':
                if UserProfile.objects.filter(email=email):
                    return HttpResponse(dumps({'status': -1, 'msg': '邮箱已经存在,请更换邮箱'}), content_type="application/json")
            user = UserProfile.objects.create(username=user_name, email=email)
            user.password = make_password('123456')
            user.save()

            group.members.add(user)
            if leaderid == 'true':
                group.leader = user
                group.save()

        return HttpResponse(dumps({'status': 0}), content_type='application/json')

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
            # user_profile.is_active = False
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_sp_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, "register.html", {"register_form": register_form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

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
                    return HttpResponseRedirect(reverse('index'))
                else:
                    result = {'status': -1, 'msg': '用户未激活'}
                    return HttpResponse(dumps(result), content_type='application/json')
            else:
                result = {'status': -1, 'msg': '用户名或密码错误'}
                return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {'status': -1, 'msg': '密码不能小于6位'}
            return HttpResponse(dumps(result), content_type='application/json')

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
                result = {'status':'0','msg':'新密码已发送至您邮箱,请查收'}
                return HttpResponse(dumps(result), content_type='application/json')
            else:
                result = {'status':'-1', 'msg':'用户不存在,请检查邮箱是否正确'}
                return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {'status':'-1', 'msg':'邮箱格式不正确'}
            return HttpResponse(dumps(result), content_type='application/json')

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            username = request.POST.get("username", "")
            pass_word = request.POST.get("oldpassword", "")
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                result = {'status':0, 'msg':'两次密码不一致'}
                return HttpResponse(dumps(result), content_type='application/json')
            user = authenticate(username=username, password=pass_word)
            if user is not None:
                user = UserProfile.objects.get(username=username)
                user.password = make_password(pwd2)
                user.save()
                result = {'status':0,'msg':'密码更改成功'}
                return HttpResponse(dumps(result), content_type='application/json')
            else:
                result = {'status':-1, 'msg':'密码错误'}
                return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {'status':-1, 'msg':'密码格式不正确'}
            return HttpResponse(dumps(result), content_type='application/json')

class AddAndEditUserView(View):
    def post(self, request):
        username = request.POST.get('username','')
        id = request.POST.get('userid', '')
        if username != '':
            if id != '':
                user = UserProfile.object.get(pk=id)
                if user != None:
                    user.username = username
                    user.save()
                    return HttpResponse(dumps({'status': 0}), content_type='application/json')
                else:
                    result = {'status': -1, 'msg': 'id错误'}
                    return HttpResponse(dumps(result), content_type='application/json')
            else:
                user = UserProfile.objects.create.init(username=username)
                user.save()
                return HttpResponse(dumps({'status': 0}), content_type='application/json')
        else:
            result = {'status': -1, 'msg':'名字不能为空'}
            return HttpResponse(dumps(result), content_type='application/json')

