#!/usr/bin/env python

import unicodedata

def stripAccents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def removeIrrelevantWords(address):
    address = address.strip()

    # casos dificeis
    address = address.replace(' QUINZE ',' XV ')
    address = address.replace(' DR ',' DOUTOR ')
    address = address.replace(' DRA ',' DOUTORA ')
    address = address.replace('RUA SERVIDAO','SERVIDAO')
    address = address.replace('RUA ALAMEDA','ALAMEDA')
    address = address.replace('RUA AVENIDA','AVENIDA')
    address = address.replace('RUA MARQUES DE OLINDA', 'AVENIDA MARQUES DE OLINDA')

    return address

def simplifyAddress(address):
    address = stripAccents(address.upper())
    address = removeIrrelevantWords(address)
    return address
