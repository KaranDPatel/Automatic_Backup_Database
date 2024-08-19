import subprocess
import time
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def autobackupmysql():
    todaysdate=datetime.today().strftime('%Y-%m-%d')
    filepath=r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqlautobackup.bat"
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()
    print (p.returncode) # is 0 if success
    print('email call--')
    send_email()
    print('email sent..')

def send_email():
    todaysdate=datetime.today().strftime('%Y-%m-%d')
    fromaddr = ""
    toaddr = ""
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Buckup of Databases are Completed"
    body = "Hi"
    
    msg.attach(MIMEText(body, 'plain'))
    filename = "database_{}.sql".format(todaysdate)
    attachment = open(r"backup.sql".format(todaysdate), "rb")
    
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    
    #2nd file
    filename = "database2{}.sql".format(todaysdate)
    attachment = open(r"database.sql".format(todaysdate), "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# schedule.every().day.at("15:35").do(autobackupmysql)
schedule.every(1).minutes.do(autobackupmysql)
# schedule.every().sunday.at("23:00").do(autobackupmysql)
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute