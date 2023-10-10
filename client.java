import java.net.*;
import java.io.*;
import java.util.Scanner;


public class Client {
public static void main(String[] args) {
try {

Scanner scanner = new Scanner(System.in);
// Connect to the server
Socket socket = new Socket("127.0.0.1", 7777);
System.out.println("Connected to the server.");
// Create streams for sending and receiving data
OutputStream out = socket.getOutputStream();
InputStream in = socket.getInputStream();
// Create a new thread to receive messages from the server
Thread receiveThread = new Thread(() -> {
while (true) {
try {
// Receive a message from the server
byte[] buffer = new byte[1024];
int len = in.read(buffer);
String received_message = new String(buffer, 0, len);
String decrypted_message = decryptData(received_message);
// Print the decrypted message
System.out.println("\nServer Response: " + decrypted_message);
} catch (IOException e) {
e.printStackTrace();
break;
}
}
});
receiveThread.start();
System.out.println("Enter Username: ");
String name = scanner.nextLine();
while (true) {
// Read a message from the user
System.out.print("\nEnter Message: ");
String message = scanner.nextLine();
String encrypted_message = encryptData(message);
String encrypted_name = encryptData(name);
// Send the encrypted message to the server
out.write(( encrypted_name + ": " +encrypted_message + "\n").getBytes());
}
} catch (IOException e) {
e.printStackTrace();
}
}
// Decrypt

public static String decryptData(String cipherText) {
StringBuilder decrypted = new StringBuilder();
for (char c : cipherText.toCharArray()) {
if (Character.isLetter(c)) {
if (Character.isUpperCase(c)) {
decrypted.append((char) (90 - (c - 65)));
} else {
decrypted.append((char) (122 - (c - 97)));
}
} else {
decrypted.append(c);
}
}
return decrypted.toString();
}
// Encrypt
public static String encryptData(String message){
StringBuilder encrypted = new StringBuilder();
for (char c : message.toCharArray()) {
if (Character.isLetter(c)) {
if (Character.isUpperCase(c)) {
encrypted.append((char) (90 - (c - 65)));
} else {
encrypted.append((char) (122 - (c - 97)));
}
} else {
encrypted.append(c);
}
}
return encrypted.toString();
}
}
