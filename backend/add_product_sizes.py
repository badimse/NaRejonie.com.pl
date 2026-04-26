import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narejonie_backend.settings')
django.setup()

from api.models import Produkt, RozmiarProduktu

# Definicje rozmiarów dla różnych kategorii
rozmiary_kategorie = {
    'bluzy': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
    't-shirty': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
    'spodnie': ['30', '31', '32', '33', '34', '36'],
    'akcesoria': ['UNI'],
}

# Dodaj rozmiary do produktów
produkty = Produkt.objects.all()
for produkt in produkty:
    kategoria = produkt.kategoria.lower()
    rozmiary = rozmiary_kategorie.get(kategoria, ['S', 'M', 'L'])
    
    print(f"Dodawanie rozmiarów do: {produkt.nazwa} ({kategoria})")
    
    for rozmiar in rozmiary:
        # Losowa ilość sztuk dla każdego rozmiaru
        import random
        stan = random.randint(5, 30)
        
        rozmiar_obj, created = RozmiarProduktu.objects.get_or_create(
            id_produkt=produkt,
            rozmiar=rozmiar,
            defaults={'stanMagazynowy': stan}
        )
        
        if created:
            print(f"  + Dodano rozmiar {rozmiar}: {stan} szt.")
        else:
            print(f"  - Rozmiar {rozmiar} już istnieje")

print("\nGotowe! Wszystkie produkty mają teraz rozmiary.")
