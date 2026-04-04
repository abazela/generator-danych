from produkty import generowanie_produktów
from zamowienie import generowanie_zamowien, aktualizuj_zamowienia
from pozycje_zamowienie import generowanie_pozycje_zamowienie
from klient import generowanie_klientow
from pracownicy import generowanie_pracownikow
import random

import pandas as pd
import os
import time


if __name__ == "__main__":

    tryb_testowy = True
    if tryb_testowy:
        start = time.perf_counter()

    liczba_zamowien = 1000
    liczba_klientow = 500
    liczba_produktow = 150
    liczba_pracownikow = 30

    # liczba_nowych_zamowien = 10
    liczba_nowych_klientow = 4

    folder = os.path.join(os.getcwd(), "dane_csv")
    os.makedirs(folder, exist_ok=True)

    plik_produkty = os.path.join(folder, "produkty.csv")
    plik_zamowienia = os.path.join(folder, "zamowienia.csv")
    plik_pozycje = os.path.join(folder, "pozycje_zamowienie.csv")
    plik_klienci = os.path.join(folder, "klienci.csv")
    plik_pracownicy = os.path.join(folder, "pracownicy.csv")

    baza_istnieje = all([
        os.path.exists(plik_produkty),
        os.path.exists(plik_zamowienia),
        os.path.exists(plik_pozycje),
        os.path.exists(plik_klienci),
        os.path.exists(plik_pracownicy)
    ])

    if not baza_istnieje:
        df_prod = generowanie_produktów(liczba=liczba_produktow)
        df_zam = generowanie_zamowien(
            liczba_zamowien=liczba_zamowien,
            klienci=liczba_klientow,
            pracownicy=liczba_pracownikow,
            nowe=False
        )
        df_poz = generowanie_pozycje_zamowienie(
            zamowienia=liczba_zamowien,
            produkty=df_prod,
            max_id_zamowienia=0,
        )
        df_kli = generowanie_klientow(
            liczba_klientow=liczba_klientow,
            pracownicy=liczba_pracownikow
        )
        df_pra = generowanie_pracownikow(liczba=liczba_pracownikow)

        df_prod.to_csv(plik_produkty, index=False, encoding="utf-8-sig")
        df_zam.to_csv(plik_zamowienia, index=False, encoding="utf-8-sig")
        df_poz.to_csv(plik_pozycje, index=False, encoding="utf-8-sig")
        df_kli.to_csv(plik_klienci, index=False, encoding="utf-8-sig")
        df_pra.to_csv(plik_pracownicy, index=False, encoding="utf-8-sig")

        print("Baza początkowa (CSV)")

        if tryb_testowy:
            end = time.perf_counter()
            czas = round(end-start, 4)
            print(czas)

    else:
        print("Pliki istnieją, generowanie nowych danych...")

        df_prod = pd.read_csv(plik_produkty)
        df_pra = pd.read_csv(plik_pracownicy)
        df_kli = pd.read_csv(plik_klienci)
        df_zam = pd.read_csv(plik_zamowienia)
        df_poz = pd.read_csv(plik_pozycje)

        df_zam["ID"] = pd.to_numeric(df_zam["ID"], errors="coerce").astype("Int64")
        df_kli["ID"] = pd.to_numeric(df_kli["ID"], errors="coerce").astype("Int64")

        max_id_zam = df_zam["ID"].max() if not df_zam.empty else 0
        max_id_kli = df_kli["ID"].max() if not df_kli.empty else 0

        df_zam = aktualizuj_zamowienia(df_zam, praw_zwrotu=0.045)

        liczba_nowych_klientow = random.randint(1,5)
        print("Klienci")
        df_kli_new = generowanie_klientow(
            liczba_klientow=liczba_nowych_klientow,
            pracownicy=len(df_pra),
            max_id=max_id_kli
        )

        liczba_nowych_zamowien = random.randint(1, 20)
        print("Zamówienia")
        df_zam_new = generowanie_zamowien(
            liczba_zamowien=liczba_nowych_zamowien,
            klienci=len(df_kli) + len(df_kli_new),
            pracownicy=len(df_pra),
            max_id=max_id_zam, 
            nowe = True
        )

        print("Pozycje zamówienia")
        df_poz_new = generowanie_pozycje_zamowienie(
            zamowienia=liczba_nowych_zamowien,
            produkty=df_prod,
            max_id_zamowienia=max_id_zam,
            max_id_pozycji=df_poz['ID_Pozycja'].max() if not df_poz.empty else 0
        )

        df_kli_updated = pd.concat([df_kli, df_kli_new], ignore_index=True)
        df_zam_updated = pd.concat([df_zam, df_zam_new], ignore_index=True)
        df_poz_updated = pd.concat([df_poz, df_poz_new], ignore_index=True)

        df_kli_updated.to_csv(plik_klienci, index=False, encoding="utf-8-sig")
        df_zam_updated.to_csv(plik_zamowienia, index=False, encoding="utf-8-sig")
        df_poz_updated.to_csv(plik_pozycje, index=False, encoding="utf-8-sig")

        df_prod.to_csv(plik_produkty, index=False, encoding="utf-8-sig")
        df_pra.to_csv(plik_pracownicy, index=False, encoding="utf-8-sig")

        print(f"Dopisano: {len(df_zam_new)} zamówień, {len(df_poz_new)} pozycji, {len(df_kli_new)} klientów.")
