import os
try:
    from colorama import init, Fore
    CLIENT = f'{Fore.GREEN}[CLIENT]{Fore.RESET}: '
    SERVER = f'{Fore.BLUE}[SERVER]{Fore.RESET}: '
    ERROR = f'{Fore.RED}[ERROR]{Fore.RESET}: '
    RESULT = Fore.LIGHTMAGENTA_EX+'[{}]'+Fore.RESET+': '
except ImportError:
    CLIENT = '[CLIENT]: '
    SERVER = '[SERVER]: '
    ERROR = '[ERROR]: '
    RESULT = '[{}]: '
    
FORMAT = "utf-8"
BUFFER_SIZE = 1024
FOLDER_PATH = f"{os.path.dirname(os.path.realpath(__file__)) }/../client_data"
IP = "127.0.0.1"#"13.89.235.252" 
PORT = 5000
ADDR = (IP, PORT)

    