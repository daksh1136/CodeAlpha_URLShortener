# 🔗 CodeAlpha URL Shortener

A backend URL shortening service built with **Python, Flask, PostgreSQL, and SQLAlchemy** as part of the CodeAlpha Backend Development Internship.

## 🚀 Features

- Create short URLs from long URLs
- Generate unique 6-character short codes
- Store URLs in PostgreSQL
- Redirect short URLs to original URLs
- Track URL click counts
- View URL statistics
- Validate submitted URLs
- Prevent duplicate URL records
- Handle invalid requests and database errors

## 🛠️ Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- SQLAlchemy
- python-dotenv

## 📁 Project Structure

```text
CodeAlpha_URLShortener/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── run.py