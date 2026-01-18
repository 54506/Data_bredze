from django.db import models
from django.contrib.auth.models import User
class ContactQuery(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)



class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    skills = models.TextField(max_length=100)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    resume = models.FileField(upload_to='resumes/')



from django.contrib.auth.hashers import make_password

class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=256)  # hashed password

    def save(self, *args, **kwargs):
        # hash password only if it's not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

