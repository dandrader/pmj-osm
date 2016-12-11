#!/usr/bin/env python

import numpy
import unicodedata
import re
import sys, getopt

# local
from pmj_osm_utils import *

import xml.etree.ElementTree as etree

class PMJConverter:
    suburb = ''
    street = ''
    mismatchCount = 0

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
        for elem in way:
            if elem.tag == 'tag':
                self.processWayTag(elem)

    def processWayTag(self, tag):
        if tag.attrib['k'] == 'bairro':
            self.processBairro(tag)
        elif tag.attrib['k'] == 'endereco':
            self.processEndereco(tag)
        elif tag.attrib['k'] == 'numero':
            self.processNumero(tag)

    def processBairro(self, tag):
        tag.attrib['k'] = 'addr:suburb'
        if tag.attrib['v'] in self.suburb.keys():
            tag.attrib['v'] = self.suburb[tag.attrib['v']]
        else:
            print("Nao achou bairro: " + tag.attrib['v'])

    def processEndereco(self, tag):
        tag.attrib['k'] = 'addr:street'

        endereco = stripAccents(tag.attrib['v'])
        endereco = removeIrrelevantWords(endereco)

        words = endereco.split()
        candidateKeys = self.street.keys()

        for word in words:
            # ignora abreviacao por enquanto
            if '.' in word:
                continue

            newCandidateKeys = []
            for key in candidateKeys:
                if word in key.split():
                    newCandidateKeys.append(key)
            candidateKeys = newCandidateKeys

        if len(candidateKeys) == 1:
            tag.attrib['v'] = self.street[candidateKeys[0]]
        else:
            # tenta comparacao exata
            if len(candidateKeys) > 1 and endereco in candidateKeys:
                tag.attrib['v'] = self.street[endereco]
            else:
                print("Não achou rua: " + tag.attrib['v'] + '. candidateKeys = ' + str(candidateKeys) + ', words = ' + str(words))
                self.mismatchCount += 1


    def processNumero(self, tag):
        tag.attrib['k'] = 'addr:housenumber'

if __name__ == "__main__":
    pmjConverter = PMJConverter()
    pmjConverter.main(sys.argv[1:])

