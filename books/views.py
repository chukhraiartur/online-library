from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, UpdateView, DeleteView, View
from dal import autocomplete

from .forms import *
from .models import *
from .utils import *

class Home(DataMixin, ListView):
    model = Category
    template_name = 'books/list_categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(c_def.items()))

class BooksAll(DataMixin, ListView):
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
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add book', button='Add')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        book = form.save(commit=False)
        book.user = self.request.user
        book.save()
        return redirect('home')

class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'books/book.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        return dict(list(context.items()) + list(c_def.items()))

class BooksCategory(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'
    allow_empty = False
    
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
        c_def = self.get_user_context(title='Sign Up', button='Sign Up')
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
        c_def = self.get_user_context(title='Sign In', button='Sign In')
        return dict(list(context.items()) + list(c_def.items()))

class ContactFormView(SuccessMessageMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'books/contact.html'
    success_url = reverse_lazy('contact')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact', button='Send')
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

class SignOutUser(View):
    def get(self, request):
        logout(request)
        return redirect('sign_in')
    
def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Oops...</h1>")

class Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Books.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q) | qs.filter(author__icontains=self.q)

        return qs

class Search(DataMixin, TemplateView):
    template_name = 'books/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        context['form'] = BookSearchForm()
        context['search_query'] = search_query
        context['books'] = Books.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
        c_def = self.get_user_context(title='Search')
        return dict(list(context.items()) + list(c_def.items()))

class ProfileView(DataMixin, View):
    template_name = 'books/profile.html'
    form_class = UserProfileForm
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    
class MyBooksView(DataMixin, ListView):
    model = Books
    template_name = 'books/my_books.html'
    context_object_name = 'books'
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Books.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='My Books')
        return dict(list(context.items()) + list(c_def.items()))
    
class EditBookView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Books
    form_class = EditBookForm
    template_name = 'books/edit_book.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'

    def get_queryset(self):
        return Books.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('my_books')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Edit Book', button='Save')
        return dict(list(context.items()) + list(c_def.items()))
    
class DeleteBookView(LoginRequiredMixin, DeleteView):
    model = Books
    template_name = 'books/delete_book.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'

    def get_queryset(self):
        return Books.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('my_books')

class AddToFavoritesView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        if request.user.is_authenticated:
            book = Books.objects.get(pk=book_id)
            FavoriteBook.objects.get_or_create(user=request.user, book=book)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))

class RemoveFromFavoritesView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        if request.user.is_authenticated:
            book = Books.objects.get(id=book_id)
            FavoriteBook.objects.filter(user=request.user, book=book).delete()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        
class FavoriteBooksView(DataMixin, LoginRequiredMixin, View):
    def get(self, request):
        books = Books.objects.filter(is_published=True)
        favorite_books = FavoriteBook.objects.filter(user=request.user)
        return render(request, 'books/favorite_books.html', {'books': books, 'favorite_books': favorite_books})
    