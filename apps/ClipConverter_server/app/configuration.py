import os

try:
    from colorama import init, Fore
    CONNECTED = f"{Fore.GREEN}[CONNECTED]{Fore.RESET}"
    DISCONNECTED = f"{Fore.GREEN}[CONNECTED]{Fore.RESET}"
    SERVERSTATED =f"{Fore.BLUE}[SEVER STARTED]{Fore.RESET}" 
except ImportError:
    CONNECTED = "[CONNECTED]"
    DISCONNECTED = "[CONNECTED]"
    SERVERSTATED ="[SEVER STARTED]" 

TCP_PORT = 5000
TCP_IP = "0.0.0.0"
BUFFER_SIZE = 1024
FORMAT = "utf-8"
FOLDER_PATH = f"{os.path.dirname(os.path.realpath(__file__)) }/../server_data"
