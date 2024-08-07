import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
            window = EmailWindow(email_html)
            self.email_windows.append(window)

if __name__ == '__main__':
    # List of HTML content for each email
    email_html_contents = [
        "<html><body><h1>Email 1 Content</h1></body></html>",
        "<html><body><h1>Email 2 Content</h1></body></html>",
        # Add more emails as needed
    ]
    app = App(email_html_contents)
    sys.exit(app.exec_())

