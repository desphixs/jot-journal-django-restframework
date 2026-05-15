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

    # The 'post' method handles HTTP POST requests.
    # This is used for "Create" operations—sending data to the server to be saved.
    def post(self, request):
        # 1. We pass the incoming data (request.data) to our Serializer.
        # Analogy: This is like handing a completed form to a clerk.
        serializer = TagSerializer(data=request.data)
        
        # 2. We check if the data follows the rules (like max_length=50).
        # Analogy: The clerk checking if you filled out all the required 
        # boxes on the form correctly.
        if serializer.is_valid():
            # 3. If valid, we save the new 'Tag' to the database.
            # Analogy: The clerk stamping the form "Approved" and filing it.
            serializer.save()
            
            # 4. We return the newly created tag data with a "201 Created" status.
            # 201 is the standard "Success! New thing created" code.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 5. If the data is bad (invalid), we return the errors and a "400 Bad Request" status.
        # 400 is the standard code for "You made a mistake in your request".
        # Analogy: The clerk handing the form back to you with red circles 
        # around the mistakes you made.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
