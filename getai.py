#!/usr/bin/python
import sys, getopt, csv, os

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

def main(argv):
   largerthan = ''
   filename = ''
   body = ''
   try:
      opts, args = getopt.getopt(argv,"hl:f:",["largerthan=","filename="])
   except getopt.GetoptError:
      print 'test.py -l <larger than> -f <filename>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -l <larger than> -f <filename>'
         sys.exit()
      elif opt in ("-l", "--largerthan"):
         largerthan = arg
      elif opt in ("-f", "--filename"):
         filename = arg
   with open(filename, 'r') as myfile:
      for data in myfile:
         list=data.rstrip('\n').split(" ")
         if (int(list[0]) < int(largerthan)):
#            print 'smaller'
            break
         else:
#            print 'list:', list
            with open('/home/apoletics_compute/stock_ai/allstock.txt','rb') as csvfile:
               reader = csv.reader(csvfile)
               for row in reader:
                  if(int(list[1]) == int(row[0])):
                     body+=list[0] + ' '+ row[0].strip() + ' '+ row[1].strip() +' ' + row[2].strip() + ' ' + row[3].strip() +'\n'
                     break
   subject=os.path.splitext(os.path.basename(filename))[0] + ' report'
   print subject
   print body
   send_email("apoletics.compute@gmail.com","!su051565","apoletics@gmail.com",subject,body)
if __name__ == "__main__":
   main(sys.argv[1:])

