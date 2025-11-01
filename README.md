
# ALX Travel App 0x03

This project implements background task management using **Celery** with **RabbitMQ** as the broker, alongside asynchronous email notifications for booking confirmations.

---

## Setup Instructions

1. **Create `.env` with the following variables:**
CHAPA_SECRET_KEY=<your-chapa-secret-key>
CELERY_BROKER_URL=amqp://localhost
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=<your-email-password>
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

markdown
Copy code

2. **Install dependencies:**
```bash
pip install -r requirements.txt
Run migrations:

bash
Copy code
python manage.py migrate
Start services:

bash
Copy code
sudo systemctl start rabbitmq-server
celery -A alx_travel_app worker --loglevel=info
python manage.py runserver
Testing
POST to /api/listings/chapa/initiate/ with booking_id and amount.

Open the returned checkout_url and complete the sandbox payment.

Verify via /api/listings/chapa/verify/?tx_ref=...

Notes
This repo is alx_travel_app_0x03 — DO NOT push to previous versions (alx_travel_app_0x02 or alx_travel_app_0x01).

Git Duplication Guide
If you already have alx_travel_app_0x02 locally and want to create alx_travel_app_0x03 with new Celery + Email features:

Clone the existing project:

bash
Copy code
git clone https://github.com/<your-username>/alx_travel_app_0x02.git alx_travel_app_0x03
cd alx_travel_app_0x03
Remove old remote and set up new GitHub repo:

bash
Copy code
git remote remove origin
Create a new repository named alx_travel_app_0x03 on GitHub and copy its URL.

Add new origin and push:

bash
Copy code
git remote add origin https://github.com/<your-username>/alx_travel_app_0x03.git
git branch -M main
git push -u origin main
Commit any changes before pushing:

bash
Copy code
git add .
git commit -m "Configured Celery with RabbitMQ and added async booking confirmation email task"
git push origin main
✅ Celery and Email Notification Setup
How to Run Background Tasks
Start RabbitMQ:

bash
Copy code
sudo systemctl start rabbitmq-server
Start Celery worker:

bash
Copy code
celery -A alx_travel_app worker --loglevel=info
Run Django:

bash
Copy code
python manage.py runserver
Features
✅ Celery configured with RabbitMQ as message broker

📧 Asynchronous email notification on booking creation

🧪 Console-based email backend for easy local testing

🚀 Step 10: Push to GitHub
bash
Copy code
git add .
git commit -m "Configured Celery with RabbitMQ and added async booking confirmation email task"
git push origin main