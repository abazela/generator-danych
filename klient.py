from constants import CHWYTLIWE_SLOWO, KATEGORIE_DZIALALNOSCI, MIASTA, KONCOWKA, TYPY_KLIENTA
import random
from faker import Faker
import pandas as pd

fake = Faker('pl_PL')

def generowanie_klientow(liczba_klientow, pracownicy, max_id = 0):

    dane = {
        'ID': range(max_id + 1, liczba_klientow + max_id + 1),
        'Nazwa': [],
        'NIP': [],
        'Miasto': [],
        'Typ_klienta': [],
        'ID_Pracownik': []
    }

    for _ in range(liczba_klientow):

        dane['Nazwa'].append(generowanie_nazwa_firmy())
        dane['NIP'].append(fake.numerify(text='##########'))

        if random.random() > 0.7:
            miasto = random.choice(MIASTA)
        else:
            miasto = fake.city()
        dane['Miasto'].append(miasto)

        dane['Typ_klienta'].append(random.choice(TYPY_KLIENTA))

        dane['ID_Pracownik'].append(random.randint(1, pracownicy))

    return pd.DataFrame(dane)



def generowanie_nazwa_firmy():

    szablon = random.choice([
        "{kategoria} {slowo}",
        "{kategoria} {slowo} {koncowka}",
        "{kategoria} {miasto}",
        "{slowo} {kategoria} {miasto}"
    ])

    kategoria = random.choice(KATEGORIE_DZIALALNOSCI)
    slowo = random.choice(CHWYTLIWE_SLOWO)
    koncowka = random.choice(KONCOWKA)
    miasto = random.choice(MIASTA)

    nazwa = szablon.format(
        kategoria=kategoria,
        slowo=slowo,
        miasto=miasto,
        koncowka=koncowka
    )

    return nazwa


# - 2 x ten sam Klient (NIP/nazwa) - zostawienie klienta jeden raz
    # duplikaty_klient_idx = random.sample(range(1, liczba + 1), k=int(liczba*0.04))
    # for idx in duplikaty_klient_idx:
    #     dane[random.choice(dane['ID_klient'])]
    #
    # return df