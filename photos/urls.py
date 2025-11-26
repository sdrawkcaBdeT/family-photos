from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('login/', views.login_view, name='login'),
    path('name/', views.set_name_view, name='set_name'),
    path('upload/', views.upload_view, name='upload'),
    path('photo/<int:photo_id>/comment/', views.add_comment, name='add_comment'),
]
