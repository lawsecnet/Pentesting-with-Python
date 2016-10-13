#
# Nmap python port scanner
#
# Based on implementation presented in 'Violent Python' by TJ O'Connor and
# uses python-nmap library by Alexandre Norman

import nmap
import optparse


def nmapScan(target_host, target_ports):
    nmScan = nmap.PortScanner()
    nmScan.scan(target_host, target_ports)
    state = nmScan[target_host]['tcp'][int(target_ports)]['state']
    print " [*] " + target_host + " tcp/"+ target_ports + " " + state

def main():

    target_host = raw_input("Specify target host: ")
    target_ports = raw_input("Specify target ports: ")

    tps = str(target_ports).split(', ')

    if (target_host == "") or (tps == ""):
        print "Please specify target host and target ports"
        exit(0)

    for target_port in tps:
        nmapScan(target_host, str(target_ports))

if __name__ == '__main__':
    main()
