import random
from smtplib import SMTP
from email.mime.text import MIMEText
from django.http import HttpResponse
import re
buyermails = {}
buyerfakemails = {}
sellermails = {}
sellerfakemails = {}

buyermails['buyer0@yongwoo.mailgun.org'] = 'rnfn6292@gmail.com'
buyerfakemails['rnfn6292@gmail.com'] = 'buyer0@yongwoo.mailgun.org'

def add_buyer_mail(mail):
    while True:
        address = "buyer"+(str(int(random.random()*10000)))+"@yongwoo.mailgun.org"
        if not buyermails.has_key(address):
            buyermails[address] = mail
            buyerfakemails[mail] = address
            return address

def remove_buyer_mail(address):
    if buyermails.has_key(address):
        buyerfakemails.pop(buyermails[address])
        buyermails.pop(address)
        return True
    return False

def add_seller_mail(mail):
    while True:
        address = "seller"+(str(int(random.random()*10000)))+"@yongwoo.mailgun.org"
        if not sellermails.has_key(address):
            sellerfakemails[mail] = address
            sellermails[address] = mail
            return address

def remove_seller_mail(address):
    if sellermails.has_key(address):
        sellerfakemails.pop(sellermails[address])
        sellermails.pop(address)
        return True
    return False

def send_message_via_smtp(sender,recipient,message):
    smtp = SMTP("smtp.mailgun.org", 587)
    smtp.login('postmaster@yongwoo.mailgun.org', '25jtuf4p4z51')
    smtp.sendmail(sender, recipient, message.as_string())
    smtp.quit()

def on_incoming_message(request):
     if request.method == 'POST':
         sender    = request.POST.get('sender')
         recipient = request.POST.get('recipient')
         subject   = request.POST.get('subject', '')

         body_plain = request.POST.get('body-plain', '')
         body_without_quotes = request.POST.get('stripped-text', '')
         # note: other MIME headers are also posted here...
         buyer = re.match('buyer([0-9]+)@yongwoo.mailgun.org',recipient)
         
         if buyer:
            senderaddres = ""
            if sellerfakemails.has_key(sender):
                senderaddres = sellerfakemails[sender]
            else:
                senderaddres = add_seller_mail(sender) 
            recipientaddress = buyermails[recipient]
            message = MIMEText(body_plain)
            message['Subject'] = subject
            message['From'] = senderaddres
            message['To'] = recipientaddress
            send_message_via_smtp(senderaddres,recipientaddress,message)
         else:
            senderaddres = ""
            if buyerfakemails.has_key(sender):
                senderaddres = buyerfakemails[sender]
            else:
                senderaddres = add_buyer_mail(sender) 
            recipientaddress = sellermails[recipient]
            message = MIMEText(body_plain)
            message['Subject'] = subject
            message['From'] = senderaddres
            message['To'] = recipientaddress
            send_message_via_smtp(senderaddres,recipientaddress,message)
       
         """
         # attachments:
         for key in request.FILES:
             file = request.FILES[key]
             # do something with the file
         """
     # Returned text is ignored but HTTP status code matters:
     # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
     return HttpResponse('OK')
