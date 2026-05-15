from django.urls import path
# We import our views from the local views.py file.
from .views import TagList

# In Django, every app can have its own private URL file.
# Analogy: This is like a sub-menu for a specific section of a store.
# Instead of one giant list of every item in the whole building, 
# you have a smaller list just for the "Journal" section.

urlpatterns = [
    # We map 'tags/' to our TagList view.
    # Note: We don't include 'api/' here because it will be added in 
    # the main project URL file.
    path('tags/', TagList.as_view(), name='tag-list'),
]
