"""
URL configuration for jot_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# 'include' is a special tool that lets us link to other URL files.
from django.urls import path, include

# The main project URL file is the "Main Switchboard".
# It doesn't need to know every single path; it just points to the 
# right app and says "You handle the rest".

urlpatterns = [
    # The default admin dashboard.
    path('admin/', admin.site.urls),

    # We tell Django: "If any URL starts with 'api/', go look inside 
    # the journal/urls.py file to find the specific match."
    # Analogy: This is like a map of a shopping mall. This file tells you 
    # where the "Journal Store" is. Once you're inside the store, that 
    # store has its own internal map (journal/urls.py).
    path('api/', include('journal.urls')),
]
