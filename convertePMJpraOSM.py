#!/usr/bin/env python

import numpy
import unicodedata
import re
import sys, getopt

import fuzzywuzzy.process as fuzzy

# local
from pmj_osm_utils import *

import xml.etree.ElementTree as etree

class PMJConverter:
    suburb = ''
    street = ''
    mismatchCount = 0
    knownMatches = {}

    def main(self, argv):
        inputfile = ''
        outputfile = ''

        try:
            opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        except getopt.GetoptError:
            print('-i <inputfile> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('-i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg

        self.suburb = numpy.load('osmSuburbJlle.npy').item()
        self.street = numpy.load('osmStreetJlle.npy').item()

        tree = etree.parse(inputfile)
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'way':
                self.processWay(elem)

        print('Mismatch count: ' + str(self.mismatchCount))

        if self.mismatchCount == 0:
            tree.write(outputfile,encoding="UTF-8",xml_declaration=True)


    def processWay(self, way):
        elemsToRemove = []
        for elem in way:
            if elem.tag == 'tag':
                if not self.processWayTag(elem):
                    elemsToRemove.append(elem)

        for elem in elemsToRemove:
            way.remove(elem)

    def processWayTag(self, tag):
        if tag.attrib['k'] == 'bairro':
            self.processBairro(tag)
            return True
        elif tag.attrib['k'] == 'endereco':
            self.processEndereco(tag)
            return True
        elif tag.attrib['k'] == 'numero':
            self.processNumero(tag)
            return True
        else:
            return False

    def processBairro(self, tag):
        tag.attrib['k'] = 'addr:suburb'
        if tag.attrib['v'] in self.suburb.keys():
            tag.attrib['v'] = self.suburb[tag.attrib['v']]
        else:
            print("Nao achou bairro: " + tag.attrib['v'])

    def processEndereco(self, tag):
        tag.attrib['k'] = 'addr:street'

        if tag.attrib['v'] in self.knownMatches:
            tag.attrib['v'] = self.knownMatches[tag.attrib['v']]
        else:
            endereco = simplifyAddress(tag.attrib['v'])

            chosenKeyAndScore = fuzzy.extractOne(endereco, self.street.keys())

            if (chosenKeyAndScore[1] < 90):
                chosenKeyAndScore = self.tryOtherAddressPrefixes(endereco, chosenKeyAndScore)

            osmStreet = self.street[chosenKeyAndScore[0]]

            if (chosenKeyAndScore[1] < 100):
                print(endereco + ' -> ' + osmStreet + ' (' + str(chosenKeyAndScore[1]) + ')')

            if (chosenKeyAndScore[1] < 90):
                self.mismatchCount += 1

            self.knownMatches[tag.attrib['v']] = osmStreet
            tag.attrib['v'] = osmStreet

    # Tenta com outros prefixos (eg: na PMJ pode estar "RUA FOO" e no OSM "SERVIDAO FOO")
    def tryOtherAddressPrefixes(self, endereco, chosenKeyAndScore):
            chosenKeyAndScore = self.tryOtherAddressPrefixes_helper(endereco, chosenKeyAndScore, "RUA")
            chosenKeyAndScore = self.tryOtherAddressPrefixes_helper(endereco, chosenKeyAndScore, "AVENIDA")
            chosenKeyAndScore = self.tryOtherAddressPrefixes_helper(endereco, chosenKeyAndScore, "SERVIDAO")
            chosenKeyAndScore = self.tryOtherAddressPrefixes_helper(endereco, chosenKeyAndScore, "ALAMEDA")
            return chosenKeyAndScore

    def tryOtherAddressPrefixes_helper(self, endereco, chosenKeyAndScore, prefix):
        enderecoAlt = re.sub(r"^(RUA|AVENIDA|SERVIDAO|ALAMEDA) ", prefix + " ", endereco)
        altKeyAndScore = fuzzy.extractOne(enderecoAlt, self.street.keys())
        if altKeyAndScore[1] > chosenKeyAndScore[1]:
            return altKeyAndScore
        else:
            return chosenKeyAndScore


    def processNumero(self, tag):
        tag.attrib['k'] = 'addr:housenumber'

if __name__ == "__main__":
    pmjConverter = PMJConverter()
    pmjConverter.main(sys.argv[1:])

