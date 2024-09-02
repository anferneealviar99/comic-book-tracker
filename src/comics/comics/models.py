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
    series_year = models.CharField(max_length=4)
    publisher = models.CharField(max_length=255)
    cover_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class ComicRole(models.Model):
    comic = models.ForeignKey(ComicBook, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.person.name} - {self.role.name} for {self.comic.title}"
    

class UserComic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comic = models.ForeignKey(ComicBook, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} follows {self.comic.title}"