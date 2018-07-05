"""blog_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from places.urls import urlpatterns as places_urls
from articles.urls import urlpatterns as articles_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('places/', include(places_urls, namespace='places')),
    path('articles/', include(articles_urls, namespace='articles')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
