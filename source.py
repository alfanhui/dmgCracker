import subprocess
import threading
import argparse
import sys
import os
import time

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
        #print('Thread ' + self.threadID + ' is beginning its journey')i
        for line in self.f:
            self.passphrase = line.rstrip()
            try:
                process = subprocess.call(['hdiutil', 'verify', '-passphrase', self.passphrase, args.dmg],
                                          stdout=open(os.devnull,'wb') ,stderr=open(os.devnull, 'wb'))
                if process == 0:
                    print('password' + self.passphrase)
                    input('HOLD THE PHONE!')
                else:
                    print('Failed:' + str(self.threadID) + ' ' + self.passphrase)


            except subprocess.CalledProcessError:
                print(self.passphrase)
                pass
        self.f.close()

count = 0
#create new threads
t = []
try:
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)
    count +=1
    newThread = myThread(count, 'passphrase' + str(count))
    t.append(newThread)

except:
    print('Fuck, a thread unable to start')
    print(sys.exc_info()[0])

count = 0
start = time.time()
for thread in t:
    print(count)
    thread.start()
    count +=1

for thread in t:
    print('HELLO')
    thread.join()
end = time.time()
print(end - start)

print("Exiting program")















