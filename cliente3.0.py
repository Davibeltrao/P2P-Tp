from threading import Thread
from time import sleep
import socket
import struct
import sys

#codigo dorgival
def carry_around_add(a, b):
    c = a + b
    return(c &0xffff)+(c >>16)

#codigo dorgival
def checksum(msg):
    s =0
    for i in range(0, len(msg),2):
        w = msg[i]+(msg[i+1]<<8)
        s = carry_around_add(s, w)
    return~s &0xffff


def sendFile(sock, filename, length):
	fin = open(filename, 'r')
	#read and send 8KB by 8KB until theres nothing left
	while True:
		data = f.read(length)
		datasz = len(data)
		if datasz==0:
			break
		#chcksum
		chck = 0
		reserved = 0

		head = struct.pack('!L', 0xDCC023C2) + struct.pack('!L', 0xDCC023C2)
		mid = struct.pack('!H', datasz) + struct.pack('!H', reserved)
		msg =  head + struct.pack('!H', chck) + mid + data
		chck = checksum(msg)
		msg = head + struct.pack('!H', chck) + mid + data

		sock.send(msg)

def makeConnection(host, port):
	sock = socket.socket(AF_INET, socket.SOCK_STREAM)
	sock.connect((host,port))
	return sock

def client(filename, host, port, length):
	sock = makeConnection(host,port)
	sendFile(sock, filename, 8192)

def receive_message():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 51515
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    while(1):
        (conn, addr) = s.accept()
        try:
            sync1 = conn.recv(4)#receive data from client
            if(sync1 == 0xdcc023c2):
                sycn2 = conn.recv(4)#receive data from client
                if(sync2 == 0xdcc23c2):
                    chksum = conn.recv(2)
    #RECEBER DADOS DANDO UNPACK
    #ESCREVER DADOS NO ARQUIVO
    pass


def main():
    thread1 = Thread(target=send_message(), args=[])
    thread2 = Thread(target=receive_message(), args=[])
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("Threads exited")
    # my code here
    # f = open("myfile", "rb")
    # try:
    #     byte = f.read(1)
    #     print(byte)
    #     while byte != "":
    #         # Do stuff with byte.
    #         byte = f.read(1)
    # finally:
    #     f.close()
    # pass


if __name__ == "__main__":
    main()
