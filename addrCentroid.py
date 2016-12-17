#!/usr/bin/env python

import sys, getopt
from shapely.geometry import Polygon
import xml.etree.ElementTree as etree
from pmj_osm_utils import Node, Way

class CentroidAddr:
    def __init__(self, inputFilePath, outputFilePath):
        self.inputNodes = {}
        self.nextAddrNodeId = -1

        self.outputFile = open(outputFilePath, 'w')
        self.outputFile.write("<?xml version='1.0' encoding='UTF-8'?>\n");
        self.outputFile.write("<osm version='0.6'>\n");

        self.processPlots(etree.parse(inputFilePath).getroot())

        self.outputFile.write("</osm>");
        self.outputFile.close()

    def processPlots(self, root):
        for elem in root:
            if elem.tag == 'node':
                self.inputNodes[int(elem.attrib['id'])] = Node(elem)
            if elem.tag == 'way':
                way = Way(elem)
                if way.containsAddress():
                    self.writeCentroidAddress(way)

    def writeCentroidAddress(self, way):
        ext = []
        for nodeId in way.nodes:
            node = self.inputNodes[int(nodeId)]
            ext.append((float(node.lat),float(node.lon)))

        centroid = Polygon(ext).centroid
        self.outputFile.write("  <node id='"+str(self.nextAddrNodeId)+"' visible='true'"
                       + " lat='"+str(centroid.x)+"' lon='"+str(centroid.y)+"'>\n")
        self.nextAddrNodeId -= 1

        for tag in way.tags:
            if tag.attrib['k'] == 'addr:housenumber' or tag.attrib['k'] == 'addr:street' or tag.attrib['k'] == 'addr:suburb':
                self.outputFile.write("    <tag k='"+tag.attrib['k']+"' v='"+tag.attrib['v']+"' />\n")

        self.outputFile.write("  </node>\n")


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print('-i <input.osm> -o <output.osm>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-i <input.osm> -o <output.osm>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputFilePath = arg
        elif opt in ("-o", "--output"):
            outputFilePath = arg

    CentroidAddr(inputFilePath, outputFilePath)
