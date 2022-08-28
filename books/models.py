from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Category')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']


class Books(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')      # verbose_name - определяет название колонки для админ панели и не является обязательным параметром
    author = models.TextField(blank=True, verbose_name='Author')
    description = models.TextField(blank=True, verbose_name='Description')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Photo')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')
    is_published = models.BooleanField(default=True, verbose_name='Publication')
    # language, rate, time_read, number_of_pages
    # жанр, теги, доступные форматы для скачивания, автор перевода, автор озвучки 
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Category')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_books', kwargs={'book_id': self.pk})

    class Meta:
        verbose_name = 'Famous book'
        verbose_name_plural = 'Famous books'
        ordering = ['time_create', 'title']
