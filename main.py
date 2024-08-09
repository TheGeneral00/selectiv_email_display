from data.credentials import *
from data.functions import *
from data.credentials import *
from GUI.setup_PyQt5 import start_app

def main():
    imap = login(username, password, imap_server)
    select_mailbox(imap, 'Inbox')
    email_ids = fetch_messages_from_address(imap, addresses)
    select_first_n_emails_to_write(imap, email_ids, 7)
    logout_and_close(imap)
    start_app()
    

if __name__ == '__main__':
    main()
