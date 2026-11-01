# GDC ZIAM Portal — Render Preview Setup (Roman Urdu)

## Important
- `render.yaml` is for a DEMO/PREVIEW ONLY. Current Render Free web services sleep after 15 minutes of inactivity and Free Postgres databases expire after 30 days. Do not use real student names, passwords, complaints, or re-admission data on the free preview.
- For the official college portal, use a paid hosting/database plan with backups and college approval.
- The remote database will be new and empty. Local accounts and `db.sqlite3` do not automatically transfer.

## Before uploading to GitHub
1. Use the **current project folder on your laptop that already runs correctly**; do not overwrite it with an older ZIP.
2. Confirm `portal/migrations/0001_initial.py` exists. The migration must be committed to the repository.
3. Do not upload `db.sqlite3`, `db_backup_before_hosting.sqlite3`, `.venv`, `.env`, passwords, or any real personal data. The project's `.gitignore` excludes SQLite databases and virtual environments, but double-check before publishing.
4. Create a **private** GitHub repository and upload the project source, including `portal/migrations/` and all static/template files.

## Render preview
1. Sign in to Render and connect the private GitHub repository.
2. Choose **New → Blueprint** (or New Web Service if you have a reviewed equivalent configuration) and select the repo containing `render.yaml`.
3. Review the Blueprint resources. It creates a Free web service and Free PostgreSQL database for preview only.
4. Start the deployment and read the build logs. If deployment fails, save the error and stop; do not change random settings.
5. After deployment succeeds, create the first Principal using Render Shell/one-off command if your chosen plan supports it: `python manage.py createsuperuser`. If Free plan has no shell access, use a reviewed, temporary, secure provisioning method or switch to an eligible paid plan—do not add a public registration form that can create Principal accounts.
6. Do not add real college data until college approval and a persistent, backed-up database are in place.

## Production go-live checklist
- Paid production web service and persistent managed database with backups.
- `DJANGO_DEBUG=0`, strong generated `DJANGO_SECRET_KEY`, accurate `ALLOWED_HOSTS`, HTTPS/CSRF settings.
- Create principal and staff accounts securely; never commit credentials.
- Re-test role permissions and private complaints on the deployed URL.
- Run `python manage.py check --deploy` against the actual production environment settings and resolve warnings that apply to that host.
