# Task Management Application

A **Python-only Flask Todo App** for managing tasks and users.  
This project provides backend functionality with SQLite for storage and RESTful API endpoints for managing todos, users, and statistics. No HTML templates are required to use the API.

---

## Features

- **Todo Management**
  - Add, delete, and update todos
  - Set priority and due dates
  - Track status (pending/completed)
  - Tag todos for easy filtering

- **Enhanced Features**
  - Filter todos by status, priority, due dates, and search terms
  - Export todos in JSON or CSV
  - Get statistics like total todos, completed, pending, and completion percentage

- **User Management**
  - Users with profiles, settings, and activity logs
  - Track created todos per user

- **Backend API**
  - `/api/todos` → Get all todos
  - `/api/todos/filter` → Filter todos by status, priority, date, and search
  - `/api/todos/export` → Export todos in JSON/CSV
  - `/api/stats` → Get statistics

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail
- **Database:** SQLite (default)
- **Environment Management:** python-dotenv

---

## Setup Instructions

1. **Clone the repository**
bash
git clone https://github.com/<USERNAME>/<REPO>.git
cd Task_Management_Application

2. Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   venv\Scripts\activate    # On Windows

3. Install Dependencies
   pip install -r requirements.txt

4. Create .env file
   DATABASE_URL=sqlite:///todo.db
   SECRET_KEY=your-secret-key
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-app-password

5.Run the app
  python3 app.py
  •	The app will run on http://0.0.0.0:5000
	•	API endpoints can be tested using Postman or Python scripts.

6. Project Structure
   Task_Management_Application/
├─ app.py
├─ __init__.py
├─ models.py
├─ config.py
├─ extensions.py
├─ schema.sql
├─ .env
├─ requirements.txt
└─ templates/  # Optional if you want to add HTML later
