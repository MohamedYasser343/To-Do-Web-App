document.addEventListener('DOMContentLoaded', function() {
  const taskForm = document.getElementById('task-form');
  const modal = document.getElementById('task-modal');
  const floatingButton = document.querySelector('.floating-button');
  const themeToggle = document.querySelector('.theme-toggle');
  const editTaskForm = document.getElementById('edit-task-form');

  if (taskForm) {
      taskForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const formData = new FormData(taskForm);
          fetch('/add', {
              method: 'POST',
              body: formData
          }).then(response => response.json()).then(data => {
              if (data.message === 'Task added successfully') {
                  window.location.reload();
              }
          });
      });
  }

  if (editTaskForm) {
      editTaskForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const formData = new FormData(editTaskForm);
          const taskId = editTaskForm.getAttribute('action').split('/').pop();
          fetch(`/edit/${taskId}`, {
              method: 'POST',
              body: formData
          }).then(response => response.json()).then(() => {
              window.location.href = '/';
          });
      });
  }

  document.querySelectorAll('.complete-task').forEach(button => {
      button.addEventListener('click', function() {
          const taskId = this.dataset.id;
          fetch(`/update/${taskId}`, {
              method: 'POST'
          }).then(response => response.json()).then(data => {
              if (data.message === 'Task status updated') {
                  window.location.reload();
              }
          });
      });
  });

  document.querySelectorAll('.delete-task').forEach(button => {
      button.addEventListener('click', function() {
          const taskId = this.dataset.id;
          fetch(`/delete/${taskId}`, {
              method: 'DELETE'
          }).then(response => response.json()).then(data => {
              if (data.message === 'Task deleted') {
                  window.location.reload();
              }
          });
      });
  });

  floatingButton.addEventListener('click', function() {
      modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
      floatingButton.classList.toggle('rotate');
  });

  window.onclick = function(event) {
      if (event.target === modal) {
          modal.style.display = 'none';
          floatingButton.classList.remove('rotate');
      }
  };

  function toggleTheme() {
      document.body.classList.toggle('dark-mode');
      themeToggle.classList.toggle('rotated');
      localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
  }

  themeToggle.addEventListener('click', toggleTheme);

  if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark-mode');
      themeToggle.classList.add('rotated');
  }
});
