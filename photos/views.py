from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from .forms import LoginForm, NameForm
from .decorators import family_auth_required
from .models import Photo, Comment
import json

# --- STEP 1: LOGIN (The Gate) ---
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == settings.FAMILY_PASSWORD:
                request.session['has_access'] = True
                return redirect('set_name')
            else:
                form.add_error('password', 'Incorrect password')
    else:
        form = LoginForm()
    return render(request, 'photos/login.html', {'form': form})

# --- STEP 2: SET NAME (The Name Tag) ---
# CRITICAL FIX: No decorator here to prevent the infinite loop.
def set_name_view(request):
    # 1. Manual Security Check: Do they have the password?
    if not request.session.get('has_access'):
        return redirect('login')

    # 2. Usability Check: If they already have a name, why are they here?
    if request.session.get('uploader_name'):
        return redirect('gallery')

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['uploader_name'] = form.cleaned_data['name']
            return redirect('gallery')
    else:
        form = NameForm()
    return render(request, 'photos/name_tag.html', {'form': form})

# --- STEP 3: THE GALLERY (Protected) ---
@family_auth_required
def gallery_view(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'photos/gallery.html', {'photos': photos})

# --- API: UPLOAD ---
@family_auth_required
def upload_view(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        count = 0
        for image in images:
            Photo.objects.create(
                image=image,
                uploader_name=request.session.get('uploader_name', 'Anonymous')
            )
            count += 1
        return JsonResponse({'status': 'ok', 'count': count})
    return JsonResponse({'status': 'error'}, status=400)

# --- API: GET PHOTO DETAILS (For the Modal) ---
@family_auth_required
def photo_detail_api(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    data = {
        'id': photo.id,
        'url': photo.image.url,
        'uploader': photo.uploader_name,
        'date': photo.created_at.strftime('%b %d, %I:%M %p'),
        'caption': photo.caption,
        'comments': [
            {
                'author': c.author_name, 
                'text': c.text,
                'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
            } 
            for c in photo.comments.all().order_by('created_at')
        ]
    }
    return JsonResponse(data)

# --- API: ADD COMMENT ---
@family_auth_required
def add_comment(request, photo_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            if text:
                photo = Photo.objects.get(id=photo_id)
                comment = Comment.objects.create(
                    photo=photo,
                    author_name=request.session.get('uploader_name', 'Anonymous'),
                    text=text
                )
                return JsonResponse({
                    'status': 'ok',
                    'author': comment.author_name,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
                })
        except Exception as e:
            print(f"Error adding comment: {e}")
            pass
    return JsonResponse({'status': 'error'}, status=400)