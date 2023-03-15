import socket
import threading

HOST = '192.168.72.12' #insert the server IP
PORT = 55555 #insert the port you want to use

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
adresses = []

def sendMessages(author, message):
    for client in clients:
        client.send(f"{author}: {message}".encode('utf-8'))


def receiveMessages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            noClient = clients.index(client)
            adress = adresses[noClient]
            print(f"{adress}: {message}")

            if message != 'exit':
                sendMessages(adress, message)
            else: 
                print(f"{adress} disconnected!")
                sendMessages(HOST, f"{adress} left the chat")
                client.send("exit".encode('utf-8'))
                adresses.remove(adress)
                clients.remove(client)
                client.close() 
                break   

        except:
            print("Something whent wrong")
            noClient = clients.index(client)
            adress = adresses[noClient]
            sendMessages(HOST, f"{adress} discconneted!")
            clients.remove(client)
            adresses.remove(adress)
            client.close()   
            break     


def acceptConnection():
    while True:
        client, adress = server.accept()
        print(f"Connection established with {adress}")
        client.send("You are connected!".encode('utf-8'))

        if len(clients) > 0 :
            sendMessages(HOST ,f"{adress} is connected")

        clients.append(client)
        adresses.append(adress)
        threading.Thread(target=receiveMessages, args=(client,)).start()


print("Waiting for connections...")
threading.Thread(target=acceptConnection).start()
