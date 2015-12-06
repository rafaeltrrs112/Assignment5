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

sourceFolder = "csc344"

myMail = "rtorres3@cs.oswego.edu"
dlEmail = ""

subject = "Rafael Torres Programming Language Assignments"

body = """ Hello Professor Lea,

            This is the final assignment email for CSC-344.
            Thank you for this semester. You said it'd be rough, you weren't kidding."""

passw = getpass.getpass("Enter password asap:")

def getType(collection):
    return str(collection[0][0])

def makeMatchFile(matchlist):
    type = getType(list(matchlist))
    filename = type.lower() + "_identifiers.txt"
    f = open(sourceFolder + '/' + filename, 'w')
    for line in matchlist:
        f.write(str(line) + "\n")
    return filename

def createZipFile():
    archive = zipfile.ZipFile("csc344/archive.zip", "w", zipfile.ZIP_DEFLATED)

    archive.write("csc344/a1.cpp")
    archive.write("csc344/a2.lisp")
    archive.write("csc344/a3.scala")
    archive.write("csc344/a4.txt")
    archive.write("csc344/a5.py")

    archive.close()
    return "archive.zip"


# Generates and sends an email to DL's address.
def generateEmail(zippedFile):
    mailHeader = MIMEMultipart()
    mailHeader['From'] = myMail
    mailHeader['to'] = dlEmail

    mailHeader['subject'] = subject

    mailBody = MIMEText(body)

    zip = MIMEBase("all_assignments", "zip")
    zipFile = open("csc344/" + zippedFile, "rb")

    zip.set_payload(zipFile.read())
    encoders.encode_base64(zip)
    zip.add_header('Context-Disposition', "Attachment; filename= " + zippedFile)

    mailHeader.attach(mailBody)
    mailHeader.attach(zip)

    mailServer = smtplib.SMTP("smtp.gmail.com:587")
    mailServer.starttls()
    mailServer.login(myMail, passw)
    mailServer.sendmail(myMail, dlEmail, mailHeader.as_string())
    mailServer.quit()

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
    f = open(sourceFolder + '/' + fileName, 'r')
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
    html.write("""<p><a href="a1.cpp">C++ Assignment</a></p>\n""")
    html.write("""<p><a href="c++_identifiers.txt">C++ Identifiers</a></p>\n""")
    html.write("""<p><a href="a2.lisp">Lisp Assignment</a></p>\n""")
    html.write("""<p><a href="lisp_identifiers.txt">Lisp Identifiers</a></p>\n""")
    html.write("""<p><a href="a3.scala">Scala Assignment</a></p>\n""")
    html.write("""<p><a href="scala_identifiers.txt">Scala Identifiers</a></p>\n""")
    html.write("""<p><a href="a4.txt">Prolog Assignment</a></p>\n""")
    html.write("""<p><a href="prolog_identifiers.txt">Prolog Identifiers</a></p>\n""")
    html.write("""<p><a href="a5.py">Python Assignment</a></p>\n""")
    html.write("""<p><a href="python_identifiers.txt">Python Identifiers</a></p>\n""")
    html.write("</html>")
    html.close()

generatehtml()
createZipFile()
# # open file
# f = open('a2.lis
# p', 'r')
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



