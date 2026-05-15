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

# The 'EntryList' view handles our journal entries.
# Since we already have the 'EntrySerializer' set up with nested tags, 
# this view will automatically show the full details of every tag!
class EntryList(APIView):
    # The 'get' method for our entries.
    def get(self, request):
        # 1. We fetch all entries from the database.
        # Analogy: Opening our notebook and looking at every page we've written.
        entries = Entry.objects.all()
        
        # 2. We pass the entries to the 'EntrySerializer'.
        # This will automatically call the 'TagSerializer' for each tag 
        # inside each entry because of how we built the serializer!
        serializer = EntrySerializer(entries, many=True)
        
        # 3. We return the final JSON.
        return Response(serializer.data)

    # The 'post' method handles creating new journal entries.
    # This is slightly more complex because we have to link tags (Many-to-Many)!
    def post(self, request):
        # 1. We pass the data to our translator.
        # Analogy: Handing the filled-out "New Entry" form to the clerk.
        serializer = EntrySerializer(data=request.data)
        
        # 2. Check if the title and body are valid.
        if serializer.is_valid():
            # 3. If valid, we save the entry first.
            # We save it to a variable 'entry' so we can link tags to it in the next step.
            # Analogy: The clerk files the new notebook page first...
            entry = serializer.save()
            
            # 4. We grab the 'tags' list from the raw request data.
            # The user should send a list of IDs, like: "tags": [1, 3]
            tag_ids = request.data.get('tags')
            
            # 5. If the user actually provided some tags, we link them.
            if tag_ids:
                # '.set()' is a special Django method for Many-to-Many fields.
                # It clears any old tags and replaces them with this new list of IDs.
                # Analogy: ...and then the clerk sticks the physical labels 
                # onto the corner of that page.
                entry.tags.set(tag_ids)
            
            # 6. We return the final entry data (including the new tags) with 201 status.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 7. If data is bad, return errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# The 'EntryDetail' view handles actions on a single, specific journal entry.
# We use the 'pk' (Primary Key) from the URL to figure out which entry 
# the user is talking about.
# Analogy: This is like a librarian going into the back room to find 
# a specific book by its unique ID number.
class EntryDetail(APIView):
    # The 'get' method for a single entry.
    def get(self, request, pk):
        # 1. We try to find the entry in the database by its unique ID (pk).
        try:
            # Analogy: The librarian searching the shelf for that specific ID.
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            # 2. If it's not there, we return a "404 Not Found" error.
            # Analogy: Telling the user "Sorry, we don't have that book in our library."
            return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # 3. If found, we translate it using our serializer.
        # Note: We don't use 'many=True' here because we are only 
        # translating ONE single object.
        serializer = EntrySerializer(entry)
        
        # 4. Return the JSON.
        return Response(serializer.data)

    # The 'put' method handles updating (editing) an existing journal entry.
    def put(self, request, pk):
        # 1. We look up the entry first, just like we did in the 'get' method.
        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # 2. We pass the EXISTING entry and the NEW data to the serializer.
        # Analogy: This is like handing the clerk the original notebook page 
        # along with a list of corrections you want to make.
        serializer = EntrySerializer(entry, data=request.data)
        
        # 3. Validate the new data.
        if serializer.is_valid():
            # 4. Save the changes.
            serializer.save()
            
            # 5. Handle the Many-to-Many tags update.
            tag_ids = request.data.get('tags')
            if tag_ids:
                # This replaces the old labels with the new ones.
                entry.tags.set(tag_ids)
                
            # 6. Return the updated data.
            return Response(serializer.data)
            
        # 7. Return errors if data was bad.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
