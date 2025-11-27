import os
import sys
import shutil
import argparse
import glob
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # project root
DEFAULT_APPS = ['users', 'courses', 'quizzes', 'analytics']

def rm_migration_files(app_dir: Path, dry_run=True):
    mig_dir = app_dir / 'migrations'
    if not mig_dir.exists() or not mig_dir.is_dir():
        print(f"  - migrations directory missing for {app_dir.name}, skipping.")
        return
    files = list(mig_dir.glob('*.py'))
    for f in files:
        if f.name == '__init__.py':
            continue
        if dry_run:
            print(f"  DRY-RUN: would remove {f}")
        else:
            print(f"  Removing {f}")
            f.unlink()

def run_manage_cmd(args_list):
    cmd = [sys.executable, str(ROOT / 'manage.py')] + args_list
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

def backup_sqlite(db_path: Path, dry_run=True):
    if not db_path.exists():
        print("No sqlite DB found at", db_path)
        return
    bak = db_path.with_suffix(db_path.suffix + '.bak')
    if dry_run:
        print(f"DRY-RUN: would copy {db_path} -> {bak}")
    else:
        print(f"Backing up {db_path} -> {bak}")
        shutil.copy2(db_path, bak)

def main():
    parser = argparse.ArgumentParser(description="Reset local app migrations and re-run makemigrations/migrate.")
    parser.add_argument('--apps', type=str, default=",".join(DEFAULT_APPS),
                        help="Comma-separated app names to clear migrations for (default: users,courses,quizzes,analytics)")
    parser.add_argument('--yes', action='store_true', help="Actually perform destructive actions (remove files, run migrate).")
    parser.add_argument('--dry-run', action='store_true', help="Explicit dry run (no changes). Default behaviour is dry-run unless --yes is used.")
    args = parser.parse_args()

    apps = [a.strip() for a in args.apps.split(',') if a.strip()]
    dry_run = not args.yes or args.dry_run

    print("Project root:", ROOT)
    print("Apps to process:", apps)
    print("Dry run:", dry_run)
    if not args.yes and not args.dry_run:
        print("Note: running in dry-run mode. Add --yes to execute changes.\n")

    db_path = ROOT / 'db.sqlite3'
    backup_sqlite(db_path, dry_run=dry_run)

    for app in apps:
        app_dir = ROOT / app
        if not app_dir.exists():
            print(f"App folder not found: {app_dir} (skipping)")
            continue
        print(f"Processing app: {app}")
        rm_migration_files(app_dir, dry_run=dry_run)

    if dry_run:
        print("\nDry run complete. No changes were made. Re-run with --yes to apply changes.")
        return

    # After deletion, recreate migrations and migrate
    try:
        run_manage_cmd(['makemigrations'])
        run_manage_cmd(['migrate'])
        print("\nMigrations recreated and applied.")
    except subprocess.CalledProcessError as e:
        print("Error while running manage.py commands:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
