from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/',views.about, name='about'),
    path('category/<int:id>/<slug:slug>/',views.category_post, name='category_posts'),
    path('contact/',views.contact, name='contact'),
    path('search/',views.search, name='search'),
    path('search_auto/',views.search_auto, name='search_auto'),
    path('faq/',views.faq, name='faq'),
]
