# 🚚 TechEazy Parcel & Delivery Order API (FastAPI + SQLite)

This project is a FastAPI backend for managing:
- Parcels
- Delivery Orders (via file upload)
- Vendors
- JWT-based login authentication

The backend uses SQLite for storage and is designed for local testing via Postman using a pre-built collection.

---

## 📁 Project Structure

```
├── main.py                 # FastAPI app entry point
├── models.py               # SQLModel ORM models for Parcel, Vendor, DeliveryOrder
├── service.py              # Business logic (CRUD operations, helpers)
├── database.py             # SQLite engine setup and session
├── auth.py                 # JWT token creation and user authentication
├── postman_collection.json # Postman collection for testing all APIs
├── parcel.db               # SQLite database (auto-generated)
└── README.md               # This file
```

---

## ✅ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YourUsername/TechEazy_backend_LokeshKrishna07.git
cd TechEazy_backend_LokeshKrishna07
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# OR
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt`, install manually:
> ```bash
> pip install fastapi uvicorn sqlmodel python-jose[cryptography] python-multipart
> ```

---

## 🚀 Running the Server

```bash
uvicorn main:app --reload
```

- FastAPI will auto-create `parcel.db` (SQLite) and required tables.
- Server runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 JWT Authentication

- Endpoint: `POST /login`
- Default credentials:
  ```json
  {
    "username": "admin",
    "password": "admin"
  }
  ```
- Response will return a JWT `access_token`
- Use this token for authenticated routes:
  ```
  Authorization: Bearer <your_token_here>
  ```

---

## 📤 Upload Delivery Order API

- Endpoint: `POST /upload-order`
- Requires:
  - `vendor_name` (text)
  - `subscription_type` (NORMAL, PRIME, VIP)
  - `order_date` (YYYY-MM-DD)
  - `file` (CSV upload).  # Here u have to use your local .csv file for upload otherwise it shows error

### ✅ CSV Format (no headers)

```
TRK001,Lokesh,Ravi,Shipped
TRK002,Alice,Bob,Delivered
```

---

## 🔬 Testing with Postman

1. Open **Postman**
2. Click **Import** and select `postman_collection.json` from the project folder
3. You’ll see a collection called `TechEazy Backend APIs`
4. Use the `Login` request to get your JWT token
5. Copy the token and set it in the `Authorization` header as:
   ```
   Bearer <your_token_here>
   ```
6. Now test the remaining APIs (like `GET /parcels`, `POST /upload-order`, etc.)
7. For the file upload (`/upload-order`), select a `.csv` file manually after import

---

## 📝 Notes

- SQLite is file-based, created automatically as `parcel.db`
- No Alembic/migration is used yet (dev-friendly setup)
- Pagination support is built-in for vendors and orders
- Models: 1 Vendor ➝ Many DeliveryOrders ➝ Many Parcels

---

Made with ❤️ by Lokesh Krishna
