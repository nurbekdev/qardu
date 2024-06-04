#!/bin/sh

# Function to wait for PostgreSQL to be ready
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."

    # Loop until we can make a successful connection to PostgreSQL
    while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
        sleep 1
    done

    echo "PostgreSQL is ready."
}

# Run the wait function
wait_for_postgres

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Compiling translations..."
python manage.py compilemessages

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Continue to the main process (CMD)
exec "$@"