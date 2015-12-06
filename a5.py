import re
import os
import zipfile

import re
import os
import zipfile
import smtplib
import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# TODO send email.
commonRegex = "[_a-zA-Z][_a-zA-z0-9]*"
lispRegex = "[-*+/a-zA-Z_][-a-zA-Z0-9_]*"

def getType(collection):
    return str(collection[0][0])

def makeMatchFile(matchlist):
    type = getType(list(matchlist))
    filename = type.lower() + "_identifiers.txt"
    f = open(filename, 'w')
    for line in matchlist:
        f.write(str(line) + "\n")
    return filename

def getRegex(fileName, pattern):
    extension = fileName.split('.')[1]
    filetype = ""
    if(extension == "cpp"):
        filetype = "C++"
    elif(extension == "lisp"):
        filetype = "Lisp"
    elif(extension == "txt"):
        filetype = "Prolog"
    elif(extension == "scala"):
        filetype = "Scala"
    elif(extension == "py"):
        filetype = "Python"

    allFound = set([])
    f = open(fileName, 'r')
    for line in f:
        identifiers = re.findall(pattern, line)
        if len(identifiers) != 0:
            for id in identifiers:
                allFound.add((filetype, id))
    f.close()
    return allFound

cppMatches = getRegex("a1.cpp", commonRegex)
lispMatches = getRegex("a2.lisp", lispRegex)
scalaMatches = getRegex("a3.scala", commonRegex)
prologMatches = getRegex("a4.txt", commonRegex)
pythonMatches = getRegex("a5.py", commonRegex)

scalaFile = makeMatchFile(scalaMatches)
lispFile = makeMatchFile(lispMatches)
cppFile = makeMatchFile(cppMatches)
prologFile = makeMatchFile(prologMatches)
pythonFile = makeMatchFile(pythonMatches)

def generatehtml():
    filename = "index.html"
    html = open(filename, "w")
    html.write("<!DOCTYPE html>\n")
    html.write("<html>\n")
    html.write("<title>Rafael Torres Programming Language Assignments</title>\n")
    html.write("""<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>\n""")
    html.write("""<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/js/materialize.min.js"></script>\n""")
    html.write("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/css/materialize.min.css\n">""")
    html.write("</head>\n")
    html.write("""<p><a href="a1.cpp">C++ Assignment</a><p>\n""")
    html.write("""<p><a href="a2.lisp">Lisp Assignment</a><p>\n""")
    html.write("""<p><a href="a3.scala">Scala Assignment</a><p>\n""")
    html.write("""<p><a href="a4.txt">Prolog Assignment</a><p>\n""")
    html.write("""<p><a href="a5.py">Python Assignment</a><p>\n""")
    html.write("</html>")

generatehtml()
# # open file
# f = open('a2.lisp', 'r')
# lisp = "^[a-zA-Z]+$"
# for line in f:
#     if ';' not in line:
#         for w in line.split(" "):
#             found = w.replace("(", "").replace(")", "")
#             filtered = re.search(lisp, found)
#             if filtered:
#                 if str(filtered) not in allFound:
#                     allFound.add(str(filtered.group()))
# # print(allFound)
# f.close()

# C++ Parse



