from django.shortcuts import render
from django.views.generic import DetailView, ListView

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
