#!/usr/bin/env python

import numpy
import unicodedata
import sys, getopt

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def main(argv):
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

    print('Input file is', inputfile)
    print('Output file is', outputfile)

    nomesRuas = open(inputfile, 'r').read().splitlines()
    nomesRuas = list(set(nomesRuas))

    osmStreetName = dict()

    for line in nomesRuas:
        line = line.rstrip()
        primitiveName = strip_accents(line.upper())
        osmStreetName[primitiveName] = line

    for key, value in osmStreetName.items():
        print(key + " -> " + value)

    numpy.save(outputfile, osmStreetName)

if __name__ == "__main__":
    main(sys.argv[1:])
