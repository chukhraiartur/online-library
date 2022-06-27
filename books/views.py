from http.client import HTTPResponse
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

# Create your views here.
def index(request):
    posts = Books.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'books/index.html', context=context)

def about(request):
    return render(request, 'books/about.html', {'menu': menu, 'title': 'О сайте'})

def addpage(request):
    return HttpResponse('Добавление статьи')

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')



def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Oops...</h1>")






def books(request, bookid):
    return HttpResponse(f"<h1>The book {bookid} view.</h1>")

def archive(request, year):
    if int(year) == 2021:
        return redirect('home', permanent=False)
    if int(year) > 2022:
        raise Http404()
    return HttpResponse(f"<h1>The books {year} view.</h1>")

