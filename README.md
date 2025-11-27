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
