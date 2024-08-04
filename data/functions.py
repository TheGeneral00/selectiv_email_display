'''This file is supposed to hold the necessary functions to access and process the emails'''

import imaplib
import email
from email.header import decode_header
import webbrowser 
import os
#get account credaentials
from credentials import username, password, adresses
#create variable for email provider imap server
imap_server= 'server_webadress'

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

def logout_and_close():
    '''
    This function logs out the user and closes the server connection

    Parameters:
        - imap: The imap connection object

    return:
        None
    '''
    imap.close()
    imap.logout()

# seperated function to change mailbox and return messages if successfull
def select_mailbox(imap, mailbox):
    '''
    Selects a requested mailbox

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
            print(f"Mailbox'{mailbox}' selected!")
            #if selection successfull return messages
            return messages
        else:
            print(f"Failed to select mailbox '{mailbox}'")
    except Exception as err:
        print(f"Failed to select mailbox with error: {err}")

def fetch_n_messages(messages, N):
    '''
    Fetches the top n messages from the mailbox

    Parameters:
        - imap: The imap connection object
        - messages: The number of messages in the mailbox
        - N: The number of messages to fetch

    return: 
        - list of tuples containing the message objects and their senders 
    '''
    for i in range(messages, messages-N, -1):
        #fetch email by adress
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            #parse bytes email into a message obj
            msg = email.message_from_bytes(response[1])
            #decode email subject
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                #if bytes decode to str
                From = From.decode(encoding)
            if select_by_address(From, adresses):
                write_email_to_file(msg, "email_storage")


def select_by_address(messages, adresses):
    '''
    Takes an email adress, or multiple, and selectes the messages from that adresses
    
    Parameters:
        - messages: A list of tuples containing the message object and the sender 
        - adress: A string/A list of strings containing the sender/s adresse/s for which the function sorts

    return:
        - return: A list of tuples where the senders adress is in the given adress list 
    '''
    pass

def write_email_to_file(email_message, path):
    '''
    Saves an object to a file in a given directory 

    Parameters:
        - email_message: The email message object
        - path: A string of a relativ or absolute path to the wanted directory

    return:
        - None
        - prints to console if saving process was successfull or not

    To Do: 
        - make sure files are save in email_storage
        - if there are attachements save them to a directory named like the email file
    '''
    try:
        #creating absolut path if not given
        if not os.path.isabs(path):
            base_dir = os.getcwd()
            path = os.path.join(base_dir, path)
        #create path if not existent
        if not os.path.exists(path):
            os.makedirs(path)
        
        #Decode the email message
        msg = email.message_from_bytes(email_message)

        #decode email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        
        #Get the senders email and decode it if necessary
        From, encoding = decode_header(msg["From"])[0]
        
        #decode From if of type bytes
        if isinstance(From, bytes):
            From = From.decode(encoding)

        #open file to write the email contents to
        #write the Sender to the first line
        with open(path, 'w') as file:
            file.write(f"from: {From}\n")
            file.write('\n')

            #Write email content to the file
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        #get email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    
                    if "attachment" not in content_disposition and content_type == "text/plain":
                        #write email body if its plain text and skip attachments
                        file.write(body)

                    elif "attachment" in content_disposition:
                        #download attachment
                        file_name = part.get_filename()
                        if file_name:
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                os.mkdir(filepath)
                            filepath = os.path.join(folder_name, file_name)
                            # download and save attachment
                            open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                #extract content type
                content_type = msg.get_content_type()
                #get email body
                body = msg.get_payload(decode=True).decode(encoding)
                if content_type == "text/plain":
                    #write only the text email Parameters
                    file.write(body)
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

