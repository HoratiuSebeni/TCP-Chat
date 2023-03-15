import socket
import threading

HOST = '192.168.72.12' #insert the server IP
PORT = 55555 #insert the port for the acces the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receiveMessages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message != 'exit':
                print(f'{message}')
            else:
                client.close()
                break
        except:
            print("Something whent wrong. The connection will be interupt")
            client.close()
            break

def writeMessages():
    while True:
        try:
            client.send(input("").encode('utf-8'))
        except:
            print("Unable to send the message. Try to reconnect to the server")
            client.close()
            break

threading.Thread(target=receiveMessages).start()
threading.Thread(target=writeMessages).start()