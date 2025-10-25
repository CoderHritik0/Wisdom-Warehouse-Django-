from django.http import JsonResponse
from django.shortcuts import render
from .models import note, note_image
from .forms import NoteForm, NoteImageForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    notes = note.objects.all().filter(is_deleted=False).order_by('-updated_at')
    note_images = note_image.objects.all()
    for n in notes:
        FIXED_WIDTH = 403

        # ✅ Fetch images for this note once
        images = list(note_images.filter(note=n))

        # ✅ Compute scaled heights
        scaled_heights = [
            (img.image.height / img.image.width) * FIXED_WIDTH
            for img in images
            if img.image and img.image.width and img.image.height
        ]

        n.max_height = max(scaled_heights, default=0)

        # ✅ Precompute per-image half-diff (integer)
        for img in images:
            if img.image and img.image.width and img.image.height:
                h = (img.image.height / img.image.width) * FIXED_WIDTH
                img.scaled_height = int(h)
                img.half_diff = int((n.max_height - h) / 2)
            else:
                img.scaled_height = 0
                img.half_diff = 0

        # ✅ Attach these processed images directly for use in template
        n.processed_images = images

    return render(request, 'notes/index.html', {'notes': notes})

@require_POST
def delete_note_image(request, image_id):
    if request.method == 'POST':
        try:
            image = get_object_or_404(note_image, image_id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

# def note_list(request):
#     notes = note.objects.all().filter(is_deleted=False).order_by('-updated_at')
#     return render(request, 'notes/note_list.html')

def create_or_edit_note(request, note_id=None):
    # If note_id exists → edit, else create new
    note_instance = get_object_or_404(note, pk=note_id, user=request.user) if note_id else None

    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note_instance)
        image_form = NoteImageForm(request.POST, request.FILES)

        if form.is_valid():
            saved_note = form.save(commit=False)
            saved_note.user = request.user
            saved_note.save()

            # If new images were uploaded, add them
            for img in request.FILES.getlist('images'):
                note_image.objects.create(note=saved_note, image=img)

            return redirect('index')  # Always redirect after POST ✅
        else:
            print(form.errors)
    else:
        form = NoteForm(instance=note_instance)
        image_form = NoteImageForm()

    return render(request, "notes/create_note.html", {
        "form": form,
        "image_form": image_form,
        "note": note_instance
    })


def delete_note(request, note_id):
    note_instance = get_object_or_404(note, pk=note_id, user=request.user)
    note_instance.is_deleted = True
    note_instance.save()
    return redirect('index')

# def note_detail(request, note_id):
#     note_instance = get_object_or_404(note, pk=note_id)
#     images = note_image.objects.filter(note=note_instance)
#     return render(request, 'notes/note_detail.html', {'note': note_instance, 'images': images})