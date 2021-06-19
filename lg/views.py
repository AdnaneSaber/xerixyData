from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.
from .models import Articles, Cities, User, UserProfile
from django.views.generic import TemplateView
from django.views.generic.base import View
from rest_framework.views import APIView
from .serializers import ArticlesSerializer
from .forms import ProfileForm
from rest_framework.response import Response
from .forms import UserForm
from lg import serializers
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ArticleForm


def index_view(request):
    if request.user.is_authenticated:
        context = User.objects.all()
        if not request.user.is_staff:
            arts = Articles.objects.filter(user=request.user.userprofile)
            count_arts = arts.count()
            return render(request, 'index.html', context={"con": context, 'count_arts': count_arts, 'arts': arts})
        else:
            # arts = Articles.objects.filter(user=request.user)
            return redirect('lg:stats')

    else:
        return redirect('lg:signup')


class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        ctx = super(SignUpView, self).get_context_data(**kwargs)
        ctx['user_form'] = UserForm(prefix='user')
        ctx['profile_form'] = ProfileForm(prefix='profile')
        return ctx

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, prefix='user')
        profile_form = ProfileForm(
            request.POST, request.FILES, prefix='profile')
        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()
            return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
        else:
            return HttpResponse("Error : <a href='/signup'>Try again</a>!")


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('Error: User authentication error <a href="/login"">Try again</a>')
        else:
            return HttpResponse('Error: Username or password is empty <a href="/login">Try again</a>')


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('/')


class buying_view(APIView):
    def post(self, request, id):
        val = Articles.objects.filter(id=id)
        buys = val[0].boughts
        out = val.update(boughts=int(int(buys)+1))
        serializer = ArticlesSerializer(out)
        return Response(serializer.data)

    def get(self, request, id):
        if id:
            buys = Articles.objects.filter(id=id)
            serializer = ArticlesSerializer(buys, many=True)
        else:
            buys = Articles.objects.all()
            serializer = ArticlesSerializer(buys, many=True)

        return Response(serializer.data)


def random_color():
    color = f'{random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}'
    return color


def statistics_city_view(request):
    if not request.user.is_staff:
        return redirect("lg:index")
    else:
        cities = UserProfile.objects.values("city").distinct()
        list_cities = []
        dataSet = []
        colors = []
        for city in cities:
            list_cities.append(Cities.objects.get(id=city['city']))
        for i in list_cities:
            dataSet.append(
                [str(i), int(UserProfile.objects.filter(city=i).count())])
            # dataSet[] =
        for _ in dataSet:
            colors.append(random_color())
        return render(request, 'stats.html', context={'cities': dataSet, 'colors': colors})


def statistics_sells_view(request):
    if not request.user.is_staff:
        return redirect("lg:index")
    else:
        items = Articles.objects.only("name", "boughts")
        dataSet = []
        colors = []
        for item in items:
            dataSet.append(
                [item.name, item.boughts])
        for _ in dataSet:
            colors.append(random_color())
        return render(request, 'sells.html', context={'items': dataSet, 'colors': colors})


def add_article(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArticleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = request.user.userprofile
            price = form.cleaned_data['price']
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            Articles.objects.create(user=user,price=price,name=name,category=category)
            # form.save()
            return HttpResponse("<a href='/'>Return to home</a>")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArticleForm()
    return render(request, "add.html", context={'form': form})
