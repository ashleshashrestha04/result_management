from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Student(models.Model):
    """Model representing a student in the system"""
    
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    
    name = models.CharField(max_length=100, help_text="Full name of the student")
    roll_number = models.CharField(
        max_length=20, 
        unique=True, 
        help_text="Unique roll number for the student"
    )
    email = models.EmailField(unique=True, help_text="Student's email address")
    course = models.CharField(max_length=100, help_text="Course/Program name")
    marks = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Marks obtained (0-100)"
    )
    grade = models.CharField(
        max_length=2, 
        choices=GRADE_CHOICES,
        help_text="Grade assigned based on marks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['roll_number']
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def __str__(self):
        return f"{self.name} ({self.roll_number})"
    
    def save(self, *args, **kwargs):
        """Auto-assign grade based on marks"""
        if self.marks >= 90:
            self.grade = 'A+'
        elif self.marks >= 85:
            self.grade = 'A'
        elif self.marks >= 80:
            self.grade = 'A-'
        elif self.marks >= 75:
            self.grade = 'B+'
        elif self.marks >= 70:
            self.grade = 'B'
        elif self.marks >= 65:
            self.grade = 'B-'
        elif self.marks >= 60:
            self.grade = 'C+'
        elif self.marks >= 55:
            self.grade = 'C'
        elif self.marks >= 50:
            self.grade = 'C-'
        elif self.marks >= 45:
            self.grade = 'D+'
        elif self.marks >= 40:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)


class Teacher(models.Model):
    """Model representing a teacher in the system"""
    
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
