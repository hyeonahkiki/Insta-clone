from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import HashTag, Post, Comment
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts':posts,
    }
    return render(request, 'posts/index.html', context)


def create(request):
    if request.method =='POST':
        # form에 이미지도 있으니 이미지를 받아오는 것도 설정해야함
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # save해야 post에 대한 id가 부여된다
            post.save()
            for word in post.content.split():
                if word.startswith('#'):
                    # hashtag추가(같은 해시태그끼리 같은 아이디를 갖게 하기 위해서 get_or_create 사용)
                    # get_or_create는 튜플반환 (obj, True or False)
                    # hashtag, created = HashTag.objects.get_or_create(content=word)
                    # created를 안쓸거기때문에 [0]을 사용
                    hashtag = HashTag.objects.get_or_create(content=word)[0]
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form':form,
    }
    return render(request, 'posts/form.html', context)

def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#'):
                    # hashtag추가(같은 해시태그끼리 같은 아이디를 갖게 하기 위해서 get_or_create 사용)
                    # get_or_create는 튜플반환 (obj, True or False)
                    # hashtag, created = HashTag.objects.get_or_create(content=word)
                    # created를 안쓸거기때문에 [0]을 사용
                    hashtag = HashTag.objects.get_or_create(content=word)[0]
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
    context = {
        'form':form,
    }
    return render(request, 'posts/form.html', context)

def delete(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('posts:index')

def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)
    posts = hashtag.taged_post.all()
    context = {
        'posts':posts,
    }
    return render(request, 'posts/index.html', context)

def like(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if post.like_users.filter(id=user.id):
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:index')

def comment_create(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return redirect('posts:comment_create', id)
    else:
        form = CommentForm()
    context={
        'post': post,
        'form':form,
    }
    return render(request, 'posts/detail.html', context)

def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('posts:comment_create', post_id)

