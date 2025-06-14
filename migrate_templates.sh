#!/bin/bash

# Stop immediately if any command fails
set -e

echo "🔁 Starting template migration..."

# Create global templates directory and subdirectories
mkdir -p templates/registration
mkdir -p templates/pages
mkdir -p templates/accounts

echo "📁 Created templates/registration, templates/pages, templates/accounts"

# Move registration templates
if [ -f accounts/templates/registration/login.html ]; then
    mv accounts/templates/registration/login.html templates/registration/
    echo "✅ Moved login.html"
fi

if [ -f accounts/templates/registration/signup.html ]; then
    mv accounts/templates/registration/signup.html templates/registration/
    echo "✅ Moved signup.html"
fi

# Move other possible app templates (edit as needed for your structure)
if [ -d pages/templates/pages ]; then
    mv pages/templates/pages/* templates/pages/ 2>/dev/null || true
    echo "✅ Moved page templates"
fi

# Clean up old template folders
rm -rf accounts/templates
rm -rf pages/templates

echo "🧼 Cleaned up old templates directories"
echo "🎉 Template migration complete. Verify with: python manage.py shell"
