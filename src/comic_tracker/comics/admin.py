from django.contrib import admin
from.models import Comic, Creator, Series, IssueCredits, Publisher
# Register your models here.
admin.site.register(Comic)
admin.site.register(Creator)
admin.site.register(Series)
admin.site.register(IssueCredits)
admin.site.register(Publisher)
