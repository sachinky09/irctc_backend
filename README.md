# IRCTC Mini System – Backend (Django + DRF)

## 📌 Project Overview
This project is a **Backend Intern Assignment – IRCTC Mini System**, implementing a simplified version of IRCTC’s backend.  
It supports **user authentication, train search, seat booking, and analytics**, using **MySQL for transactional data** and **MongoDB Atlas for analytics/logging**.

The project strictly follows the assignment requirements and focuses on **clean API design, proper data modeling, security, and scalability**.

---

## 🧰 Tech Stack
### Backend
- **Django 5.x**
- **Django REST Framework (DRF)**

### Authentication & Security
- **JWT Authentication** (`djangorestframework-simplejwt`)
- Role-based access (User / Admin)
- Password hashing using Django’s auth system

### Databases
- **MySQL** – Users, Trains, Bookings (Transactional)
- **MongoDB Atlas** – API logs & analytics

### Tools & Environment
- Python 3.10+
- Virtualenv
- dotenv (.env)
- Git & GitHub
- cURL / Postman
- Linux (Pop!_OS)

---

## 🗂 Project Structure
```
irctc_backend/
│
├── users/        # Authentication & user management
├── trains/       # Train search & management
├── bookings/     # Seat booking logic
├── analytics/    # Analytics APIs
├── irctc_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── mongo.py
│
├── .env.example
├── requirements.txt
├── README.md
```

---

## 🗃 Database Design

### User Model (Custom)
- email (unique)
- name
- password (hashed)
- is_staff / is_superuser

### Train Model (MySQL)
```python
train_number (unique)
name
source
destination
departure_time
arrival_time
total_seats
available_seats
```

### Booking Model (MySQL)
```python
user (FK → User)
train (FK → Train)
seats_booked
booking_time
```

### MongoDB Collection
**train_search_logs**
```json
{
  "endpoint": "/api/trains/search/",
  "params": {"source": "Delhi", "destination": "Mumbai"},
  "user_id": 2,
  "execution_time": 0.0234,
  "timestamp": ISODate()
}
```

---

## 🔐 Authentication APIs

### Register
```
POST /api/register/
```
```bash
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d '{
  "name": "Sachin Yadav",
  "email": "sachin@example.com",
  "password": "StrongPassword@123"
}'
```

### Login
```
POST /api/login/
```
```bash
curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{
  "email": "sachin@example.com",
  "password": "StrongPassword@123"
}'
```

🔑 **All protected APIs require:**
```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 🚆 Train APIs

### Search Trains
```
GET /api/trains/search/?source=&destination=&date=&limit=&offset=
```

```bash
curl -X GET "http://127.0.0.1:8000/api/trains/search/?source=Delhi&destination=Mumbai" -H "Authorization: Bearer <ACCESS_TOKEN>"
```

✔ Logs each request to MongoDB  
✔ Supports pagination and date filtering  

---

### Create / Update Train (Admin Only)
```
POST /api/trains/
```

```bash
curl -X POST http://127.0.0.1:8000/api/trains/ -H "Authorization: Bearer <ADMIN_TOKEN>" -H "Content-Type: application/json" -d '{
  "train_number": "12951",
  "name": "Mumbai Rajdhani",
  "source": "Delhi",
  "destination": "Mumbai",
  "departure_time": "2025-01-10T17:00:00Z",
  "arrival_time": "2025-01-11T08:30:00Z",
  "total_seats": 500,
  "available_seats": 500
}'
```

---

## 🎟 Booking APIs

### Book Seats
```
POST /api/bookings/
```

```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{
  "train_id": 1,
  "seats_booked": 2
}'
```

✔ Validates seat availability  
✔ Deducts seats atomically  

---

### My Bookings
```
GET /api/bookings/my/
```

```bash
curl -X GET http://127.0.0.1:8000/api/bookings/my/ -H "Authorization: Bearer <ACCESS_TOKEN>"
```

✔ Includes train details in response  

---

## 📊 Analytics API

### Top Routes
```
GET /api/analytics/top-routes/
```

```bash
curl -X GET http://127.0.0.1:8000/api/analytics/top-routes/ -H "Authorization: Bearer <ACCESS_TOKEN>"
```

✔ Aggregates MongoDB logs  
✔ Returns top 5 most searched routes  

---

## ⚙ Environment Configuration

### `.env.example`
```
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=irctc_db
DB_USER=irctc_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/
```

---

## 🚀 Setup Instructions
```bash
git clone <repo_url>
cd irctc_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

