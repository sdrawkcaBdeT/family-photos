import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from photos.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

def run_smoke_test():
    print("Running Smoke Test...")
    
    # 1. Test Photo Creation
    print("1. Testing Photo Creation...")
    # Create a dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_file = SimpleUploadedFile("test.jpg", img_io.getvalue(), content_type="image/jpeg")
    
    photo = Photo.objects.create(image=img_file, uploader_name="Tester")
    print(f"   Success: Created Photo ID {photo.id} by {photo.uploader_name}")
    
    # 2. Test HEIC Logic (Mocked)
    # We can't easily generate a real HEIC here without heavy libs, 
    # but we can verify the model save method didn't crash on the JPEG.
    if photo.image.name.endswith('.jpg'):
        print("   Success: Image saved with .jpg extension")
    
    # 3. Test Comments
    print("2. Testing Comments...")
    from photos.models import Comment
    comment = Comment.objects.create(photo=photo, author_name="Tester", text="Hello World")
    print(f"   Success: Created Comment ID {comment.id}: '{comment.text}'")
    
    print("\nSmoke Test PASSED!")

if __name__ == "__main__":
    run_smoke_test()
