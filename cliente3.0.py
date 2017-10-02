from threading import Thread
import time
import socket
import struct
import sys
import binascii
import math

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

def makeConnection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    return sock

def client(filename, host, port, length):
    sock = makeConnection(host,port)
    sendFile(sock, filename, length)

def send_message(sock, filename):
    #TCP_IP = '127.0.0.1'
    #PORT = 51515
    sendFile(sock, filename, 8192)

def sendFile2():
    fin = open("filename2", 'r')
    #read and send 8KB by 8KB until theres nothing left
    while True:
        data = fin.read(8192)
        datasz = len(data)
        if datasz==0:
            break
        #chcksum
        chck = 0
        reserved = 0
        print(datasz)
        head = struct.pack('!L', 0xDCC023C2) + struct.pack('!L', 0xDCC023C2)
        #head3 = struct.pack('!L', 0xDCC023C2)
        #head2 = struct.unpack('!L', head3)[0]
        #print(hex(head2))
        #print(binascii.unhexlify(head2))
        mid = struct.pack('!H', datasz) + struct.pack('!H', reserved)
        data = bytes(data,'utf-8')
        msg =  head + struct.pack('!H', chck) + mid + struct.pack('!s', data)
        #chck = checksum(msg)
        msg = head + struct.pack('!H', chck) + mid + struct.pack('!s', data)
        print(msg)

''' 
def sendFile(sock, filename, length):
    f = open(filename, 'r')
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
        data = bytes(data, 'utf-8')
        msg =  head + struct.pack('!H', chck) + mid + struct.pack('!s', data)
        chck = checksum(msg)
        msg = head + struct.pack('!H', chck) + mid + struct.pack('!s', data)
        print(msg)
        sock.send(msg)
'''

def sendFile(sock, filename, length):
    f = open(filename, "rb")
    #read and send 8KB by 8KB until theres nothing left
    while True:
        data = f.read(length)
        datasz = len(data)
        if datasz == 0:
            break
        #chcksum
        chck = 0
        reserved = 0

        head = struct.pack('!L', 0xDCC023C2) + struct.pack('!L', 0xDCC023C2)
        if datasz%2==1:
            leng = datasz+1
        else:
            leng = datasz
        mid = struct.pack('!H', datasz) + struct.pack('!H', reserved)
        #data = bytes(data, 'utf-8')
        print(datasz)
        #print(data)
        msg =  head + struct.pack('@H', chck) + mid + data
        if(len(msg)%2==1):
            #print(len(msg))
            msg += struct.pack('1B',*([0]))
        chck = checksum(msg)
        print(chck)
        #print(len(msg))
        msg = head + struct.pack('@H', chck) + mid + data
        
        if(len(msg)%2==1):
            #print(len(msg))
            #msg += struct.pack('1B',*([0])) 
            chck = checksum(msg+struct.pack('1B',*([0])))    
        else:
            chck = checksum(msg)
        print(chck)
        print(msg)
        #print(len(msg))
        sock.send(msg)

# def receive_message():
#     TCP_IP = '127.0.0.1'
#     TCP_PORT = 51515
#     BUFFER_SIZE = 1024
#     #RECEBER DADOS DANDO UNPACK
#     #ESCREVER DADOS NO ARQUIVO
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((TCP_IP, TCP_PORT))
#     s.listen(1)
#     while(1):
#         (conn, addr) = s.accept()
#         try:
#             sync1 = conn.recv(4)#receive data from client
#             if(sync1 == 0xdcc023c2):
#                 sycn2 = conn.recv(4)#receive data from client
#                 if(sync2 == 0xdcc023c2):
#                     chksum = conn.recv(2)

def receive_message():
    TCP_IP = '127.0.0.1'
    PORT = 51515
    receiveFile("Out_file", TCP_IP, PORT)

def receiveFile(sock, out_file):
    fout = open(out_file, 'wb')
    #(conn, addr) = sock.accept()
    conn = sock
    while True:
        #while 1:
        teste = checkSyncs(socket, conn)
        print(teste)
        if(teste == False):
            break
        print(" did not break")
        data = conn.recv(2)#bytes do checksum
        #check = struct.unpack('!H', data)[0]
        length = conn.recv(2)#bytes do length
        print("LEN === ")
        print(length)
        size = struct.unpack('!H', length)[0]
    #   length = hex(length)
        byte_num = size
        #byte_num = math.ceil(byte_num)
        print(byte_num)
        rsvrd = conn.recv(2)
        payload = conn.recv(byte_num)
        if len(payload)%2==1:
            payload += struct.pack('1B',*([0]))

        #checksum stuff
        frame = struct.pack('!L', 0xdcc023c2)+struct.pack('!L', 0xdcc023c2)+data+length+rsvrd+payload
        check = checksum(frame)
        print(check)
        if check!=0:
            print("FUUUUUUUU")
            break

        #print(bytearray(payload))
        fout.write(bytearray(payload[0:size]))
    #print(hex(payload))
    #payload = struct.unpack('!H', payload)[0]
    #payload.decode()
    #payload = str(payload,'utf-8')
    #print(hex(payload))
    
    #for i in range(length):
    #   print(i)
    #print("chegou no 50")
    fout.close()

    conn.close()

        #print(hex(data))
        #data = data.decode()

def checkSyncs(socket, conn):
    data = conn.recv(1)
    if(len(data) == 0):
        return False
    data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
    #data = hex(data)
    #data = data + 1
    print(hex(data))
    if(data == 0xdc):
        data = conn.recv(1)
        data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
        print(hex(data))
        if(data == 0xc0):
            data = conn.recv(1)
            data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
            print(hex(data))
            if(data == 0x23):
                data = conn.recv(1)
                data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
                print(hex(data))
                if(data == 0xc2):
                    data = conn.recv(1)
                    data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
                    print(hex(data))
                    if(data == 0xdc):
                        data = conn.recv(1)
                        data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
                        print(hex(data))
                    if(data == 0xc0):
                        data = conn.recv(1)
                        data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
                        print(hex(data))
                        if(data == 0x23):
                            data = conn.recv(1)
                            data = struct.unpack('!L', b'\x00' + b'\x00' + b'\x00' + data)[0]
                            print(hex(data))
                            if(data == 0xc2):
                                return True
                            else: checkSyncs(socket, conn)
                        else: checkSyncs(socket, conn)
                    else: checkSyncs(socket, conn)
                else: checkSyncs(socket, conn)
            else: checkSyncs(socket, conn)
        else: checkSyncs(socket, conn)
    else: checkSyncs(socket, conn)

def receiveConnection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    (conn, addr) = s.accept()
    return conn

def main():

    argc = len(sys.argv)
    if argc != 6:
        return

    # 0 exe name 1 file in 2 file out 3 ip 4 port 5 mode

''' lol python
    print("arg0 = ")
    print(sys.argv[0])
    print("arg1 = ")
    print(sys.argv[1])
    print("arg2 = ")
    print(sys.argv[2])
    print("arg3 = ")
    print(sys.argv[3])
    print("arg4 = ")
    print(sys.argv[4])
    print("arg5 = ")
    print(sys.argv[5])'''

    if sys.argv[5]=="ativo":
        sock = makeConnection(sys.argv[3], int(sys.argv[4]))
    elif sys.argv[5]=="passivo":
        sock = receiveConnection(sys.argv[3], int(sys.argv[4]))
    else:
        return

    thread1 = Thread(target=receiveFile, args=(sock, sys.argv[2]))
    thread2 = Thread(target=send_message, args=(sock, sys.argv[1]))
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
