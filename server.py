import socket
import threading
key = 5
clients = []
server_address = ('127.0.0.1', 7777)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server started")
def handle_client(client_socket, client_address):
  # Add the client to the list of clients
  clients.append(client_socket)
  print(f"Client {client_address} connected")
  # Receive and Decrypt
  while True:
    try:
    received_message = client_socket.recv(1024).decode()
    if not received_message:
      break
    print("Received from {client_address}: {received_message}")
    
    # received_message = client_socket.recv(1024).decode()
    # if not received_message:
    #   print("Server disconnected")
    #   break
    # # Decrypt
    # decrypted_message = ""
    # for i in range(len(received_message)):
    #   char = received_message[i]
    #   if char.isupper():
    #     decrypted_message += chr(90 - (ord(char) - 65))
    #   elif char.islower():
    #     decrypted_message += chr(122 - (ord(char) - 97))
    #   else:
    #     decrypted_message += char
    # print(f"Received from {client_address}: {received_message}")
    
    # Encrypt
    for c in clients:
      if c != client_socket:
        c.sendall(received_message.encode())
  except:
    break
  
  # Remove Clients
  clients.remove(client_socket)
  print(f"Client {client_address} disconnected")
  client_socket.close()
  
  # Listen
  while True:
    client_socket, client_address = server_socket.accept()
    # Create a separate thread to handle the incoming connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,
  client_address))
    client_thread.start()
