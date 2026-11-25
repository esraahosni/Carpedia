# 🚗 Carpedia

A full-stack car marketplace web application built with Django, where users can browse new and used cars, search and filter listings, save favourites, and admins can manage cars and users through a custom dashboard.

**Live site:** https://carpedia-production.up.railway.app/
**Repository:** https://github.com/esraahosni/Carpedia.git

---

## Features

- 🏠 Modern, responsive homepage with hero section, stats, and featured cars
- 🚘 Browse cars by category — New / Used
- 🔍 Search and filter by brand, year, fuel type, and price
- 📄 Detailed car pages with specs, description, and image gallery
- 👤 User authentication — register, login, profile
- ❤️ Favourites system — save cars to your profile
- 🛠️ Admin dashboard:
  - Add / edit / delete car listings
  - Manage users (promote/demote/delete)
- 🎨 Fully custom dark-themed UI (no frontend framework — plain HTML/CSS/JS + Django templates)

---

## Tech Stack

- **Backend:** Django 5, Python 3.12+
- **Database:** SQLite (development), PostgreSQL (production via Railway)
- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Auth:** Django's built-in authentication system
- **Deployment:** Vercel (see below)


---

## Deploying on Vercel

Required environment variables:

| Variable | Notes |
|---|---|
| `SECRET_KEY` | Long random string (required, the app refuses to start without it) |
| `DATABASE_URL` | External Postgres (Neon, Supabase or Vercel Postgres). SQLite does not work on Vercel. |
| `EXTRA_HOSTS` | Optional, comma separated custom domains |
| `DEBUG` | Leave unset (off). Use `DEBUG=True` only locally. |

The build runs `build_files.sh` (collectstatic, plus migrate when `DATABASE_URL` is set).
Note: uploaded car images need external storage on Vercel because its disk is read-only/ephemeral.

Run tests locally: `DEBUG=True python manage.py test`
