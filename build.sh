#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install Dependencies (Including Pillow)
pip install -r requirements.txt

# 2. AUTO-FIX: Generate missing migration files 🪄
# (This fixes the "Missing Notification Table" error)
python manage.py makemigrations --no-input

# 3. Update the Database
python manage.py migrate

# 4. Collect Static Files
python manage.py collectstatic --no-input

# 5. Create Superuser (if needed)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')"