from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),                       # http://127.0.0.1:8000/
    path('about/', about, name='about'),                # http://127.0.0.1:8000/about/
    path('books/<int:bookid>/', books),                 # http://127.0.0.1:8000/books/1/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)   # http://127.0.0.1:8000/archive/2022/
]