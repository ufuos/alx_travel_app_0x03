
# alx_travel_app (alx_travel_app_0x02)

## Chapa Payment Integration

### Setup
1. Create .env with:
   - CHAPA_SECRET_KEY
   - CELERY_BROKER_URL
   - EMAIL settings

2. Install deps:
pip install -r requirements.txt

markdown
Copy code

3. Run migrations:
python manage.py migrate

markdown
Copy code

4. Start services:
redis-server
python manage.py runserver
celery -A project_name worker -l info

markdown
Copy code

### Testing
- POST to `/api/listings/chapa/initiate/` with `booking_id` and `amount`.
- Open returned `checkout_url` and complete sandbox payment.
- Verify via `/api/listings/chapa/verify/?tx_ref=...`

### Notes
- This repo is `alx_travel_app_0x02` — DO NOT push to `alx_travel_app_0x01`.
13 — Git: duplicate project and push to alx_travel_app_0x02 (exact commands)
If you already have alx_travel_app_0x01 locally and want to create alx_travel_app_0x02 with the new changes:

Clone the original repo (if you only have remote):

bash
Copy code
git clone https://github.com/yourusername/alx_travel_app_0x01.git alx_travel_app_0x02
cd alx_travel_app_0x02
(Optional) Remove the existing remote origin and create a fresh repo locally:

bash
Copy code
# remove origin that points to 0x01
git remote remove origin
Create a new GitHub repository named alx_travel_app_0x02 on GitHub (use the website UI). Copy the new repo URL (HTTPS or SSH).

Add the new remote and push:

bash
Copy code
# replace <NEW_REPO_URL> with your alx_travel_app_0x02 URL
git remote add origin https://github.com/yourusername/alx_travel_app_0x02.git
git branch -M main
git push -u origin main
If you already made changes, commit them before pushing:

bash
Copy code
git add .
git commit -m "Add Chapa payment integration: Payment model, views, tasks, README"
git push origin main
Important: These commands remove any reference to the old alx_travel_app_0x01 remote, so pushing will go only to alx_travel_app_0x02. Double-check git remote -v to ensure it points to the new repo before pushing.