# events/views.py
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import Event, Media, Category
from .forms import RegistrationForm, EventForm, MediaForm
from .decorators import role_required

def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = form.cleaned_data['role']
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request,'events/register.html',{'form':form})

def home(request):
    #fetch only last 6-8 events
    events = Event.objects.order_by('-date')[:8]
    #Fetch only last 6-8 media
    media = Media.objects.filter(status='approved').order_by('-upload_date')[:8]
    return render(request,'events/home.html',{'events':events,'media':media})

@login_required
@role_required(['faculty','student','faculty'])
def create_event(request):
    # only faculty + admin can create
    if not (request.user.is_superuser or request.user.profile.role=='faculty'):
        return HttpResponseForbidden()
    if request.method=='POST':
        form = EventForm(request.POST)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.created_by = request.user
            ev.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request,'events/create_event.html',{'form':form})

def event_list(request):
    events = Event.objects.order_by('-date')
    return render(request,'events/event_list.html',{'events':events})

def event_detail(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    media = ev.media.filter(status='approved')
    return render(request,'events/event_detail.html',{'event':ev,'media':media})

@login_required
def upload_media(request):
    # student & faculty only
    if not (request.user.is_superuser or request.user.profile.role in ['student','faculty']):
        return HttpResponseForbidden()
    if request.method=='POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save(commit=False)
            m.uploaded_by = request.user
            # auto-approve faculty uploads
            if request.user.is_superuser or request.user.profile.role=='faculty':
                m.status='approved'
            m.save()
            return redirect('gallery')
    else:
        form = MediaForm()
    return render(request,'events/upload_media.html',{'form':form})

@login_required
def approve_media(request, pk, action):
    # only admin
    print(request.user.profile.role)
    if not (request.user.is_superuser or request.user.profile.role=='faculty'):
        return HttpResponseForbidden()
    m = get_object_or_404(Media, pk=pk, status='pending')
    if action=='approve':
        m.status='approved'
    else:
        m.status='rejected'
    m.save()
    return redirect('pending_media_list')

@login_required
def pending_media_list(request):
    if (request.user.is_superuser or request.user.profile.role=='faculty'):
        pending = Media.objects.filter(status='pending')
        return render(request,'events/pending_media.html',{'pending_list':pending})
    else:
        return HttpResponseForbidden()

def gallery(request):
    qs = Media.objects.filter(status='approved')
    cat = request.GET.get('category')
    date = request.GET.get('date')
    if cat:
        qs = qs.filter(category__name=cat)
    if date:
        qs = qs.filter(upload_date__date=date)
    categories = Category.objects.all()
    return render(request,'events/gallery.html',{
        'media_list':qs, 'categories':categories
    })


def custom_logout_view(request):
    logout(request)
    return redirect('login') 

def about(request):
    return render(request, 'events/about.html')

def contact(request):
    return render(request, 'events/contact.html')