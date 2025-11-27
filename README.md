Smart Learning backend (Django)

Notes:
- Use a virtual environment before installing dependencies:
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt

- Initialize git and push:
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/yourusername/yourrepo.git
  git branch -M main
  git push -u origin main

Troubleshooting: "fatal: not a git repository / does not have a commit checked out"
- This happens if a nested folder (e.g. FINAL-PROJECT/) contains its own Git repository or is a broken submodule with no commit.
- Fixes:
  1) If you want that folder as regular files (not a repo): delete the nested .git inside it then add again:
     - Windows (cmd): rmdir /s /q "FINAL-PROJECT\.git"
     - PowerShell: Remove-Item -Recurse -Force .\FINAL-PROJECT\.git
     - Unix: rm -rf FINAL-PROJECT/.git
     Then: git add . && git commit -m "Add project files"
  2) If it's meant to be a submodule: add it properly
     git submodule add <repo-url> FINAL-PROJECT
     git submodule update --init --recursive
  3) Quick ignore (if you don't want to add it): ensure .gitignore contains `FINAL-PROJECT/` and then run git add . (if it's not already tracked).
- If you've partially added it and get errors, try:
  git rm --cached FINAL-PROJECT
  then apply one of the fixes above.

Migration-fix checklist (InconsistentMigrationHistory)
- Make a backup first (important):
  copy db.sqlite3 db.sqlite3.bak     # Windows (cmd/powershell)
  cp db.sqlite3 db.sqlite3.bak       # Unix / Git Bash

1) Inspect migrations and DB state
- See which migrations exist and which are applied:
  python manage.py showmigrations
  python manage.py showmigrations users

- Check whether the users table exists (sqlite):
  sqlite3 db.sqlite3 "SELECT name FROM sqlite_master WHERE type='table' AND name='users_user';"
  # or open dbshell:
  python manage.py dbshell
  sqlite> .tables
  sqlite> .quit

- For Postgres/MySQL use psql / mysql client or run a quick Python check:
  python - <<PY
  import sqlite3, sys
  conn = sqlite3.connect('db.sqlite3')
  cur = conn.cursor()
  cur.execute(\"\"\"SELECT name FROM sqlite_master WHERE type='table' AND name='users_user';\"\"\")
  print(cur.fetchone())
  conn.close()
  PY

2) If users_user table already exists (fastest safe fix)
- Mark the users migration as applied without running it:
  python manage.py migrate users --fake
  python manage.py migrate

3) If users_user table does NOT exist and admin or other app was applied earlier
- Unapply the dependent migration and re-run all migrations to apply in correct order:
  python manage.py migrate admin zero
  python manage.py migrate

4) Verification
- Confirm all migrations applied:
  python manage.py showmigrations

Migration reset (use only when migration graph is irreparably tangled)
1) Backup your DB (mandatory)
   Windows:
     copy db.sqlite3 db.sqlite3.bak
   Unix/Git Bash:
     cp db.sqlite3 db.sqlite3.bak

2) Manual clean (one app at a time)
   Inside each app folder (e.g. users, courses, analytics, quizzes):
     - Open <app>/migrations/
     - Delete all files EXCEPT __init__.py
   Do NOT touch migrations for Django built-ins (auth, admin, contenttypes, sessions).

3) Recreate migrations and apply
   python manage.py makemigrations
   python manage.py migrate

4) Create superuser
   python manage.py createsuperuser

Automated helper (optional)
- There's a helper script at `scripts/reset_migrations.py` that automates steps:
  - makes a db.sqlite3.bak
  - deletes migrations (keeps __init__.py) for apps you specify
  - runs `makemigrations` and `migrate`
- Usage (dry-run by default):
  python scripts/reset_migrations.py --apps users,courses,analytics --dry-run
- To actually perform the reset pass --yes:
  python scripts/reset_migrations.py --apps users,courses,analytics --yes

Safety notes
- Test on a copy of your DB if you have production or important data.
- If you are unsure which apps to include, list them explicitly with --apps.
- If your project uses a DB other than sqlite, edit the script accordingly or perform manual steps.
