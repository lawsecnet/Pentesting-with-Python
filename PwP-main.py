import port_scanner as pscan
#import tcp_proxy as tproxy
import tcp_server as tserver
import p_netcat as pnetcat
import mechbrowser as mbrowser
#import keylog as klog
import nmapscanner as nscanner
import sniffer as psniff

print 'Welcome to Pentesting-with-Python'
print 'PwP is a simple framework providing basic toolkit \n'
print 'Available remote tools:'
print '\t1. TCP port scanner'
print '\t2. Nmap port scanner (requires nmap-python)'
print '\t3. Netcat'
print '\t4. TCP server'
print '\t5. TCP proxy (not working yet)'
print '\t6. Website source code grabber'
print '\n'
print 'Available local tools:'
print '\t7. Keylogger'
print '\t8. Packet sniffer'

def main_menu():
    choice = raw_input("Select tool > ")

    if choice == "1":
        pscan.main()
    elif choice == "2":
        nscanner.main()
    elif choice == "3":
        pnetcat.main()
    elif choice == "4":
        tserver.server()
    elif choice == "5":
        tproxy.main()
    elif choice == "6":
        mbrowser.main()
    elif choice == "7":
        klog.main()
    elif choice == "8":
        psniff.main()
    else:
        print 'Command not recognised. Please select tool from the list'

main_menu()
