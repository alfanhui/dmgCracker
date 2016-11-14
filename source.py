import threading
import sys
import os
import shlex
import Queue
import time
from subprocess import Popen, PIPE
queue = Queue.Queue()
t = []
found = False
class MyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            passphrase = str(self.queue.get())
            args = shlex.split("hdiutil verify PJM.dmg -passphrase " + passphrase)
            proc = Popen(args, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            if "checksum" in err:
                print('password found: ' + passphrase)
                passwordSave = open("PASSWORD IN HERE.txt", "w")
                passwordSave.write(passphrase)
                passwordSave.close()
                global found
                found = True
                return
            else:
                print("Failed:" + passphrase)
            self.queue.task_done()
            time.sleep(0.0001)

    def stop(self):
        self.stopped = True


def main(success):
    if success:
        print("closing threads... ")
        for thread in t:
            if thread.isAlive():
                thread.stop()
        print("Exiting Program.")
        return
    else:
        count = 348
        fileCheck = False
        for i in range(count):
            if os.path.isfile('passphrase' + str(i)):
                f = open("passphrase" + str(i))
                for line in f:
                    check = line.rstrip()
                    if "FILECOMPLETED" in check:
                        fileCheck = True
                        break
                    else:
                        count = i
                        break
                if fileCheck:
                    fileCheck = False
                    continue
                else:
                    break
        if(count !=349):
            try:
                for i in range(5):
                    myThread = MyThread(queue)
                    myThread.setDaemon(True)
                    t.append(myThread)
                f = open("passphrase" + str(count), 'r')
                for line in f:
                    queue.put(line.rstrip())
                f.close()
                for myThread in t:
                    myThread.start()
                while True:
                    time.sleep(.001)
                    if found == True:
                        raise KeyboardInterrupt
                queue.join()
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
        else:
            print("No more files available.")
        if(queue.empty()):
            with open("passphrase" + str(count), 'r') as original: data = original.read()
            with open('passphrase' + str(count), 'w') as modified: modified.write("FILECOMPLETED\n" + data)

if __name__ == '__main__':
    found = False
    start = time.time()
    main(False)
    end = time.time()
    print("Time taken to complete: ", end - start)
    os._exit(1)



