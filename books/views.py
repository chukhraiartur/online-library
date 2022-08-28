from http.client import HTTPResponse
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import *

menu = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add page', 'url_name': 'add_page'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
]

# Create your views here.
def index(request):
    posts = Books.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'books/index.html', context=context)

def about(request):
    return render(request, 'books/about.html', {'menu': menu, 'title': 'О сайте'})

def add_page(request):
    return HttpResponse('Добавление статьи')

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def show_books(request, book_id):
    return HttpResponse(f'Отображение статьи с id = {book_id}')

def show_category(request, cat_id):
    posts = Books.objects.filter(cat_id=cat_id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(request, 'books/index.html', context=context)

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

