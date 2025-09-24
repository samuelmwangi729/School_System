# 🎓 School Management System – Built with Django

## 📘 ALX Capstone Project using Django REST Framework

---

## 🚀 Features

This project includes a custom user management system and role-based access control.

### ✅ User Registration

User registration is built using a **custom user model** extending Django's `AbstractUser`. Key features:

- Required fields: `first_name`, `last_name`, `email`, and `password`
- Users must belong to an **Institution**
- Role-based access control with user roles such as:
  - `student`
  - `teacher`
  - `principal`
  - `admin`
  - `super_admin`

---

## 🧪 Testing

Testing is powered by **`coverage`** to ensure test completeness.

### Run Tests with Coverage:

```bash
coverage run manage.py test && coverage report && coverage html
