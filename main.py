from produkty import generowanie_produktów
from zamowienie import generowanie_zamowien
from pozycje_zamowienie import generowanie_pozycje_zamowienie
from klient import generowanie_klientow
from pracownicy import generowanie_pracownikow

import pandas as pd
import os
from datetime import datetime

if __name__ == "__main__":

    liczba_zamowien= 450
    liczba_klientow= 200
    liczba_produktow = 100
    liczba_pracownikow = 25

    liczba_nowych_zamowien = 10
    liczba_nowych_klientow = 4

    plik = r"C:\Users\agata\Desktop\Inzynierka\SalesData\generowanieDanych\dane.xlsx"

    if not os.path.exists(plik):
        df_prod = generowanie_produktów(liczba=liczba_produktow)
        df_zam = generowanie_zamowien(liczba_zamowien=liczba_zamowien, klienci=liczba_klientow, pracownicy=liczba_pracownikow)
        df_poz = generowanie_pozycje_zamowienie(zamowienia=liczba_zamowien, produkty=liczba_produktow, max_id=0)
        df_kli = generowanie_klientow(liczba_klientow=liczba_klientow, pracownicy=liczba_pracownikow)
        df_pra = generowanie_pracownikow(liczba=liczba_pracownikow)


        with pd.ExcelWriter(plik, engine='openpyxl') as writer:
            df_prod.to_excel(writer, sheet_name='Produkty', index=False, header=True)
            df_zam.to_excel(writer, sheet_name='Zamowienia', index=False, header=True)
            df_poz.to_excel(writer, sheet_name='Pozycje_zamowienie', index=False, header=True)
            df_kli.to_excel(writer, sheet_name='Klienci', index=False, header=True)
            df_pra.to_excel(writer, sheet_name='Pracownicy', index=False, header=True)

        print("Baza początkowa")

    else:
        print("Plik istnieje, generowanie nowych danych")

        df_prod = pd.read_excel(plik, sheet_name='Produkty')
        # print(df_prod.head(10))
        df_pra = pd.read_excel(plik, sheet_name='Pracownicy')

        df_kli = pd.read_excel(plik, sheet_name='Klienci')
        df_zam = pd.read_excel(plik, sheet_name='Zamowienia')
        df_poz = pd.read_excel(plik, sheet_name='Pozycje_zamowienie')


        df_zam['ID'] = pd.to_numeric(df_zam['ID'], errors='coerce').astype('Int64')
        df_kli['ID'] = pd.to_numeric(df_kli['ID'], errors='coerce').astype('Int64')

        max_id_zam = df_zam['ID'].max() if not df_zam.empty else 0
        # max_id_poz = df_poz['ID_Pozycja'].max() if not df_poz.empty else 0
        max_id_kli = df_kli['ID'].max() if not df_kli.empty else 0

        print("Klienci")
        df_kli_new = generowanie_klientow(
            liczba_klientow=liczba_nowych_klientow,
            pracownicy=liczba_pracownikow,
            max_id=max_id_kli)

        print("zamoowienia")
        df_zam_new = generowanie_zamowien(
            liczba_zamowien=liczba_nowych_zamowien,
            klienci=len(df_kli_new),
            pracownicy=len(df_poz),
            max_id= max_id_zam)

        print("pozycje zamowienia")
        df_poz_new = generowanie_pozycje_zamowienie(zamowienia=liczba_nowych_zamowien, produkty=liczba_produktow, max_id = max_id_zam)

        with pd.ExcelWriter(plik, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df_kli_new.to_excel(writer, sheet_name='Klienci', startrow=len(df_kli), header=False, index=False)
            df_zam_new.to_excel(writer, sheet_name='Zamowienia', startrow=len(df_zam)+1, header=False, index=False)
            df_poz_new.to_excel(writer, sheet_name='Pozycje_zamowienie', startrow=len(df_poz)+1, header=False)

        print(f"Dopisano: {len(df_zam_new)} zamówień, {len(df_poz_new)} pozycji, {len(df_kli_new)} klientów.")





