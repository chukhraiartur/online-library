from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),                                       # http://127.0.0.1:8000/
    path('about/', about, name='about'),                                # http://127.0.0.1:8000/about/
    path('addbook/', add_book, name='add_book'),                        # http://127.0.0.1:8000/addbook/
    path('contact/', contact, name='contact'),                          # http://127.0.0.1:8000/contact/
    path('login/', login, name='login'),                                # http://127.0.0.1:8000/login/
    path('book/<slug:book_slug>/', show_book, name='show_book'),        # http://127.0.0.1:8000/books/1/
    path('category/<slug:cat_slug>/', show_category, name='category'),  # http://127.0.0.1:8000/category/1/
    
    
    
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)               # http://127.0.0.1:8000/archive/2022/
]