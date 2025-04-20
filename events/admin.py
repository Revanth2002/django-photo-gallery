# events/admin.py
from django.contrib import admin
from .models import Profile, Category, Event, Media

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Media)
