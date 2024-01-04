from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from catalog_app.forms import SignUp, CommentForm
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
    paginate_by = 4


class kinodetail(generic.DetailView):
    model = Kino


class directorlist(generic.ListView):
    model = Director
    paginate_by = 4


class directordetail(generic.DetailView):
    model = Director


def proverka(newcom):
    blacklist = ['жопа']
    spisok = newcom.body.split()
    active = True
    for one in spisok:
        if one in blacklist:
            newcom.delete()
            active = False

    if active:
        newcom.active = True
        newcom.save()
        # breakpoint()


def kinodetail(request, pk):
    film = Kino.objects.get(id=pk)
    comments = film.comment_set.filter(active=True)
    forma = CommentForm()
    if request.POST:
        newcom = Comment()
        newcom.body = request.POST.get('body')
        newcom.kino = film
        newcom.user = request.user
        newcom.save()
        proverka(newcom)
    data = {'kino': film, 'form': forma, 'comments': comments}
    return render(request, 'catalog_app/kino_detail.html', data)


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
            ProfileUser.objects.create(user_id=newuser.id, podpiska_id=1)
            login(request, newuser)
            return redirect('home')
    else:
        f = SignUp()
    data = {'forma': f}
    return render(request, "registration/registration.html", data)
    # return redirect('home')


class actorlist(generic.ListView):
    model = Actor
    paginate_by = 4


class actordetail(generic.DetailView):
    model = Actor


def topodpiska(request, userid):
    data = {}
    if request.POST:
        print(userid)
        print('ok1')
        if request.POST.get('stype'):
            stype = request.POST.get('stype')
            print(stype)
            user = User.objects.get(id=userid)
            newpodp = Podpiska.objects.get(level=stype)
            if stype == 'free':
                user.profileuser.podpiska = newpodp
            elif stype == 'based' and user.profileuser.balance >= 1:
                user.profileuser.balance -= 1
                user.profileuser.podpiska = newpodp
            elif stype == 'super' and user.profileuser.balance >= 5:
                user.profileuser.balance -= 5
                user.profileuser.podpiska = newpodp
                user.profileuser.save()
        elif request.POST.get('summa'):
            summa = request.POST.get('summa')
            print(summa)
            user = User.objects.get(id=userid)
            user.profileuser.balance += int(summa)
            user.profileuser.save()
    return render(request, 'catalog_app/podpiska.html', data)
