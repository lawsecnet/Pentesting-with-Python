#
# Protocol analyser based on packet sniffer and ICMP decoder implementation
# form 'Black Hat Python' by Justin Seitz
#



import socket
import os
import struct
from ctypes import *

# IP header structure
class IP(Structure):
    _fields_ = [
    ("ihl", c_ubyte, 4),
    ("version", c_ubyte, 4),
    ("tos", c_ubyte),
    ("len", c_ushort),
    ("id", c_ushort),
    ("offset", c_ushort),
    ("ttl", c_ubyte),
    ("protocol_num", c_ubyte),
    ("sum", c_ushort),
    ("src", c_ulong),
    ("dst", c_ulong)
    ]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):

        # map protocol constatnts to their names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        # IP addresses in readable form
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # protocol in human readable form
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

class ICMP(Structure):
    _fields_ = [
    ("type", c_ubyte),
    ("code", c_ubyte),
    ("checksum", c_ushort),
    ("unused", c_ushort),
    ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


def main():

    # specify host to listen on
    host = raw_input("Specify host to listen on: ")

    # create a raw socket and bind it to the interface
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP


    sniff = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    sniff.bind((host, 0))

    # including IP headers in the capture
    sniff.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # in case of windows, IOCTL is required to set promiscous mode
    if os.name == "nt":
        sniff.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # read in a packet
            raw_buffer = sniff.recvfrom(65565)[0]

            # create an IP header from the first 20 bytes of the buffer
            ip_header = IP(raw_buffer[0:20])

            # print out detected protocol and host
            print "Protocol: %s %s -> %s" % (ip_header.protocol,
            ip_header.src_address, ip_header.dst_address)

            #identify ICMP packets
            if ip_header.protocol == "ICMP":

                # calculate where the packet starts
                offset = ip_header.ihl * 4

                buf = raw_buffer[offset:offset + sizeof(ICMP)]

                # create ICMP Structure
                icmp_header = ICMP(buf)

                print "ICMP - > Type: %d Code: %d" %(icmp_header.type,
                icmp_header.code)

            # CTRL-C interruption
    except KeyboardInterrupt:
            # turn of the promiscous mode after the scanner
            if os.name == "nt":
                sniff.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
