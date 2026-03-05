#!/bin/bash

# Litfunder Backend - Database Initialization Script
# This script initializes the database with migrations and optional mock data

set -e

echo "================================"
echo "Litfunder Database Initialization"
echo "================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Wait for database to be ready
echo -e "${BLUE}Waiting for database to be ready...${NC}"
python manage.py dbshell -c "SELECT 1" > /dev/null 2>&1 || {
    echo -e "${YELLOW}Database not ready, waiting...${NC}"
    sleep 5
}

# Run migrations
echo -e "${BLUE}Running database migrations...${NC}"
python manage.py migrate --noinput

# Check if migrations were successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrations completed successfully${NC}"
else
    echo -e "${YELLOW}✗ Migration failed${NC}"
    exit 1
fi

# Show migration status
echo -e "${BLUE}Migration status:${NC}"
python manage.py showmigrations

# Create superuser if it doesn't exist
echo -e "${BLUE}Checking for superuser...${NC}"
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@litfunder.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")
END

# Collect static files
echo -e "${BLUE}Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Static files collected${NC}"
else
    echo -e "${YELLOW}✗ Static file collection failed${NC}"
fi

# Optional: Generate mock data
if [ "$1" = "--mock-data" ] || [ "$1" = "-m" ]; then
    echo -e "${BLUE}Generating mock data...${NC}"
    python manage.py shell < litfunder/utils/generate_date.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Mock data generated${NC}"
    else
        echo -e "${YELLOW}✗ Mock data generation failed${NC}"
    fi
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Database initialization complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Access points:"
echo -e "  Admin:   http://localhost:8000/admin/"
echo -e "  API:     http://localhost:8000/api/"
echo -e "  Swagger: http://localhost:8000/api/docs/"
echo ""
echo "Default credentials:"
echo -e "  Username: admin"
echo -e "  Email:    admin@litfunder.com"
echo -e "  Password: admin123"
echo ""
