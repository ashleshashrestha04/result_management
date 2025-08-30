from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Student, Teacher
from .forms import StudentForm, TeacherForm, StudentSearchForm, TeacherSearchForm, StudentSignupForm, TeacherSignupForm

# Create your views here.
def home(request):  
    return render(request, 'student_app/home.html')

def signup(request):
    """Combined signup page for both students and teachers"""
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        
        if user_type == 'student':
            form = StudentSignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, f'🎉 Student account created successfully for {user.get_full_name()}! Welcome to MyAcademia!')
                login(request, user)  # Auto login after signup
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Please correct the errors below to create your student account.')
        elif user_type == 'teacher':
            form = TeacherSignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, f'🎉 Teacher account created successfully for {user.get_full_name()}! Welcome to MyAcademia!')
                login(request, user)  # Auto login after signup
                return redirect('student_dashboard')  # You can create a teacher dashboard later
            else:
                messages.error(request, 'Please correct the errors below to create your teacher account.')
        else:
            messages.error(request, 'Please select a valid user type (Student or Teacher).')
    
    context = {
        'student_form': StudentSignupForm(),
        'teacher_form': TeacherSignupForm(),
    }
    return render(request, 'student_app/signup.html', context)

def student_signup(request):
    """
    Django view function for student registration.
    
    Handles POST and GET requests:
    - GET: Displays the signup form
    - POST: Processes form submission, validates input, saves student profile,
            logs student in automatically, and redirects to dashboard
    """
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        
        if form.is_valid():
            try:
                # Save the user and create student profile
                user = form.save()
                
                # Add success message
                messages.success(
                    request, 
                    f'🎉 Student account created successfully for {user.get_full_name()}! Welcome to MyAcademia!'
                )
                
                # Log the student in automatically
                login(request, user)
                
                # Redirect to student dashboard
                return redirect('student_dashboard')
                
            except Exception as e:
                # Handle any unexpected errors during save
                messages.error(request, f'An error occurred while creating your account: {str(e)}')
        else:
            # Form has validation errors
            messages.error(request, 'Please correct the errors below to create your student account.')
    else:
        # GET request - create empty form
        form = StudentSignupForm()
    
    # Render the signup form (for GET requests or invalid POST)
    context = {
        'form': form,
    }
    return render(request, 'student_app/signup_student.html', context)

def teacher_signup(request):
    """
    Django view function for teacher registration.
    
    Handles POST and GET requests:
    - GET: Displays the signup form
    - POST: Processes form submission, validates input, saves teacher profile,
            logs teacher in automatically, and redirects to teacher dashboard
    """
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        
        if form.is_valid():
            try:
                # Save the user and create teacher profile
                user = form.save()
                
                # Add success message
                messages.success(
                    request, 
                    f'🎉 Teacher account created successfully for {user.get_full_name()}! Welcome to MyAcademia!'
                )
                
                # Log the teacher in automatically
                login(request, user)
                
                # Redirect to teacher dashboard
                return redirect('teacher_dashboard')
                
            except Exception as e:
                # Handle any unexpected errors during save
                messages.error(request, f'An error occurred while creating your account: {str(e)}')
        else:
            # Form has validation errors
            messages.error(request, 'Please correct the errors below to create your teacher account.')
    else:
        # GET request - create empty form
        form = TeacherSignupForm()
    
    # Render the signup form (for GET requests or invalid POST)
    context = {
        'form': form,
    }
    return render(request, 'student_app/signup_teacher.html', context)

