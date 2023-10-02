# Tre Howard 9/28/23
# CSC285 - Assignment 4.1: Building a Multithreaded Web Server

import socket  # create/manager network sockets for networking communication
import threading  # functionality for thread/multi-threading

# test by putting these into your browser
# http://127.0.0.1:8080/sample.txt
# http://127.0.0.1:8080/sample1.txt
# http://127.0.0.1:8080/totallyarealfile.txt


def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')  # set variable to client_socket, which is a socket object that represents a clients connection
    # reads the http request by client at 1024 bytes, decodes as utf-8 (unicode standard for web), and extracts the filename from request (below)
    filename = request.split()[1].lstrip('/')
    # the two above this line is the HTTP GET request

    # attempts to open and read the file specified by client connected
    # if the file is found, sents a http response with "200 OK" status and sends the file back to the client
    # if the file is NOT found it raises a FileNoteFoundError, sends a http response of "404 Not Found" status and the message (see FileNotFoundError)
    # if any other exception occurs during handling, sends a http response of "500 Internal Server Error" status and the message (see Exception)
    try:
        with open(filename, 'rb') as file:  # r = read, b = binary mode (audio, images, non-text files), rb = read in binary mode
            response = file.read()
            client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n" + response)  #.send means to send the information back to the client, in this case it would be .txt files
    except FileNotFoundError:
        client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\nFile not found.")
    except Exception as e:
        client_socket.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nAn error occurred: " + str(e).encode('utf-8'))

    # b"HTTP/1.1 200 OK\r\n\r\n" is a HTTP response header, b means bytes literal which is a sequence of bytes rather than characters (.recv(1024) above)
    # \r\n\r\n drops two lines and is letting the program know that this is the end of the header
    # when the server sends the header to client, it informs client that the request was successful via HTTP
    # information after \r\n\r\n will be displayed or provided back to user, in this case the .txt file and its contents
    # if you dont end the header, then the information wont go back correctly (example: client_socket.send(b"HTTP/1.1 200 OK" + response) provides a blank white screen

    # closest client connection/request
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket (server_socket) using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))  # this binds the server local/ip address to 127.0.0.1 and port 8080 (can connect via browser)
    server_socket.listen(5)  # will "listen" for client connections up to a max of 5
    print('Server listening on port 8080')

    while True:  # this loop constantly goes and accepts new clients (up to 5 from the listen above)
        client_socket, client_addr = server_socket.accept()  # takes the client_socket (or client connection) as well as their IP address/Port
        print(f'Connection from: {client_addr}')  # when the new client connects, print to console to confirm

        # spawn a new thread to handle the request
        # threading.Thread() is what creates a new thread for each client that connects
        client_thread = threading.Thread(target=handle_request, args=(client_socket,))  # creates a variable for making a new thread, target = function and args = client or inputted variable
        client_thread.start()  #starts the thread that was added to the variable


if __name__ == "__main__":
    main()

