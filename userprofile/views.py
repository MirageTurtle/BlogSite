from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # 清洗出合法数据
            data = user_login_form.cleaned_data
            # 验证账号密码
            user = authenticate(
                username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在session中，即实现了登录动作
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('账号或密码输入有误，请重新输入。')
        else:
            return HttpResponse('账号或密码输入不合法。')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用POST或GET请求数据。')


def user_logout(request):
    logout(request)
    return redirect('article:article_list')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重试。')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用POST或GET请求数据。')


@login_required(login_url='/userprofile/login')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse('你没有删除操作的权限。')
    else:
        return HttpResponse('仅接受post请求。')


@login_required(login_url='/userprofile/login')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():  # user_id是OneToOneField自动生成的字段
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse('您没有权限修改此用户信息。')

        # 表单上传的文件对象存储在类字典对象request.FILES中
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data  # cd应该是cleaned data的缩写
            profile.phone = profile_cd.get('phone')
            profile.bio = profile_cd.get('bio')
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd.get('avatar')  # 保存的是文件地址
            profile.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('信息表单输入有误，请重新输入。')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form,
                   'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用POST或GET方式请求数据。')
