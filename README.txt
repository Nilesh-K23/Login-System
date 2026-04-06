# Authentication System (Flask + PostgreSQL)

## 📌 Setup

### 1. Install PostgreSQL

### 2. Create Database


CREATE DATABASE auth_system_pg;


### 3. Create Table

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);


### 4. Configure Database

Update `database.py`:


db = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="your_password",
    database="auth_system_pg"
)


### 5. Run Project


setup.bat   (Windows)
./setup.sh  (Linux/macOS)

python app.py

---

## 🔐 Admin Login

* Username: admin
* Password: admin123

---


