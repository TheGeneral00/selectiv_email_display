'''This file is supposed to hold the necessary functions to access and process the emails'''

import imaplib
import email
from email.header import decode_header 
import os

def login(username, password, imap_server):
    '''
    Trys to connect to the server with given credentials

    Parameters:
        - username: A string containing the username for the email account
        - password: A string containing the password to the account
        - imap_server: A string containing the server adress

    return:
        - if loggin is successfull returns imap connection object
        - else prints out the error from the loggin attempt
    '''
    try:
        #connect to server via SSL 
        imap=imaplib.IMAP4_SSL(imap_server)
        #login with given credentials
        imap.login(username, password)
        print('Logged in successfully!')
        #return the imap connection object
        return imap
    #if login failed print the error message to console
    except Exception as err:
        print('Failed to login:', err)
        return None

def logout_and_close(imap):
    '''
    This function logs out the user and closes the server connection

    Parameters:
        - imap: The imap connection object

    return:
        None
    '''
    try:
        if imap.select():
            imap.close()
        imap.logout()
        print("Logged out successfully!")
    except Exception as err:
        print(f"Failed to logout with error: {err}")

def select_mailbox(imap, mailbox):
    '''
    Selects a requested mailbox, based on imap.select(), but offers some more feedback

    Parameters:
        - imap: The imap connection object
        - mailbox: A string of the mailbox name

    return: 
        - if selection worked returns the number messages of the mailbox
        - else returns None and prints error
    '''
    try:
        #select where you want to go
        status, messages = imap.select(mailbox)

        if status == 'OK':
            print(f"Mailbox '{mailbox}' selected!")
            #if selection successfull return messages
        else:
            print(f"Failed to select mailbox '{mailbox}'")
    except Exception as err:
        print(f"Failed to select mailbox with error: {err}")

def fetch_messages_from_address(imap, addresses):
    '''
    Fetches the top n messages from the mailbox

    Parameters:
        - imap: The imap connection object
        - messages: The number of messages in the mailbox

    return: 
        - email_ids: A list of email ids  
    '''
    #define serach criteria from given addresses
    search_criteria = ' OR '.join([f'FROM "{email}"' for email in addresses])
    #using search to collect emails fitting the criteria
    status, search_data = imap.search(None, search_criteria)
    email_ids = search_data[0].split()
    #give feedback if no emails matching the criteria 
    if not email_ids:
        print("No emails found from specified addresses.")
        exit()
    #give feedback on found emails
    print(f"Found {len(email_ids)} emails from specified addresses.")
    return email_ids

def select_first_n_emails_to_write(imap, email_ids, N):
    '''
    The function selects the first N emails from the emails ids and fetches the contents to return them.
    
    Parameters:
        - email_ids: A list of email ids from fetch_messages_from_address()
        - N: An integer to specify the amount of messages fetch_messages_from_address

    return:
        - A list containing the first N email ids
    '''
    for email_id in email_ids[-N:]:
        write_email_to_file(imap, email_id)

        

def write_email_to_file(imap, email_id):
    '''
    Saves an object to a file in a given directory 

    Parameters:
        - imap: The imap connection object
        - email_id: An email id 

    return:
        - None
        - prints to console if saving process was successfull or not

    To Do: 
        - make sure files are save in email_storage
        - if file exsists replace with new file
        - if there are attachements save them to a directory named like the email file
    '''
    try:
        path = 'email_storage'
        #creating absolut path if not given
        if not os.path.isabs(path):
            base_dir = os.getcwd()
            path = os.path.join(base_dir, path)

        #create path if not existent
        print("Checkpoint 1")
        if not os.path.exists(path):
            os.makedirs(path)
        print("Checkpoint 2")
        #Decode the email message
        status, data = imap.fetch(email_id, '(RFC822)')

        #Handle cases where no content is fetched 
        if status != 'OK':
            print("Failed to fetch email")
            return None
        print("Checkpoint 3")
        #get raw email
        raw_email = data[0][1]
        #parse raw email
        msg = email.message_from_bytes(raw_email)

        #decode email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding)
        print("Checkpoint 4")
        #create file name as clean subject
        file_name = clean(subject)+ ".eml"
        
        #create complete file path
        path = os.path.join(path, file_name)
        print("Checkpoint 5")
        #open file to write the email contents to
        #write the Sender to the first line
        with open(path, 'wb') as file:
            print(f"File writen to {path}")
            file.write(raw_email)
    
    #give feedback if function call failed
    except Exception as err:
        print(f"An error occurred while processing the email: {err}")

def clean(text):
    '''
    Helperfunction to clean text

    Parameters:
        - text: A string containing the "dirty" text

    return:
        - text: A modified string thats considered "clean"
    '''
    return "".join(c if c.isalnum() else "_" for c in text)