def student_login(request):
    """Combined login page for both students and teachers"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'student')  # Default to student
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Check if user type matches their profile
            try:
                if user_type == 'student':
                    student_profile = Student.objects.get(user=user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect('student_dashboard')
                elif user_type == 'teacher':
                    teacher_profile = Teacher.objects.get(user=user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect('student_dashboard')  # You can create teacher dashboard later
            except (Student.DoesNotExist, Teacher.DoesNotExist):
                # If profile doesn't match selected type, still allow login
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'student_app/student_login.html')

@login_required
def student_dashboard(request):
    return render(request, 'student_app/student_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'student_app/teacher_dashboard.html')

def student_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ============== STUDENT CRUD VIEWS ==============

def student_list(request):
    """Display list of all students with search and pagination"""
    students = Student.objects.all()
    search_form = StudentSearchForm(request.GET)
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        course_filter = search_form.cleaned_data.get('course_filter')
        grade_filter = search_form.cleaned_data.get('grade_filter')
        
        if search_query:
            students = students.filter(
                Q(name__icontains=search_query) |
                Q(roll_number__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(course__icontains=search_query)
            )
        
        if course_filter:
            students = students.filter(course__icontains=course_filter)
            
        if grade_filter:
            students = students.filter(grade=grade_filter)
    
    # Pagination
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_students': students.count(),
    }
    return render(request, 'student_app/student_list.html', context)


def student_detail(request, pk):
    """Display detailed view of a single student"""
    student = get_object_or_404(Student, pk=pk)
    context = {
        'student': student,
    }
    return render(request, 'student_app/student_detail.html', context)


def student_create(request):
    """Create a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.name}" created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'student_app/student_form.html', context)


def student_update(request, pk):
    """Update an existing student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student "{student.name}" updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'action': 'Update',
    }
    return render(request, 'student_app/student_form.html', context)


def student_delete(request, pk):
    """Delete a student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_name = student.name
        student.delete()
        messages.success(request, f'Student "{student_name}" deleted successfully!')
        return redirect('student_list')
    
    context = {
        'student': student,
        'object_type': 'Student',
    }
    return render(request, 'student_app/confirm_delete.html', context)


# ============== TEACHER CRUD VIEWS ==============

def teacher_list(request):
    """Display list of all teachers with search and pagination"""
    teachers = Teacher.objects.all()
    search_form = TeacherSearchForm(request.GET)
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        course_filter = search_form.cleaned_data.get('course_filter')
        
        if search_query:
            teachers = teachers.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(course__icontains=search_query)
            )
        
        if course_filter:
            teachers = teachers.filter(course__icontains=course_filter)
    
    # Pagination
    paginator = Paginator(teachers, 10)  # 10 teachers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_teachers': teachers.count(),
    }
    return render(request, 'student_app/teacher_list.html', context)


def teacher_detail(request, pk):
    """Display detailed view of a single teacher"""
    teacher = get_object_or_404(Teacher, pk=pk)
    context = {
        'teacher': teacher,
    }
    return render(request, 'student_app/teacher_detail.html', context)


def teacher_create(request):
    """Create a new teacher"""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher "{teacher.name}" created successfully!')
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'student_app/teacher_form.html', context)


def teacher_update(request, pk):
    """Update an existing teacher"""
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Teacher "{teacher.name}" updated successfully!')
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
        'action': 'Update',
    }
    return render(request, 'student_app/teacher_form.html', context)


def teacher_delete(request, pk):
    """Delete a teacher"""
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        teacher_name = teacher.name
        teacher.delete()
        messages.success(request, f'Teacher "{teacher_name}" deleted successfully!')
        return redirect('teacher_list')
    
    context = {
        'teacher': teacher,
        'object_type': 'Teacher',
    }
    return render(request, 'student_app/confirm_delete.html', context)


# ============== API VIEWS (Optional) ==============

def student_search_api(request):
    """AJAX endpoint for student search"""
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(email__icontains=query)
        )[:10]  # Limit to 10 results
        
        data = [{
            'id': student.id,
            'name': student.name,
            'roll_number': student.roll_number,
            'email': student.email,
            'course': student.course,
            'grade': student.grade,
        } for student in students]
        
        return JsonResponse({'students': data})
    
    return JsonResponse({'students': []})


def teacher_search_api(request):
    """AJAX endpoint for teacher search"""
    query = request.GET.get('q', '')
    if query:
        teachers = Teacher.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )[:10]  # Limit to 10 results
        
        data = [{
            'id': teacher.id,
            'name': teacher.name,
            'email': teacher.email,
            'course': teacher.course,
            'hire_date': teacher.hire_date.strftime('%Y-%m-%d'),
        } for teacher in teachers]
        
        return JsonResponse({'teachers': data})
    
    return JsonResponse({'teachers': []})


def get_student_grade(request, pk):
    """Get student grade by marks (AJAX endpoint)"""
    student = get_object_or_404(Student, pk=pk)
    return JsonResponse({
        'grade': student.grade,
        'marks': float(student.marks),
    })
