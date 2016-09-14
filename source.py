import subprocess
import threading
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("threads", help="each thread must have an associated 'passphrase' Dictionary File")
parser.add_argument("-d", "--dmg", help=".dmg to crack")

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
        retcode = ''
        #print('Thread ' + self.threadID + ' is beginning its journey')
        for line in self.f:
            self.passphrase = line.rstrip()
            try:
                retcode = subprocess.check_output(['hdiutil', 'verify', '-passphrase', self.passphrase, args.dmg])
            except subprocess.CalledProcessError:
                print(':::::'+ retcode)
                print(self.passphrase)
                pass
        self.f.close()

count = 0
#create new threads
t = []
try:
    for i in args.threads:
        newThread = myThread(count, 'passphrase' + str(count))
        t.append(newThread)
        count +=1
except:
    print('Fuck, a thread unable to start')
    print(sys.exc_info()[0])

count = 0
for thread in t:
    print(count)
    thread.start()
    count +=1

while(t.isAlive):
    #somthing
    pass
print("Exiting program")















