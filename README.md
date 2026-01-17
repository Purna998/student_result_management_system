# Student Result Management System

A comprehensive web-based application built with Django for managing student results, classes, subjects, and notices. This system allows administrators to manage academic records efficiently while providing students with easy access to their results.

## 🚀 Features

### Admin Module
The system provides a robust dashboard for administrators to manage all aspects of the academic process:
*   **Authentication**: Secure Admin Login and Password Management.
*   **Dashboard**: Overview of total students, declared results, classes, and subjects.
*   **Class Management**: Create, view, update, and delete classes and sections.
*   **Subject Management**: Manage subjects and subject codes.
*   **Subject Combinations**: Assign specific subjects to classes.
*   **Student Management**: Register new students, update profiles, and manage active/inactive status.
*   **Result Management**: 
    *   Declare results for students by class.
    *   Manage and update existing results.
    *   Automatic calculation of totals and percentages.
*   **Notice Board**: Post and manage important announcements for students.

### Student/Public Module
*   **Home Page**: View latest notices and announcements via a dynamic marquee.
*   **Result Search**: Students can search for their results using their Roll ID and Class.
*   **Result View**: Detailed mark sheet view with subject-wise breakdown, total marks, and percentage.
*   **Print Result**: Option to print or save the result sheet as PDF.

## 🛠️ Technology Stack

*   **Backend**: Python, Django Framework
*   **Database**: SQLite (Default)
*   **Frontend**: HTML5, Bootstrap 5, FontAwesome 6
*   **Templating**: Django Template Language (DTL)

## ⚙️ Installation & Setup

Follow these steps to set up the project locally:

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd student_result_management_system
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django
    ```

4.  **Apply Database Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application**
    *   Open your browser and navigate to `http://127.0.0.1:8000/`
    *   Admin Login: `http://127.0.0.1:8000/admin_login/`

## 📂 Project Structure

```
StudentResultManagement/
├── db.sqlite3                  # Database file
├── manage.py                   # Django management script
├── StudentResultManagement/    # Project configuration directory
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── resultapp/                  # Main application directory
    ├── admin.py
    ├── models.py               # Database models (Student, Result, Class, etc.)
    ├── views.py                # Application logic
    └── templates/              # HTML Templates
        ├── admin_dashboard.html
        ├── result_page.html
        └── ...
```

## 📝 Usage Guide

1.  **Login as Admin**: Use the credentials created during the superuser creation step.
2.  **Setup Academic Data**:
    *   Add **Classes** first.
    *   Add **Subjects**.
    *   Create **Subject Combinations** (link subjects to classes).
3.  **Register Students**: Add students to specific classes.
4.  **Declare Results**: Enter marks for students based on their subjects.
5.  **View Results**: Go to the public homepage or "Student Result" section to search and view results.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📄 License

This project is licensed under the MIT License.
