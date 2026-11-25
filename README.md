# Carpedia

A full-stack car marketplace built with Django. Visitors browse new and used cars, search and filter listings, and save favourites. Staff manage cars and users from a custom dashboard.

**Live demo:** https://carpedia1-iota.vercel.app

![Home page](docs/screenshots/home.jpg)

| Browse cars | Car details | Mobile |
|---|---|---|
| ![Cars list](docs/screenshots/cars.jpg) | ![Car detail](docs/screenshots/detail.jpg) | ![Mobile](docs/screenshots/mobile.jpg) |

## Features

- Home page with an animated hero, quick search, featured new and used cars, and a brand strip
- Browse all, new, or used cars with pagination
- Filter by brand, year, fuel type, and maximum price
- Car detail page with specs (engine, horsepower, fuel, transmission) and description
- User registration, login, logout, and profile page
- Favourites: save and remove cars (POST + CSRF protected)
- Staff dashboard: add, edit, and delete cars; promote, demote, or delete users
- Photo uploads stored on Cloudinary
- Responsive dark UI with a red accent, scroll animations, and reduced-motion support

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python, Django 6 |
| Database | PostgreSQL on [Neon](https://neon.tech) (SQLite for local development) |
| Media storage | [Cloudinary](https://cloudinary.com) |
| Static files | WhiteNoise |
| Frontend | Django templates, plain CSS and JavaScript (no framework) |
| Hosting | [Vercel](https://vercel.com) |

## Project structure

```
carsite/            Django project (settings, urls, wsgi)
cars/               Main app (models, views, forms, templates, static CSS/JS)
cars/management/    seed_cars command (sample data)
static/images/      Hero images and sample car photos
build_files.sh      Vercel build step (collectstatic + migrate)
vercel.json         Vercel configuration
```

## Run locally

Requirements: Python 3.12+ (Django 6 requires it).

```bash
git clone https://github.com/esraahosni/Carpedia.git
cd Carpedia
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export DEBUG=True                # Windows PowerShell: $env:DEBUG="True"
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_cars       # optional: adds 10 sample cars
python manage.py runserver
```

Open http://127.0.0.1:8000. With no `DATABASE_URL`, the app uses a local SQLite file. Run the tests with `python manage.py test`.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes (production) | Long random string. The app refuses to start without it when `DEBUG` is off. |
| `DATABASE_URL` | Yes (production) | PostgreSQL connection string, for example from Neon. Falls back to SQLite if unset. |
| `CLOUDINARY_URL` | For photo uploads | Format `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`. Without it, uploads go to local disk, which is not persistent on Vercel. |
| `DEBUG` | No | Off by default. Set `True` for local development only. |
| `EXTRA_HOSTS` | No | Comma-separated custom domains to allow, for example `carpedia.example.com`. |

## Deploy to Vercel

1. Create a Postgres database on Neon and a Cloudinary account.
2. Import the repository in Vercel.
3. Add `SECRET_KEY`, `DATABASE_URL`, and `CLOUDINARY_URL` under Project Settings, then Environment Variables.
4. Deploy. The build runs `build_files.sh`, which installs dependencies in a virtualenv, collects static files, and applies migrations when `DATABASE_URL` is set.
5. Create an admin user once against the production database: `DATABASE_URL=... SECRET_KEY=... python manage.py createsuperuser`.

Pushes to `main` redeploy automatically.

## Security notes

- Debug mode is off by default and `SECRET_KEY` comes from the environment.
- Destructive actions (delete car, delete user, promote, demote, favourite) accept POST only, with CSRF tokens.
- Admin views require staff permissions.
- Secure cookies and a proxy SSL header are enabled in production.

## Sample data and credits

The sample cars, prices, and specs from `seed_cars` are placeholders for demonstration, not real listings. Sample car photos are from Wikimedia Commons (CC BY-SA 4.0 or CC0); the file names and licenses are listed in [`static/images/seed/CREDITS.md`](static/images/seed/CREDITS.md).

## Author

Built by [Esraa Hosni](https://github.com/esraahosni).
