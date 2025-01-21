from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from blog.models import Category, Comment
from user.models import UserProfile
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView

@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'profile': profile,
    }
    return render(request, 'user/user_profile.html', context)

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.avatar.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,'login failed, WRONG username or password')
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'user/login_form.html', context)

def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.avatar = 'avatar/default.jpg'
            data.save()
            messages.success(request, 'Successfully CREATED username！')

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return  render(request, 'user/signup_form.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Successfully updated！')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user/user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Successfully changed!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'follow instructions：<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user/user_password.html', context)


class PasswordReset(PasswordResetView):
    template_name = 'user/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('home')
    form_valid_message = ("Successfully changed!")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required(login_url='/login')
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user/user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomments(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Successfully deleted!')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def user_bookmarks(request):
    category = Category.objects.all()
    user = request.user

    bookmark_list = user.bookmark.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(bookmark_list, 3)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'user/user_bookmarks.html', context)