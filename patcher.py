######
#Libs#
######
#For interate with os
import os
#For regular expressions
import re
#For ASCII drawing
import pyfiglet
#
import readline, glob
import crypt
import getpass
from pyparsing import Regex
from zipfile import ZipFile

#import binwalk
#import apt
#import mmap


#Welcome text
print(str(pyfiglet.figlet_format("iot - patcher")+str("      Developed by https://github.com/TrueDru\n")))

#Autocomplete function
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

#Replace root hash function
def replace_string_file(path):
 password = crypt.crypt(getpass.getpass('Please, specify new root password: '))
 file=open(path, 'r+', encoding = 'utf-8')
 start = 'root:'
 end = ':'
 for num, line in enumerate(f,1): 

 #regex_root = r'^root:*'
 #content = re.sub(regex_root, 'root:'+password+':0:0:root:/:/bin/sh', content)
 #file.write(content)
 file.close()
 print('Password for root user in '+path+' succesfully updated!\n')
 

#Binwalk dialog
binpath = input('Please enter path to *.bin file you want to decompile\nPath: ') #Path to binary file
binname = os.path.basename(binpath)                                              #Extract filename from binpath   
bindir = binpath.replace(binname,'')                                             #Extract directory of the binary file (replace filename with nothing)   
outpath = input('Please enter path to output directory\nPath: ')
if outpath == "":
  outpath = bindir
  print("Output of binwalk wiil be in the current directory.\n")
  extraction = str("binwalk --signature --term -e '"+binpath+"' --log "+outpath+"binwalk.log -t")
else:
  extraction = str("binwalk --signature --term -e '"+binpath+"' --log "+outpath+"binwalk.log --directory "+outpath+" -t")
os.system(extraction)

#Firmware checking
workdir = str(bindir+'_'+binname+'.extracted/squashfs-root')
os.chdir(workdir)
print('\nBinwalk finished it''s work, firmware checking process is started. ')   

#Shadow check
if os.path.exists("etc/shadow") == True:
 print("Shadow file exist, start scanning")
 replace_string_file('etc/shadow')
else:
 print("Shadow doesn't exist.\n")

#Passwd check
if os.path.exists("etc/passwd") == True:
 print("Passwd file exist, start scanning")
 replace_string_file('etc/passwd')
else:
 print("Passwd doesn't exist.\n")











#Kill telnet
if os.path.exists("etc/inetd.conf") == True:
 print("Checking inetd.conf for possible vulnerabilities")
 file = open('etc/inetd.conf', 'r+', encoding = 'utf-8')
 content = re.sub(r'^telnet', '#telnet  stream  tcp     nowait  root    /usr/sbin/telnetd telnetd', content)
 file.write(content)
 print('Succesfully disabled telnet!\n')
 file.close()
 
#Create new bin file
print("Generating new binary file")
workdir = str(bindir+'_'+binname+'.extracted/')
os.chdir(workdir)
zipstr = str("zip -D -X '../new-"+binname+"' *  >> /dev/null")
os.system(zipstr)
print("New binary file succesfully generated, please flash your device with it.")
