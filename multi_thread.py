import threading
import time
import random
import queue

nb_fruits = 50
exitFlag = 0
fruit_tree = nb_fruits
dirty_basket = 0
clean_basket = 0


class Counter (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        #print("Starting " + self.name)
        print_time(self.name)
        #print("Exiting " + self.name)


class Picker (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.carrying = 0
        self.q = q

    def run(self):
        #print("Starting " + self.name)
        pick_fruit(self, self.name, self.q)
        #print("Exiting " + self.name)


class Cleaner (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.carrying = 0
        self.q = q

    def run(self):
        #print("Starting " + self.name)
        clean_fruit(self, self.name, self.q)
        #print("Exiting " + self.name)


def print_time(threadName):
    global fruit_tree
    while not exitFlag or clean_basket < nb_fruits:
        time.sleep(1)
        print("%s Tree (%s fruits) - dirty_basket (%s fruits) - clean_basket (%s fruits) - farmer1 (%i) - farmer2 (%i) - farmer3 (%i) - cleaner1 (%i) - cleaner2 (%i) - cleaner3 (%i)" % (
              time.ctime(time.time()), fruit_tree, dirty_basket, clean_basket, threads[0].carrying, threads[1].carrying, threads[2].carrying, threads2[0].carrying, threads2[1].carrying, threads2[2].carrying))


def pick_fruit(self, threadName, q):
    global fruit_tree
    global dirty_basket
    while fruit_tree > 0 and dirty_basket < nb_fruits:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            #print("%s processing %s" % (threadName, data))
            time.sleep(random.randrange(3, 4))
            fruit_tree -= 1
            self.carrying += 1
            time.sleep(random.randrange(0, 2))
            self.carrying -= 1
            dirty_basket += 1

        else:
            queueLock.release()


def clean_fruit(self, threadName, q):
    global dirty_basket
    global clean_basket
    while clean_basket < nb_fruits:
        queueLock2.acquire()
        if not workQueue2.empty():
            if (dirty_basket > 0):
                data = q.get()
                queueLock2.release()
                #print("%s processing %s" % (threadName, data))
                time.sleep(random.randrange(2, 3))
                dirty_basket -= 1
                self.carrying += 1
                time.sleep(random.randrange(0, 1))
                self.carrying -= 1
                clean_basket += 1
            else:
                queueLock2.release()
                time.sleep(1)
        else:
            queueLock2.release()


nameList = list(range(nb_fruits))

# Create threads for pickers
threadList = ["farmer-1", "farmer-2", "farmer-3"]
queueLock = threading.Lock()
workQueue = queue.Queue(nb_fruits)
threads = []
threadID = 1

for tName in threadList:
    thread = Picker(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1


# Create threads for cleaners
threadList2 = ["cleaner-1", "cleaner-2", "cleaner-3"]
queueLock2 = threading.Lock()
workQueue2 = queue.Queue(nb_fruits)
threads2 = []
threadID2 = 1

for tName in threadList2:
    thread = Cleaner(threadID, tName, workQueue2)
    thread.start()
    threads2.append(thread)
    threadID2 += 1

# Create thread for counter
thread0 = Counter(0, "Thread-0")
thread0.start()

# Fill the queue for pickers
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# Fill the queue for Cleaners
queueLock2.acquire()
for word in nameList:
    workQueue2.put(word)
queueLock2.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
thread0.join()
for t in threads:
    t.join()
for t in threads2:
    t.join()
#print("Exiting Main Thread")
