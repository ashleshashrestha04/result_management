from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeacherSignupForm
from .models import TeacherProfile


def teacher_login(request):
    """
    Teacher login view with authentication.
    
    Handles POST and GET requests:
    - GET: Displays the login form
    - POST: Authenticates teacher and redirects to dashboard
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if user has a teacher profile
                if hasattr(user, 'teacher_profile'):
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect('teacher_app:teacher_dashboard')
                else:
                    messages.error(request, 'This account is not registered as a teacher.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')
    
    return render(request, 'teacher_app/login.html')


@login_required
def teacher_logout(request):
    """
    Teacher logout view.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('teacher_app:teacher_login')


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
                return redirect('teacher_app:teacher_dashboard')
                
            except Exception as e:
                # Handle any unexpected errors during save
                messages.error(request, f'An error occurred while creating your account: {str(e)}')
        else:
            # Form has validation errors
            print("=== TEACHER SIGNUP FORM ERRORS ===")
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors)
            print("=== END ERRORS ===")
            messages.error(request, 'Please correct the errors below to create your teacher account.')
    else:
        # GET request - create empty form
        form = TeacherSignupForm()
    
    # Render the signup form (for GET requests or invalid POST)
    context = {
        'form': form,
    }
    return render(request, 'teacher_app/signup.html', context)


@login_required
def teacher_dashboard(request):
    """
    Teacher dashboard view.
    
    Displays teacher-specific information and quick actions.
    Requires authentication.
    """
    context = {
        'teacher': request.user,
    }
    return render(request, 'teacher_app/dashboard.html', context)
