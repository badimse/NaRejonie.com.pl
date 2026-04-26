import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narejonie_backend.settings')
django.setup()

from api.models import User

# Utwórz superużytkownika
if not User.objects.filter(email='admin@narejonie.pl').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@narejonie.pl',
        password='admin123',
        imie='Admin',
        nazwisko='Sklep'
    )
    print("Superuser utworzony: admin@narejonie.pl / admin123")
else:
    print("Superuser już istnieje")
