import subprocess
import threading
import argparse
import sys
import os
'''
run the program by:
    python3 source.py image.dmg
the program will use 4 threads to open and check
passphrase0, passphrase1, passphrase2 and passphrase3 files for dictionary attack


'''

parser = argparse.ArgumentParser()
parser.add_argument("-t","--threads", help="thread count")
parser.add_argument("dmg", help=".dmg to crack")
args = parser.parse_args()

class myThread(threading.Thread):
    def __init__(self, threadID, phraseFile):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.phraseFile = phraseFile
        #open file
        print('opening ' + self.phraseFile + ' ...')
        self.f = open(self.phraseFile, 'r')
        print('File opened.')

    def run(self):
        subprocess.call(['hdiutil', 'verify', '-passphrase', "dmgCrackerPasswordCheck", args.dmg],stderr = open('results'+str(self.threadID), 'w'))
        statinfo = os.stat('results'+str(self.threadID))
        fileSize = statinfo.st_size
        for line in self.f:
            self.passphrase = line.rstrip()
            try:
                subprocess.call(['hdiutil', 'verify', '-passphrase', self.passphrase, args.dmg],stderr = open('results'+str(self.threadID), 'w'))
                statinfo = os.stat('results'+str(self.threadID))
                if statinfo.st_size != fileSize:
                    print('password found: ' + self.passphrase)
                    input('HOLD THE PHONE!')
                    break
                print('Failed:' + str(self.threadID) + ' ' + self.passphrase)
            except:
                print('Password check error:')
                print(sys.exc_info()[0])
        self.f.close()

count = 0
t = []
try:
    while(count < int(args.threads)):
        newThread = myThread(count, 'passphrase' + str(count))
        t.append(newThread)
        count +=1
except:
    print('Fuck, a thread unable to start')
    print(sys.exc_info()[0])

for thread in t:
    thread.start()
for thread in t:
    thread.join()
print("Exiting program")















