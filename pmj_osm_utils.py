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
    address = address.replace('RUA TRAVESSA','TRAVESSA')
    address = address.replace('RUA MARQUES DE OLINDA', 'AVENIDA MARQUES DE OLINDA')

    return address

def simplifyAddress(address):
    address = stripAccents(address.upper())
    address = removeIrrelevantWords(address)
    return address

class Node:
    def __init__(self, elem):
        self.id = int(elem.attrib['id'])
        self.lat = elem.attrib['lat']
        self.lon = elem.attrib['lon']

    def __str__(self):
        return "<node id='"+str(self.id)+"' visible='true' lat='"+self.lat+"' lon='"+self.lon+"' />"

    def __repr__(self):
        return "Node(lat=" + self.lat + " lon=" + self.lon + ")"

class Way:
    def __init__(self, wayElem):
        self.nodes = []
        self.tags = []
        self.id = int(wayElem.attrib['id'])
        for elem in wayElem:
            if elem.tag == 'nd':
                self.nodes.append(int(elem.attrib['ref']))
            elif elem.tag == 'tag':
                self.tags.append(elem)

    def __repr__(self):
        return "Way(nodes=" + str(self.nodes) + ")"

    def containsAddress(self):
        hasStreet = False
        hasNumber = False
        for tag in self.tags:
            if tag.attrib['k'] == 'addr:housenumber':
                hasNumber = True
            elif tag.attrib['k'] == 'addr:street':
                hasStreet = True
        return hasStreet and hasNumber
