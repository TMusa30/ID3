Implementacija ID3 algoritma za izgradnju stabla odluke.

Program može učitati podatke iz CSV datoteka, trenirati model stabla odluke i predviđati rezultate na ispitnim testovima.

Instalacija :
  1. Potrebna instalirana verzija Python-a 3.x
  2. Preuzmite solution.py i datoteku primjeri


Upute za pokretanje :
  1. Otvorite terminal i pozicionirajte se u direktorij gdje se nalazi "solution.py" te naredbom :
     "python solution.py <putanja_do_datoteke_za_treniranje> <putanja_do_datoteke_za_testiranje>"
     npr. "python solution.py primjeri/volleyball.csv primjeri/volleyball_test.csv"

  2. Ako želite ograničiti dubinu stabla odluke onda upisujemo :
     "python solution.py primjeri/volleyball.csv primjeri/volleyball_test.csv 1", gdje "1" predstavlja željenu dubinu stabla.
