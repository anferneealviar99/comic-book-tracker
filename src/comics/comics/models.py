from django.db import models
from accounts.models import CustomUser

class Role(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class ComicBook(models.Model):
    comic_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    series = models.CharField(max_length=255)
    number = models.CharField(max_length=7)
    series_year = models.CharField(max_length=4)
    publisher = models.CharField(max_length=255)
    store_date = models.DateField(null=True, blank=True)
    cover_date = models.DateField(null=True, blank=True)
    cover_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class ComicRole(models.Model):
    comic = models.ForeignKey("ComicBook", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.person.name} - {self.role.name} for {self.comic.title}"
    
class ReadingList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    creator = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name='created_lists')
    is_curated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"

class ListItem(models.Model):
    reading_list = models.ForeignKey("ReadingList", on_delete=models.CASCADE, related_name='items')
    comic = models.ForeignKey("ComicBook", on_delete=models.CASCADE, related_name='list_items')
    order_index = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('reading_list', 'comic')
        ordering = ['order_index']

class UserComic(models.Model):
    STATUS_CHOICES = [
        ("WANT", "Want to Read/Collect"),
        ("COLLECTED", "Collected"),
        ("READ", "Read"),
    ]
    
    LIST_TYPE_CHOICES = [
        ("BACKLOG", "Backlog/Back Issues"),
        ("PULL", "Pull List"),
    ]
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    comic = models.ForeignKey("ComicBook", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WANT')
    list_type = models.CharField(max_length=10, choices=LIST_TYPE_CHOICES, default="BACKLOG")
    source_lists = models.ManyToManyField(ReadingList, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'comic')
    
    def __str__(self):
        return f"{self.user.username} - {self.comic.title} ({self.get_status_display()})"