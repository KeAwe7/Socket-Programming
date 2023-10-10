#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <pthread.h>
// #include <winsock2.h>
#define PORT 7777
#define SERVER_ADDRESS "127.0.01"

using namespace std;
void* client_thread(void*);
int main() {
WSADATA wsa;
SOCKET client_socket;
sockaddr_in server_address;
char message[1024], response[1024];
int read_size;
char name[20];
cout << "Enter Username: ";
cin.ignore();
cin >> name;
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
cout << "Error initializing Winsock" << endl;
exit(EXIT_FAILURE);
}
if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
cout << "Error creating socket" << endl;
exit(EXIT_FAILURE);
}
server_address.sin_family = AF_INET;
server_address.sin_addr.s_addr = inet_addr(SERVER_ADDRESS);
server_address.sin_port = htons(PORT);
// Connect to server
if (connect(client_socket, (sockaddr*)&server_address, sizeof(server_address)) < 0) {
cout << "Error connecting to server" << endl;
exit(EXIT_FAILURE);
}
pthread_t thread;
pthread_create(&thread, NULL, client_thread, (void*)&client_socket);

// Send messages to server
while (true) {
cout << "\nEnter message: ";
cin.getline(message, 1024);
int i;
for (i = 0; message[i] != '\0'; i++) {
if (message[i] >= 'A' && message[i] <= 'Z') {
message[i] = ("%c", 'Z' - (message[i] - 'A'));
} else if (message[i] >= 'a' && message[i] <= 'z') {
message[i] = ("%c", 'z' - (message[i] - 'a'));
}
}
// Username
char formatted_message[1100]; // Increased size to accommodate the nickname
sprintf(formatted_message, "%s: %s", name, message);
send(client_socket, formatted_message, strlen(formatted_message), 0);
}
closesocket(client_socket);
WSACleanup();
return 0;
}
void* client_thread(void* socket) {
int client_socket = *((int*)socket);
char response[1024];
int read_size;
while (true) {
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
cout << "\n\nServer response: " << response << endl;
}
}
return NULL;
}
//g++ -fdiagnostics-color=always -g Client+.cpp -o Client+.exe -lws2_32 -pthread
