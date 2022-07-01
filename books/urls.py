from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),                                   # http://127.0.0.1:8000/
    path('about/', about, name='about'),                            # http://127.0.0.1:8000/about/
    path('addpage/', add_page, name='add_page'),                    # http://127.0.0.1:8000/addpage/
    path('contact/', contact, name='contact'),                      # http://127.0.0.1:8000/contact/
    path('login/', login, name='login'),                            # http://127.0.0.1:8000/login/
    path('books/<int:book_id>/', show_books, name='show_books'),    # http://127.0.0.1:8000/books/1/
    
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)               # http://127.0.0.1:8000/archive/2022/
]