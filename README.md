🧾 Django Expense Tracker

A full-stack Expense Tracker web application built with Django, Django REST Framework, and PostgreSQL, featuring CRUD APIs, third-party API integration, currency conversion, and data visualization.
The application is production-deployed and publicly accessible.

🔗 Live Demo

👉 Live Application:
https://expense-tracker-g0ig.onrender.com/dashboard/

👉 GitHub Repository:
https://github.com/Harsh3681/Django_base_expense_tracker_app

🚀 Features
✅ Core Functionality

Create, Read, Update, Delete (CRUD) expenses via REST APIs

Filter expenses by category and date range

Real-time dashboard updates without page reloads

🌍 Currency Conversion (API Integration)

Integrated with a third-party exchange rate API

Fetches live currency rates and stores them in the database

Converts expense amounts into worldwide currencies dynamically

📊 Data Visualization

Category-wise expense breakdown

Bar visualization and pie chart using Chart.js

Total expense summary on dashboard

☁️ Production Ready

PostgreSQL database hosted on Supabase

Deployed on Render

Secure environment variable handling

Static files served with WhiteNoise

🛠️ Tech Stack
Backend

Python 3

Django

Django REST Framework

PostgreSQL (Supabase)

psycopg

Frontend

HTML

Tailwind CSS

Vanilla JavaScript

Chart.js

Deployment

Render (Web Service)

Supabase (PostgreSQL Database)

🧩 Architecture Overview
Frontend (HTML + JS)
↓
REST APIs (Django REST Framework)
↓
PostgreSQL Database (Supabase)
↓
Third-Party Exchange Rate API

📂 Project Structure
django-expense-tracker/
│
├── core/
│ ├── models.py # Expense & ExchangeRate models
│ ├── views.py # API views + dashboard view
│ ├── serializers.py # DRF serializers
│ ├── services.py # External API integration
│ ├── urls.py # API routing
│ └── templates/
│ └── dashboard.html
│
├── config/
│ ├── settings.py # Project configuration
│ ├── urls.py # Root URL routing
│ └── wsgi.py
│
├── static/ # Frontend JS & CSS
├── requirements.txt
├── manage.py
└── README.md

🔌 API Endpoints
Expense APIs
GET /api/expenses/
POST /api/expenses/
PATCH /api/expenses/{id}/
DELETE /api/expenses/{id}/

Exchange Rate APIs
POST /api/integrations/exchange-rate/
GET /api/integrations/rates/

🔄 Third-Party API Integration

The backend fetches exchange rates from an external currency API.

Rates are stored relative to a base currency.

Conversion is handled efficiently on the frontend using stored rates.

⚙️ Environment Variables

Create a .env file locally:

DEBUG=1
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@host:port/dbname
TIME_ZONE=UTC
EXCHANGE_RATE_API_KEY=your_api_key

⚠️ .env is ignored via .gitignore for security.

🏃‍♂️ Local Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/Harsh3681/Django_base_expense_tracker_app
cd django-expense-tracker

2️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start server
python manage.py runserver

Access at:
👉 http://127.0.0.1:8000/dashboard/

☁️ Deployment Notes

Database hosted on Supabase

Application deployed on Render

Uses dj-database-url for database configuration

Static files handled using WhiteNoise

🎯 Design Decisions

Used Django REST Framework for clean API design

Stored exchange rates in DB to reduce repeated API calls

Frontend uses vanilla JavaScript to keep logic transparent

Separation of concerns between services, views, and serializers

Production-safe deployment practices followed

📌 Future Improvements

User authentication & multi-user support

Expense export (CSV / Excel)

Monthly and yearly reports

Caching exchange rates

Pagination for large datasets

👤 Author

Harshal Sonawane
Full-Stack Developer (Python / Django / React / Spring Boot)
