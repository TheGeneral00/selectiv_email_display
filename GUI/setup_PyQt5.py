import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
from data.functions import load_emails_from_storage

class NotebookApp(QWidget):
    def __init__(self, emails):
        super().__init__()
        self.setWindowTitle('Selectiv Email Display')
        #main layout
        layout = QVBoxLayout(self)
        #creat a widget that organises tabs
        tab_widget = QTabWidget()
        
        #got through emails and create a tab for each
        for filename, email_html in emails:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            
            #load html in WebEngine 
            web_view = QWebEngineView()
            web_view.setHtml(email_html)
            
            #add tab to the manager 
            tab_layout.addWidget(web_view)
            tab.setLayout(tab_layout)
            tab_widget.addTab(tab, filename)

        layout.addWidget(tab_widget)
        self.setLayout(layout)
            

def start_app():
    app = QApplication(sys.argv)

    # List of HTML content for each email
    email_htmls = load_emails_from_storage('email_storage')
    
    #generate app
    notebook_app = NotebookApp(email_htmls)
    notebook_app.show()
    
    #wait for close
    sys.exit(app.exec_())
