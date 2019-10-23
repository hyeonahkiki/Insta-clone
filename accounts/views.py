from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
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