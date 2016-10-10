import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions"
        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connection information
        print "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # send data to local client if Available
        if len(remote_buffer):
            print "[<=] Sending %d bytes to localhost" % len(remote_buffer)
            client_socket.send(remote_buffer)

        # loop for sending and receiving to/from local
        while True:

            # read from local host
            local_buffer = receive_from(client_socket)

            if len(local_buffer):

                print "Received %d bytes from localhost" % len(local_buffer)
                hexdump(local_buffer)

                # send data to request handler
                local_buffer = request_handler(local_buffer)

                # send data to remote host
                remote_socket.send(local_buffer)
                print "Sent to remote"

            # receive response
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print "[<=] Received %d bytes from remote" % len(remote_buffer)
                hexdump(remote_buffer)

                # send to response handler
                remote_buffer = response_handler(remote_buffer)

                # send response to local socket
                client_socket.send(remote_buffer)

                print "[<=] Sent to localhost"

            # close the connection if no more data on either side is left
            if not len(local_buffer) or not len(remote_buffer):
                client_sender.close()
                remote_socket.close()
                print "No data left. Closing connections..."

                break
def main():

    # this tells our proxy to connect and receive data
    # before sending to remote host

    rf = raw_input("Receive first? [y/N]: ")

    # setup local listening parameters
    local_host = raw_input("Provide local host: ")
    local_port = int(raw_input("Provide local port: "))

    # setup remote target
    remote_host = raw_input("Provide remote host: ")
    remote_port = int(raw_input("Provide remote port:")

    #if rf == 'y':
    #    receive_first = True
    #else:
    #    receive_first = False

    # now spin our listening socket
    server_loop(local_host, local_port, remote_host, remote_port)

main()
