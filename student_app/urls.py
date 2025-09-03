from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication routes
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('student-signup/', views.student_signup, name='student_signup'),
    path('student-login/', views.student_login, name='student_login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-logout/', views.student_logout, name='student_logout'),

    # Student Results page for students
    path('student-results/', views.student_results, name='student_results'),

    # Student CRUD routes
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Teacher CRUD routes
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/<int:pk>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    # API endpoints (optional - for AJAX operations)
    path('api/students/search/', views.student_search_api, name='student_search_api'),
    path('api/teachers/search/', views.teacher_search_api, name='teacher_search_api'),
    path('api/students/<int:pk>/grade/', views.get_student_grade, name='get_student_grade'),
]
