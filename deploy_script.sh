#!/bin/bash

# Replace with your actual project directory and virtual environment path
PROJECT_DIR="/usr/local/lsws/Example/html/demo"
VENV_DIR="/usr/local/lsws/Example/html/bin"

# Activate virtual environment
source $VENV_DIR/bin/activate

# Navigate to project directory
cd $PROJECT_DIR

# Pull the latest code
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Restart the Django app (replace 'your_django_project' with your actual project name)
sudo systemctl restart snox_pro
