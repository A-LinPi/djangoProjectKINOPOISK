from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from catalog_app.forms import SignUp
from catalog_app.models import *
from django.views import generic


# Create your views here.
def index(request):
    items = Kino.objects.all()
    items2 = Kino.objects.filter(podpiska__level='free')
    data = {'k1': items.count(), 'K2': items2.count()}
    return render(request, 'index.html', data)


class kinolist(generic.ListView):
    model = Kino


class kinodetail(generic.DetailView):
    model = Kino


class directorlist(generic.ListView):
    model = Director


class directordetail(generic.DetailView):
    model = Director


def reg(request):
    if request.POST:
        f = SignUp(request.POST)
        if f.is_valid():
            f.save()
            K1 = f.cleaned_data.get('username')
            K2 = f.cleaned_data.get('password')
            K3 = f.cleaned_data.get('email')
            K4 = f.cleaned_data.get('first_name')
            K5 = f.cleaned_data.get('last_name')

            user = authenticate(username=K1, password=K2)
            newuser = User.objects.get(username=K1)
            newuser.email = K3
            newuser.first_name = K4
            newuser.last_name = K5
            newuser.save()
            login(request, newuser)
            return redirect('home')
    else:
        f = SignUp()
    data = {'forma': f}
    return render(request, "registration/registration.html", data)
    # return redirect('home')
