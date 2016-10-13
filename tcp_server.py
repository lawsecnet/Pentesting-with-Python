#
# TCP server as presented in 'Black Hat Python' by Justin Seitz
#

import socket
import threading


# this is our client-handling thread
def handle_client(client_socket):

  #print out what client sends
  request = client_socket.recv(1024)

  print "[*] Received %s" % request

  # send back some packet
  client_socket.send("ACK!")

  client_socket.close()

def server():

    bind_ip = "0.0.0.0"
    bind_port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    server.listen(5)

    print "[*] Listetning on %s:%d" % (bind_ip, bind_port)

    client, addr = server.accept()

    print "[*] Accepted connection from %s:%d" % (addr[0],addr[1])

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client))
    client_handler.start()
