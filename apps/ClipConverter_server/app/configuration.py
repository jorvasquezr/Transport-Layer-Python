import os

try:
    from colorama import init, Fore
    CONNECTED = f"{Fore.GREEN}[CONNECTED]{Fore.RESET}"
    DISCONNECTED = f"{Fore.LIGHTBLACK_EX}[DISCONNECTED]{Fore.RESET}"
    SERVERSTATED =f"{Fore.BLUE}[SEVER STARTED]{Fore.RESET}" 
    RESULT = Fore.LIGHTMAGENTA_EX+'[{}]'+Fore.RESET+': '
except ImportError:
    CONNECTED = "[CONNECTED]"
    DISCONNECTED = "[DISCONNECTED]"
    SERVERSTATED ="[SEVER STARTED]"
    RESULT = '[{}]: ' 

TCP_PORT = 5000
TCP_IP = "0.0.0.0"
BUFFER_SIZE = 1024
FORMAT = "utf-8"
FOLDER_PATH = f"{os.path.dirname(os.path.realpath(__file__)) }/../server_data"
