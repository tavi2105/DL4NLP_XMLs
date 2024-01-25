from bs4 import BeautifulSoup
import glob
import os
import numpy as np

folder_path = '.\\results\\'
for filename in glob.glob(os.path.join(folder_path, '*.html')):
    with open(filename, 'r', encoding="utf8") as f:
        html = f.read()

    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    f_write = open("final_results\\" + filename.split("\\")[-1].split('.')[0] + ".txt", "a", encoding="utf8")

    groups = ""
    for data in soup.find_all("p"):
        line = data.get_text()[1:]
        first_word = line.split(" ")[0][:-1]
        if first_word.isupper() and first_word[0].isalpha():
            groups = groups + "| NEW_GROUP |"

        groups = groups + line

    string_arr = str(np.array(groups.split("| NEW_GROUP |")))
    f_write.write(string_arr)

    f_write.close()






