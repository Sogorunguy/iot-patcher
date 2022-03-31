#Libs
import os
import re
import readline, glob
import apt

cache = apt.Cache()
cache.open()
#Welcome text
print("Welcome to IOT-patcher by https://github.com/TrueDru\n")
print("IOT-patcher requirements check:")
try:
    cache['binwalk'].is_installed
    print("binwalk ✅")
except:
    print("binwalk ❌")
try:
    cache['python3'].is_installed
    print("python3 ✅")
except:
    print("python3 ❌")
print("")
#Autocomplete function
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

binpath = input('Please enter path to *.bin file you want to decompile\nPath: ')
print("Please enter path to output directory\nPath: ")
outpath = input()
if outpath == "":
  extraction = str("binwalk --signature --term -e '"+binpath+"' --log binwalk.log")
else:
  extraction = str("binwalk --signature --term -e '"+binpath+"' --directory "+outpath+" --log "+outpath+"/binwalk.log")
  #check if directory exists
print(extraction)
os.system(extraction)




