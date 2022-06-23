from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.TextField(blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    # language, rate, time_read, number_of_pages
    # жанр, теги, доступные форматы для скачивания, автор перевода, автор озвучки 

    def __str__(self):
        return self.title