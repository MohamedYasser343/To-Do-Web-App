document.addEventListener("DOMContentLoaded", function () {
  const taskForm = document.getElementById("task-form");
  const modal = document.getElementById("task-modal");
  const floatingButton = document.querySelector(".floating-button");
  const themeToggle = document.querySelector(".theme-toggle");

  taskForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(taskForm);
    fetch("/add", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "Task added successfully") {
          window.location.reload();
        }
      });
  });

  document.querySelectorAll(".complete-task").forEach((button) => {
    button.addEventListener("click", function () {
      const taskId = this.dataset.id;
      fetch(`/update/${taskId}`, {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message === "Task status updated") {
            window.location.reload();
          }
        });
    });
  });

  document.querySelectorAll(".delete-task").forEach((button) => {
    button.addEventListener("click", function () {
      const taskId = this.dataset.id;
      fetch(`/delete/${taskId}`, {
        method: "DELETE",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message === "Task deleted") {
            window.location.reload();
          }
        });
    });
  });

  floatingButton.addEventListener("click", function () {
    modal.style.display = "flex";
    floatingButton.classList.toggle("open");
  });

  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
      floatingButton.classList.remove("open");
    }
  };

  themeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    this.style.transform = document.body.classList.contains("dark-mode")
      ? "rotate(180deg)"
      : "rotate(0deg)";
  });
});
