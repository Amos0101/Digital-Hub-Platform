# Digital Hub Launch Management Platform — Phase 1

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Create an admin user
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the landing page.
Visit http://127.0.0.1:8000/admin/ for the admin panel.

## Phase 1 Features
- ✅ Responsive landing page (Navy / Cyan / Orange palette)
- ✅ Fixed navigation bar with mobile hamburger menu
- ✅ Hero section with live countdown timer
- ✅ About section (mission, vision, objectives, impact)
- ✅ Upcoming Events cards (Town Hall, Launch, Hackathon)
- ✅ Event Posters section (admin-uploadable)
- ✅ Footer with contact info and social links
- ✅ Django admin authentication

## Admin Credentials (dev only — change in production)
Username: admin
Password: Admin@1234

## Customise via Admin
1. Go to /admin/
2. Under **Core > Site settings** — set Hub name, tagline, launch date, contact info
3. Under **Core > Events** — add Town Hall, Launch, Hackathon details
4. Under **Core > Posters** — upload poster images for each event
