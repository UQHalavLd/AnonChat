import socket
import threading
from colorama import Fore, Style, init
import random
import re


init()


print(Fore.CYAN + '''
  /$$$$$$  /$$   /$$  /$$$$$$  /$$   /$$        /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$$$
 /$$__  $$| $$$ | $$ /$$__  $$| $$$ | $$       /$$__  $$| $$  | $$ /$$__  $$|__  $$__/
| $$  \ $$| $$$$| $$| $$  \ $$| $$$$| $$      | $$  \__/| $$  | $$| $$  \ $$   | $$   
| $$$$$$$$| $$ $$ $$| $$  | $$| $$ $$ $$      | $$      | $$$$$$$$| $$$$$$$$   | $$   
| $$__  $$| $$  $$$$| $$  | $$| $$  $$$$      | $$      | $$__  $$| $$__  $$   | $$   
| $$  | $$| $$\  $$$| $$  | $$| $$\  $$$      | $$    $$| $$  | $$| $$  | $$   | $$   
| $$  | $$| $$ \  $$|  $$$$$$/| $$ \  $$      |  $$$$$$/| $$  | $$| $$  | $$   | $$   
|__/  |__/|__/  \__/ \______/ |__/  \__/       \______/ |__/  |__/|__/  |__/   |__/   
                                                                                      
                                                                                      
''' + Style.RESET_ALL)
nickname = input("Nickname girin: ")


available_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
user_color = random.choice(available_colors)


server_address = (input("Sunucu adresini girin: "))
server_port = int(input("Sunucu portunu girin: "))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_address, server_port))

def receive():
    while True:
        try:
            
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message.lower() == 'exit':
                print("Çıkış yapılıyor...")
                client.close()
                break
            else:
                
                message_parts = message.split(": ")
                if len(message_parts) == 2:
                    sender_nickname = message_parts[0]
                    message_body = message_parts[1]
                    colored_sender = user_color + sender_nickname + Style.RESET_ALL
                    colored_message = f"{colored_sender}: {message_body}"
                    print(colored_message)
                    
                    
                    save_chat(clean_color_codes(colored_message))
                else:
                    
                    colored_message = user_color + message + Style.RESET_ALL
                    print(colored_message)
                    
                    
                    save_chat(clean_color_codes(colored_message))
        except:
            
            print(Fore.RED + "Bir hata oluştu!" + Style.RESET_ALL)
            client.close()
            break


def clean_color_codes(text):
    return re.sub(r'x1b[[0-9;]*m', '', text)


def save_chat(chat_message):
    with open("chat_history.txt", "a") as chat_file:
        chat_file.write(chat_message + "\n")


def write():
    while True:
        message = input('')
        if message.lower() == '/getchat':
            with open("chat_history.txt", "r") as chat_file:
                chat_history = chat_file.read()
                print(chat_history)
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('utf-8'))
            save_chat(message)  

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
