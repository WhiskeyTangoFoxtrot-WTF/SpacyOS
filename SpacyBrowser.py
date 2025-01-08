from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import sys
import sqlite3
class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)
        self.setWindowTitle('SpacyBrowser')
        self.setGeometry(100, 100, 1200, 800)
        self.style = """
            QMainWindow {
                background-color: #000;
                color: #0f0; 
            }
            QLineEdit {
                background-color: #222;
                color: #0f0;
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #555;
            }
            QPushButton {
                background-color: #222; 
                color: #0f0; 
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #555;
            }
            QPushButton#go_btn {
                background-color: #0f0;
                color: #000;
                border: 1px solid #0f0;
            }
            QTabBar::tab {
                background: #222; 
                color: #0f0; 
                padding: 10px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #0f0; 
                color: #000; 
            }
            QProgressBar {
                border: 1px solid #0f0; 
                border-radius: 5px;
                text-align: center;
                color: #0f0;
            }
            QProgressBar::chunk {
                background-color: #0f0; 
                width: 20px;
            }

        """
        self.setStyleSheet(self.style)
        self.incognito = False
        self.init_db()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search term...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)
        self.add_new_tab(QUrl('http://google.com'), 'New Tab')
        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()
        self.back_btn = QPushButton('<')
        self.back_btn.clicked.connect(self.navigate_back)
        self.forward_btn = QPushButton('>')
        self.forward_btn.clicked.connect(self.navigate_forward)
        self.refresh_btn = QPushButton('⟳')
        self.refresh_btn.clicked.connect(self.refresh_page)
        self.stop_btn = QPushButton('⨂')
        self.stop_btn.clicked.connect(self.stop_loading)
        self.home_btn = QPushButton('🏠')
        self.home_btn.clicked.connect(self.navigate_home)
        self.history_btn = QPushButton('📜')
        self.history_btn.clicked.connect(self.show_history)
        self.incognito_btn = QPushButton('🕵️')
        self.incognito_btn.setCheckable(True)
        self.incognito_btn.clicked.connect(self.toggle_incognito)
        self.bookmark_btn = QPushButton('★')
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.view_bookmarks_btn = QPushButton('⭐')
        self.view_bookmarks_btn.clicked.connect(self.show_bookmarks)
        self.downloads_btn = QPushButton('⬇')
        self.downloads_btn.clicked.connect(self.show_downloads) 
        self.new_tab_btn = QPushButton('New Tab')
        self.new_tab_btn.clicked.connect(self.new_tab)
        self.go_btn = QPushButton('Go')
        self.go_btn.setObjectName('go_btn')
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.refresh_btn)
        self.horizontal.addWidget(self.stop_btn)
        self.horizontal.addWidget(self.home_btn)
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.history_btn)
        self.horizontal.addWidget(self.bookmark_btn)
        self.horizontal.addWidget(self.view_bookmarks_btn)
        self.horizontal.addWidget(self.downloads_btn)
        self.horizontal.addWidget(self.incognito_btn)
        self.horizontal.addWidget(self.new_tab_btn)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(20)
        self.progress_bar.setVisible(False)
        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.show()
    def init_db(self):
        self.conn = sqlite3.connect('browser_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history
                               (id INTEGER PRIMARY KEY, url TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookmarks
                               (id INTEGER PRIMARY KEY, url TEXT)''')
        self.conn.commit()
    def add_new_tab(self, qurl=None, label="Blank"):
        browser = QWebEngineView()
        browser.setUrl(QUrl('http://google.com') if qurl is None else qurl)
        browser.urlChanged.connect(self.update_url)
        browser.loadProgress.connect(self.update_progress)
        browser.loadFinished.connect(self.add_to_history)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.page().titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser, title))
    def update_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)
    def current_browser(self):
        return self.tabs.currentWidget()
    def navigate_back(self):
        self.current_browser().back()
    def navigate_forward(self):
        self.current_browser().forward()
    def refresh_page(self):
        self.current_browser().reload()
    def stop_loading(self):
        self.current_browser().stop()
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://www.google.com/search?q=" + url
        self.current_browser().setUrl(QUrl(url))
    def navigate_home(self):
        self.current_browser().setUrl(QUrl('http://google.com'))
    def new_tab(self):
        self.add_new_tab(QUrl('http://google.com'), 'New Tab')
    def close_tab(self, index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(index)
    def current_tab_changed(self, index):
        qurl = self.current_browser().url()
        self.update_url(qurl)
    def toggle_incognito(self):
        self.incognito = not self.incognito
        if self.incognito:
            self.incognito_btn.setChecked(True)
            self.setWindowTitle('Beebo Browser - Incognito Mode')
            self.setStyleSheet(self.dark_style)
        else:
            self.incognito_btn.setChecked(False)
            self.setWindowTitle('Beebo Browser')
            self.setStyleSheet(self.default_style)
    def update_url(self, q):
        self.url_bar.setText(q.toString())
    def update_progress(self, progress):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(progress)
        if progress == 100:
            self.progress_bar.setVisible(False)
    def add_to_history(self):
        if not self.incognito:
            url = self.current_browser().url().toString()
            self.cursor.execute('INSERT INTO history (url) VALUES (?)', (url,))
            self.conn.commit()
    def show_history(self):
        self.cursor.execute('SELECT url FROM history')
        history_data = self.cursor.fetchall()
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("Browsing History")
        history_dialog.setGeometry(300, 200, 800, 400)
        history_layout = QVBoxLayout()
        history_list = QListWidget()
        history_list.addItems([url[0] for url in history_data])
        history_layout.addWidget(history_list)
        close_button = QPushButton("Close")
        close_button.clicked.connect(history_dialog.close)
        history_layout.addWidget(close_button)
        history_dialog.setLayout(history_layout)
        history_dialog.exec_()
    def add_bookmark(self):
        url = self.current_browser().url().toString()
        self.cursor.execute('INSERT INTO bookmarks (url) VALUES (?)', (url,))
        self.conn.commit()
        QMessageBox.information(self, "Bookmark Added", f"Bookmarked {url}")
    def show_bookmarks(self):
        self.cursor.execute('SELECT url FROM bookmarks')
        bookmarks_data = self.cursor.fetchall()
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        bookmarks_dialog.setGeometry(300, 200, 800, 400)
        bookmarks_layout = QVBoxLayout()
        bookmarks_list = QListWidget()
        bookmarks_list.addItems([url[0] for url in bookmarks_data])
        bookmarks_list.itemClicked.connect(self.load_bookmarked_page)
        bookmarks_layout.addWidget(bookmarks_list)
        close_button = QPushButton("Close")
        close_button.clicked.connect(bookmarks_dialog.close)
        bookmarks_layout.addWidget(close_button)
        bookmarks_dialog.setLayout(bookmarks_layout)
        bookmarks_dialog.exec_()
    def load_bookmarked_page(self, item):
        self.current_browser().setUrl(QUrl(item.text()))
    def show_downloads(self):
        downloads_dialog = QDialog(self)
        downloads_dialog.setWindowTitle("Downloads")
        downloads_dialog.setGeometry(300, 200, 800, 400)
        downloads_layout = QVBoxLayout()
        downloads_list = QListWidget()
        downloads_list.addItems(self.downloads)
        downloads_layout.addWidget(downloads_list)
        close_button = QPushButton("Close")
        close_button.clicked.connect(downloads_dialog.close)
        downloads_layout.addWidget(close_button)
        downloads_dialog.setLayout(downloads_layout)
        downloads_dialog.exec_()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWebBrowser()
    app.exec_()
