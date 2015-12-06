import re
import zipfile
import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

commonRegex = "[_a-zA-Z][_a-zA-z0-9]*"
lispRegex = "[-*+/a-zA-Z_][-a-zA-Z0-9_]*"
emailRegex = "[^@]+@[^@]+\.[^@]+"

sourceFolder = "csc344"

myMail = "rtorres3@oswego.edu"

subject = "Rafael Torres Programming Language Assignments"

body = """ Hello Professor Lea,
           This is the final assignment email for CSC-344.
           Thank you for this semester. You said it'd be rough, you weren't kidding."""

passw = getpass.getpass("Enter password asap:")

def getMail():
    while 1:
        dlEmail = input("Enter recipient now!")
        if not re.match(emailRegex, dlEmail):
            print("Invalid Email")
        else:
            break
    return dlEmail

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
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    UN = user
    PW = pwd
    SUBJECT = subject
    TEXT = body

    head = MIMEMultipart()
    head['From'] = UN
    head['to'] = recipient
    head['subject'] = SUBJECT

    # Prepare actual message
    messageBody = MIMEText(TEXT)
    zipFileName = createZipFile()

    attachedZip = MIMEBase("All Sources for all Assignments", "zip")
    zipFile = open("csc344/" + zipFileName, "rb")
    attachedZip.set_payload(zipFile.read())
    encoders.encode_base64(attachedZip)

    attachedZip.add_header("Content-Disposition", "Attachment; filename= " + zipFileName)

    head.attach(messageBody)
    head.attach(attachedZip)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(UN, PW)
    server.sendmail(myMail, recipient, head.as_string())
    server.quit()


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
    html.write("""
      <h1 align="center">Rafael Torres CSC 344 Assignments</h1>
      <table class="centered highlight">
        <thead>
          <tr>
              <th data-field="id">Language</th>
              <th data-field="name">Source File</th>
              <th data-field="price">Symbols File</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>C++</td>
            <td><p><a href="a1.cpp">C++ Source</a></p></td>
            <td><p><a href="c++_identifiers.txt">C++ Symbols</a></p></td>
          </tr>
          <tr>
            <td>Lisp</td>
            <td><p><a href="a2.lisp">Lisp Source</a></p></td>
            <td><p><a href="lisp_identifiers.txt">Lisp Symbols</a></p></td>
          </tr>
          <tr>
            <td>Scala</td>
            <td><p><a href="a3.scala">Scala Source</a></p></td>
            <td><p><a href="scala_identifiers.txt">Scala Symbols</a></p></td>
          </tr>
          <tr>
            <td>Prolog</td>
            <td><p><a href="a4.txt">Prolog Source</a></p></td>
            <td><p><a href="prolog_identifiers.txt">Prolog Symbols</a></p></td>
          </tr>
          <tr>
            <td>Python</td>
            <td><p><a href="a5.py">Python Source</a></p></td>
            <td><p><a href="python_identifiers.txt">Python Symbols</a></p></td>
          </tr>
        </tbody>
      </table>
            """)

    html.write("</html>")
    html.close()

generatehtml()
# send_email("rtorres3@oswego.edu", passw, getMail(), subject, body)
