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

Open http://127.0.0.1:5000. The SQLite database is created under `instance/` by default. Set `NEON_DATABASE_URL` to connect to Neon, or `DATABASE_URL` to use another PostgreSQL or SQLAlchemy-compatible database. `NEON_DATABASE_URL` takes precedence if both variables are set. PostgreSQL URLs are supported through Psycopg.

## Connect to Neon

This app uses `NEON_DATABASE_URL` when it is set, so it can connect to Neon even if Render also provides a `DATABASE_URL` for an existing Render database. The app does not copy data from that database. On startup, SQLAlchemy's `db.create_all()` creates any missing tables in the selected database, so a new, empty Neon database starts with an empty application schema.

1. In the Neon Console, open your project and select **Connect**. Copy the connection string for the database and branch you want the app to use. Keep the credentials private; do not commit the URL to the repository. Use the URL as provided by Neon (including its SSL parameters).
2. In Render, open your Resume Builder web service, go to **Environment**, and add `NEON_DATABASE_URL` with that connection string as its value. Save the change and redeploy the service. Leave `DATABASE_URL` alone if Render uses it for the old database; the app will prefer `NEON_DATABASE_URL`.
3. After the deployment, open the app and register a new account. Confirm that you can create a resume. These records will be in Neon; the old Render database is neither read nor modified by the app while `NEON_DATABASE_URL` is set.

To test locally in PowerShell, set the same variable before starting the app:

```powershell
$env:NEON_DATABASE_URL = "paste-your-Neon-connection-string-here"
python run.py
```

The local process will also create missing tables in the Neon database. To return to the local SQLite database, close that PowerShell session or remove the variable with `Remove-Item Env:NEON_DATABASE_URL`.

## MVP features

- Email and password registration, login, logout, and session protection
- Multiple resume profiles per account with ownership checks
- Editable contact information, summary, education, experience, and skills
- Browser preview and A4 PDF download
- CSRF protection on forms and state-changing routes

Stripe payments and additional resume designs are intentionally not included; they are future roadmap items in `resumebuilder_planning_document.md`.
