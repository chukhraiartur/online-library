from http.client import HTTPResponse
import pkgutil
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from .models import *

menu = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add page', 'url_name': 'add_page'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
]

# Create your views here.
def index(request):
    books = Books.objects.all()

    context = {
        'books': books,
        'menu': menu,
        'title': 'Main page',
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

def show_book(request, book_slug):
    book = get_object_or_404(Books, slug=book_slug)

    context = {
        'book': book,
        'menu': menu,
        'title': book.title,
        'cat_selected': book.cat_id,
    }

    return render(request, 'books/book.html', context=context)


def show_category(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    books = Books.objects.filter(cat_id=cat.id)

    if len(books) == 0:
        raise Http404()

    context = {
        'books': books,
        'menu': menu,
        'title': 'Display by category',
        'cat_selected': cat.id,
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

