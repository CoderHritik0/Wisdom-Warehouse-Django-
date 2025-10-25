from django.urls import path
from . import views

# app_name='notes'
urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.note_list, name='note_list'),
    path('create/', views.create_or_edit_note, name='create_note'),
    path('edit/<int:note_id>/', views.create_or_edit_note, name='edit_note'),
    path('delete_image/<int:image_id>/', views.delete_note_image, name='delete_note_image'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
]
