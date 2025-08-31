from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TeacherProfile(models.Model):
    """Extended profile for teachers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    course = models.CharField(max_length=100, help_text="Course/Subject taught")
    hire_date = models.DateField(
        default=timezone.now,
        help_text="Date when the teacher was hired"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = "Teacher Profile"
        verbose_name_plural = "Teacher Profiles"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course}"
    
    @property
    def years_of_service(self):
        """Calculate years of service"""
        today = timezone.now().date()
        return (today - self.hire_date).days // 365


class Teacher(models.Model):
    """Model representing a teacher in the system (legacy - keeping for compatibility)"""
    
    name = models.CharField(max_length=100, help_text="Full name of the teacher")
    email = models.EmailField(unique=True, help_text="Teacher's email address")
    course = models.CharField(max_length=100, help_text="Course/Subject taught")
    hire_date = models.DateField(
        default=timezone.now,
        help_text="Date when the teacher was hired"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
    
    def __str__(self):
        return f"{self.name} - {self.course}"
    
    @property
    def years_of_service(self):
        """Calculate years of service"""
        today = timezone.now().date()
        return (today - self.hire_date).days // 365
