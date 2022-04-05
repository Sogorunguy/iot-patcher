#Libs
import os
import re
import readline, glob
import mmap
import crypt
from jmespath import search
import getpass
from pyparsing import Regex
from zipfile import ZipFile
#import apt_pkg
import binwalk

#Welcome text
print("Welcome to IOT-patcher by https://github.com/TrueDru\n")
#print("IOT-patcher requirements check:")
#Installation check by array function
#def package_check():
# cache = apt.Cache()
# cache.open()
# packages = ['python3', 'binwalk', 'python3-apt']
# for i in range(0, len(packages)):
#  try:
#   cache[packages[i]].is_installed
#   print(packages[i], " ✅")
#  except:
#   print(packages[i], " ❌")
#package_check()

#Replace root hash function
def replace_string_file(path):
 password = crypt.crypt(getpass.getpass('Please, specify new root password: '))
 file_r = open(path, 'r', encoding = 'utf-8')
 content = file_r.read()
 file_r.close()
 file_w = open(path, 'w', encoding = 'utf-8')
 regex_root = r'^root:*'
 content = re.sub(regex_root, 'root:'+password+':0:0:root:/:/bin/sh', content)
 file_w.write(content)
 print('Password for root user in '+path+' succesfully updated!\n')
 file_w.close()

#Autocomplete function
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

#Binwalk dialog
binpath = input('Please enter path to *.bin file you want to decompile\nPath: ') #Path to binary file
binname = os.path.basename(binpath)                                              #Extract filename from binpath   
bindir = binpath.replace(binname,'')                                             #Extract directory of the binary file (replace filename with nothing)   

outpath = input('Please enter path to output directory\nPath: ')
if outpath == "":
  outpath = bindir
  print("Output of binwalk wiil be in "+bindir+" directory.\n")
  extraction = str("binwalk --signature --term -e '"+binpath+"' --log "+outpath+"binwalk.log --directory "+outpath+" -t 2> /dev/null")
else:
  extraction = str("binwalk --signature --term -e '"+binpath+"' --log "+outpath+"binwalk.log --directory "+outpath+" -t 2> /dev/null")

#Firmware checking
os.system(extraction)
workdir = str(bindir+'_'+binname+'.extracted/squashfs-root')
os.chdir(workdir)
print('\nBinwalk finished it''s work, firmware checking process is started. ')   

#Passwd check
if os.path.exists("etc/passwd") == True:
 print("Passwd file exist, start scanning")
 replace_string_file('etc/passwd')

else:
 print("Passwd doesn't exist.\n")

#Shadow check
if os.path.exists("etc/shadow") == True:
 print("Shadow file exist, start scanning")
 replace_string_file('etc/shadow')
else:
 print("Shadow doesn't exist.\n")

#Kill telnet
if os.path.exists("etc/inetd.conf") == True:
 print("Checking inetd.conf for possible vulnerabilities")
 file_r = open('etc/inetd.conf', 'r', encoding = 'utf-8')
 content = file_r.read()
 file_r.close()
 file_w = open('etc/inetd.conf', 'w', encoding = 'utf-8')
 content = re.sub(r'^telnet', '#telnet  stream  tcp     nowait  root    /usr/sbin/telnetd telnetd', content)
 file_w.write(content)
 print('Succesfully disabled telnet!\n')
 file_w.close()
 
#Create new bin file
print("Generating new binary file")
workdir = str(bindir+'_'+binname+'.extracted/')
os.chdir(workdir)
zipstr = str("zip -D -X '../new-"+binname+"' *  >> /dev/null")
os.system(zipstr)
print("New binary file succesfully generated, please flash your device with it.")
