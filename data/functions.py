'''This file is supposed to hold the necessary functions to access and process the emails'''

from email.message import EmailMessage
from email.policy import EmailPolicy
import imaplib
import email
from email.header import decode_header 
import os
from posix import write
import shutil
import re



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
equell 
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
    try:
        path = 'email_storage'
        #creating absolut path if not given
        if not os.path.isabs(path):
            base_dir = os.getcwd()
            path = os.path.join(base_dir, path)

        #create path if not existent
        if not os.path.exists(path):
            os.makedirs(path)
        #otherwise clear directory
        else:
            clear_directory(path)
        for email_id in email_ids[-N:]:
            status, data = imap.fetch(email_id, 'RFC822')
            if status != 'OK':
                print(f'Failed to fetch email with id {email_id}')
            
            raw_email = data[0][1]
            From = get_From(raw_email)
            if f'{From}.eml' in os.listdir(path):
                print(f'Replaced File: {From}.eml')
            write_email_to_file(imap, raw_email, path, From)
            html = extract_html(raw_email) 
            save_html_content(path, html, From)

    except Exception as err:
        print(f'Failed to save emails with error: { err }')


def clear_directory(directory_path):
    '''
    Clears all file from a directory.

    Parameters:
        - directory_path: The path of the directory to clear_directory

    return:
        - None
    '''
    if not os.path.exists(directory_path):
        print(f'Directory does not exist: {directory_path}')
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) #Removes file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as err:
            print(f'Failed to delete {file_path} with error : {err}')


def write_email_to_file(imap, raw_email, storage_path, From):
    '''
    Saves an object to a file in a given directory 

    Parameters:
        - imap: The imap connection object
        - email_id: An email id 
        - storage_path: The path of the storage directory 

    return:
        - None
        - prints to console if saving process was successfull or not

    To Do: 
        - make sure files are save in email_storage
        - if file exsists replace with new file
        - if there are attachements save them to a directory named like the email file
    '''
    try:
        try:
            file_name = clean(From) + ".eml"
        except TypeError as err:
            print(f'Error cleaning From: { err }')
            file_name = 'unknown_From.eml'
        #create complete file path
        path = os.path.join(storage_path, file_name)

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

def get_From(raw_email):
    '''
    Function to return the sender of the email

    Parameters:
        - imap: imap connection object
        - email_id: The id of the email to process 

    return:
        - From: Name of the sender of the Email
    '''
    msg = email.message_from_bytes(raw_email)
    From, encoding =  decode_header(msg['From'])[0]
    if isinstance(From, bytes):
        From = From.decode(encoding or 'utf-8')
    From = clean(From)
    return From


def extract_html(email_content):
    """Extracts HTML content from a raw email."""
    # Very basic extraction - this should be improved for real email parsing
    msg = email.message_from_bytes(email_content)
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True)
            charset = part.get_content_charset() or 'utf-8'
            # return decoded html_content and remove carriage returns
            return html_content.decode(charset).replace('\r', '')
    return ""

def save_html_content(directory_path, html_content, From):
    """Saves HTML content to a separate .html file."""
    html_filename = f'{From}.html'
    html_path = os.path.join(directory_path, html_filename)

    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def load_emails_from_storage(directory_path):
    '''
    Load email contents and display names (like filenames) from .eml files.
    
    Parameters:
        - directory_path: Path where .eml files are stored.

    Returns:
        - List of tuples (filename, email content).
    '''
    emails = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            with open(os.path.join(directory_path, filename), 'r') as file:
                emails.append((filename, file.read()))
    return emails
