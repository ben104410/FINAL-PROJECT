#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess


def main():
    # Ensure the project root is on sys.path so 'backend' package imports correctly
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Ensure correct settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Improved diagnostic message to help fix virtualenv / installation issues
        print("\nError: Couldn't import Django. Common fixes:")
        print(f"  - Activate your virtualenv (Windows):    .\\venv\\Scripts\\activate")
        print(f"  - Then install deps:                     pip install -r requirements.txt")
        print("  - Or install essentials directly:        pip install Django djangorestframework djangorestframework-simplejwt django-cors-headers")
        print()
        print("Diagnostics:")
        try:
            print("  Python executable:", sys.executable)
        except Exception:
            pass
        print("  Run: python -c \"import django; print(django.get_version())\" to verify Django availability with this interpreter.")
        print()
        # Re-raise original ImportError with additional context
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and you're using the project's Python environment? "
            "Activate your virtualenv or install dependencies (pip install -r requirements.txt)."
        ) from exc

    try:
        execute_from_command_line(sys.argv)
    except Exception as exc:
        # Detect inconsistent migration history and print clear remedial steps
        try:
            from django.db.migrations.exceptions import InconsistentMigrationHistory
            if isinstance(exc, InconsistentMigrationHistory):
                print("\nInconsistentMigrationHistory detected.")
                print("This usually happens when a contrib app migration (e.g. admin) was applied before a dependent app's initial migration (users).")
                print("\nRecommended fixes (pick the one that matches your situation):")
                print("1) If the users table already exists in the database (created earlier), mark the new users migration as applied without running it:")
                print("   python manage.py migrate users --fake")
                print("   python manage.py migrate")
                print("\n2) If you prefer to reapply migrations in order, unapply the dependent migration and re-run:")
                print("   python manage.py migrate admin zero")
                print("   python manage.py migrate")
                print("\nAfter applying one of the above, re-run your original command.")
                # Opt-in automated fix via environment variable:
                auto_fix = os.environ.get('AUTO_FIX_MIGRATIONS', '').lower()
                if auto_fix == 'fake_users':
                    print("\nAUTO_FIX_MIGRATIONS=fake_users detected — attempting to run the 'fake' fix automatically now.")
                    # Run: python manage.py migrate users --fake
                    try:
                        manage_py = os.path.join(project_root, 'manage.py')
                        cmd1 = [sys.executable, manage_py, 'migrate', 'users', '--fake']
                        print("Running:", " ".join(cmd1))
                        subprocess.check_call(cmd1)
                        # Then run: python manage.py migrate
                        cmd2 = [sys.executable, manage_py, 'migrate']
                        print("Running:", " ".join(cmd2))
                        subprocess.check_call(cmd2)
                        print("\nAutomatic fix applied. Re-run your original command now.")
                        sys.exit(0)
                    except subprocess.CalledProcessError as e:
                        print("\nAutomatic fix failed:", e)
                        print("Please run the recommended commands manually.")
                        sys.exit(1)
                # exit with non-zero so the user notices
                sys.exit(1)
        except Exception:
            pass
        # Re-raise other exceptions
        raise


if __name__ == '__main__':
    main()
