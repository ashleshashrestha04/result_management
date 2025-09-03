from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Teacher


class StudentSignupForm(UserCreationForm):
    """Form for student signup with additional fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    roll_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your roll number'
        })
    )
    course = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your course/program'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if Student.objects.filter(roll_number=roll_number).exists():
            raise ValidationError('A student with this roll number already exists.')
        return roll_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create Student profile and link to user
            Student.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}",
                roll_number=self.cleaned_data['roll_number'],
                email=user.email,
                course=self.cleaned_data['course'],
                marks=0  # Default marks to 0
            )
        return user


class TeacherSignupForm(UserCreationForm):
    """Form for teacher signup with additional fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    course = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter course/subject you teach'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create Teacher profile
            from django.utils import timezone
            Teacher.objects.create(
                name=f"{user.first_name} {user.last_name}",
                email=user.email,
                course=self.cleaned_data['course'],
                hire_date=timezone.now().date()  # Set hire_date to today
            )
        return user


class StudentForm(forms.ModelForm):
    """Form for creating and updating Student records"""
    
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'course', 'marks']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'roll_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter roll number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter marks (0-100)',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
        }
        labels = {
            'name': 'Full Name',
            'roll_number': 'Roll Number',
            'email': 'Email Address',
            'course': 'Course/Program',
            'marks': 'Marks Obtained',
        }
        help_texts = {
            'roll_number': 'Enter a unique roll number for the student',
            'marks': 'Enter marks between 0 and 100 (grade will be auto-calculated)',
        }

    def clean_roll_number(self):
        """Validate roll number uniqueness"""
        roll_number = self.cleaned_data['roll_number']
        if Student.objects.filter(roll_number=roll_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A student with this roll number already exists.')
        return roll_number

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data['email']
        if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A student with this email address already exists.')
        return email

    def clean_marks(self):
        """Validate marks range"""
        marks = self.cleaned_data['marks']
        if marks < 0 or marks > 100:
            raise ValidationError('Marks must be between 0 and 100.')
        return marks


class TeacherForm(forms.ModelForm):
    """Form for creating and updating Teacher records"""
    
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'course', 'hire_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course/subject taught'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'course': 'Course/Subject',
            'hire_date': 'Hire Date',
        }
        help_texts = {
            'course': 'Enter the main course or subject this teacher handles',
            'hire_date': 'Select the date when this teacher was hired',
        }

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data['email']
        if Teacher.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A teacher with this email address already exists.')
        return email

    def clean_hire_date(self):
        """Validate hire date"""
        from django.utils import timezone
        hire_date = self.cleaned_data['hire_date']
        today = timezone.now().date()
        
        if hire_date > today:
            raise ValidationError('Hire date cannot be in the future.')
        return hire_date


class StudentSearchForm(forms.Form):
    """Form for searching students"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, roll number, email, or course...'
        })
    )
    course_filter = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    grade_filter = forms.ChoiceField(
        choices=[('', 'All Grades')] + Student.GRADE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class TeacherSearchForm(forms.Form):
    """Form for searching teachers"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or course...'
        })
    )
    course_filter = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
