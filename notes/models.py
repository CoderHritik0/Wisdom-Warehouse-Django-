from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class note(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    tag = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#ffffff")
    is_hidden = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.note_id}';

class note_image(models.Model):
    image_id = models.AutoField(primary_key=True)
    note = models.ForeignKey(note, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="notes/images/", max_length=None)

    def __str__(self):
        return f"Image {self.image_id} for Note_ID: {self.note.note_id}"