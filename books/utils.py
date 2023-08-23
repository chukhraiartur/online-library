from .models import *
from django.db.models import Count
from django.core.cache import cache

class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('books'))
            cache.set('cats', cats, 60)

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        if self.request.user.is_authenticated:
            favorite_books = self.request.user.favoritebook_set.all()
            context['favorite_books'] = favorite_books

        return context