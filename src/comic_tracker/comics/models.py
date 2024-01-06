from django.db import models

# Create your models here.
class Series(models.Model):
    name = models.CharField(max_length=255)
    volume = models.IntegerField()
    year = models.IntegerField()
    pass

class Creator (models.Model):
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name
    
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    series = models.ManyToManyField(Series)
    
class Comic (models.Model):
    name = models.CharField(max_length=255)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    creators = models.ManyToManyField(Creator, through='IssueCredits')
    release_date = models.DateField()
    publisher = models.ManytoManyField(Publisher)

class IssueCredits(models.Model):
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
    creator = models.ForeignKey(Creator)
    issue = models.ForeignKey(Comic)
    role = models.CharField(max_length=2, choices=ROLES)








    