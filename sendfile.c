#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <sys/socket.h>
#include <arpa/inet.h>


int sendFile(char* filename){

    char data[8304]; //16 bits de enquadramento = 8192 + 112
    int datasz = 0;
    FILE* fin = fopen(filename, "r");
    int sz = fread((void*)(&data[112]), 1, 8192, fin);

    uint32_t* temp = (uint32_t*)data;
    temp[0] = 0xDCC023C2;
    temp[1] = 0xDcc023C2;

    int s = socket(AF_INET, SOCK_STREAM, 0);
    if(s==-1) fprintf(stderr, "ERROR: socket\n");

    struct in_addr addr = { .s_addr = htonl(INADDR_LOOPBACK) };
    struct sockaddr_in dst = { .sin_family = AF_INET,
                               .sin_port = htons(51515),
                               .sin_addr = addr };
    struct sockaddr *sa_dst = (struct sockaddr *)&dst;     

    if(connect(s, sa_dst, sizeof(dst))) fprintf(stderr, "ERROR: connect\n");

    send(s, data, 112+8304, 0);
}

int main(){

}
