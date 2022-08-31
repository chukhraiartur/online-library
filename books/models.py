from django.db import models
from django.urls import reverse

# Create your models here.

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
    title = models.CharField(max_length=255, verbose_name='Title')      # verbose_name - определяет название колонки для админ панели и не является обязательным параметром
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    author = models.TextField(blank=True, verbose_name='Author')
    description = models.TextField(blank=True, verbose_name='Description')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Photo')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')
    is_published = models.BooleanField(default=True, verbose_name='Publication')
    # language, rate, time_read, number_of_pages
    # жанр, теги, доступные форматы для скачивания, автор перевода, автор озвучки 
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_book', kwargs={'book_slug': self.slug})

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['time_create', 'title']
