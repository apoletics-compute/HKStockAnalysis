#!/usr/bin/python
import sys, getopt

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
            print 'smaller'
            break
         else:
            print 'list:', list
if __name__ == "__main__":
   main(sys.argv[1:])
