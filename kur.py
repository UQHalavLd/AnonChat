import socket
import threading
from colorama import Fore, Style, init
import datetime  


init()


host = '127.0.0.1'
port = 8000


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
nicknames = []

def get_chat_log_filename():
    now = datetime.datetime.now()
    
    return "chatlog-{}.txt".format(now.strftime("%Y-%m-%d-%H-%M-%S"))

chat_log_file = open(get_chat_log_filename(), "a")

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            colored_message = Fore.RED + '{} left!'.format(nickname) + Style.RESET_ALL
            broadcast(colored_message)
            nicknames.remove(nickname)
            break

def handle(client):
    while True:
        try:
            
            message = client.recv(1024).decode('utf-8')
            
            
            if message.startswith("/getchat"):
                
                chat_log_file.seek(0)
                history_message = chat_log_file.read()
                client.send(history_message.encode('utf-8'))
            else:
                
                chat_log_file.write(message + "\n")
                chat_log_file.flush()  
                broadcast(message)
        except:
            
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            colored_message = Fore.RED + '{} left!'.format(nickname) + Style.RESET_ALL
            broadcast(colored_message)
            nicknames.remove(nickname)
            break

def receive():
    while True:
        
        client, address = server.accept()
        print(Fore.GREEN + "Connected with {}".format(str(address)) + Style.RESET_ALL)

        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        
        colored_message = Fore.RED + "{} joined!".format(nickname) + Style.RESET_ALL
        print(colored_message)
        broadcast(colored_message)
        client.send('Connected to server!'.encode('utf-8'))

        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
