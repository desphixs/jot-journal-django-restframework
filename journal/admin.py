from django.contrib import admin
# We import our models so we can tell the Admin panel about them.
from .models import Tag, Entry

# Registering a model means it will show up in the Django Admin dashboard.
# Analogy: This is like adding a new folder to a filing cabinet so you 
# can easily see and edit the papers inside.

# We register 'Tag' so we can create new labels like #bugfix or #learning.
admin.site.register(Tag)

# We register 'Entry' so we can write journal posts and attach our tags.
admin.site.register(Entry)
