import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
from datetime import date


mail_head = '''<html>
Dear sir,
<br>Please find attached online articles from yesterday relevant to HVPI. Following are the headlines:
<br><br>
'''

mail_tail = '''
<br>Thank you.
<br>
<br>Regards,
<br>Rohit Koganti
<br>Assistant Director (M&C)
<br>Vice President Secretariat
<br>Mob: 8860944780
<br>Twitter: @VPSecretariat
</html>
'''


def send_mail(sender_name, sender_address, sender_pass, receiver_address, filename, headlines):
    basename = os.path.basename(filename)

    #Setup the MIME and creating headers
    print("Send: Generating the mail body.")
    message = MIMEMultipart()
    message['From'] = sender_name
    message['To'] = ', '.join(receiver_address)
    message['Subject'] = 'HVPI Online Articles - ' + date.today().strftime("%d %B")

    #The body and the attachments for the mail
    body = ''
    for i,line in enumerate(headlines):
        title = line[3]
        source = line[4]
        journalist = line[5]
        if journalist == '':
            journalist = 'NA'
        link = line[6]
        body+= str(i+1) + '. <b>' + title + '</b>' + ' <br>'
        body+= 'Source: ' + source + '&ensp;|&ensp;' + 'Journalist: ' + journalist + ' <br>'
        body+= 'Link: ' + link + ' <br><br>'

    mail_content = mail_head + body + mail_tail
    message.attach(MIMEText(mail_content, 'html'))
    attach_file = open(filename, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream', Name= basename+'.pdf')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=basename)
    message.attach(payload)

    #Create SMTP session for sending the mail
    print("Send: Attempting to login to gmail.")
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    print("Send: Logged in, sending mail.")
    text = message.as_string()
    err = session.sendmail(sender_address, receiver_address, text)

    if err is None:
        session.quit()
        return True
    else:
        return False
