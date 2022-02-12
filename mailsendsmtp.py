import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
from datetime import date
import natsort


mail_head = '''<html>
Dear sir,
<br>Please find attached today's newspaper clippings relevant to HVPI. Following are the headlines:
<br><br>
'''

mail_tail = '''
<br>
<br>Regards,
<br>Rohit Koganti
<br>Assistant Director (M&C)
<br>Vice President Secretariat
<br>Mob: 8860944780
<br>Twitter: @VPSecretariat
</html>
'''


def send_mail(sender_name, sender_address, sender_pass, receiver_address, headlines, final_dir):

    #Setup the MIME and creating headers
    print("Send: Generating the mail body.")
    message = MIMEMultipart()
    message['From'] = sender_name
    message['To'] = ', '.join(receiver_address)
    message['Subject'] = 'HVPI Print Articles - ' + date.today().strftime("%d %B")

    #The body and the attachments for the mail
    body = ''
    for i,line in enumerate(headlines):
        title = line[4]
        source = line[5]
        journalist = line[6]
        if journalist == '':
            journalist = 'NA'
        link = line[7]
        body+= str(i+1) + '. <b>' + title + '</b>' + ' <br>'
        body+= 'Source: ' + source + '&ensp;|&ensp;' + 'Journalist: ' + journalist + ' <br><br>'
#        body+= 'Link: ' + link + ' <br><br>'  #Removing the link of the article from the mail body as there are no login credentials for the end-user

    mail_content = mail_head + body + mail_tail
    message.attach(MIMEText(mail_content, 'html'))

    for filename in natsort.natsorted(os.listdir(final_dir)):
        f = os.path.join(final_dir, filename)
        attach_file = open(f, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream', Name= filename)
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=filename)
        message.attach(payload)

    #Create SMTP session for sending the mail
    print("Send: Attempting to login to gmail.")
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    try:
        session.login(sender_address, sender_pass) #login with mail_id and password
        print("Send: Logged in, sending mail.")
    except:
        print("Send: Failed to login to mail. Exiting.")
        return False
    text = message.as_string()
    err = session.sendmail(sender_address, receiver_address, text)

    if err is None:
        session.quit()
        return True
    else:
        return False
