#!/usr/bin/env python

import sys, getopt
import xml.etree.ElementTree as etree
from shapely.geometry import Polygon
from rtree import index
from pmj_osm_utils import Node, Way

class NumeraPredios:
    def __init__(self):
        self.nodesEdf = {}
        self.waysEdf = {}
        self.polygonsEdf = {}
        self.idxEdf = index.Index()

        self.nodesLotes = {}
        self.waysLotes = {}
        self.polygonsLotes = {}

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

        for poly in list(self.polygonsEdf.values()):
            self.idxEdf.insert(poly.id, poly.bounds)

        self.processaLotes(etree.parse(lotesFile).getroot())
        self.buildPolygons(self.nodesLotes, self.waysLotes, self.polygonsLotes)

        for polyLote in list(self.polygonsLotes.values):
            intersection = self.idxEdf.intersection(polyLote.bounds)
            for edfId in list(intersection):



    def processaEdificacoes(self, root):
        for elem in root:
            if elem.tag == 'node':
                self.nodesEdf[int(elem.attrib['id'])] = Node(elem)
            if elem.tag == 'way':
                self.waysEdf[int(elem.attrib['id'])] = Way(elem)

    def buildPolygons(self, nodesDict, waysDict, polyDict):
        waysList = list(waysDict.values())
        for way in waysList:
            ext = []
            for nodeId in way.nodes:
                node = nodesDict[int(nodeId)]
                ext.append((float(node.lat),float(node.lon)))

            poly = Polygon(ext)
            poly.id = way.id

            polyDict[way.id] = poly

    def processaLotes(self, root):
        for elem in root:
            if elem.tag == 'node':
                self.nodesLotes[int(elem.attrib['id'])] = Node(elem)
            if elem.tag == 'way':
                self.waysLotes[int(elem.attrib['id'])] = Way(elem)

if __name__ == "__main__":
    numeraPredios = NumeraPredios()
    numeraPredios.run(sys.argv[1:])
