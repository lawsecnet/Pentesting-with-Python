#
# Python implementation of netcat. Based on implementation presented in
# 'Black Hat Python' by Justin Seitz
#

import sys
import socket
import getopt
import threading
import subprocess

# define global varaibles
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    target = raw_input('Specify target host: ')
    port = int(raw_input('Specify target port: '))
    com = raw_input('Select functionality (type h for help): ')

    if com == "h" or com == "":
        print "'l': listen on [host]:[port] for incoming connections"
        print """'e':  execute the given file upon receiving a connection"""
        print "'c': initialize command shell"
        print """'u': upon receiving connection upload a file
        and write to [destination]"""
        main()
    elif com == "l":
        listen = True
        server_loop()
    elif com == "e":
        execute = raw_input('Provide file to execute: ')
    elif com == "c":
        command = True
        comm = raw_input('Provide command: ')
        run_command(comm)
    elif com == "u":
        upload_destination = raw_input('Provide upload destination: ')
    else:
        print "Command unknown. Type 'h' fpr help."
        main()


    # are we going to listen or just send data from stdin
    if not listen and len(target) and port > 0:

        #read in the buffer from the commandline
        #this will block, so send CTRL-D if not sending input
        #to stdin
        buffer = sys.stdin.read()

        #send data off
        client_sender(buffer)

    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
        server_loop()

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to our target host
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:

            #now wait for data back
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            # wait for more input
            buffer = raw_input("")
            buffer += "/n"

            # send it off
            client.send(buffer)

    except:

        print "[*] Exception... exiting"

        # tear down connection
        clinet.close()

def server_loop():
    global target

    # if no target is defined, we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off a thread to handle our new client
        client_thread = threading.Thread(target = client_handler,
        args = (client_socket))
        client_thread.start()
        print "Listening on %s" % target

def run_command(command):

    # trim the newline
    command = command.rstrip()

    # run the command an get the output back
    try:
        output = subprocesss.check_output(command, stderr=subprocesss.STDOUT,
        shell = True)
    except:
        output = "Failed to execute command \r\n"

    # send output back to the client
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):
        # read in all of the bytes an write to our destination
        file_buffer = ""
        # keep reading data until none is available

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        # now we takes theses bytes ant try to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            # acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s \r\n" % upload_destination)

    # check fot command execution
    if len(execute):
        # run the command
        output = run_command(execute)
        client_socket.send(output)

    # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            client_socket.send("<prompt:#> ")
            # now we receive until we see a line feed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back the command output
            response = run_command(cmd_buffer)

            # send back teh response
            client_socket.send(response)
