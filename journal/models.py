from django.db import models

# A 'Model' is like a blueprint for a database table.
# Think of this 'Tag' model as a list of labels you can stick on things.
# Analogy: Like a box of physical "Post-it" tags labeled 'Bugfix' or 'Learning'.
class Tag(models.Model):
    # 'CharField' is for short text. We limit it to 50 characters.
    # Analogy: This is the text written on the label itself.
    name = models.CharField(max_length=50)

    # The '__str__' method tells Django how to display this object as text.
    # Without this, it would just say "Tag object (1)" in the admin panel.
    def __str__(self):
        return self.name

# The 'Entry' model represents a single journal post.
# Analogy: Think of this as a single page in your physical notebook.
class Entry(models.Model):
    # We use 'CharField' for a short, single-line title.
    # Analogy: The bold heading at the top of your notebook page.
    title = models.CharField(max_length=255)
    
    # 'TextField' is for long paragraphs of text.
    # Analogy: The actual body of your journal entry where you write your notes.
    body = models.TextField()
    
    # 'ManyToManyField' is the magic part! It links an Entry to many Tags.
    # One entry can have many tags, and one tag can be on many entries.
    # 'blank=True' means you can save an entry even if you don't add any tags.
    # Analogy: This is like having a page in your notebook where you can 
    # stick multiple different colored labels on the corner.
    tags = models.ManyToManyField(Tag, blank=True)
    
    # 'DateTimeField' with 'auto_now_add=True' sets the date automatically.
    # Analogy: This is like a time-stamp machine that clicks the date 
    # onto the paper the moment you finish writing and save it.
    created_at = models.DateTimeField(auto_now_add=True)

    # We return the title so it's easy to identify which entry is which.
    def __str__(self):
        return self.title
