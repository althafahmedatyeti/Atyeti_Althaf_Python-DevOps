# 🚌 RedBus Booking Application

A FastAPI-based backend application that mimics core functionalities of a RedBus-like ticket booking system. This includes user registration, authentication via JWT, bus listing, seat booking, and booking summary features.

---

## 📌 Features

- User registration and login with JWT authentication
- Secure booking with seat conflict prevention
- View all available buses
- Track your own bookings
- Cancel your bookings
- Booking summary with source, destination, and seat insights
- Logging of booking actions and events

---

## 🛠 Tech Stack

| Layer         | Tool        |
|---------------|-------------|
| Backend       | FastAPI     |
| Database      | SQLite      |
| ORM           | SQLAlchemy  |
| Auth          | JWT (via JOSE) |
| Validation    | Pydantic    |
| Logging       | Python `logging` |
| Docs UI       | Swagger (auto via FastAPI) |

---

## 📁 Project Structure

redbus-app/
├── app/
│ ├── api/v1/
│ │ ├── booking_routes.py
│ │ ├── bus_routes.py
│ │ └── user_routes.py
│ ├── models/
│ │ ├── booking.py
│ │ ├── bus.py
│ │ ├── user.py
│ │ └── booked_bus_summary.py
│ ├── services/
│ │ ├── booking_service.py
│ │ └── summary_service.py
│ ├── schemas/
│ │ ├── user_schema.py
│ │ └── booking_schema.py
│ ├── utils/
│ │ ├── jwt_token.py
│ │ └── log_config.py
│ ├── database.py
│ └── main.py
├── logs/
│ └── app.log
├── requirements.txt
└── README.md


___currently working...................