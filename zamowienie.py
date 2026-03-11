import random
from datetime import date, timedelta

import pandas as pd

from constants import STATUS


def generowanie_zamowien(liczba_zamowien, klienci, pracownicy, max_id=0):

    dane = {
        'ID': range(max_id + 1, max_id + liczba_zamowien + 1),
        'Data_zamowienia': [],
        'Status': [],
        'Rabat': [],
        'Vat_procent': 0.05,
        'ID_Klient': [],
        'ID_Pracownik': []
    }


    for _ in range(liczba_zamowien):
        dane['Data_zamowienia'].append(losowa_data_zamowienia())
        dane['Status'].append(random.choice(STATUS))
        #do dopracowania - po klientach
        dane['Rabat'].append(round(random.uniform(0.05, 0.3),2))
        dane['ID_Klient'].append(random.randint(1, klienci))
        dane['ID_Pracownik'].append(random.randint(1, pracownicy))

    return pd.DataFrame(dane)


def losowa_data_zamowienia():
    return date.today() - timedelta(days=random.randint(0, 30))