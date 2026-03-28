import random
from datetime import date, timedelta
import pandas as pd
from constants import STATUS


def generowanie_zamowien(liczba_zamowien, klienci, pracownicy, max_id=0, nowe=False):

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
        if nowe: 
            data_zam = date.today()
            dni = 0
        else:
            dni = random.randint(0, 360)
            data_zam = date.today()-timedelta(days=dni)

        if dni <= 2:
            status = 'Nowe'
        elif dni <= 7:
            status = 'Wysłane'
        elif dni <= 30:
            status = random.choices(['Dostarczone', 'Zwrot'], weights=[0.92, 0.08])[0]
        else:
            status = random.choices(['Dostarczone', 'Zwrot'], weights=[0.94, 0.06])[0]
            
        dane['Data_zamowienia'].append(data_zam)
        dane['Status'].append(status)
        #do dopracowania - po klientach
        dane['Rabat'].append(round(random.uniform(0.05, 0.3),2))
        dane['ID_Klient'].append(random.randint(1, klienci))
        dane['ID_Pracownik'].append(random.randint(1, pracownicy))

    return pd.DataFrame(dane)

def aktualizuj_zamowienia(df_zam, praw_zwrotu=0.045):

    today = date.today()
    df = df_zam.copy()

    for idx, row in df.iterrows():
        try:
            data_zam = pd.to_datetime(row['Data_zamowienia']).date()
        except:
            continue

        dni = (today - data_zam).days
        status = row['Status']

        nowy_status = status

        if status == 'Nowe':
            if dni > 2:
                nowy_status = 'Wysłane'

        elif status == 'Wysłane':
            if dni > 7:
                nowy_status = 'Dostarczone'

        elif status == 'Dostarczone':
            if 14 <dni <= 60:
                if random.random() < praw_zwrotu:
                    nowy_status = 'Zwrot'

        # Zapisujemy zmianę tylko jeśli status się zmienił
        if nowy_status != status:
            df.at[idx, 'Status'] = nowy_status


    return df