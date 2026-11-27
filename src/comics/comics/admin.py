from django.contrib import admin
from .models import ComicBook, UserComic, ReadingList, ListItem

@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'is_curated', 'created_at')
    list_filter = ('is_curated', 'creator')
    search_fields = ('title', 'description')
    
@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ('reading_list', 'comic', 'order_index')
    list_filter = ('reading_list',)
    ordering = ('reading_list', 'order_index')