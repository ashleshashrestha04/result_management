from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'teacher_app'

urlpatterns = [
    # Teacher authentication routes
    path('signup/', views.teacher_signup, name='teacher_signup'),
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
