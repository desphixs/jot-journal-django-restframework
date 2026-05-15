from django.urls import path
# We import our views from the local views.py file.
from .views import TagList, EntryList, EntryDetail

# In Django, every app can have its own private URL file.
# Analogy: This is like a sub-menu for a specific section of a store.
# Instead of one giant list of every item in the whole building, 
# you have a smaller list just for the "Journal" section.

urlpatterns = [
    # We map 'tags/' to our TagList view.
    # Note: We don't include 'api/' here because it will be added in 
    # the main project URL file.
    path('tags/', TagList.as_view(), name='tag-list'),

    # We map 'entries/' to our EntryList view.
    # When someone goes to 'api/entries/', they will see all journal posts.
    path('entries/', EntryList.as_view(), name='entry-list'),

    # We map 'entries/<int:pk>/' to our EntryDetail view.
    # '<int:pk>' is a placeholder for the ID of the entry.
    # Analogy: This is like pointing to a specific locker in a hallway by its number.
    path('entries/<int:pk>/', EntryDetail.as_view(), name='entry-detail'),
]
