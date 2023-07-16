# Create & activate environment
    python -m venv .venv
    source .venv/Scripts/activate

# Create new project
    django-admin startproject <project-name> .

# Create new application
    django-admin startapp <app-name>
    or
    python manage.py startapp <app-name>

# Run migration all
    python manage.py migrate
# Create migration
    python manage.py makemigrations <snippets>
# Run migration with specified app
    python manage.py migrate <snippets>

# Start app
    python manage.py runserver
    python manage.py runserver <ip:port>
    python manage.py runserver <port>

# Create user
    python manage.py createsuperuser --email <admin@example.com> --username <admin>

# Shell
    python manage.py shell
    