from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'author', 'description', 'photo', 'get_html_photo', 'is_published', 'cat', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    # the function specifies not to escape the content (so that the image is displayed)
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Thumbnail'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Books, BooksAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_header = 'Admin panel of the website about books'
admin.site.site_title = 'Admin panel of the website about books'