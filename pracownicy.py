from faker import Faker
import pandas as pd

fake = Faker('pl_PL')

def generowanie_pracownikow(liczba):

    dane ={
        'ID': range(1, liczba+1),
        'Imie': [],
        'Nazwisko': [],
        'Email': []
    }

    for _ in range(liczba):
        imie = fake.first_name()
        nazwisko = fake.last_name()

        dane['Imie'].append(imie)
        dane['Nazwisko'].append(nazwisko)

        email = "{Imie}.{Nazwisko}@gmail.com".format(Imie=imie, Nazwisko=nazwisko)
        dane['Email'].append(email)

    return pd.DataFrame(dane)