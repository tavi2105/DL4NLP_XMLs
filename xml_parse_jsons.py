import csv
import glob
import json
import os
from lxml import etree


folder_path = '.\\resources\\DL_XMLs'
fields_sent = []
fields = []
tags = []
entry_sent = {
    "tokens": [],
    "labels": []
}
entry = {
    "tokens": [],
    "labels": []
}
for filename in glob.glob(os.path.join(folder_path, '*.xml')):
    with open(filename, 'r', encoding="utf8") as f:
        testXML = f.read()

        root = etree.fromstring(testXML)
        for element in root.iter():
            if str(element.tag) == "entry":
                fields_sent.append(entry_sent)
                entry_sent = {
                            "tokens": [],
                            "labels": []
                        }
                fields.append(entry)
                entry = {
                            "tokens": [],
                            "labels": []
                        }
            if str(element.text).strip() and str(element.text) != 'None' and "cyfunction Comment" not in str(element.tag):
                for word in str(element.text).strip().split(" "):
                    entry["tokens"].append(word)
                    entry["labels"].append(element.tag)
                entry_sent["tokens"].append(element.text)
                entry_sent["labels"].append(element.tag)


with open("dataset/dataset.json", "w") as outfile:
    json_object = json.dumps(fields, indent=4)
    outfile.write(json_object)

with open("dataset/dataset_sentence.json", "w") as outfile:
    json_object = json.dumps(fields_sent, indent=4)
    outfile.write(json_object)

