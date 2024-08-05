from data.credentials import *
from data.functions import login, logout_and_close

def main():
    imap = login(username, password, imap_server)
    logout_and_close(imap)

if __name__ == '__main__':
    main()
