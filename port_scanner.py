#
#
# Simple TCP port scanner. Performs TCP full connection using socket library
#
# Based on implementation presented in 'Violent Python' by TJ O'Connor
#

import sys
import optparse
from socket import *
from threading import *
screenLock = Semaphore(value = 1)

def scanner(target_host, target_port):

    try:
        conn = socket(AF_INET, SOCK_STREAM)
        conn.connect((target_host, target_port))
        conn.send("Scanning\r\n")
        results = conn.recv(100)
        screenLock.acquire()
        print "[*]%d/ TCP open" % target_port
        print "[*]" + str(results)

    except:
        screenLock.acquire()
        print "[-]%d/ TCP closed" % target_port
    finally:
        screenLock.release
        conn.close()

def portScan(target_host, target_ports):
    try:
        target_ip = gethostbyname(target_host)
    except:
        print "[-] Cannot resolve '%s': unknown host" % target_host
        return

    try:
        target_name = gethostbyname(target_ip)
        print "\n [*] Scan reults for: " + target_name
    except:
        print "\n [*] Scan results for " + target_ip

    setdefaulttimeout(1)

    for target_port in target_ports:

        t = Thread(target = scanner, args = (target_host, int(target_port)))
        t.start()

def main():
    target_host = raw_input('Specify target host: ')
    tp = raw_input('Specify target ports (separated by comma): ')
    target_ports = str(tp).split(', ')

    if (target_host == "") or (target_ports == ""):
        print "Please specify target host and target port"
        exit(0)

    portScan(target_host, target_ports)

if __name__ == "__main__":
    main()
