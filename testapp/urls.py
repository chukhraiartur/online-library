from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),                              # http://127.0.0.1:8000/
    path('books/<int:bookid>/', books),           # http://127.0.0.1:8000/books/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]