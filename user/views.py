from django.shortcuts import render, redirect
from admin_pannel.models import ContactQuery, Job, JobApplication
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, JobApplicationForm
from django.contrib.auth import logout
from django.core.mail import send_mail
# from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
# from .models import Job, JobApplication
# from .forms import RegisterForm, JobApplicationForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def casestudy(request):
    return render(request, 'casestudy.html')


def contact(request):
    if request.method == "POST":
        ContactQuery.objects.create(
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            email=request.POST.get('email'),
            subject = request.POST.get('inquiry'),
            message=request.POST.get('message')
        )
    return render(request, 'contact.html')

def career(request):
    jobs = Job.objects.filter()
    return render(request, 'career.html', {'jobs': jobs})

# def apply_job(request, job_id):
#     job = Job.objects.get(id=job_id)
#     if request.method == "POST":
#         JobApplication.objects.create(
#             job=job,
#             name=request.POST['name'],
#             email=request.POST['email'],
#             resume=request.FILES['resume']
#         )
#         return redirect('career')
#     return render(request, 'apply.html', {'job': job})

# 🔹 LOGIN VIEW (OLD USER)
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             next_url = request.GET.get('next')
#             return redirect(next_url if next_url else 'career')
#         else:
#             messages.error(request, "Invalid credentials")

#     return render(request, 'login.html')


# 🔹 REGISTER VIEW (NEW USER)
def user_register(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            
            # 🔹 Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered. Please login instead.")
                return redirect('login')  # or you can redirect back to register

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)   # auto login

            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'career')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



# 🔹 APPLY JOB (LOGIN REQUIRED)
@login_required(login_url='login')
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if JobApplication.objects.filter(job=job, user=request.user).exists():
        messages.warning(request, "You already applied for this job")
        print("warning")
        return redirect('career')

    if request.method == "POST":

        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            messages.success(request, "Applied successfully!")
            return redirect('career')
            
            
            
    else:
        form = JobApplicationForm()
        print("wrong")
    

    return render(request, 'apply.html', {'job': job, 'form': form})

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid email or password"})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to apply page if coming from ?next=, otherwise career
            return redirect(request.GET.get('next', 'career'))

        return render(request, "login.html", {"error": "Invalid email or password"})

    return render(request, "login.html")




def user_logout(request):
    logout(request)
    next_url = request.GET.get('next', 'career')
    return redirect(next_url)

def industry(request):
    return render(request,'industries.html')



def forgot(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect('forgot')


        
        user = User.objects.get(email=email)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"


        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        messages.success(request, "Password reset link sent to your email")
        # return redirect('')
    else:
        print(5)

    return render(request, "forgot_pass.html")



def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, "Invalid or expired link")
        return redirect("/")

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect(request.path)

        user.set_password(password1)
        user.save()

        messages.success(request, "Password reset successful")
        return redirect("login")

    return render(request, "create_user.html")
        
            
            


