import os
from email.message import EmailMessage
from email.utils import formataddr
import smtplib
import random 

def send_simple_mail(data):
    sender_mail = os.environ['EMAIL_ADDR']
    reciver_mail = data['email']
    password = os.environ['PASS']
    msg = EmailMessage()
    # Send the message to the mail server.  This will send it to the recipient as well  as the sender.
    msg['Subject'] = f"Hey, Dear {data['name']}  from Blue Education"
    msg['From'] = formataddr(("Blue Education",sender_mail))
    msg['To'] = formataddr(("Blue Education",reciver_mail))
    msg.add_alternative(f"""
    <!DOCTYPE html>
    <html>
    <body>
    <di>Hey, Dear your otp {data['otp']}, Please Complete Your {data['purpose']}</div>
    </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_mail, password)
        smtp.send_message(msg)
        print('done')

def code_generator():
    digits="0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[random.randint(0,9)]
    print(OTP)
    return OTP
