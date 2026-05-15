from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# We import our models and serializers from the current app.
from .models import Tag, Entry
from .serializers import TagSerializer, EntrySerializer

# An 'APIView' is like the brain of your endpoint.
# It takes in a request (like "Get me all tags"), processes it, 
# and sends back a response (like a list of JSON tags).
# Analogy: Think of this as the Chef in a kitchen. They receive 
# an order, cook the food, and put it on a plate to be served.

class TagList(APIView):
    # The 'get' method handles HTTP GET requests.
    # This is used for "Read" operations—simply asking for data.
    def get(self, request):
        # 1. We grab all the 'Tag' objects from our database.
        # Analogy: Getting all the labeled jars out of the pantry.
        tags = Tag.objects.all()
        
        # 2. we pass the tags to our Serializer (the translator).
        # 'many=True' tells the translator that we are giving it a 
        # list of objects, not just one single object.
        serializer = TagSerializer(tags, many=True)
        
        # 3. We return the translated JSON data inside a Response object.
        # This sends the data back to the user with a "200 OK" status by default.
        return Response(serializer.data)
