from django.db import models

# Create your models here.
class Series(models.Model):
    name = models.CharField(max_length=255)
    volume = models.IntegerField()
    year = models.IntegerField()
    pass

class Creator(models.Model):
    ROLES = {
        "WR": "Writer",
        "AR": "Artist",
        "PE": "Penciller",
        "IN": "Inker",
        "LE": "Letterer",
        "CO": "Colourist",
        "PL": "Plot",
        "ED": "Editor"
    }
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=2, choices=ROLES)

class Publisher(models.Model):
    pass

class Comic (models.Model):
    name = models.CharField(max_length=255)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    writer = models.ManyToManyField(Creator, related_name="Writer")
    publisher = models.ManytoManyField(Publisher)
    

    