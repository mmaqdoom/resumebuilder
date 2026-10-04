# ResumeBuilder

A Flask application for maintaining multiple role-specific resume profiles, previewing them in the browser, and downloading a print-ready PDF.

## Requirements

- Python 3.10 or newer
- The dependencies listed in `requirements.txt`
- PDF generation uses WeasyPrint where its native platform libraries are available and xhtml2pdf on Windows (or as a fallback). Both are included in the Python dependencies, so Windows can generate PDFs without manually installing GTK.

## Setup

From this directory, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set a private `SECRET_KEY` before running outside local development:

```powershell
$env:SECRET_KEY = "replace-with-a-long-random-secret"
```

Start the development server:

```powershell
python run.py
```

Open http://127.0.0.1:5000. The SQLite database is created under `instance/` by default. Set `DATABASE_URL` to use PostgreSQL or another SQLAlchemy-compatible database; PostgreSQL URLs are supported through Psycopg.

## MVP features

- Email and password registration, login, logout, and session protection
- Multiple resume profiles per account with ownership checks
- Editable contact information, summary, education, experience, and skills
- Browser preview and A4 PDF download
- CSRF protection on forms and state-changing routes

Stripe payments and additional resume designs are intentionally not included; they are future roadmap items in `resumebuilder_planning_document.md`.
