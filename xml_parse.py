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


with open('dataset/dataset.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["word", "tag"])
    for field in fields:
        for word in field[0].split(" "):
            writer.writerow([word, field[1]])


with open('dataset/dataset_sentence.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["word", "tag"])
    for field in fields:
        writer.writerow([field[0], field[1]])

with open('dataset/all_tags.txt', 'w', encoding='UTF8', newline='') as f:
    f.write(",".join(str(item) for item in set(tags)))


dict_words = {
    "tokens": [],
    "labels": []
}
dict_sent = {
    "tokens": [],
    "labels": []
}
for field in fields:
    dict_sent["tokens"].append(field[0])
    dict_sent["labels"].append(field[1])
    for word in field[0].split(" "):
        dict_words["tokens"].append(word)
        dict_words["labels"].append(field[1])

with open("dataset/dataset.json", "w") as outfile:
    json_object = json.dumps(dict_words, indent=4)
    outfile.write(json_object)

with open("dataset/dataset_sentence.json", "w") as outfile:
    json_object = json.dumps(dict_sent, indent=4)
    outfile.write(json_object)

