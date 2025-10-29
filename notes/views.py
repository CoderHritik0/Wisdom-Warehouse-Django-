from datetime import timedelta
from time import timezone
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from .models import note, note_image
from .forms import NoteForm, NoteImageForm, UserRegistrationForm, AuthenticationForm, PinUpdateForm, PinCheckForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
@login_required
def index(request):
    """Display all non-hidden notes, or handle PIN verification to show hidden notes."""
    hidden = False
    form = PinCheckForm(request.POST or None)

    # ✅ Handle PIN form submission
    if request.method == "POST" and form.is_valid():
        input_pin = form.cleaned_data.get('pin')
        profile = request.user.profile

        if profile and check_password(input_pin, profile.pin):
            request.session['pin_verified'] = True
            return redirect('hidden_notes')
        else:
            form.add_error('pin', 'Incorrect PIN. Please try again.')

    # ✅ Fetch visible notes
    notes = (
        note.objects.filter(user=request.user, is_deleted=False, is_hidden=False)
        .prefetch_related('note_image_set')  # Optimized image fetch
        .order_by('-updated_at')
    )

    # ✅ Preprocess note images (common logic)
    process_note_images(notes)

    return render(
        request,
        'notes/index.html',
        {'notes': notes, 'PinCheckForm': form, 'hidden': hidden}
    )

@require_POST
@login_required
def delete_note_image(request, image_id):
    if request.method == 'POST':
        try:
            image = get_object_or_404(note_image, image_id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
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
        "note": note_instance,
        "pin_form": PinUpdateForm(request)
    })


@login_required
def delete_note(request, note_id):
    note_instance = get_object_or_404(note, pk=note_id, user=request.user)
    note_instance.is_deleted = True
    note_instance.save()
    return redirect('index')

@login_required
def show_hidden_notes(request):
    """Show hidden notes only if user has recently verified PIN."""
    pin_verified = request.session.get('pin_verified', False)

    # ✅ Optional timeout: re-verify after 10 minutes
    if pin_verified:
        hidden = True
        notes = (
            note.objects.filter(user=request.user, is_deleted=False, is_hidden=True)
            .prefetch_related('note_image_set')
            .order_by('-updated_at')
        )
        process_note_images(notes)
        return render(request, 'notes/index.html', {'notes': notes, 'hidden': hidden})

    # Redirect if not verified
    return redirect('index')

def signup(request):
    # print("signup view")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('index')  # Redirect to index or login page after successful signup
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # or your notes list page
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, 'website/index.html')

def setPin(request):
    if request.method == "POST":
        if request.user.profile:
            profile = request.user.profile
            profile.pin = make_password(request.POST.get('pin'))
            profile.save()
    return JsonResponse({'status': 'PIN set successfully'}, status=200)

# ✅ Common helper function
def process_note_images(notes):
    """Attach scaled image data to each note (DRY)."""
    FIXED_WIDTH = 403
    for n in notes:
        images = list(n.note_image_set.all())
        scaled_heights = [
            (img.image.height / img.image.width) * FIXED_WIDTH
            for img in images if img.image and img.image.width and img.image.height
        ]
        n.max_height = max(scaled_heights, default=0)
        for img in images:
            if img.image and img.image.width and img.image.height:
                h = (img.image.height / img.image.width) * FIXED_WIDTH
                img.scaled_height = int(h)
                img.half_diff = int((n.max_height - h) / 2)
            else:
                img.scaled_height, img.half_diff = 0, 0
        n.processed_images = images