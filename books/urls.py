from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', BooksHome.as_view(), name='home'),
    path('add_book/', AddBook.as_view(), name='add_book'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('sign_up/', SignUpUser.as_view(), name='sign_up'),
    path('sign_in/', SignInUser.as_view(), name='sign_in'),
    path('sign_out/', sign_out_user, name='sign_out'),
    path('book/<slug:book_slug>/', ShowBook.as_view(), name='show_book'),
    path('category/<slug:cat_slug>/', BooksCategory.as_view(), name='category'),
    path('search/', Search.as_view(), name='search'),
    path('autocomplete/', Autocomplete.as_view(), name='autocomplete'),
]