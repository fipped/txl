from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse,HttpResponseRedirect
from .models import User
from django import forms
from django.conf import settings

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        f = LoginForm(request.POST)
        if f.is_valid():

            username = f.cleaned_data['username']
            password = f.cleaned_data['password']

            user = authenticate(username=username,password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'code':'success', 'info':'登录成功'})
            return JsonResponse({'code':'error','errors':{'登录失败': '请检查用户名和密码'}})
        return JsonResponse({'code':'error','errors':f.errors})

def SignUp(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        res = User.objects.filter(username=username)
        if len(res):
            return JsonResponse({'code':'error','errors':{'注册失败':'用户名已存在'}})
        user = User.objects.create_user(username=username,password=password)
        user.save()
        return JsonResponse({'code':'success', 'info':'注册成功'})
    return JsonResponse({'code':'failed', 'errors':{'请求错误': '请确保正常操作'}})


@login_required()
def Logout(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)