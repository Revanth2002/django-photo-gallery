# events/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.create_event, name='create_event'),
    path('media/upload/', views.upload_media, name='upload_media'),
    path('media/pending/', views.pending_media_list, name='pending_media_list'),
    path('media/<int:pk>/<str:action>/', views.approve_media, name='approve_media'),
    path('gallery/', views.gallery, name='gallery'),
]
