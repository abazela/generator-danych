import random
import pandas as pd

def generowanie_pozycje_zamowienie(zamowienia, produkty, max_id_zamowienia, max_id_pozycji=0):

    dane = {
        'ID_Pozycja': [],
        'Ilosc_opakowan': [],
        'ID_Produkt': [],
        'ID_Zamowienie': []
    }

    lista_produktow = produkty['ID'].tolist()
    id_pozycji = max_id_pozycji + 1

    for zamowienie in range(max_id_zamowienia + 1, max_id_zamowienia + zamowienia + 1):
        liczba_pozycji = random.randint(2, 10)


        for _ in range(liczba_pozycji):
            dane['ID_Pozycja'].append(id_pozycji)
            id_pozycji += 1
            dane['ID_Produkt'].append(random.choice(lista_produktow))
            dane['Ilosc_opakowan'].append(random.randint(5, 100))
            dane['ID_Zamowienie'].append(zamowienie)



    df =  pd.DataFrame(dane)

#Generowanie błędów

    #Dwa razy ta sama pozycja w jednym zamówieniu + 5%
    zamowienie_z_duplikatem_idx = random.sample(range(max_id_zamowienia + 1, max_id_zamowienia + zamowienia + 1), k=int(zamowienia * 0.05))

    for idx in zamowienie_z_duplikatem_idx:
        pozycje_zamowienia = df[df['ID_Zamowienie'] == idx]['ID_Produkt']

        if len(pozycje_zamowienia) == 0:
            continue

        powtorzony_produkt = random.choice(pozycje_zamowienia.tolist())

        # nowe_id_pozycji = df['ID_Pozycja'].max() + 1
        nowa_pozycja = {
            'ID_Pozycja': id_pozycji,
            'ID_Produkt': powtorzony_produkt,
            'Ilosc_opakowan': random.randint(5, 100),
            'ID_Zamowienie': idx
        }

        df = pd.concat([df, pd.DataFrame([nowa_pozycja])], ignore_index=True)
        id_pozycji += 1

    # ujemna/zerowa ilość produktów - 6%
    bledna_ilosc_idx = random.sample(range(len(df)), k = int(len(df)*0.06))
    for idx in bledna_ilosc_idx:
        df.at[idx, 'Ilosc_opakowan'] = 0


    # #odstająca ilość produktów - 4%
    # odstajaca_ilosc_idx = random.sample(range(len(df)), k = int(len(df)*0.04))
    # for idx in odstajaca_ilosc_idx:
    #     df.at[idx, 'Ilosc_opakowan'] = df.at[idx, 'Ilosc_opakowan'] * random.randint(8, 15)



    return df


