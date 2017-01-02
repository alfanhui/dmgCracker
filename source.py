from __future__ import print_function
import threading
import sys
import os
import shlex
import Queue
import time 
from time import strftime
from subprocess import Popen, PIPE
from optparse import OptionParser

#Global Variables
queue = Queue.Queue()
printQueue = Queue.Queue()
t = []
timeRemaining = 0
fileCount = 0
found = False

#Options
parser = OptionParser()
parser.add_option("-u", "--update",
                  action="store_false", dest="update", default=True,
                  help="use to update program")
(options, args) = parser.parse_args()

#Main Thread
class MyThread(threading.Thread):
    def __init__(self, queue, printQueue):
        thread = threading.Thread(target=self.run,args=())
        self.queue = queue
	self.printQueue = printQueue
	thread.daemon = True
	thread.start()
    
    def run(self):
        while not self.queue.empty():
    	    passphrase = str(self.queue.get())
            args = shlex.split("hdiutil verify PJM.dmg -passphrase " + passphrase)
            proc = Popen(args, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            self.queue.task_done()
            if "checksum" in err:
                print('password found: ' + passphrase)
                passwordSave = open("PASSWORD IN HERE.txt", "w")
                passwordSave.write(passphrase)
                passwordSave.close()
                global found
                found = True
                return
            else:
		result = str(self.queue.qsize()) + "\tFailed\t" + passphrase 
		self.printQueue.put(result)

    def stop(self):
        self.stopped = True

#Time remaining thread
class timerThread(threading.Thread):
    def __init__(self,queue,printQueue):
        thread = threading.Thread(target=self.run,args=())
        self.queue = queue
	self.printQueue = printQueue
	thread.daemon = True
	thread.start()
    
    def run(self):
	global timeRemaining
	time.sleep(1)
	while True:
	    start = queue.qsize()
	    time.sleep(1)
	    end = queue.qsize()
	    timeRemaining = (end / (start - end)) / 60
	    time.sleep(10)

    def stop(self):
        self.stopped = True

def main():
    load_file_into_queue()
    try:
	for i in range(4):
	    thread = MyThread(queue, printQueue)
	    t.append(thread)
	thread = timerThread(queue,printQueue)
	t.append(thread)
	print("Minutes\tQueue\tStatus\tPassphrase")	
	while not queue.empty():
	    sys.stdout.write("\r                                                     ")
	    sys.stdout.write("\r" + str(timeRemaining) + "\t"+ printQueue.get())
	    sys.stdout.flush()
	    if found == True:
		raise KeyboardInterrupt
    except KeyboardInterrupt:
	print("closing threads... ")
	for thread in t:
	    if thread.isAlive():
		thread.stop()
	print("Exiting Program.")
	return
    except:
	print("Fuck, a thread unable to start")
	print(sys.exc_info()[0])
    if(queue.empty()):
	with open("passphrase" + str(fileCount), 'r') as original: data = original.read()
	with open('passphrase' + str(fileCount), 'w') as modified: modified.write("FILECOMPLETED\n" + data)


def load_file_into_queue():
    nextFile = False
    while os.path.isfile('passphrase' + str(fileCount)):
	f = open("passphrase" + str(fileCount), 'r')
	for line in f:
	    check = line.rstrip()
	    if not "FILECOMPLETED" in check:
		queue.put(line.rstrip())
	    else:
		nextFile = True
		break
	f.close()
	if nextFile == True:
	    i +=1
	    nextFile = False
	else:
	    return
    print("ERROR: No more unchecked files")
    os._exit(1)


if __name__ == '__main__':
    if not options.update:
	print("Updating program...")
	args = shlex.split("curl -o source.py https://raw.githubusercontent.com/alfanhui/dmgCracker/master/source.py")
	proc = Popen(args, stdout=PIPE, stderr=PIPE)
	print("program updated.")
	os._exit(1)
    if os.path.isfile("PASSWORD IN HERE.txt"):
        print("Did you know the password may have been found?")
        raw_input("please check your folder!")
        print("if it is a mistake, please remove it..")
        os._exit(1)
    found = False
    start = time.time()
    main()
    end = time.time()
    print("Time taken to complete: ", end - start , " seconds..")
    os._exit(1)
