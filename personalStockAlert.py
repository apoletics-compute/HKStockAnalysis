#!/usr/bin/python
import subprocess
import urllib2
import pprint
import sys, getopt, csv, os
from HTMLParser import HTMLParser
from datetime import date
import httplib2
import os
import sys, getopt
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools
def getPrice(symbol):
    import urllib2, re
    number=int(symbol)
    req = urllib2.Request('http://www.aastocks.com/en/mobile/Quote.aspx?symbol={:05d}'.format(number))
    response = urllib2.urlopen(req)
    the_page = response.read()
    lines = the_page.split('\n')
    for num in range(0,len(lines)):
        if 'text_last' in lines[num]:
            current = lines[num+1]        
            m = re.search('bold">.*</span>',current)
            current = m.group(0)
            m = re.search('>.*<',current)
            current = m.group(0)
            current = current[1:-1]
            return current
            
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'HKStockCheck'


CURRENT=''
list={}
googlecredential=''
googleclientcert=''
def send_email(user, pwd, recipient, subject, body):
    import smtplib
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
def get_credentials():
    global googlecredential
    global googleclientcert
    credential_path = googlecredential
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(googleclientcert, SCOPES,redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        flow.user_agent = APPLICATION_NAME
        auth_uri = flow.step1_get_authorize_url()
        print "open browser for:  ",auth_uri
        auth_code = raw_input('Enter the auth code: ')
        credentials = flow.step2_exchange(auth_code)
        print 'Storing credentials to ',credential_path
        store.put(credentials)
    return credentials
    

def main(argv):
    largerthan = ''
    sender = ''
    recipient = ''
    emailpassword = ''
    allstockfile =''
    body = ''
    outputPath =''
    global googlecredential
    global googleclientcert
    today = date.today()
    try:
        opts, args = getopt.getopt(argv,"hl:s:r:p:a:g:c:o:",["largerthan=","sender=","recipient=","emailpassword=","allstockfile=","googlecredential=","googleclientcert=", "outputPath="])
    except getopt.GetoptError:
        print 'test.py -l <larger than> -s <sender> -r <recipient> -p <email password> -a <all stockfile path> -g <google credential file> -c <google client json> -o <outputPath>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -l <larger than> -s <sender> -r <recipient> -p <email password> -a <all stockfile path> -g <google credential file> -c <google client json> -o <outputPath>'
            sys.exit()
        elif opt in ("-l", "--largerthan"):
            largerthan = arg
        elif opt in ("-s", "--sender"):
            sender = arg
        elif opt in ("-r", "--recipient"):
            recipient = arg
        elif opt in ("-p", "--emailpassword"):
            emailpassword = arg			
        elif opt in ("-a", "--allstockfile"):
            allstockfile = arg						    
        elif opt in ("-g", "--googlecredential"):
            googlecredential = arg
        elif opt in ("-c", "--googleclientcert"):
            googleclientcert = arg            
        elif opt in ("-o", "--outputPath"):
            outputPath = arg                        
            
# read data            /home/apoletics_compute/data/algoresult
    result = subprocess.Popen("cd "+outputPath+"; grep 'Should Enter' *|grep -v false", shell=True, stdout=subprocess.PIPE).stdout.read()
    for line in result.split("\n"):
        stocknumber =  line[:4]
#	print "Processing: "+stocknumber 
        if not stocknumber:
            continue
        with open(allstockfile,'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if(int(stocknumber) == int(row[0])):
                    price=getPrice(stocknumber)
                    body+=today.strftime("%Y%h%d") + ','+ row[0].strip() + ','+ row[1].strip() +',' + row[2].strip() + ',' + row[3].strip() + ',' + price + ',' + str( float(price)* float(row[3].strip()))+ ','+ '\n'
                    break;
    subject="MY STOCK ALERT:"+today.strftime("%Y%h%d")+' BUY!!'
    print body
    send_email(sender,emailpassword,recipient,subject,body)

    result = subprocess.Popen("cd "+outputPath+"; grep 'Should Exit' *|grep -v false", shell=True, stdout=subprocess.PIPE).stdout.read()
    for line in result.split("\n"):
        stocknumber =  line[:4]
#	print "Processing: "+stocknumber 
        if not stocknumber:
            continue
        with open(allstockfile,'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if(int(stocknumber) == int(row[0])):
                    price=getPrice(stocknumber)
                    body+=today.strftime("%Y%h%d") + ','+ row[0].strip() + ','+ row[1].strip() +',' + row[2].strip() + ',' + row[3].strip() + ',' + price + ',' + str( float(price)* float(row[3].strip()))+ ','+ '\n'
                    break;
    subject="MY STOCK ALERT:"+today.strftime("%Y%h%d")+' EXIT!!'
    print body
    send_email(sender,emailpassword,recipient,subject,body)
if __name__ == "__main__":
   main(sys.argv[1:])

