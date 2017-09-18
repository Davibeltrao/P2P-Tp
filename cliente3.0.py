from threading import Thread
from time import sleep
import socket
import struct
import sys



def send_message():
    # f = open("myfile", "rb")
    # try:
    #     byte = f.read(1)
    #     while byte != "":
    #         # Do stuff with byte.
    #         byte = f.read(1)
    # finally:
    #     f.close()
    #while(1) fazer tudo abaixo:(ENQUANTO EXISTIREM DADOS NO TXT)
    #VERIFICAR SE SYNC SYNC ESTAO CORRETOS
    #VERIFICAR SE LENGTH > 0
    #VERIFICAR CHECKSUM
    #PULAR 16BITS RESERVED
    #LER DADOS ATE O TAMANHO LENGTH
    #CRIAR SOCKET COM NUMERO DA PORTA DADO E CONECTA-SE AO IP DADO
    #DAR PACK NOS DADOS
    #ENVIAR DADOS
    pass


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