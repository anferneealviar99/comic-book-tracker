from django.db import models
from django.contrib import admin
from .models import ComicBook, UserComic, ReadingList, ListItem

class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 1
    autocomplete_fields = ['comic']
    ordering = ['order_index']

@admin.register(ComicBook)
class ComicBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'series', 'number', 'publisher', 'cover_date')
    list_filter = ('publisher', 'series')
    search_fields = ('title', 'series', 'publisher')  # This enables autocomplete
    ordering = ('-cover_date', 'series', 'number')
    
@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'is_curated', 'created_at')
    list_filter = ('is_curated', 'creator')
    search_fields = ('title', 'description')
    inlines = [ListItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    
    item_count.short_description = "Number of Comics"
    
    def save_formset(self, request, form, formset, change):
        if formset.model == ListItem:
            # Get the current max order_index for this reading list
            instances = formset.save(commit=False)
            reading_list = form.instance
            
            # Find the highest order_index currently in use
            max_order = reading_list.items.aggregate(
                models.Max('order_index')
            )['order_index__max'] or 0
            
            # Assign incrementing order_index to new items
            next_order = max_order + 1
            for instance in instances:
                if instance.reading_list == reading_list and not instance.pk:
                    # Only set order_index for new items (not yet saved)
                    if not instance.order_index or instance.order_index == 0:
                        instance.order_index = next_order
                        next_order += 1
                    instance.save()
            
            # Handle deleted items
            for obj in formset.deleted_objects:
                obj.delete()
        else:
            formset.save()
    
@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ('reading_list', 'comic', 'order_index')
    list_filter = ('reading_list',)
    ordering = ('reading_list', 'order_index')
    autocomplete_fields = ['reading_list', 'comic']