import pandas as pd
import random
import numpy as np
from datetime import date, timedelta

from constants import KATEGORIE_PRODUKTU, NAZWY, PRODUCENCI, FORMY

def generowanie_produktów(liczba):

    dane = {
        'ID': range(1, liczba + 1),
        'Nazwa': [],
        'Kategoria': [],
        'Producent': [],
        'Cena': [],
        'Forma': [],
        'Data_ważności': []
    }

    for _ in range(liczba):

        kategoria = random.choice(KATEGORIE_PRODUKTU)
        nazwa = random.choice(NAZWY[kategoria])

        dane['Nazwa'].append(nazwa)
        dane['Kategoria'].append(kategoria)

        dane['Producent'].append(random.choice(PRODUCENCI))
        dane['Forma'].append(random.choice(FORMY))

        cena = round(random.uniform(9.99, 249.99), 2)
        dane['Cena'].append(cena)

        #chyba do usunięcia
        data = losowa_data()
        dane['Data_ważności'].append(data)

    df = pd.DataFrame(dane)

#Generowanie błędnych wartości

    #Ujemne ceny - 6%
    # ujemne_idx = random.sample(range(liczba), k=int(liczba*0.06))
    # for idx in ujemne_idx:
    #     df.at[idx, 'Cena'] = -df.at[idx, 'Cena'] #odwracanie wartości


    # #Brak cen - 7%
    # brak_ceny_idx = random.sample(range(liczba), k=int(liczba*0.07))
    # for idx in brak_ceny_idx:
    #     df.at[idx, 'Cena'] = np.nan

    #Duplikaty produktów o różnym ID - 6%
    liczba_duplikatów = int(liczba*0.06)

    if liczba_duplikatów > 0:
        #lista oryginalnych indeksów, która zostanie podmieniona przez double
        oryginalne_idx = random.sample(df.index.tolist(), k=liczba_duplikatów)

        duplikaty = []

        for org_idx in oryginalne_idx:
            nowy_wiersz = df.loc[org_idx].copy() #kopiujemy wiersz

            #nowe ID - duplikaty na dole danych
            if 'ID' in df.columns:
                max_id = df['ID'].max()
                nowy_wiersz['ID'] = max_id + 1 + len(duplikaty)

            duplikaty.append(nowy_wiersz)

        df_duplikaty = pd.DataFrame(duplikaty)
        df = pd.concat([df, df_duplikaty], ignore_index=True)

    # #Odstająca cena - 5%
    # zawyzone_ceny_idx = random.sample(range(liczba), k=int(liczba*0.05))
    # for idx in zawyzone_ceny_idx:
    #     df.at[idx, 'Cena'] = np.round(df.at[idx, 'Cena'] * random.uniform(5, 12), 2) #5-12 x drożej
    #
    return df


def losowa_data():
    return date.today() + timedelta(days=random.randint(0, 1080))