from rest_framework import serializers
# We import our models so the serializers know what data they are translating.
from .models import Tag, Entry

# A 'Serializer' is like a professional translator.
# It takes complex Python objects (models) and translates them into JSON, 
# which is a simple format that any app (frontend, mobile, etc.) can understand.

class TagSerializer(serializers.ModelSerializer):
    # The 'Meta' class tells the serializer which model to use and which fields to include.
    class Meta:
        # We target the 'Tag' model we built in models.py.
        model = Tag
        # '__all__' means we want to include every field (id and name).
        fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
    # This is where the magic happens! 
    # Instead of just showing the ID number of the tags, we use the TagSerializer
    # to show the full tag objects (id and name) inside a list.
    # 'many=True' tells it there could be multiple tags.
    # 'read_only=True' means this nested view is for displaying data, not creating it.
    # Analogy: Like a restaurant menu that doesn't just list "Dish #5", 
    # but actually describes the ingredients inside that dish.
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        # We target the 'Entry' model.
        model = Entry
        # We include all fields (id, title, body, tags, created_at).
        fields = '__all__'
