import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narejonie_backend.settings')
django.setup()

from api.models import User, Produkt, Zamowienie, PozycjaZamowienia, AdresDostawy, Koszyk

# Pobierz użytkowników
user1 = User.objects.get(email='user@user.pl')
user2 = User.objects.get(email='test@test.pl')
admin = User.objects.get(email='admin@narejonie.pl')

# Pobierz produkty
produkty = list(Produkt.objects.all())

if len(produkty) < 2:
    print("Brak wystarczającej liczby produktów w bazie!")
    exit(1)

print(f"Znaleziono {len(produkty)} produktów")

# Funkcja tworząca zamówienie
def create_order(user, status, kwota, data_offset=0):
    zamowienie = Zamowienie.objects.create(
        id_uzytkownik=user,
        status=status,
        kwota=kwota,
        dataZlozenia=timezone.now() - timedelta(days=data_offset)
    )
    return zamowienie

# Funkcja tworząca pozycję zamówienia
def create_order_item(zamowienie, produkt, ilosc, cena):
    PozycjaZamowienia.objects.create(
        id_zamowienie=zamowienie,
        id_produkt=produkt,
        ilosc=ilosc,
        cenaJednostkowa=cena
    )

# Funkcja tworząca adres dostawy
def create_adres(zamowienie, ulica, miasto, kod, kraj='Polska'):
    AdresDostawy.objects.create(
        id_zamowienie=zamowienie,
        ulica=ulica,
        miasto=miasto,
        kodPocztowy=kod,
        kraj=kraj
    )

# Zamówienie 1 - zakończone (user@user.pl)
print("Tworzenie zamówienia 1 - zakończone...")
z1 = create_order(user1, 'zakończone', 299.98, data_offset=10)
create_order_item(z1, produkty[0], 2, 149.99)
create_adres(z1, 'ul. Przykładowa 1/2', 'Warszawa', '00-001')

# Zamówienie 2 - wysłane (user@user.pl)
print("Tworzenie zamówienia 2 - wysłane...")
z2 = create_order(user1, 'wysłane', 89.99, data_offset=5)
create_order_item(z2, produkty[1], 1, 89.99)
create_adres(z2, 'ul. Przykładowa 1/2', 'Warszawa', '00-001')

# Zamówienie 3 - w realizacji (user@user.pl)
print("Tworzenie zamówienia 3 - w realizacji...")
z3 = create_order(user1, 'w realizacji', 250.00, data_offset=2)
create_order_item(z3, produkty[2], 1, 250.00)
create_adres(z3, 'ul. Przykładowa 1/2', 'Warszawa', '00-001')

# Zamówienie 4 - oczekujące (test@test.pl)
print("Tworzenie zamówienia 4 - oczekujące...")
z4 = create_order(user2, 'oczekujące', 199.98, data_offset=1)
create_order_item(z4, produkty[0], 1, 149.99)
create_order_item(z4, produkty[3], 1, 49.99)
create_adres(z4, 'ul. Testowa 10', 'Kraków', '30-001')

# Zamówienie 5 - anulowane (test@test.pl)
print("Tworzenie zamówienia 5 - anulowane...")
z5 = create_order(user2, 'anulowane', 350.00, data_offset=3)
create_order_item(z5, produkty[2], 1, 250.00)
create_order_item(z5, produkty[3], 2, 50.00)
create_adres(z5, 'ul. Testowa 10', 'Kraków', '30-001')

# Zamówienie 6 - zakończone (admin)
print("Tworzenie zamówienia 6 - zakończone (admin)...")
z6 = create_order(admin, 'zakończone', 449.97, data_offset=15)
create_order_item(z6, produkty[0], 3, 149.99)
create_adres(z6, 'ul. Adminowska 5', 'Lublin', '20-001')

print("\n=== Podsumowanie ===")
print(f"Łączna liczba zamówień: {Zamowienie.objects.count()}")
for status in ['oczekujące', 'w realizacji', 'wysłane', 'zakończone', 'anulowane']:
    count = Zamowienie.objects.filter(status=status).count()
    print(f"  {status}: {count}")

print("\nGotowe! Zamówienia zostały dodane do bazy danych.")
