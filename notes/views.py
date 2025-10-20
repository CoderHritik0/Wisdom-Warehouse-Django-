from django.shortcuts import render
from .models import note, note_image
from .forms import NoteForm, NoteImageForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
def index(request):
    return render(request, 'notes/index.html')

def note_list(request):
    notes = note.objects.all().filter(is_deleted=False).order_by('-updated_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        image_form = NoteImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            for img in request.FILES.getlist('image'):
                note_img = note_image(note=new_note, image=img)
                note_img.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'note_form': NoteForm(), 'image_form': NoteImageForm()})

def edit_note(request, note_id):
    note_instance = get_object_or_404(note, pk=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note_instance)
        image_form = NoteImageForm(request.POST, request.FILES, instance=note_instance)
        if form.is_valid() and image_form.is_valid():
            form.save()
            for img in request.FILES.getlist('image'):
                note_img = note_image(note=note_instance, image=img)
                note_img.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note_instance)
    return render(request, 'notes/create_note.html', {'note_form': form, 'image_form': NoteImageForm(), 'note': note_instance})

def delete_note(request, note_id):
    note_instance = get_object_or_404(note, pk=note_id, user=request.user)
    note_instance.is_deleted = True
    note_instance.save()
    return redirect('note_list')

def note_detail(request, note_id):
    note_instance = get_object_or_404(note, pk=note_id)
    images = note_image.objects.filter(note=note_instance)
    return render(request, 'notes/note_detail.html', {'note': note_instance, 'images': images})