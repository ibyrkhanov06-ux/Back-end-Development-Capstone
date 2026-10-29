from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req
import os


# Create your views here.

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'signup.html', {'form': form})


def index(request):
    return render(request, "index.html")


def songs(request):
    response = req.get(os.environ.get('SONGS_URL', 'http://127.0.0.1:5001') + '/song', timeout=10)
    response.raise_for_status()
    data = response.json()
    return render(request, 'songs.html', {'songs': data.get('songs', []) if isinstance(data, dict) else data})


def photos(request):
    response = req.get(os.environ.get('PICTURES_URL', 'http://127.0.0.1:5000') + '/picture', timeout=10)
    response.raise_for_status()
    photos = response.json()
    if request.GET.get('id'):
        photos = [photo for photo in photos if str(photo['id']) == request.GET['id']]
    return render(request, 'photos.html', {'photos': photos})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def concerts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    rows = []
    for concert in Concert.objects.all():
        attending = concert.attendee.filter(user=request.user).first()
        rows.append({'concert': concert, 'status': attending.attending if attending else '-'})
    return render(request, 'concerts.html', {'concerts': rows})


def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
