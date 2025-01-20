from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
)
from blog.models import Post, Category, Comment, Youtube, PostImage
from blog.forms import CommentForm
from blog.models import Post, Category, PostImage

# Create your views here.

def post_detail(request, id, slug):
    category = Category.objects.all()
    post = Post.objects.get(pk=id)
    images = PostImage.objects.filter(post_id=id)
    comments = Comment.objects.filter(post_id=id, status=True)
    total_likes = post.total_likes()
    is_liked = False
    is_bookmark = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    
    if post.bookmark.filter(id=request.user.id).exists():
        is_bookmark = True
    context = {
        'post': post,
        'images': images,
        'category': category,
        'comments': comments,
        'total_likes': total_likes,
        'is_liked': is_liked,
        'is_bookmark': is_bookmark
    }
    return render(request, 'blog/post_detail.html', context)

def addcomment(request, id, parent_id=None):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            try:
                parent_id = request.POST.get('parent_id')
            except:
                parent_id = None

            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.post_id=id
            current_user = request.user
            data.user_id = current_user.id
            data.parent_id = parent_id
            data.save()
            messages.success(
                request, 'messages sent！')
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)

def post_image(request):
    post_list = PostImage.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    category = Category.objects.all()

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/post_image.html', context)

def post_image_detail(request, id):
    category = Category.objects.all()
    image = PostImage.objects.get(pk=id)
    is_liked = False
    if image.likes_image.filter(id=request.user.id).exists():
        is_liked = True
    
    context = {
        'category': category,
        'image': image,
        'is_liked': is_liked
    }

    return render(request, 'blog/post_image_detail.html', context)


def post_video(request):
    videos_list = Youtube.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(videos_list, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    category = Category.objects.all()
    context = {
        'category': category,
        'posts':posts,
    }
    return render(request, 'blog/post_video.html', context)


@login_required(login_url='/login')
def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
    'post': post,
    'is_liked': is_liked,
    }
    return HttpResponseRedirect(post.get_absolute_url())


@login_required(login_url='/login')
def bookmark_post(request, id):
    current_user = request.user
    post = get_object_or_404(Post, id=id)
    if post.bookmark.filter(id=request.user.id).exists():
        post.bookmark.remove(request.user)
    else:
        post.bookmark.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

@login_required(login_url='/login')
def like_image(request, pk):
    image = get_object_or_404(PostImage, id=request.POST.get('image_id'))
    is_liked = False
    if image.likes_image.filter(id=request.user.id).exists():
        image.likes_image.remove(request.user)
        is_liked = False
    else:
        image.likes_image.add(request.user)
        is_liked = True
    context = {
    'image': image,
    'is_liked': is_liked,
    }
    return HttpResponseRedirect(image.get_absolute_url())
