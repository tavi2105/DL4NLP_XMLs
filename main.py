import glob
import os

folder_path = '.\\resources\\results\\'

for filename in glob.glob(os.path.join(folder_path, '*.html')):
    with open(filename, 'r', encoding="utf8") as f:
        content = f.readlines()

    f_write = open("results\\" + filename.split("\\")[-1], "a", encoding="utf8")

    DIV = False
    P = False
    SPAN = False
    SPAN2 = False
    buff = ""
    for line in content:
        while line[0] == ' ':
            line = line[1:]

        if DIV and P and SPAN and line[:6] == "<span ":
            buff = buff + line
            SPAN2 = True
            # elif DIV and P and SPAN and SPAN2:
            f_write.write("<hr>\n")
            f_write.write(buff)
            buff = ""
            DIV = False
            P = False
            SPAN = False
            SPAN2 = False
        elif DIV and P and not SPAN and line[:6] == "<span ":
            buff = buff + line
            SPAN = True
        elif DIV and P and not SPAN and line[:3] == "<p ":
            buff = buff + line
            P = True
        elif line[:5] == "<div ":
            buff = buff + line
            DIV = True
        else:
            f_write.write(buff)
            f_write.write(line)
            buff = ""
            DIV = False
            P = False
            SPAN = False
            SPAN2 = False

    f_write.close()
