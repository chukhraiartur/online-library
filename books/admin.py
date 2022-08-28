from django.contrib import admin
from .models import *

# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Books, BooksAdmin)
admin.site.register(Category, CategoryAdmin)