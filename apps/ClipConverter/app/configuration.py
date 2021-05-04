import os
try:
    from colorama import init, Fore
    CLIENT = f'{Fore.GREEN}[CLIENT]{Fore.RESET}: '
    SERVER = f'{Fore.BLUE}[SERVER]{Fore.RESET}: '
    ERROR = f'{Fore.RED}[ERROR]{Fore.RESET}: '
except ImportError:
    CLIENT = '[CLIENT]: '
    SERVER = '[SERVER]: '
    ERROR = '[ERROR]: '
    
FORMAT = "utf-8"
BUFFER_SIZE = 1024
FOLDER_PATH = f"{os.path.dirname(os.path.realpath(__file__)) }/../client_data"


    