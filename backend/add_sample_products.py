import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narejonie_backend.settings')
django.setup()

from api.models import Produkt

# Przykładowe produkty
products = [
    {
        'nazwa': 'Bluza Oversize Black',
        'opis': 'Wygodna bluza oversize w kolorze czarnym. Idealna na co dzień.',
        'cenaBrutto': 149.99,
        'kategoria': 'bluzy',
        'kolor': 'czarny',
        'rozmiar': 'M',
        'zdjecie': '',
        'stanMagazynowy': 20
    },
    {
        'nazwa': 'Bluza Hoodie Grey',
        'opis': 'Klasyczna bluza z kapturem w kolorze szarym.',
        'cenaBrutto': 129.99,
        'kategoria': 'bluzy',
        'kolor': 'szary',
        'rozmiar': 'L',
        'zdjecie': '',
        'stanMagazynowy': 15
    },
    {
        'nazwa': 'T-shirt Basic White',
        'opis': 'Biały t-shirt z bawełny organicznej.',
        'cenaBrutto': 49.99,
        'kategoria': 't-shirty',
        'kolor': 'biały',
        'rozmiar': 'M',
        'zdjecie': '',
        'stanMagazynowy': 50
    },
    {
        'nazwa': 'T-shirt Graphic Black',
        'opis': 'Czarny t-shirt z graficznym nadrukiem.',
        'cenaBrutto': 69.99,
        'kategoria': 't-shirty',
        'kolor': 'czarny',
        'rozmiar': 'L',
        'zdjecie': '',
        'stanMagazynowy': 30
    },
    {
        'nazwa': 'Spodnie Cargo Green',
        'opis': 'Zielone spodnie cargo z wieloma kieszeniami.',
        'cenaBrutto': 199.99,
        'kategoria': 'spodnie',
        'kolor': 'zielony',
        'rozmiar': '32',
        'zdjecie': '',
        'stanMagazynowy': 25
    },
    {
        'nazwa': 'Jeansy Slim Fit',
        'opis': 'Niebieskie jeansy w kroju slim fit.',
        'cenaBrutto': 179.99,
        'kategoria': 'spodnie',
        'kolor': 'niebieski',
        'rozmiar': '31',
        'zdjecie': '',
        'stanMagazynowy': 20
    },
    {
        'nazwa': 'Czapka Beanie Black',
        'opis': 'Czarna czapka zimowa beanie.',
        'cenaBrutto': 39.99,
        'kategoria': 'akcesoria',
        'kolor': 'czarny',
        'rozmiar': 'UNI',
        'zdjecie': '',
        'stanMagazynowy': 40
    },
    {
        'nazwa': 'Plecak Street Style',
        'opis': 'Miejski plecak w stylu streetwear.',
        'cenaBrutto': 249.99,
        'kategoria': 'akcesoria',
        'kolor': 'czarny',
        'rozmiar': 'UNI',
        'zdjecie': '',
        'stanMagazynowy': 10
    },
    {
        'nazwa': 'Bluza Zip-Up Navy',
        'opis': 'Granatowa bluza rozpinana na zamek.',
        'cenaBrutto': 159.99,
        'kategoria': 'bluzy',
        'kolor': 'granatowy',
        'rozmiar': 'XL',
        'zdjecie': '',
        'stanMagazynowy': 12
    },
    {
        'nazwa': 'T-shirt V-Neck Red',
        'opis': 'Czerwony t-shirt z dekoltem w serek.',
        'cenaBrutto': 59.99,
        'kategoria': 't-shirty',
        'kolor': 'czerwony',
        'rozmiar': 'S',
        'zdjecie': '',
        'stanMagazynowy': 35
    },
]

# Dodaj produkty
for product_data in products:
    produkt, created = Produkt.objects.get_or_create(
        nazwa=product_data['nazwa'],
        defaults=product_data
    )
    if created:
        print(f"Dodano: {produkt.nazwa}")
    else:
        print(f"Istnieje: {produkt.nazwa}")

print(f"\nŁącznie produktów w bazie: {Produkt.objects.count()}")
