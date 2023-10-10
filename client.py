import socket
import sys
import threading

nickname = input("Enter your nickname: ")
server_address = ('127.0.0.1', 7777)
key = 5

#Encrypting Nickname
newNick = ""
for i in range(len(nickname)):
  char = nickname[i]
  if char.isupper():
    newNick += chr(90 - (ord(char) - 65))
  elif char.islower():
    newNick += chr(122 - (ord(char) - 97))
  else:
    newNick += char
nickname = newNick

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
def send_message():
  
# Read input from the user and send it to the server
  while True:
  message = input("Enter message: ")
  # Encrypt the message using Caesar cipher
  encrypted_message = ""
  for i in range(len(message)):
    char = message[i]
    if char.isupper():
      encrypted_message += chr(90 - (ord(char) - 65))
    elif char.islower():
      encrypted_message += chr(122 - (ord(char) - 97))
    else:
      encrypted_message += char
  # Send the encrypted message to the server
  client_socket.sendall((f"{nickname} : " + encrypted_message).encode())
  
def receive_message():
# Receive messages from the server and print them to the console
  while True:
    received_message = client_socket.recv(1024).decode()
    if not received_message:
      print("Server disconnected")
      break
    # Decrypt the message using Caesar cipher
    decrypted_message = ""
    for i in range(len(received_message)):
      char = received_message[i]
      if char.isupper():
        decrypted_message += chr(90 - (ord(char) - 65))
      elif char.islower():
        decrypted_message += chr(122 - (ord(char) - 97))
      else:
        decrypted_message += char
    print("Server Response: " + decrypted_message)
    
# Start two threads, one for sending messages and one for receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)
send_thread.start()
receive_thread.start()
# Wait for both threads to finish
send_thread.join()
receive_thread.join()
# Close the socket
client_socket.close()
