from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

# UserCreationForm => ModelForm을 상속받기 때문에 model을 알아야함
# AuthenticationForm => Form을 상속받기 때문에 model에 영향을 받지 않음



# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect("accounts:login")

def user_page(request, id):
    user_info = get_object_or_404(User, id=id)
    context = {
        'user_info':user_info,
    }
    return render(request, 'accounts/user_page.html', context)

def follow(request, id):
    # 내가 팔로우 하려는 사람
    you = get_object_or_404(User, id=id)
    # 지금 로그인한사람
    me = request.user
    
    if  you != me:
        # 내가 이미 팔로우 했으면 취소
        if you in me.follwings.all():
            me.follwings.remove(you)
        # 아니면 팔로우
        else:
            me.follwings.add(you)
    return redirect ('accounts:user_page', id)

    # if me in you.followers.all():
    #     me.follwings.remove(you)
    #     you.followers.remove(me)
    # else:
    #     me.follwings.add(you)
    #     you.followers.add(me)
    # return redirect('accounts:user_page', id)

def delete(request, id):
    # 내가 보고있는 페이지의 유저
    # 확인하는 절차
    user_info = get_object_or_404(User, id=id)
    user = request.user

    if user == user_info:
        user.delete()
    return redirect('posts:index')

def update(request):
    if request.method =='POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/form.html', context)

def password(request):
    if request.method =='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # 비밀번호바꾸면 로그아웃됨(위에 코드를 안쓰면)
            return redirect('posts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/form.html', context)

def profile(request):
    user_info = request.user
    context = {
        'user_info':user_info,
    }
    return render(request, 'accounts/user_page.html', context)