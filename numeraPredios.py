#!/usr/bin/env python

import sys, getopt
import xml.etree.ElementTree as etree
from shapely.geometry import Polygon

class Node:
    id = ''
    lat = ''
    lon = ''

    def __init__(self, elem):
        self.id = elem.attrib['id']
        self.lat = elem.attrib['lat']
        self.lon = elem.attrib['lon']

    def __str__(self):
        return "Node(lat=" + self.lat + " lon=" + self.lon + ")"
        return "<node id='"+self.id+"' visible='true' lat='"+self.lat+"' lon='"+self.lon+"' />"

    def __repr__(self):
        return "Node(lat=" + self.lat + " lon=" + self.lon + ")"

class Way:
    id = ''
    nodes = []

    def __init__(self, wayElem):
        self.id = wayElem.attrib['id']
        for elem in wayElem:
            if elem.tag == 'nd':
                self.nodes.append(elem.attrib['ref'])

    def __repr__(self):
        return "Way(nodes=" + str(self.nodes) + ")"


class NumeraPredios:
    nodesEdf = {}
    waysEdf = []
    polygonsEdf = []

    def run(self, argv):
        lotesFile = ''
        edificacoesFile = ''

        try:
            opts, args = getopt.getopt(argv,"hl:e:",["lotes=","edificacoes="])
        except getopt.GetoptError:
            print('-l <lotes.osm> -e <edificacoes.osm>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('-l <lotes.osm> -e <edificacoes.osm>')
                sys.exit()
            elif opt in ("-l", "--lotes"):
                lotesFile = arg
            elif opt in ("-e", "--edificacoes"):
                edificacoesFile = arg

        self.processaEdificacoes(etree.parse(edificacoesFile).getroot())
        self.buildPolygons()

        for poly in self.polygonsEdf:
            print(str(poly))

    def processaEdificacoes(self, root):
        for elem in root:
            if elem.tag == 'node':
                self.nodesEdf[elem.attrib['id']] = Node(elem)
            if elem.tag == 'way':
                self.waysEdf.append(Way(elem))

    def buildPolygons(self):
        for wayEdf in self.waysEdf:
            ext = []
            for nodeId in wayEdf.nodes:
                node = self.nodesEdf[nodeId]
                ext.append((float(node.lat),float(node.lon)))

            self.polygonsEdf.append(Polygon(ext))

if __name__ == "__main__":
    numeraPredios = NumeraPredios()
    numeraPredios.run(sys.argv[1:])
