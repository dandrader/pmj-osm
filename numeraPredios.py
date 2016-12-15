#!/usr/bin/env python

import sys, getopt
import xml.etree.ElementTree as etree
from shapely.geometry import Polygon
from rtree import index

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
                self.nodes.append(elem.attrib['ref'])
            elif elem.tag == 'tag':
                self.tags.append(elem)

    def __repr__(self):
        return "Way(nodes=" + str(self.nodes) + ")"


class NumeraPredios:
    def __init__(self):
        self.nodesEdf = {}
        self.waysEdf = {}
        self.polygonsEdf = []
        self.idxEdf = index.Index()

        self.nodesLotes = {}
        self.waysLotes = {}
        self.polygonsLotes = []

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
        self.buildPolygons(self.nodesEdf, self.waysEdf, self.polygonsEdf)

        for poly in self.polygonsEdf:
            self.idxEdf.insert(poly.id, poly.bounds)

        self.processaLotes(etree.parse(lotesFile).getroot())
        self.buildPolygons(self.nodesLotes, self.waysLotes, self.polygonsLotes)


    def processaEdificacoes(self, root):
        for elem in root:
            if elem.tag == 'node':
                self.nodesEdf[int(elem.attrib['id'])] = Node(elem)
            if elem.tag == 'way':
                self.waysEdf[int(elem.attrib['id'])] = Way(elem)

    def buildPolygons(self, nodesDict, waysDict, polyList):
        waysList = list(waysDict.values())
        for way in waysList:
            ext = []
            for nodeId in way.nodes:
                node = nodesDict[int(nodeId)]
                ext.append((float(node.lat),float(node.lon)))

            poly = Polygon(ext)
            poly.id = way.id

            polyList.append(poly)

    def processaLotes(self, root):
        for elem in root:
            if elem.tag == 'node':
                self.nodesLotes[int(elem.attrib['id'])] = Node(elem)
            if elem.tag == 'way':
                self.waysLotes[int(elem.attrib['id'])] = Way(elem)

if __name__ == "__main__":
    numeraPredios = NumeraPredios()
    numeraPredios.run(sys.argv[1:])
