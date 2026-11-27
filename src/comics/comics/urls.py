"""
URL configuration for comics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepage_view, name="home"),
    path('my-comics/', views.user_comics, name='user_comics'),
    path('add-comic/', views.add_comic, name='add_comic'),
    path('select-comic/', views.select_comic, name='select_comic'),
    path('fetch-comic-details/<str:comic_id>/', views.fetch_comic_details, name='fetch_comic_details'),
    path('new-comics/', views.new_comics, name='new_comics'),
    path('remove-comic/<str:comic_id>', views.remove_comic, name='remove_comic'),
    path('change-username/', views.change_username, name='change_username'),
    path('reading-list/<int:pk>/', views.reading_list_detail, name='reading_list_detail')
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


