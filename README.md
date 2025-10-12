# 🎓 School Management System – Built with Django

## 📘 ALX Capstone Project using Django REST Framework

---

## 🚀 Features

This project is a **School Management System** built using **Django REST Framework**.
It provides a robust backend with role-based access control, allowing secure and structured management of school operations.

---

## ✅ Core Models Implemented

The system currently includes the following models:

* **Users** – Custom user model extending Django’s `AbstractUser` with role-based access control.
* **Examinations** – Manages exam details, schedules, and related information.
* **Institutions** – Represents schools and organizations where users are registered.
* **Results** – Stores and manages students’ academic results.

---

## ✅ API Endpoints

Users can perform the following operations through the REST API:

* **POST** → Create new records (Users, Institutions, Examinations, Results)
* **GET** → Retrieve records (single or multiple entries)
* **PUT/PATCH** → Update existing records
* **DELETE** → Remove records

---

## 🔐 Role-Based Access Control

User registration requires belonging to an **Institution** and includes multiple roles such as:

* `student`
* `teacher`
* `principal`
* `admin`
* `super_admin`

This ensures proper separation of responsibilities and access permissions.

---

## 🧪 Testing

Testing is powered by **`coverage`** to ensure reliability and completeness of the codebase.

### Run Tests with Coverage:

```bash
coverage run manage.py test && coverage report && coverage html
```

---

## 🛠️ Tech Stack

* **Django** – Backend framework
* **Django REST Framework (DRF)** – API development
* **SQLite/PostgreSQL** – Database (configurable)
* **Coverage.py** – Testing coverage

---

## 📌 Next Steps

* Expand API endpoints with filtering and pagination
* Add authentication with JWT for enhanced security
* Implement CI/CD pipeline for automated testing and deployment

---
