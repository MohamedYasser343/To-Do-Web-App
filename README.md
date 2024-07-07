# Do-It ⚡️ - CS50x Final Project 2024

Watch my [YouTube demo](https://youtu.be/i3d-CTnY4-k) to see Do-It ⚡️ in action!

<p float="left">
  <img src="https://github.com/adhamhaithameid/Do-it/assets/154730935/ee23d8e3-bc89-44e7-8e3e-19871b5cc8d7" alt="Do-It App Screenshot" width="400" />
  <img src="https://github.com/adhamhaithameid/Do-it/assets/154730935/c2b01685-4c17-4282-bcb0-a684b548c650" alt="Do-It App Screenshot" width="400" />
</p>

## Overview

Do-It ⚡️ is a simple and user-friendly task manager designed for the CS50x 2024 final project. It helps users manage their tasks efficiently with an intuitive interface.

## Features

- **Task Management**: Add, edit, complete, and delete tasks.
- **Deadline Management**: Set deadlines using a datetime picker.
- **Dark Mode**: Toggle between light and dark modes.
- **Responsive Design**: Works across desktop and mobile devices.
- **User-Friendly Interface**: Intuitive layout for easy task management.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Database**: SQLite (via SQLAlchemy)

## Setup

To run Do-It locally, follow these steps:

1. **Clone the repository:**
   ```bash
   https://github.com/adhamhaithameid/Do-it.git
   cd do-it
2. **Build the Docker image:**
    ```bash
    docker build -t do-it-app
    ```
3. **Run the Docker Container:**
    ```bash
    docker run -p 5000:5000 do-it-app
    ```
4. **Access the application:**
   
   Once the Docker container is running, the Do-It application will be accessible at http://localhost:5000.

## Usage
Adding a Task: Click on the "+" button to open the task modal. Fill in the details and click "Add Task".
Editing a Task: Click on "Edit" next to a task, modify the details, and click "Save Task".
Completing a Task: Click on "Complete" next to a task to mark it as complete.
Deleting a Task: Click on "Delete" next to a task to remove it.

Demo Video

Watch my [YouTube demo](https://youtu.be/i3d-CTnY4-k) to see Do-It ⚡️ in action!
