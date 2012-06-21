#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def daj_polaczenie(host='localhost', user='root', password='', baza='bazy'):
    conn = MySQLdb.connect(host, user, password, baza)
    return conn

def pobierz_dane():
    conn = daj_polaczenie()
    c = conn.cursor()
    c.execute("SELECT c.customerNumber, c.creditLimit, p.productCode, p.productLine, p.productScale, p.productVendor, p.buyPrice \
                FROM Customers c, Orders o, OrderDetails d, Products p\
                where c.customerNumber = o.customerNumber and o.orderNumber = d.orderNumber and p.productCode = d.productCode")
    dane = []
    for line in c.fetchall():
        dane.append(list(line))
    return dane

def pobierz_klientow():
    conn = daj_polaczenie()
    c = conn.cursor()
    c.execute("SELECT customerNumber from Customers")
    return [k[0] for k in c.fetchall()]



def pobierz_ostatnie_k_zakupow(K, klient_id):
    """
    Funkcja zwracajaca ostatnie K zakupow od klienta o customerNumber==klient_id
    """
    # dokladnie taka sama kolejnosc danych, ale:
    # 1. Tylko dla customerNumber == klient_id
    # 2. K najnowszych rekordow wzgledem daty o.orderDate
    conn = daj_polaczenie()
    c = conn.cursor()

    c.execute("SELECT c.customerNumber, c.creditLimit, p.productCode, p.productLine, p.productScale, p.productVendor, p.buyPrice \
              FROM Customers c, Orders o, OrderDetails d, Products p WHERE c.customerNumber = %s\
              and c.customerNumber = o.customerNumber and o.orderNumber = d.orderNumber and p.productCode = d.productCode\
              order by o.orderDate DESC" % (klient_id))

    dane = []
    for line in c.fetchall():
        dane.append(list(line))
    return dane[:K]

def pobierz_info_produktu(produkt_id):
    """
    Zwraca informacje o produkcie dla celow wyświetlania.
    """

    conn = daj_polaczenie()
    c = conn.cursor()

    c.execute("SELECT p.productCode, p.productLine, p.productScale, p.productVendor,p.productDescription, p.buyPrice \
              FROM Products p WHERE p.productCode = '%s'" % (produkt_id))

    return c.fetchall()[0]

