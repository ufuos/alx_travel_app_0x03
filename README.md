# alx_travel_app (alx_travel_app_0x02)

> **Note:** This repository is `alx_travel_app_0x02`. **Do NOT** push these changes to `alx_travel_app_0x01`.

---

## 🧳 ALX_TRAVEL_APP — Overview

ALX_TRAVEL_APP is a Django + Django REST Framework project that powers a travel platform. It supports Listings (places to book), Bookings, and Reviews, with management commands for database seeding.

### ✨ Features

* 🏨 **Listings:** Create, view, and manage travel listings.
* 📅 **Bookings:** Manage reservations tied to listings.
* ⭐ **Reviews:** Users can add reviews for listings.
* ⚙️ **Database Seeding:** Seed the database with sample listings, bookings, and reviews via a management command.
* 🔐 **API-Ready:** Built with Django REST Framework for easy API consumption.

### 📂 Project Structure

```
alx_travel_app/
├── alx_travel_app/    # Main project settings
├── listings/          # Core app with models, views, serializers
│   ├── models.py      # Listing, Booking, Review models
│   ├── serializers.py # API serializers
│   ├── views.py       # API views
│   ├── management/
│   │   ├── commands/
│   │   │   └── seed.py # Custom command for seeding data
├── requirements.txt   # Project dependencies
├── manage.py          # Django project manager
```

---

## ⚡ Installation & Setup

1. **Clone the repo**

```bash
git clone https://github.com/your-username/alx_travel_app_0x02.git
cd alx_travel_app_0x02
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create .env** (example variables — adapt to your deployment)

```
CHAPA_SECRET_KEY=your_chapa_secret
CELERY_BROKER_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=supersecret
EMAIL_USE_TLS=True
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Create superuser (admin access)**

```bash
python manage.py createsuperuser
```

7. **Start services (development)**

```bash
# Start Redis (for Celery) — make sure redis-server is installed
redis-server

# Start Django dev server
python manage.py runserver

# Start Celery worker (replace `project_name` with your Django project module if different)
celery -A alx_travel_app worker -l info
```

---

## 🌱 Database Seeding

Populate the database with demo listings, bookings, and reviews using the custom seed command:

```bash
python manage.py seed
```

This will create:

* Sample listings (hotels, destinations)
* Example bookings tied to listings
* Reviews with random ratings

---

## 🧾 API Endpoints

* **Listings**

  * GET `/api/listings/`
  * POST `/api/listings/`
  * GET `/api/listings/{id}/`
  * PUT `/api/listings/{id}/`
  * DELETE `/api/listings/{id}/`

* **Bookings**

  * GET `/api/bookings/`
  * POST `/api/bookings/`
  * GET `/api/bookings/{id}/`
  * PUT `/api/bookings/{id}/`
  * DELETE `/api/bookings/{id}/`

* **Reviews**

  * GET `/api/reviews/`
  * POST `/api/reviews/`
  * GET `/api/reviews/{id}/`
  * PUT `/api/reviews/{id}/`
  * DELETE `/api/reviews/{id}/`

* **Swagger UI (if enabled)**

  * `/api/swagger/`

---

## 💳 Chapa Payment Integration

This repository includes a Chapa integration to handle payments for bookings.

### Setup (Chapa & Payment-related)

1. Add `CHAPA_SECRET_KEY` to your `.env` (see above).
2. Ensure Celery and Redis are running if payment verification is delegated to background tasks.
3. Install dependencies: `pip install -r requirements.txt` (already covered above).
4. Run migrations and start services (see Installation & Setup section).

### How to test

* **Initiate payment** — POST to `/api/listings/chapa/initiate/` with `booking_id` and `amount`.
* The endpoint will return a `checkout_url`. Open the URL and complete the sandbox payment.
* **Verify payment** — GET `/api/listings/chapa/verify/?tx_ref=...` to confirm payment status.

### Notes

* Make sure you use sandbox/test credentials from Chapa for development.
* Payment verification may be implemented synchronously (verify endpoint) or asynchronously via Celery tasks depending on your implementation.

---

## 🧰 Git: Duplicate project and push to `alx_travel_app_0x02` (exact commands)

If you already have `alx_travel_app_0x01` locally and want to create `alx_travel_app_0x02` with the new changes:

```bash
# Clone the original remote (if you only have remote and want a local copy named 0x02)
git clone https://github.com/yourusername/alx_travel_app_0x01.git alx_travel_app_0x02
cd alx_travel_app_0x02

# (Optional) Remove the existing origin that points to 0x01
git remote remove origin

# Create a new GitHub repository named alx_travel_app_0x02 using the GitHub UI and copy the new repo URL
# Then add the new remote and push

git remote add origin <NEW_REPO_URL>
git branch -M main

# If you already made changes locally, commit them first
git add .
git commit -m "Add Chapa payment integration: Payment model, views, tasks, README"

# Push to the new remote
git push -u origin main

# Verify remotes
git remote -v
```

**Important:** Removing/changing remotes in this procedure removes references to the old `alx_travel_app_0x01` remote. Double-check `git remote -v` before pushing.

---

## 📦 Deployment

You can deploy this app to:

* Heroku
* Render
* Railway
* Docker

(Include deployment instructions in this README if you set up any specific buildpacks, Dockerfile, or CI/CD pipelines.)

---

## 📸 Screenshots

(Add screenshots here of your API responses, Django Admin, or Swagger UI if added)

---

## 👨‍💻 Author

Developed by **Ufuoma Ogedegbe** 🚀

* Portfolio: [https://ufuosMernPortfolio.onrender.com](https://ufuosMernPortfolio.onrender.com)
* GitHub: [https://github.com/ufuos](https://github.com/ufuos)

---

If you'd like, I can also:

* add example `curl` or Postman requests for the Chapa endpoints
* add a sample `.env.example` file content
* convert the README into a more compact Quickstart section
