from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', BooksHome.as_view(), name='home'),                         # http://127.0.0.1:8000/
    path('about/', about, name='about'),                                # http://127.0.0.1:8000/about/
    path('addbook/', AddBook.as_view(), name='add_book'),                        # http://127.0.0.1:8000/addbook/
    path('contact/', contact, name='contact'),                          # http://127.0.0.1:8000/contact/
    path('login/', login, name='login'),                                # http://127.0.0.1:8000/login/
    path('book/<slug:book_slug>/', ShowBook.as_view(), name='show_book'),        # http://127.0.0.1:8000/books/1/
    path('category/<slug:cat_slug>/', BooksCategory.as_view(), name='category'),  # http://127.0.0.1:8000/category/1/
    
    
    
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)               # http://127.0.0.1:8000/archive/2022/
]