import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget
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

class NotebookApp(QWidget):
    def __init__(self, emails):
        super().__init__()
        self.setWindowTitle('Selectiv Email Display')

        layout = QVBoxLayout(self)

        tab_widget = QTabWidget()

        for filename, email_html in emails:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            
            web_view = QWebEngineView()
            web_view.setHtml(email_html)

            tab_layout.addWidget(web_view)
            tab.setLayout(tab_layout)
            tab_widget.addTab(tab, filename)

        layout.addWidget(tab_widget)
        self.setLayout(layout)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # List of HTML content for each email
    email_htmls = load_emails_from_storage('email_storage')
    notebook_app = NotebookApp(email_htmls)
    notebook_app.show()
    
    sys.exit(app.exec_())
