function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
  const deleteModal = document.getElementById("deleteModal");
  const confirmBtn = document.getElementById("confirmDeleteBtn");

  // Variables to hold current delete context
  let deleteType = null; // "note" or "image"
  let deleteId = null;
  let triggerBtn = null; // Button that triggered modal (used to remove DOM element)

  // When modal is shown, capture data from button that opened it
  deleteModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget; // the button that triggered the modal
    deleteType = button.getAttribute("data-type");
    deleteId =
      deleteType === "note"
        ? button.getAttribute("data-note-id")
        : button.getAttribute("data-image-id");
    triggerBtn = button;
  });

  // Handle confirmation click
  confirmBtn.addEventListener("click", async function () {
    if (!deleteId || !deleteType) return;

    let url = "";
    if (deleteType === "note") {
      url = `/notes/${deleteId}/delete/`;
    } else if (deleteType === "image") {
      url = `/notes/delete_image/${deleteId}/`;
    }

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const modal = bootstrap.Modal.getInstance(
      document.getElementById("deleteModal")
    );
    if (modal) {
      modal.hide();
    }
    triggerBtn.closest(".position-relative").remove();

    if (response.ok) {
      if (deleteType === "note") {
        window.location.reload();
      } else if (deleteType === "image") {
        // Optional: fade-out animation before removal
        const imageContainer = triggerBtn.closest(".position-relative");
        imageContainer.style.transition = "opacity 0.3s";
        imageContainer.style.opacity = "0";
        setTimeout(() => imageContainer.remove(), 300);
      }
    } else {
      alert("Error deleting item.");
    }
  });
});
