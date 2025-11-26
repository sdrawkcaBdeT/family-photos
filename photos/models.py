from django.db import models
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
import os
from io import BytesIO
from django.core.files.base import ContentFile

# Register HEIF opener to handle .heic files
register_heif_opener()

class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    uploader_name = models.CharField(max_length=100)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Open image using Pillow (handles HEIC via pillow-heif)
        if self.image:
            img = Image.open(self.image)
            
            # Fix Orientation from EXIF
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                
                exif = img._getexif()
                if exif is not None:
                    orientation = exif.get(orientation)
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # No EXIF or other error, ignore
                pass

            # Convert to RGB (removes alpha channel, required for JPEG)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save as JPEG
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)

            # Change extension to .jpg
            new_name = os.path.splitext(self.image.name)[0] + '.jpg'
            self.image.save(new_name, ContentFile(output.read()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo by {self.uploader_name} at {self.created_at}"

class Comment(models.Model):
    photo = models.ForeignKey(Photo, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author_name} on {self.photo}"
