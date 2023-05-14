"""social_media_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, 
                                   document_root = settings.MEDIA_ROOT)

# urlpatterns is a list of URL patterns defined in a Django application that maps URLs to view functions or classes.
# static() is a utility function provided by Django to serve static files, including media files.
# settings.MEDIA_URL is a string that specifies the URL prefix for media files. This is usually set to '/media/' in Django settings.
# settings.MEDIA_ROOT is a string that specifies the absolute filesystem path to the directory where media files are stored.
# The + operator is used to concatenate the existing URL patterns in urlpatterns with the new URL pattern that serves media files.
# The new URL pattern is generated using static() function, which takes two arguments:
# The first argument, settings.MEDIA_URL, specifies the URL prefix for media files that need to be served.
# The second argument, document_root=settings.MEDIA_ROOT, specifies the absolute filesystem path to the directory where media files are stored.
# The document_root argument tells Django where to look for the media files when serving them.
# So, the line urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) adds a new URL pattern to the existing list of URL patterns in urlpatterns, which maps the settings.MEDIA_URL to the directory specified in settings.MEDIA_ROOT, allowing Django to serve media files from the specified directory.
