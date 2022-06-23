from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import *

menu = ['Главная страница', 'О сайте', 'Поиск книги', 'Добавить книгу', 'Обратная связь', 'Войти']

# Create your views here.
def index(request):
    db_books = Books.objects.all()
    return render(request, 'books/index.html', {'db_books': db_books, 'menu': menu, 'title': 'Главная страница'})

def about(request):
    db_books = Books.objects.all()
    return render(request, 'books/about.html', {'db_books': db_books, 'menu': menu, 'title': 'О сайте'})

def books(request, bookid):
    return HttpResponse(f"<h1>The book {bookid} view.</h1>")

def archive(request, year):
    if int(year) == 2021:
        return redirect('home', permanent=False)
    if int(year) > 2022:
        raise Http404()
    return HttpResponse(f"<h1>The books {year} view.</h1>")

def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Oops...</h1>")