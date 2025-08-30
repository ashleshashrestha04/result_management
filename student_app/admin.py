from django.contrib import admin
from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin configuration for Student model"""
    list_display = ['name', 'roll_number', 'email', 'course', 'marks', 'grade', 'created_at']
    list_filter = ['course', 'grade', 'created_at']
    search_fields = ['name', 'roll_number', 'email', 'course']
    list_editable = ['marks']
    readonly_fields = ['grade', 'created_at', 'updated_at']
    ordering = ['roll_number']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('name', 'roll_number', 'email', 'course')
        }),
        ('Academic Information', {
            'fields': ('marks', 'grade')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin configuration for Teacher model"""
    list_display = ['name', 'email', 'course', 'hire_date', 'years_of_service', 'created_at']
    list_filter = ['course', 'hire_date', 'created_at']
    search_fields = ['name', 'email', 'course']
    readonly_fields = ['created_at', 'updated_at', 'years_of_service']
    ordering = ['name']
    
    fieldsets = (
        ('Teacher Information', {
            'fields': ('name', 'email', 'course', 'hire_date')
        }),
        ('Service Information', {
            'fields': ('years_of_service',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
