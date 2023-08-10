from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.cache import cache
from django.core.mail import send_mail

from .models import *
from .forms import *
from .utils import *


class BooksHome(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        books = cache.get('books')
        if not books:
            books = Books.objects.filter(is_published=True).order_by('-time_create').select_related('cat')
            cache.set('books', books, 60)
        return books


class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    # raise_exception = True
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add book')
        return dict(list(context.items()) + list(c_def.items()))


class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'books/book.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'                 # user slug name in the urls
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        return dict(list(context.items()) + list(c_def.items()))


class BooksCategory(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'
    allow_empty = False                 # if slug is incorrect show 404 error
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Display by ' + str(category.name), cat_selected=category.pk)
        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        return Books.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


class SignUpUser(DataMixin, CreateView):
    form_class = SignUpUserForm
    template_name = 'books/sign_up.html'
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign Up')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class SignInUser(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'books/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign In')
        return dict(list(context.items()) + list(c_def.items()))


# FormView - the standard base class for forms that are not model-bound. This form will not work with DB
class ContactFormView(SuccessMessageMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'books/contact.html'
    success_url = reverse_lazy('contact')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        send_mail(
            subject=f"Contact Form Submission from {form.cleaned_data['name']}",
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['arturchukhrai@gmail.com'],  # Your work email
            fail_silently=False,
        )
        messages.success(self.request, "Your message has been successfully sent!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in the contact form submission.")
        return super().form_invalid(form)
        

def sign_out_user(request):
    logout(request)
    return redirect('sign_in')
    
def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Oops...</h1>")

def books(request, bookid):
    return HttpResponse(f"<h1>The book {bookid} view.</h1>")

def about(request):
    return render(request, 'books/about.html', {'menu': menu, 'title': 'About the site'})

def archive(request, year):
    if int(year) == 2021:
        return redirect('home', permanent=False)
    if int(year) > 2022:
        raise Http404()
    return HttpResponse(f"<h1>The books {year} view.</h1>")
