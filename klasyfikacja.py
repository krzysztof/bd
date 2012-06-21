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

def KNN(dane, K, transakcja, kol_decyz, indeksy, metryka=metrykaEuklidesowa):
    odleglosci = []
    for w_idx in range(len(dane)):
        # rozpatrujemy tylko transakcje o roznych produktach niz ten klasyfikowany
        # i pomijamy transakcje danego klienta
        if transakcja[kol_decyz] != dane[w_idx][kol_decyz] and transakcja[0]!=dane[w_idx][0]:
            odl = metryka(transakcja, dane[w_idx], indeksy)
            odleglosci.append((w_idx, odl))
    odleglosci.sort(key=lambda x:x[1])
    wybrane_k_decyzji = [dane[m][kol_decyz] for m in [o[0] for o in odleglosci[:K]]]
    juz_kupione = [rekord[kol_decyz] for rekord in dane if rekord[0]==transakcja[0]]

    wybrane_nie_kupione = list(wybrane_k_decyzji)
    for przedmiot in juz_kupione:
        # po kolei filtrujemy liste z przedmiotow juz zakupionych
        wybrane_nie_kupione = filter(lambda a: a!=przedmiot, wybrane_nie_kupione)

    # obiekt Counter zamienia liste ['a','a','a','b','b','c','a'] na {'a':4,'b':2,'c':1} (czyli licznosci w zbiorze)
    return Counter(wybrane_nie_kupione)
