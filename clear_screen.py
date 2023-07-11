import os
import platform


def clear_screen():
    # Clear the console screen based on the platform
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
