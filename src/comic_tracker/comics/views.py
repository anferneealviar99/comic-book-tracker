from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def comics_list(request):
    return HttpResponse("Hello world!")