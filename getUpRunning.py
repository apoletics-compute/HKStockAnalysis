#!/usr/bin/python
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
    
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        global CURRENT
        global list
        if "head shoulders bottom" in data.lower():	
           CURRENT="head shoulders bottom"
        if "golden cross" in data.lower():	
           CURRENT="golden cross"
        if "range breakout" in data.lower():	
           CURRENT="range breakout"
        if "triangle breakout" in data.lower():	
           CURRENT="triangle breakout"
        if "triple bottom" in data.lower():
           CURRENT="triple bottom"
        if "oversold signal" in data.lower():	
           CURRENT="oversold signal"
        if "trend reversal" in data.lower():
           CURRENT="trend reversal"
        if "cup with a handle" in data.lower():	
           CURRENT="cup with a handle"
        if ".HK" in data:
           if data.strip()[:-3] in list:
              list[data.strip()[:-3]] += "|"+CURRENT
           else:
              list[data.strip()[:-3]] = CURRENT
def main(argv):
    largerthan = ''
    sender = ''
    recipient = ''
    emailpassword = ''
    allstockfile =''
    body = ''
    global googlecredential
    global googleclientcert
    today = date.today()
    try:
        opts, args = getopt.getopt(argv,"hl:s:r:p:a:g:c:o:",["largerthan=","sender=","recipient=","emailpassword=","allstockfile=","googlecredential=","googleclientcert=", "outputPath="])
    except getopt.GetoptError:
        print 'test.py -l <larger than> -f <filename> -s <sender> -r <recipient> -p <email password> -a <all stockfile path> -g <google credential file> -c <google client json> -o <outputPath>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -l <larger than> -f <filename> -s <sender> -r <recipient> -p <email password> -a <all stockfile path> -g <google credential file> -c <google client json> -o <outputPath>'
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
    req = urllib2.Request('http://www.aastocks.com/en/LTP/RTAI.aspx?type=1')
    response = urllib2.urlopen(req)
    the_page = response.read()			
# instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    outputlist=[]
    parser.feed(the_page)
    for key in list:
        outputlist.append([len(list[key].split("|")), key, list[key]])
    outputlist.sort(reverse=True)
    outputfile = open(os.path.join(outputPath,today.strftime("%Y%h%d")+'U.txt'),'w')
    for item in outputlist:
        outputfile.write("%s,%s,%s\n" % (item[0],item[1],item[2]))
        if int(item[0]) < int(largerthan):
            break
        else:
            with open(allstockfile,'rb') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if(int(item[1]) == int(row[0])):
                        body+=today.strftime("%Y%h%d")+','+str(item[0]) + ','+ row[0].strip() + ','+ row[1].strip() +',' + row[2].strip() + ',' + row[3].strip() + ',' + item[2]+'\n'
                        break
    for item in outputlist:
        outputfile.write("%s,%s,%s\n" % (item[0],item[1],item[2]))
    outputfile.close()
    subject=today.strftime("%Y%h%d")+'U'
    send_email(sender,emailpassword,recipient,subject,body)
    print body
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1JKsNu2b1_5X1MhlSUfUS5263YawF6okdVACw6baRlzk'
    rangeName = 'Up Signal!A:F'
    dataarray=[]
    for line in body.split("\n"):
        dataarray.append(line.rstrip('\n').split(","))
    print dataarray
    myvalues = {'values':dataarray}
    service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption="USER_ENTERED", body=myvalues).execute()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print 'No data found.'
    else:
        print 'Name, Major:'
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print '%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4])    
if __name__ == "__main__":
   main(sys.argv[1:])
