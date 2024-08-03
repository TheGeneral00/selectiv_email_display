'''This file is supposed to hold the necessary functions to access and process the emails'''

import imaplib
import email
from email.header import decode_header
import webbrowser 
import os
#get account credaentials
from credentials import username, password
#create variable for email provider imap server
imap_server= 'server_webadress'

def login(username, password, imap_server, ):
    try:
        #connect to server via SSL 
        imap=imaplib.IMAP4_SSL(imap_server)
        #login with given credentials
        imap.login(username, password)
        print('Logged in successfully!')

        return imap
    #if login failed print the error message to console
    except Exception as err:
        print('Failed to login:', err)
        return None

# seperated function to change mailbox and return messages if successfull
def select_mailbox(imap, mailbox):
    '''
    input: imap from login, mailbox name
    return: if selection worked returns the messages of the mailbox
            else returns None and prints error
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
        print(f"Error selecting mailbox '{mailbox}':" err)

def select_by_adress(messages, adress):
    '''
    takes an email adress, or multiple, and selectes the messages from that adresses
    input: messages, adress
    return: messages from adress
    '''
    
