# 🗓️ Consultation Appointment Booking System

A Django-based web application for booking consultation appointments between users and consultants.  
This is a **self-developed practice project**, designed with scalability in mind.

## 🚀 Features

### Users:
- Sign up / login
- Edit profile
- Browse consultants
- Search consultants
- Reserve available time slots
- View upcoming appointments
- **Limited to 2 active (future) appointments**

### Consultants:
- Sign up / login
- Update personal profile
- Add available time slots
- View upcoming booked appointments (with filters: Today, This Week, This Month)
- See list of users who reserved their sessions

## 🧩 App Structure

- `main/` — Home page and consultant listing
- `users/` — User panel: registration, login, dashboard, and booking
- `consultant/` — Consultant panel: registration, schedule management, and dashboard
- `appointment/` — Appointment models only (decoupled for easier scalability)

> 🔧 The project is structured to be **extendable** in the future.

## 🛠️ Tech Stack

- Python 3
- Django
- SQLite (easily replaceable with PostgreSQL)
- HTML / CSS / Bootstrap
- jQuery (for interactivity)
- Django messages framework