#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db_dane import pobierz_dane, pobierz_klientow, pobierz_ostatnie_k_zakupow, pobierz_info_produktu
from klasyfikacja import KNN
from string import Template
from collections import Counter

DEBUG = True

def dyskretyzacja(wektor, N):
    whole, rem = len(wektor)/N, len(wektor)%N
    indices = [whole]*N
    for i in range(rem):
        indices[i]+=1

    wektor2 = [[wektor[i],i] for i in range(len(wektor))]
    w_s = sorted(wektor2,key=lambda x:x[0])
    idx = 0
    for i in range(len(indices)):
        for j in range(indices[i]):
            w_s[idx][0]=i
            idx+=1
    return [i[0] for i in sorted(w_s,key=lambda x:x[1])]

def mapowanie(wektor):
    """
    Tworzy tablice mapującą ['ala', 'kot', 'ala', 'pies'] na liczby ( w obie strony )
     { 'ala':0, 'kot':1, 'pies':2,
        0:'ala', 1:'kot', 2:'pies' }
    """
    unikalne = list(set(wektor))
    mapa = dict()
    for i in range(len(unikalne)):
        mapa[i] = unikalne[i]
        mapa[unikalne[i]] = i
    return mapa

def itemizacja(wektor, mapa):
    return [mapa[i] for i in wektor]

def get_column(data, i):
    """
    Zwraca kolumne z macierzy 2D
    i = 2
    [1,2,3,4]
    [4,5,6,7] ->[3,6,0]
    [8,9,0,1]

    """
    return [d[i] for d in data]

def set_column(data, col, i):
    """
    Wstawia w data (Macierz 2D) kolumne col(Macierz 1D) w kolumnie o indeksie i
    col = [0,0,0,0, ...], i = 1
    [1, 2, 3, 4]    [1, 0, 3 ,4]
    [1, 4, 6, 1] -> [1, 0, 6, 1]
       ...             ...
    [3, 1, 5, 6]    [3, 0, 5, 6]
    """
    for r_idx in range(len(data)):
        data[r_idx][i] = col[r_idx]

def przygotuj_dane(dane, kolumny_dyskretyzacji, poziom_dyskretyzacji, kolumny_do_itemizacji):
    """
    Zamienia wartości w zbiorze danych na wartosci dyskretne, lub zitemizowane

    ['ala', 'Portland', 1.33, 3, 5 ] -> [0, 0, 0, 3, 5]
    ['kot', 'Portland', 4.33, 3, 5 ] -> [1, 0, 1, 3, 5]
    ['kot', 'Cleveland', 1.53, 3, 5 ] -> [1, 1, 0, 3, 5]
    """
    for k in kolumny_dyskretyzacji:
        col = get_column(dane,k)
        dyskr = dyskretyzacja(col, poziom_dyskretyzacji)
        set_column(dane, dyskr, k)

    for k in kolumny_do_itemizacji:
        col = get_column(dane,k)
        mapa = mapowanie(col)
        itemiz = itemizacja(col, mapa)
        set_column(dane, itemiz, k)

    return dane

def wykryj_brakujace_dane(dane):
    brakujace_krotki_count = 0
    ilosc_zm = len(dane[0])
    for krotka in dane:
        if len(krotka) != ilosc_zm:
            brakujace_krotki_count += (ilosc_zm - len(krotka))
        else:
            for zmienna in krotka:
                if not zmienna:
                    brakujace_krotki_count += 1
    return brakujace_krotki_count


def wypisz_info_produktu(produkt):
    temp = """    ProductCode: ${code}
    ProductLine: ${line}
    Scale: ${scale}
    Vendor: ${vendor}
    Description: ${description}
    Price: ${price}"""
    return Template(temp).substitute(code=produkt[0],line=produkt[1],scale=produkt[2],
        vendor=produkt[3], description=produkt[4], price=produkt[5])

def wygeneruj_dla_wszystkich(K, M, filename):

    klienci = pobierz_klientow()
    file = open(filename,'w')
    for id_klienta in klienci:
        polecane = [pol[0] for pol in znajdz_polecane_dla_k_ostatnich(K, id_klienta).most_common(M)]
        file.write("Klient %d\n"%id_klienta)
        file.write("Polecane:\n")
        for p in polecane:
            file.write(wypisz_info_produktu(pobierz_info_produktu(p)))
            file.write("\n\n")
    file.close()

def print_menu():
    print "Witaj, wybierz opcje:"
    print "[0] Wyjscie z programu"
    print "[1] Wypisanie klientow z bazy"
    print "[2] Wygenerowanie polecenia dla klienta o podanym id"
    print "[3] Wygenerowanie polecenia dla wszystkich klientow w bazie i zapis do pliku"

def podaj_klientow_size():
    print "Podaj ilosc klientow do wypisania"
    k = raw_input()
    return int(k)

