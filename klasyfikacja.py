#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
from collections import Counter

def najczesciejWyst(lista):
    return max(set(lista), key=lista.count)

def metrykaEuklidesowa(A, B, indeksy):
      suma = 0
      for i in indeksy:
         suma += pow(A[i] - B[i],2)
      suma = sqrt(suma)
      return suma

def KNN(dane, K, wiersz_do_klas, kol_decyz, indeksy, metryka=metrykaEuklidesowa):
    osobnik = dane[wiersz_do_klas]
    #nie osobnik a cos innego, np ostatni zakup
    odleglosci = []
    for w_idx in range(len(dane)):
        if w_idx != wiersz_do_klas:
            odl = metryka(osobnik, dane[w_idx], indeksy)
            # Przypisujemy indeks i odleglosc
            odleglosci.append((w_idx, odl))
    odleglosci.sort(key=lambda x:x[1])
    wybrane_k_decyzji = [dane[m][kol_decyz] for m in [o[0] for o in odleglosci[:K]]]
    juz_kupione = [rekord[kol_decyz] for rekord in dane if rekord[0]==osobnik[0]]

    wybrane_nie_kupione = list(wybrane_k_decyzji)
    for przedmiot in juz_kupione:
        # po kolei filtrujemy liste z przedmiotow juz zakupionych
        wybrane_nie_kupione = filter(lambda a: a!=przedmiot, wybrane_nie_kupione)

    # Counter zamienia liste ['a','a','a','b','b','c','a'] na {'a':4,'b':2,'c':1} (czyli licznosci w zbiorze)
    # Counter.most_common() zwraca listę [('a',4), ('b',2), ('c',1)] w kolejnosci licznosci wystepowan
    return Counter(wybrane_nie_kupione).most_common()
    #print potencjale_do_zakupu
    #return potencjale_do_zakupu
    #return najczesciejWyst(wybrane_k_decyzji)
