# events/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student','Student'),
        ('faculty','Faculty'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,
                            help_text="Student or Faculty. Superusers are Admin.")
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    date        = models.DateField()
    created_by  = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Media(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )
    MEDIA_TYPE_CHOICES = (
        ('image','Image'),
        ('video','Video'),
    )
    file         = models.FileField(upload_to='media/%Y/%m/%d/')
    media_type   = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    uploaded_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    event        = models.ForeignKey(Event, related_name='media', on_delete=models.CASCADE)
    description  = models.TextField(blank=True)
    category     = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    upload_date  = models.DateTimeField(auto_now_add=True)
    status       = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.media_type} by {self.uploaded_by} for {self.event}"
