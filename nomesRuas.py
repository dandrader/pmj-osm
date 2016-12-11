#!/usr/bin/env python

import numpy
import unicodedata
import sys, getopt

# local
from pmj_osm_utils import *

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

        if line in osmStreetName.values():
            continue

        primitiveName = simplifyAddress(line)

        if primitiveName in osmStreetName.keys():
            print(primitiveName + ' ja existe! ' + line)
            exit()

        osmStreetName[primitiveName] = line
        print(primitiveName + ' ' + line)

        oldName = primitiveName

        primitiveName = primitiveName.replace('’','')
        primitiveName = primitiveName.replace('-',' ')

        if oldName != primitiveName and primitiveName in osmStreetName.keys():
            print(primitiveName + ' ja existe! ' + line)
            exit()

        if oldName != primitiveName:
            osmStreetName[primitiveName] = line
            print(primitiveName)
            print(primitiveName + ' ' + line)

    for key, value in osmStreetName.items():
        print(key + " -> " + value)

    numpy.save(outputfile, osmStreetName)

if __name__ == "__main__":
    main(sys.argv[1:])
