from http.client import HTTPResponse
# import pkgutil
from django.views.generic import ListView, DetailView, CreateView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *

menu = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add book', 'url_name': 'add_book'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
]

# Create your views here.

class BooksHome(ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context
    
    def get_queryset(self):
        return Books.objects.filter(is_published=True).order_by('-time_create')

# def index(request):
#     # books = Books.objects.all()
#     books = Books.objects.order_by('-time_create')

#     context = {
#         'books': books,
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0,
#     }

#     return render(request, 'books/index.html', context=context)

def about(request):
    return render(request, 'books/about.html', {'menu': menu, 'title': 'About the site'})

class AddBook(CreateView):
    form_class = AddBookForm
    template_name = 'books/add_book.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add book'
        context['menu'] = menu
        return context

# def add_book(request):
#     if request.method == 'POST':
#         form = AddBookForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')       
#     else:
#         form = AddBookForm()

#     context = {
#         'form': form, 
#         'menu': menu, 
#         'title': 'Add a book that you like and want to share with other people 😊'
#     }

#     return render(request, 'books/add_book.html', context=context)

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

class ShowBook(DetailView):
    model = Books
    template_name = 'books/book.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'                 # user slug name in the urls
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['book']
        context['menu'] = menu
        # context['cat_selected'] = Category.objects.get(slug=self.kwargs['cat_slug']).id
        context['cat_selected'] = context['book'].cat_id
        return context

# def show_book(request, book_slug):
#     book = get_object_or_404(Books, slug=book_slug)

#     context = {
#         'book': book,
#         'menu': menu,
#         'title': book.title,
#         'cat_selected': book.cat_id,
#     }

#     return render(request, 'books/book.html', context=context)


class BooksCategory(ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'
    allow_empty = False                 # if slug is incorrect show 404 error
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Display by ' + str(context['books'][0].cat)
        context['menu'] = menu
        # context['cat_selected'] = Category.objects.get(slug=self.kwargs['cat_slug']).id
        context['cat_selected'] = context['books'][0].cat_id
        return context

    def get_queryset(self):
        return Books.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

# def show_category(request, cat_slug):
#     cat = Category.objects.get(slug=cat_slug)
#     books = Books.objects.filter(cat_id=cat.id)

#     if len(books) == 0:
#         raise Http404()

#     context = {
#         'books': books,
#         'menu': menu,
#         'title': 'Display by category',
#         'cat_selected': cat.id,
#     }

#     return render(request, 'books/index.html', context=context)

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

