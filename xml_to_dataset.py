import glob
import os
import re

tag_groups = [
    'orth',
    'gramGrp',
    'MorfDef',
    'usg',
    'RegDef',
    'quote',
    'abbr',
    'hi',
    'usg'
]

folder_path = '.\\resources\\DL_XMLs'
fields = []
for filename in glob.glob(os.path.join(folder_path, '*.xml')):
    with open(filename, 'r', encoding="utf8") as f:
        testXML = f.read()

        for tag in tag_groups:
            fieldsArray = re.findall("<" + tag + "(.)*?>((.|\n)+?)</" + tag + ">", testXML)
            for entry in fieldsArray:
                fields.append([re.sub(r"<[a-zA-Z1-9]+(.)*?>((.|\n)*?)</[a-zA-Z1-9]+>", "", entry[1]), tag])

print(fields)