def podaj_k():
    print "Podaj wartosci K - ilosc ostatnich transakcji"
    k = raw_input()
    return int(k)

def podaj_m():
    print "Podaj wartosci M - ilosc propozycji"
    m = raw_input()
    return int(m)

def podaj_id_klienta():
    print "Podaj id_klienta"
    id = raw_input()
    return int(id)

def podaj_nazwe():
    print "Podaj nazwe pliku"
    plik = raw_input()
    return plik

def menu_loop():
    choice = -1
    while(choice != 0):
        print_menu()
        choice = int(raw_input())
        if choice == 0:
            return
        elif choice == 1:
            klient_size = podaj_klientow_size()
            # wypisanie
        elif choice == 2:
            id = podaj_id_klienta()
            K = podaj_k()
            M = podaj_m()


def main():
    """
    Przykladowa krotka to:
    (customerNumber,    creditLimit,    productCode,   productLine,     productScale,   productVendor,      buyPrice)
    (379L,              70700.0,        'S18_2957',    'Vintage Cars', '1:18',          'Min Lin Diecast',  34.35)
    (...)

    Logika biznesowa polega na polecaniu M konkretnych produktów (productCode) dla danego klienta (customerNumber) biorąc
    pod uwagę K jego ostatnich zakupów. Wykorzystuje ona ideę algorytmu klasyfikacji KNN.
    Dla każdej z K ostatnich transakcji wyliczamy polecany produkt (transakcje najbardziej podobną do tej którą rozważamy - z pewnymi wyjątkami).
    Obliczamy sumę mnogościową "Poleceń" i wybieramy M najbardziej polecane produkty.
    """


def znajdz_polecane_dla_k_ostatnich(K, id_klienta):
    dane = pobierz_dane()
    dane = przygotuj_dane(dane, [1,6], 3, [3,4,5])
    k_sasiadow = 20
    kol_decyz = 2
    # indeksy sa to zmienne kolumn brane pod uwagę, w KNN
    # productLine, productScale, productVendor, buyPrice
    indeksy = [3,4,5,6]
    ostatnie = pobierz_ostatnie_k_zakupow(10, id_klienta)
    ostatnie = przygotuj_dane(ostatnie, [1,6], 3, [3,4,5])

    polecenia = Counter()
    for transakcja in ostatnie:
        pol = KNN(dane, k_sasiadow, transakcja, kol_decyz, indeksy)
        polecenia += pol
    return polecenia

#
# TESTY i DEBUG
#
def test_K_ostatnich():
    for id in [125]:
        ostatnie = pobierz_ostatnie_k_zakupow(8, id)
        print len(ostatnie)
        for o in ostatnie:
            print o

def test_KNM():
    dane = pobierz_dane()
    dane = przygotuj_dane(dane, [1,6], 3, [3,4,5])

    ostatnie = pobierz_ostatnie_k_zakupow(1, 141L)
    ostatnie = przygotuj_dane(ostatnie, [1,6], 3, [3,4,5])

    transakcja = ostatnie[0]

    k_sasiadow = 20
    kol_decyz = 2
    indeksy = [3,4,5,6]
    pol = KNN(dane, k_sasiadow, transakcja, kol_decyz, indeksy)
    print pol

def test():
    dane = pobierz_dane()
    for d in dane:
        print d
    #print 'Brakujace krotki:', wykryj_brakujace_dane(dane)

def test_product_info():
    info = pobierz_info_produktu('S24_4258')
    print info

def test2():
    #a = ['ala', 'kot', 'ala', 'abc', 'abc']
    #print itemizacja(a)

    #a = [1.33, 3.66, 0.31, 0.23, 0.677,6.33]
    #print dyskretyzacja(a, 3)

    #a = [[1,2,3],[4,5,6],[8,8,8]]
    #print get_column(a,0)

    #set_column(a, [-1,-2,-3], 1)
    #print a
    pass

def test3():
    dane = pobierz_dane()
    dane = przygotuj_dane(dane, [1,6], 3, [3,4,5])
    for d in dane:
        print d

def test_dla_wszystkich():
    wygeneruj_dla_wszystkich(5,3,'wyniki_all.txt')

def test_wypisz_klientow():
    klienci = pobierz_klientow()
    for k in klienci:
        print k

def test4():
    dane = pobierz_dane()
    dane = przygotuj_dane(dane, [1,6], 3, [3,4,5])
    K = 30
    kol_decyz = 2
    indeksy = [3,4,5,6]

    print KNN(dane, K, wiersz_do_klas, kol_decyz, indeksy)


if __name__ == "__main__":
    #test_KNM()
    #main()
    test_dla_wszystkich()
    #test_product_info()
    #test_wypisz_klientow()
    #test4()
    #test()
    #test_K_ostatnich()

