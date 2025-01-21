from django.urls import path
import user.views as views
from user.views import (
    PasswordReset,
    PasswordResetDone,
    PasswordResetConfirm,
)

urlpatterns = [
    path('user/', views.index, name='user'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_form, name='logout'),
    path('signup/', views.signup_form, name='signup'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('user/update/', views.user_update, name='user_update'),
    path('user/password/', views.user_password, name='user_password'),
    path('user/comments/', views.user_comments, name='user_comments'),
    path('user/bookmarks/', views.user_bookmarks, name='user_bookmarks'),
    path('user/deletecomments/<int:id>', views.user_deletecomments, name='user_deletecomments'),
]
