#!/usr/bin/env python
# coding: utf-8

'''
Alexander Winkler
11.6.2021
'''

from lxml import etree
from glob import glob
import json
from PIL import Image
from datetime import datetime
from sys import argv



JSONS = argv[1:]


def parse_json(json_path):
    '''
    Nimmt den JSON-Dateipfad, leitet daraus den Bild-Dateipfad.
    Liest Dimension der Bilddatei aus.
    Extrahiert aus JSON die Koordinaten der Textregion und der Zeilen     
    '''
    with open(json_path, 'r') as IN:
        krak = json.load(IN)
    img = json_path.replace('processing','input').replace('json','png')
    bin_img = json_path.replace('.json','bin.png')
    w,h = get_img_size(img)
    text_region = krak['regions']['text']
    try:
        text_coords = [(x[0],x[1]) for x in text_region[0]]
        text_coords = [",".join(map(str,x)) for x in text_coords]
        text_coords = " ".join(text_coords)
    except Exception as e:
        print(json_path,e)
        text_coords = ""
    lines = []
    for line in krak['lines']:
        coord_points = [(x[0],x[1]) for x in line['boundary']]
        coord_points = [",".join(map(str,x)) for x in coord_points]
        coord_points = " ".join(coord_points)
        lines.append(coord_points)
    return img,w,h,text_coords,lines

def get_img_size(IMG):
    image = Image.open(IMG)
    width, height = image.size
    return width,height

def make_header():
    '''
    Erstellt Root-Element und Header einer PageXML
    '''
    
    nsmap = {None: "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"} # Namespace-Definition noch nicht perfekt, es fehlt bspw die Schema-Location
    root = etree.Element("PcGts", nsmap=nsmap)
    
    # Metadata block
    metadata = etree.SubElement(root,"Metadata")
    creator = etree.SubElement(metadata,"Creator")
    created = etree.SubElement(metadata,"Created")
    created.text = datetime.now().isoformat()
    last_changed = etree.SubElement(metadata, "LastChange")
    last_changed.text = datetime.now().isoformat()
    comments = etree.SubElement(metadata,"Comments")
    
    return root

def make_page(json_path):
    '''
    
    '''
    
    img,w,h,text_region,lines = parse_json(json_path)

    
    root = make_header()
    
    
    # Page block
    page = etree.SubElement(root,"Page",attrib = {
        'imageFilename' : img.split('/')[-1].replace('png','bin.png'),
        'imageHeight' : str(h),
        'imageWidth' : str(w)
    })
    
    # Text Region
    # Die Region-Details sind hier noch fest kodiert. Müsste wohl
    # verallgemeinert werden. Dafür müsste aber parse_json() die
    # Region-Informationen als Liste ausgeben.
    region = etree.SubElement(page,"TextRegion", attrib = {
        'id' : 'r1',
        'orientation' : '0.0',
        'type' : 'paragraph'
    })
    
    reg_coords = etree.SubElement(region,"Coords", attrib = {'points' : text_region})
    
    # Lines
    for n,line in enumerate(lines):
        textline = etree.SubElement(region,"TextLine", attrib = {'id' : "l" + str(n)})
        etree.SubElement(textline,"Coords", attrib = {'points' : line})
        
    return root



for i in JSONS:
    try:
        pagexml = make_page(i)
        with open(i.replace('json','xml'), "w") as OUT:
            print(etree.tostring(pagexml,pretty_print=True,encoding='unicode'),file=OUT)
            print(f"{i} --> ok!!!")
    except  Exception as e:
        print(e,i)
    

