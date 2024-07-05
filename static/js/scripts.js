/* static/js/scripts.js */
document.addEventListener("DOMContentLoaded", () => {
  const tasks = document.querySelectorAll(".task");
  const form = document.querySelector("#task-form");
  const floatingButton = document.querySelector(".floating-button");
  const modal = document.querySelector(".modal");
  const themeToggle = document.querySelector(".theme-toggle");
  const footerIcon = document.querySelector("footer img");

  let isModalOpen = false;

  function toggleModal() {
    isModalOpen = !isModalOpen;
    modal.style.display = isModalOpen ? "flex" : "none";
    floatingButton.classList.toggle("open", isModalOpen);
  }

  floatingButton.addEventListener("click", toggleModal);

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      toggleModal();
    }
  });

  tasks.forEach((task) => {
    task.addEventListener("click", (e) => {
      if (e.target.classList.contains("complete-task")) {
        task.classList.toggle("complete");
      }
    });
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    fetch("/add", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle response
        console.log(data);
        toggleModal(); // Close the modal
        location.reload(); // Refresh the page to see the new task
      });
  });

  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    if (document.body.classList.contains("dark-mode")) {
      footerIcon.src = "{{ url_for('static', filename='img/ghw.png') }}";
    } else {
      footerIcon.src = "{{ url_for('static', filename='img/ghb.png') }}";
    }
  });
});
