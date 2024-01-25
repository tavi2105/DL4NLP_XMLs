import csv
import glob
import json
import os
from lxml import etree


folder_path = '.\\resources\\DL_XMLs'
fields = []
tags = []

for filename in glob.glob(os.path.join(folder_path, '*.xml')):
    with open(filename, 'r', encoding="utf8") as f:
        testXML = f.read()

        root = etree.fromstring(testXML)
        for element in root.iter():
            if str(element.text).strip() and str(element.text) != 'None' and "cyfunction Comment" not in str(element.tag):
                fields.append([str(element.text).strip(), element.tag])
                tags.append(element.tag)

