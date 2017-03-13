#import subprocess
#p = subprocess.Popen(['date','+%Y%h%d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#(output , err) = p.communicate()
#p_status = p.wait()
#print "Command output :", output
#print "exit code: ", p_status


import csv
with open('/home/apoletics_compute/stock_ai/allstock.txt','rb') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    print ', R'.join(row.strip())
