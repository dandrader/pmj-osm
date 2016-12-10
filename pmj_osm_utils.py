#!/usr/bin/env python

import unicodedata

def stripAccents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def removeIrrelevantWords(address):
    address = address.replace('SERVIDAO','')
    address = address.replace('RUA','')
    address = address.replace('AVENIDA','')
    address = address.replace('TRAVESSA','')
    address = address.replace(' DA ',' ')
    address = address.replace(' DO ',' ')
    address = address.replace(' DAS ',' ')
    address = address.replace(' DOS ',' ')
    address = address.replace(' DE ',' ')
    address = address.strip()
    return address
