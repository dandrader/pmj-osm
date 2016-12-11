#!/usr/bin/env python

import unicodedata

def stripAccents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def removeIrrelevantWords(address):
    address = address.strip()
    address = address.replace(' QUINZE ',' XV ')
    return address

def simplifyAddress(address):
    address = stripAccents(address.upper())
    address = removeIrrelevantWords(address)
    return address
