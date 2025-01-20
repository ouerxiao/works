from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from home.models import Setting, ContactMessage, FAQ
from blog.models import Category, Post
from home.forms import ContactForm, SearchForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    post_slider = Post.objects.filter(status='Published').order_by('-id')[:3]

    post_list = Post.objects.filter(status='Published')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'setting': setting,
        'category': category,
        'post_slider': post_slider,
        'posts': posts,
        }
    return render(request, 'home/index.html', context)

def about(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category}
    return render(request, 'home/about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(
                request, 'Meesage sent, thanks for contacting!')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm()
    context = {'setting': setting, 'category': category, 'form': form}
    return render(request, 'home/contact.html', context)

def category_post(request, id, slug):
    category = Category.objects.all()
    query = Category.objects.get(pk=id)
    post_list = Post.objects.filter(category_id=id, status='Published')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts, 
        'category': category,
        'query': query       
    }
    return render(request, 'home/category_posts.html', context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                posts = Post.objects.filter(title__icontains=query)
            else:
                posts = Post.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            
            context = { 
                'posts': posts,
                'category': category,
                'query': query}
            return render(request, 'home/search_posts.html', context)
    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        posts = Post.objects.filter(title__contains=q)
        results = []
        for rs in posts:
            post_json = {}
            post_json = rs.title
            results.append(post_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status=True).order_by("postnumber")
    context = {
        'category': category,
        'faq': faq,
    }
    return render(request, 'home/faq.html', context)
