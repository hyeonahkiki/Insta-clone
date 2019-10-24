from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 사용자가 실제로 입력할 정보
        fields=('content', 'image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)