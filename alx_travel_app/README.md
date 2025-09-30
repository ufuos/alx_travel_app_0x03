🧳 ALX_TRAVEL_APP

ALX_TRAVEL_APP is a Django + Django REST Framework project that powers a travel platform.
It supports Listings (places to book), Bookings, and Reviews, with management commands for database seeding.

✨ Features

🏨 Listings: Create, view, and manage travel listings.

📅 Bookings: Manage reservations tied to listings.

⭐ Reviews: Users can add reviews for listings.

⚙️ Database Seeding: Seed the database with sample listings, bookings, and reviews via a management command.

🔐 API-Ready: Built with Django REST Framework for easy API consumption.

📂 Project Structure
alx_travel_app/
├── alx_travel_app/ # Main project settings
├── listings/ # Core app with models, views, serializers
│ ├── models.py # Listing, Booking, Review models
│ ├── serializers.py # API serializers
│ ├── views.py # API views
│ ├── management/
│ │ ├── commands/
│ │ │ └── seed.py # Custom command for seeding data
├── requirements.txt # Project dependencies
├── manage.py # Django project manager

⚡ Installation & Setup

1. Clone the repo
   git clone https://github.com/your-username/ALX_TRAVEL_APP.git
   cd ALX_TRAVEL_APP

2. Create a virtual environment
   python3 -m venv venv
   source venv/bin/activate # Mac/Linux
   venv\Scripts\activate # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Run migrations
   python manage.py migrate

5. Create superuser (admin access)
   python manage.py createsuperuser

6. Run the development server
   python manage.py runserver

🌱 Database Seeding

You can populate the database with demo listings, bookings, and reviews using the custom seed command:

python manage.py seed

This will create:

Sample listings (hotels, destinations)

Example bookings tied to listings

Reviews with random ratings

🔑 API Endpoints
Method Endpoint Description
GET /api/listings/ Fetch all listings
POST /api/listings/ Create a listing
GET /api/bookings/ Fetch all bookings
POST /api/bookings/ Create a booking
GET /api/reviews/ Fetch all reviews
POST /api/reviews/ Create a review
🛠️ Tech Stack

Backend: Django, Django REST Framework

Database: PostgreSQL (can be swapped with SQLite/MySQL)

Auth: Django default authentication system

Management: Custom Django commands for seeding

📸 Screenshots

(Add screenshots here of your API responses, Django Admin, or Swagger UI if added)

🚀 Deployment

You can deploy this app to:

Heroku

Render

Railway

Docker

(Add deployment instructions if you set this up.)

👨‍💻 Author

Developed by Ufuoma Ogedegbe 🚀

Portfolio: ufuosMernPortfolio.onrender.com

GitHub: @ufuos
