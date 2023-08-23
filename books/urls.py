from django.urls import path
from .views import *

urlpatterns = [
    # path('', BooksHome.as_view(), name='home'),
    path('', Home.as_view(), name='home'),
    path('add_book/', AddBook.as_view(), name='add_book'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('sign_up/', SignUpUser.as_view(), name='sign_up'),
    path('sign_in/', SignInUser.as_view(), name='sign_in'),
    path('sign_out/', SignOutUser.as_view(), name='sign_out'),
    path('book/<slug:book_slug>/', ShowBook.as_view(), name='show_book'),
    path('category/all_books/', BooksAll.as_view(), name='all_books'),
    path('category/<slug:cat_slug>/', BooksCategory.as_view(), name='category'),
    path('search/', Search.as_view(), name='search'),
    path('autocomplete/', Autocomplete.as_view(), name='autocomplete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my_books/', MyBooksView.as_view(), name='my_books'),
    path('edit_book/<int:book_id>/', EditBookView.as_view(), name='edit_book'),
    path('delete_book/<int:book_id>/', DeleteBookView.as_view(), name='delete_book'),
    path('add_to_favorites/<int:book_id>/', AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('remove_from_favorites/<int:book_id>/', RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
    path('favorite_books/', FavoriteBooksView.as_view(), name='favorite_books'),
]