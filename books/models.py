from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Category')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

class Books(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    author = models.TextField(blank=True, verbose_name='Author')
    description = models.TextField(blank=True, verbose_name='Description')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Photo')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')
    is_published = models.BooleanField(default=True, verbose_name='Publication')
    pdf_file = models.FileField(upload_to='books/pdfs/', blank=True, null=True, verbose_name='PDF File')
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('show_book', kwargs={'book_slug': self.slug})

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['time_create', 'title']

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name='Book')

    class Meta:
        unique_together = ('user', 'book')