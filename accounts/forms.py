from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User # 클래스를 직접 언급

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        # User랑 get_user_model()의미는 같은 get_user_model도 클래스 User(모델) 를 반환한다
        # setting.AUTH_USER_MODEL은 문자열 자체를 반환 'accounts.user'
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)