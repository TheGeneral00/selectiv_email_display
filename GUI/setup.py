import tkinter as tk 
from tkinter import ttk 
from tkhtmlview import HTMLLabel 
import os

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
        if filename.endswith('.eml'):
            with open(os.path.join(directory_path, filename), 'r') as file:
                emails.append((filename, file.read()))
    return emails

class EmailViewer(tk.Tk):
    def __init__(self, emails):
        super().__init__()
        
        self.emails = emails
        self.current_index = 0

        self.title('Email Viewer')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        for filename, email_content in emails:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=filename)

            email_html = HTMLLabel(frame, html=email_content)
            email_html.pack(expand=True, fill=tk.BOTH)


if __name__ =='__main__':
    directory_path = 'email_storage'
    emails = load_emails_from_storage(directory_path)
    app = EmailViewer(emails)
    app.mainloop()

        
