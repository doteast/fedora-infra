#!/usr/bin/python
from sys import argv
import socket
import commands
import time
# arguments: [-4:only IPv4 addresses][-6:only IPv6 addresses]

log_file="timeout.log"

curl_command="curl --globoff --silent --max-time 30 --insecure -H 'Host: mirrors.fedoraproject.org' "
url="'https://%s/metalink?repo=epel-7&arch=x86_64'"

#get list of addresses for mirrors. this is necessary since some of the addresses are anycasted

resolve=socket.getaddrinfo("mirrors.fedoraproject.org",80)
addr_list_v4=[]
addr_list_v6=[]
for addrinfo in resolve:
  if addrinfo[4][0].find(':') != -1 and not addrinfo[4][0] in addr_list_v6:
   addr_list_v6.append(addrinfo[4][0])
  if addrinfo[4][0].find(':') == -1  and not addrinfo[4][0] in addr_list_v4:
   addr_list_v4.append(addrinfo[4][0])

addr_list=addr_list_v4+addr_list_v6
if "-4" in argv:
 addr_list=addr_list_v4
if "-6" in argv:
 addr_list=addr_list_v6

logfile=file(log_file,"w")
logfile.truncate()
logfile.write(time.asctime()+":Attempting to probe the following mirrors: %r \n" % addr_list)
logfile.flush()

while True:
 logfile.write("." * 5 + "\n")
 logfile.flush()
 for ip in addr_list:
  command=curl_command + url % ip
  result=commands.getstatusoutput(command)
  if result[0] != 0:
   logfile.write(time.asctime()+" timeout/error (%r) occured on ip=%s" % (result, ip) + "\n")
   logfile.flush()
 time.sleep(600)
