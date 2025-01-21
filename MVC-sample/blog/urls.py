from django.urls import path
import blog.views as views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('blog/<int:id>/<slug:slug>/', views.post_detail, name='post-detail'),
    path('blog/addcomment/<int:id>', views.addcomment, name='comment'),
    path('image/', views.post_image, name='image'),
    path('image/<int:id>', views.post_image_detail, name='image-detail'),
    path('video/', views.post_video, name='video'),
    path('like/<int:pk>/', views.like_post, name='like-post'),
    path('likeimage/<int:pk>/', views.like_image, name='like-image'),
    path('bookmark/<int:id>/', views.bookmark_post, name='bookmark-post'),
    
]