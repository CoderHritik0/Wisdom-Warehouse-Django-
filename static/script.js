function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if cookie name matches
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
  const deleteModal = document.getElementById('deleteModal');
  const confirmBtn = document.getElementById('confirmDeleteBtn');

  deleteModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget; // Button that triggered the modal
    const noteId = button.getAttribute('data-note-id');


    // Store data on confirm button
    confirmBtn.dataset.noteId = noteId;
  });

  confirmBtn.addEventListener('click', function () {
    const noteId = this.dataset.noteId;
    console.log("Deleting note with ID:", noteId);

    // Example: send AJAX request to delete the note
    fetch(`/notes/${noteId}/delete/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'), // if using Django
      },
    }).then(response => {
      if (response.ok) {
        window.location.reload(); // or dynamically remove the note from the DOM
      }
    });
  });
});
