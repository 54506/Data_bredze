from django.shortcuts import render, redirect,get_object_or_404
from .models import ContactQuery, Job, JobApplication


def admin_main(request):
    return render(request,'admin.html')


def dashboard(request):
    context = {
        "total_applicants": JobApplication.objects.count(),
        "total_queries": ContactQuery.objects.count(),
        "total_jobs": Job.objects.count(),
    }
    return render(request, "dashboard.html", context)



def contacts(request):
    data = ContactQuery.objects.all()
    return render(request, 'contacts.html', {'data': data})

def delete_contact(request, query_id):
    if request.method == "POST":
        query = get_object_or_404(ContactQuery, id=query_id)
        query.delete()
        messages.success(request, "Message deleted successfully")
    return redirect("contacts")

def jobs(request):
    jobs = Job.objects.all()
    return render(request, 'jobs.html', {'jobs': jobs})

def add_job(request):
    if request.method == "POST":
        Job.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            experience = request.POST['Experience'],
            skills = request.POST['skills'],
        )
        return redirect('job')
    return render(request, 'add_jobs.html')
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        job.title = request.POST['title']
        job.experience = request.POST['experience']
        job.location = request.POST['location']
        job.skills = request.POST['skills'],
        job.is_active = True if request.POST.get('is_active') == 'on' else False
        job.save()
        return redirect('job')

    return render(request, 'edit.html', {'job': job})


# Delete Job
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('job')

def applications(request):
    apps = JobApplication.objects.all()
    return render(request, 'applications.html', {'apps': apps})

def delete_application(request, app_id):
    if request.method == "POST":
        application = get_object_or_404(JobApplication, id=app_id)
        application.delete()
        # messages.success(request, "Application deleted successfully!")
    return redirect('applications')
# admin_panel/views.py
from django.shortcuts import render, redirect
from .models import AdminUser
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = AdminUser.objects.get(username=username)
            if check_password(password, admin.password):
                request.session['admin_logged_in'] = True
                request.session['admin_username'] = username
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password")
        except AdminUser.DoesNotExist:
            messages.error(request, "Invalid username")

    return render(request, 'admin-login.html')


