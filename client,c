#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <pthread.h>
#define PORT 7777
#define SERVER_ADDRESS "127.0.0.1"
void *client_thread(void *);
int main() {
WSADATA wsa;
SOCKET client_socket;
struct sockaddr_in server_address;
char message[1024], response[1024], encrypted[1024];
int read_size;
char name[20];
printf("Enter Username:");
scanf("%s", name);
getchar();
// Encrypt Username
int i;
for (i = 0; name[i] != '\0'; i++) {
if (name[i] >= 'A' && name[i] <= 'Z') {
name[i] = ("%c", 'Z' - (name[i] - 'A'));
} else if (name[i] >= 'a' && name[i] <= 'z') {
name[i] = ("%c", 'z' - (name[i] - 'a'));
}
}
if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
printf("Error initializing Winsock");
exit(EXIT_FAILURE);
}

if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
printf("Error creating socket");
exit(EXIT_FAILURE);
}
server_address.sin_family = AF_INET;
server_address.sin_addr.s_addr = inet_addr(SERVER_ADDRESS);
server_address.sin_port = htons(PORT);
// Server Connect
if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) <
0) {
printf("Error connecting to server");
exit(EXIT_FAILURE);
}
pthread_t thread;
pthread_create(&thread, NULL, client_thread, (void *)&client_socket);
// Send messages to server
while (1) {
printf("\nEnter message: ");
fgets(message, 1024, stdin);
// Encrypt Caesar
int i;
for (i = 0; message[i] != '\0'; i++) {
if (message[i] >= 'A' && message[i] <= 'Z') {
message[i] = ("%c", 'Z' - (message[i] - 'A'));
} else if (message[i] >= 'a' && message[i] <= 'z') {
message[i] = ("%c", 'z' - (message[i] - 'a'));
}
}
char formatted_message[1100];
sprintf(formatted_message, "%s: %s", name, message);
send(client_socket, formatted_message, strlen(formatted_message), 0);
}
closesocket(client_socket);
WSACleanup();
return 0;
}
void *client_thread(void *socket) {
int client_socket = *((int *)socket);
char response[1024];
int read_size;

while (1)
{
// Receive response from server
if ((read_size = recv(client_socket, response, 1024, 0)) > 0) {
response[read_size] = '\0';
// Decrypt
int i;
for (i = 0; response[i] != '\0'; i++) {
if (response[i] >= 'A' && response[i] <= 'Z') {
response[i] = 'Z' - (response[i] - 'A');
} else if (response[i] >= 'a' && response[i] <= 'z') {
response[i] = 'z' - (response[i] - 'a');
} else if (response[i] == ' ') {
response[i] = ' ';
}
}
response[i] = '\0';
printf("\nServer response: %s\n", response);
}
}
return NULL;
}
//gcc -fdiagnostics-color=always -g Client.c -o Client.exe -lws2_32 -lpthread
