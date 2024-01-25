import glob
import os
import re

folder_path = '.\\resources\\results\\'

for filename in glob.glob(os.path.join(folder_path, '*.html')):
    with open(filename, 'r', encoding="utf8") as f:
        content = f.readlines()

    f_write = open("results\\" + filename.split("\\")[-1], "a", encoding="utf8")

    for line in content:
        # print(line)
        reg = re.findall('>(.*?)<', line)
        reg2 = re.findall('<span', line)
        reg3 = re.findall('</span', line)
        if len(reg) > 0 and reg[0] != '':
            f_write.write(reg[0] + " ")
        elif len(reg2) > 0 or len(reg3) > 0:
            pass
        else:
            f_write.write(line)

    f_write.close()
