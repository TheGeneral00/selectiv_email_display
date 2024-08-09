import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
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
        if filename.endswith('.html'):
            with open(os.path.join(directory_path, filename), 'r') as file:
                emails.append((filename, file.read()))
    return emails

class EmailWindow(QMainWindow):
    def __init__(self, email_html):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setHtml(email_html)
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Email Viewer")
        self.show()

class App(QApplication):
    def __init__(self, emails):
        super().__init__(sys.argv)
        self.email_windows = [] 
        for email_html in emails:
            window = EmailWindow(email_html[1])
            window.setWindowTitle(email_html[0])
            self.email_windows.append(window)

if __name__ == '__main__':
    # List of HTML content for each email
    email_html_contents = load_emails_from_storage('email_storage')
    app = App(email_html_contents)
    sys.exit(app.exec_())

