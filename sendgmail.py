#!/usr/bin/python
import sys, getopt

def main(argv):
   subject = ''
   recv = ''
   body = ''
   try:
      opts, args = getopt.getopt(argv,"hs:r:b:",["subject=","recv=","body="])
   except getopt.GetoptError:
      print 'test.py -s <subject> -r <recipient> -b <body>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
      	 print 'test.py -s <subject> -r <recipient> -b <body>'
         sys.exit()
      elif opt in ("-s", "--subject"):
         subject = arg
      elif opt in ("-r", "--recv"):
         recv = arg
      elif opt in ("-b", "--body"):
         body = arg
   print 'subject is "', subject
   print 'recv is "', recv 
   print 'body is "', body

if __name__ == "__main__":
   main(sys.argv[1:])

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
#send_email("apoletics.compute@gmail.com","!su051565","apoletics@gmail.com","Test python","Test python")
