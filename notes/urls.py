from django.urls import path
from . import views

# app_name='notes'
urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.note_list, name='note_list'),
    path('create/', views.create_note, name='create_note'),
    # path('<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
]
