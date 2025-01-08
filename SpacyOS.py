import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import pickle
import threading
import time
from difflib import get_close_matches
import webbrowser
import psutil
from datetime import datetime,timedelta
from tkinter import simpledialog 
import signal 
from tkinter import filedialog
import platform
import socket
import calendar
from tkinter import ttk
import math
import operator
import uuid
import re
import pytz
from unit_convert import UnitConvert
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import wmi
import pyautogui 
from tkinter import filedialog, messagebox, colorchooser
from tkinter.simpledialog import askstring
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys
import sqlite3
import requests
from threading import Thread
from tkhtmlview import HTMLLabel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import googletrans
import win32gui
import win32con
import win32process
from pywinauto import Desktop, application
VERSION="5.1.0"
CACHE_FILE = "program_cache.pkl"
PROGRAMS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "file explorer": "explorer.exe",
    "command prompt": "cmd.exe",
    "chrome": "chrome.exe",
    "roblox": "Roblox Player.lnk",
    "visual studio code":"code.exe"

}
cancel_requested = False
is_fullscreen = False
command_history = []
history_index = -1
confirm_command = None  
theme = 'dark'
def wifi():
    try:
        output = subprocess.check_output("netsh wlan show networks", shell=True, text=True, stderr=subprocess.STDOUT)  
        networks = []
        lines = output.split("\n")
        for line in lines:
            if "SSID" in line and "BSSID" not in line : 
                ssid = line.split(":")[1].strip()
                networks.append(ssid)
        if networks:
            display_output("\nAvailable Wi-Fi Networks:", animate=True)
            for network in networks:
                display_output(f"- {network}", animate=True)
        else:
            display_output("No Wi-Fi networks found.", animate=True)
    except subprocess.CalledProcessError as e:
        display_output(f"Error listing networks: {e.output}", animate=True)
    except Exception as e: 
        display_output(f"An unexpected error occurred: {e}", animate=True)
def connect_to_wifi(ssid):
    password = simpledialog.askstring("Wi-Fi Password", f"Enter password for {ssid}:", show='*')
    if password:
        try:
            command = f'netsh wlan connect ssid="{ssid}" name="{ssid}" interface=Wi-Fi' 
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True, input=password) 
            display_output(f"Connecting to {ssid}...", animate=True)
        except subprocess.CalledProcessError as e:
            display_output(f"Error connecting to {ssid}: {e.stderr}", animate=True) 
        except Exception as e:
            display_output(f"An unexpected error occurred: {e}", animate=True)
def open_translator():
    display_output(f"Launching Translator... ", speed=200, animate=True)
    log_action("Translator opened.")
    def translate_text():
        try:
            text = input_text.get("1.0", tk.END)
            translated = translator.translate(text, dest=target_lang.get())
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", translated.text)
        except AttributeError as e: 
            if "'NoneType' object has no attribute 'group'" in str(e):
                output_text.delete("1.0", tk.END)
                output_text.insert("1.0", "Translation failed.  Try again or rephrase your input.")
            else:
                output_text.delete("1.0", tk.END)
                output_text.insert("1.0", f"Translation Error:\n{e}")
        except Exception as e: 
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", f"Translation Error:\n{e}")
    translator = googletrans.Translator()
    root = tk.Tk()
    root.title("SpacyTranslator")
    root.configure(bg="black")
    style = ttk.Style()
    style.theme_use("clam") 
    style.configure("TButton", background="darkgreen", foreground="lime", font=("Courier", 12))
    style.configure("TCombobox", fieldbackground="black", foreground="lime", background="darkgreen") 
    style.configure("TScrollbar", troughcolor="black",  background="darkgreen", arrowcolor="lime")
    input_frame = tk.Frame(root, bg="black")
    input_frame.pack(pady=10)
    input_label = tk.Label(input_frame, text="Enter Text:", fg="lime", bg="black", font=("Courier", 12))
    input_label.pack(side=tk.LEFT)
    input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=50, height=10, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12))
    input_text.pack(side=tk.LEFT, padx=5)
    lang_frame = tk.Frame(root, bg="black")
    lang_frame.pack()
    target_lang = tk.StringVar(value="en")  
    target_lang_label = tk.Label(lang_frame, text="Target Language:", fg="lime", bg="black", font=("Courier", 12))
    target_lang_label.pack(side=tk.LEFT,pady=5)
    available_langs = googletrans.LANGUAGES  
    lang_options = list(available_langs.values())
    target_lang_dropdown = ttk.Combobox(lang_frame, textvariable=target_lang, values=lang_options)
    target_lang_dropdown.current(lang_options.index(available_langs['en']))
    target_lang_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True,pady=5)
    translate_button = ttk.Button(root, text="Translate", command=translate_text)
    translate_button.pack(pady=5)
    output_frame = tk.Frame(root, bg="black")
    output_frame.pack()
    output_label = tk.Label(output_frame, text="Translated Text:", fg="lime", bg="black", font=("Courier", 12))
    output_label.pack(side=tk.LEFT)
    output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=50, height=10, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12))  
    output_text.pack(side=tk.LEFT, padx=5)
    root.mainloop()
def weather():
    API_KEY = "b70d044fa49d37c55b39116f15ad2def"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
    def display_weather(data):
        if data.get("cod") != 200:
            weather_label.config(text="City not found!")
            return
        city = data["name"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        wind = data["wind"]["speed"]
        weather_label.config(text=f"{city}\nTemperature: {temp}\u00b0C\n{desc}\nWind Speed: {wind} m/s")
    def display_forecast(data):
        if data.get("cod") != "200" or "list" not in data:
            return
        for widget in forecast_frame.winfo_children():
            widget.destroy()
        forecast_title = tk.Label(forecast_frame, text="5-Day Forecast", font=("Courier", 16, "bold"), bg="black", fg="lime")
        forecast_title.grid(row=0, column=0, pady=10)
        for i, item in enumerate(data["list"][:5]):
            time_text = item["dt_txt"]
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"].capitalize()
            forecast_entry = tk.Label(forecast_frame, text=f"{time_text}\n{temp}\u00b0C, {desc}", font=("Courier", 12), bg="black", fg="lime", justify="center")
            forecast_entry.grid(row=i + 1, column=0, pady=5, sticky="n")
    def animate_text():
        text = "SpacyWeather"
        displayed = ""
        for char in text:
            displayed += char
            title_label.config(text=displayed)
            time.sleep(0.1)
    def threaded_update():
        city = city_entry.get()
        if city:
            thread = Thread(target=update_weather, args=(city,))
            thread.start()
    def fetch_weather(city):
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        return response.json()
    def fetch_forecast(city):
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(FORECAST_URL, params=params)
        return response.json()
    def update_weather(city):
        try:
            weather_data = fetch_weather(city)
            forecast_data = fetch_forecast(city)
            display_weather(weather_data)
            display_forecast(forecast_data)
        except Exception as e:
            weather_label.config(text=f"Error: {e}")
    root = tk.Tk()
    root.title("SpacyWeather")
    root.geometry("800x600")
    root.configure(bg="black")
    title_label = tk.Label(root, text="", font=("Courier", 24, "bold"), bg="black", fg="lime")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
    city_entry = ttk.Entry(root, font=("Courier", 14), justify="center")
    city_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
    city_entry.insert(0, "Enter a City!")
    search_button = ttk.Button(root, text="Get Weather", command=threaded_update)
    search_button.grid(row=2, column=0, columnspan=2, pady=(0, 20))
    weather_label = tk.Label(root, text="", font=("Courier", 14), bg="black", fg="lime", justify="center")
    weather_label.grid(row=3, column=0, columnspan=2, pady=10)
    forecast_frame = ttk.Frame(root, style="Custom.TFrame")
    forecast_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky="n")
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", background="gray10", foreground="lime", padding=6, relief="flat", font=("Courier", 12))
    style.map("TButton", background=[('active', "gray20")])
    style.configure("Custom.TFrame", background="black")
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    city_entry.bind("<Return>", lambda event: threaded_update())
    animation_thread = Thread(target=animate_text, daemon=True)
    animation_thread.start()
    root.mainloop()
def browser():
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
def drawing():
    class DrawingApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Drawing X")
            self.root.geometry("1000x700")
            self.root.configure(bg="black")
            self.pen_color = "lime"
            self.bg_color = "black"
            self.brush_size = 5
            self.font_size = 20
            self.tool = "pen"
            self.text_tool_active = False
            self.text_position = None
            self.text_font = None  
            self.canvas_width = 800
            self.canvas_height = 600
            self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=self.bg_color)
            self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.bg_color)
            self.draw = ImageDraw.Draw(self.image)
            self.controls_frame = tk.Frame(self.root, bg="lightgrey")
            self.controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
            self.create_controls()
            self.canvas.bind("<B1-Motion>", self.paint)
            self.canvas.bind("<ButtonRelease-1>", self.reset)
            self.canvas.bind("<Button-1>", self.set_text_position)
            self.last_x, self.last_y = None, None
        def create_controls(self):
            tk.Label(self.controls_frame, text="Brush Size:", bg="lightgrey").pack(pady=5)
            self.brush_slider = tk.Scale(self.controls_frame, from_=1, to=20, orient=tk.HORIZONTAL, bg="lightgrey")
            self.brush_slider.set(self.brush_size)
            self.brush_slider.pack()
            tk.Label(self.controls_frame, text="Font Size:", bg="lightgrey").pack(pady=5)
            self.font_slider = tk.Scale(self.controls_frame, from_=5, to=100, orient=tk.HORIZONTAL, bg="lightgrey")
            self.font_slider.set(self.font_size)
            self.font_slider.pack()
            tk.Button(self.controls_frame, text="Pick Color", command=self.pick_color, bg="white").pack(pady=10)
            self.create_tool_button("Pen", "pen")
            self.create_tool_button("Brush", "brush")
            self.create_tool_button("Text", "text")
            tk.Button(self.controls_frame, text="Erase All", command=self.erase_all, bg="white").pack(pady=5)
            tk.Button(self.controls_frame, text="Save", command=self.save_image, bg="white").pack(pady=20)
        def create_tool_button(self, text, tool_name):
            button = tk.Button(self.controls_frame, text=text, bg="white", command=lambda: self.select_tool(tool_name))
            button.pack(fill=tk.X, pady=2)
        def pick_color(self):
            color = colorchooser.askcolor()[1]
            if color:
                self.pen_color = color
        def select_tool(self, tool_name):
            if tool_name == "text":
                self.text_tool_active = True
            else:
                self.tool = tool_name
                self.text_tool_active = False
        def paint(self, event):
            x, y = event.x, event.y
            if self.last_x and self.last_y:
                if self.tool == "pen" or self.tool == "brush":
                    self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=self.brush_slider.get(), capstyle="round", smooth=True)
                    self.draw.line((self.last_x, self.last_y, x, y), fill=self.pen_color, width=self.brush_slider.get())
            self.last_x, self.last_y = x, y
        def reset(self, event):
            self.last_x, self.last_y = None, None
        def set_text_position(self, event):
            if self.text_tool_active:
                self.text_position = (event.x, event.y)
                self.font_size = self.font_slider.get()
                self.text_font = ImageFont.truetype("arial.ttf", self.font_size)
                user_text = askstring("Text Input", "Enter your text:")
                if user_text:
                    font_str = f"Arial {self.font_size}"
                    self.canvas.create_text(self.text_position, text=user_text, fill=self.pen_color, font=font_str)
                    self.draw.text(self.text_position, user_text, font=self.text_font, fill=self.pen_color)
                    self.text_tool_active = False
        def erase_all(self):
            self.canvas.delete("all")
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.bg_color)
            self.draw = ImageDraw.Draw(self.image)
        def save_image(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Image Saved", "Your drawing has been saved!")
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
def screenshot():
    save_path = ""
    root = tk.Toplevel()
    root.title("SS System")
    root.geometry("400x250")
    root.config(bg="black")
    def take_screenshot():
        try:
            screenshot_img = pyautogui.screenshot()
            img_dir = os.path.join(os.getcwd(), "img") 
            os.makedirs(img_dir, exist_ok=True)       
            save_path = filedialog.asksaveasfilename(initialdir=img_dir, defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if save_path:
                screenshot_img.save(save_path)
                messagebox.showinfo("Screenshot Saved", f"Screenshot saved to {save_path}")
                log_action(f"Screenshot saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not take screenshot: {e}")
            log_action(f"Screenshot error: {e}")
    screenshot_button = tk.Button(root, text="Take Screenshot", command=take_screenshot, bg="black", fg="lime")
    screenshot_button.pack(pady=20)
    preview_label = tk.Label(root, bg="black")
    preview_label.pack()
    def update_preview():
        try:
            if 'save_path' in locals() and save_path:  
                img = Image.open(save_path)
                img.thumbnail((350, 200))
                photo = ImageTk.PhotoImage(img)
                preview_label.config(image=photo)
                preview_label.image = photo
        except Exception as e:
            log_action(f"Preview update error: {str(e)}")
        root.after(1000, update_preview)
    update_preview()
def converter():
    log_action("Converter Opened.")
    converter_window = tk.Toplevel(root)
    converter_window.title("Unit Converter")
    converter_window.configure(bg="black")
    unit_types = ["length", "mass", "temperature", "currency", "time", "digital storage"]
    from_unit_var = tk.StringVar(converter_window)
    to_unit_var = tk.StringVar(converter_window)
    value_var = tk.StringVar(converter_window)
    unit_type_label = tk.Label(converter_window, text="Select Unit Type:", bg="black", fg="lime")
    unit_type_label.grid(row=0, column=0, padx=5, pady=5)
    unit_type_dropdown = ttk.Combobox(converter_window, values=unit_types, state="readonly") 
    unit_type_dropdown.current(0)  
    unit_type_dropdown.grid(row=0, column=1, padx=5, pady=5)
    from_unit_label = tk.Label(converter_window, text="From Unit:", bg="black", fg="lime")
    from_unit_label.grid(row=1, column=0, padx=5, pady=5)
    from_unit_dropdown = ttk.Combobox(converter_window, textvariable=from_unit_var, state="readonly")
    from_unit_dropdown.grid(row=1, column=1, padx=5, pady=5)
    to_unit_label = tk.Label(converter_window, text="To Unit:", bg="black", fg="lime")
    to_unit_label.grid(row=2, column=0, padx=5, pady=5)
    to_unit_dropdown = ttk.Combobox(converter_window, textvariable=to_unit_var, state="readonly")
    to_unit_dropdown.grid(row=2, column=1, padx=5, pady=5)
    value_label = tk.Label(converter_window, text="Value:", bg="black", fg="lime")
    value_label.grid(row=3, column=0, padx=5, pady=5)
    value_entry = tk.Entry(converter_window, textvariable=value_var, bg="black", fg="lime")
    value_entry.grid(row=3, column=1, padx=5, pady=5)
    result_label = tk.Label(converter_window, text="", bg="black", fg="lime")
    result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    class UnitConvert:
        def __init__(self, unit_type):
            self.unit_type = unit_type
            self.units = {
                "length": ["millimeters", "centimeters", "meters", "kilometers", "inches", "feet", "yards", "miles"],
                "mass": ["milligrams", "grams", "kilograms", "metric_tons", "ounces", "pounds", "stones"],
                "temperature": ["celsius", "fahrenheit", "kelvin"],
                "currency": ["USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "HKD", "SGD"],
                "time": ["nanoseconds", "microseconds", "milliseconds", "seconds", "minutes", "hours", "days", "weeks", "months", "calendar years"],
                "digital storage": ["bits", "bytes", "kilobytes", "kibibytes", "megabytes", "mebibytes", "gigabytes", "gibibytes", "terabytes", "tebibytes", "petabytes", "pebibytes", "exabytes", "exbibytes", "zettabytes", "zebibytes", "yottabytes", "yobibytes"]
            }
        def available_units(self):
            return self.units.get(self.unit_type, [])
        def convert(self, from_unit, to_unit, value):
            try:
                value = float(value)
            except ValueError:
                return "Invalid input value"
            if self.unit_type == "length":
                lengths = {
                    "millimeters": 0.001,
                    "centimeters": 0.01,
                    "meters": 1,
                    "kilometers": 1000,
                    "inches": 0.0254,
                    "feet": 0.3048,
                    "yards": 0.9144,
                    "miles": 1609.344
                }
                if from_unit in lengths and to_unit in lengths:
                    return value * lengths[from_unit] / lengths[to_unit]
            elif self.unit_type == "mass":
                masses = {
                    "milligrams": 0.000001,
                    "grams": 0.001,
                    "kilograms": 1,
                    "metric_tons": 1000,
                    "ounces": 0.0283495231,
                    "pounds": 0.45359237,
                    "stones": 6.35029318

                }
                if from_unit in masses and to_unit in masses:
                    return value * masses[from_unit] / masses[to_unit]
            elif self.unit_type == "temperature":
                if from_unit == "celsius" and to_unit == "fahrenheit":
                    return (value * 9/5) + 32
                elif from_unit == "fahrenheit" and to_unit == "celsius":
                    return (value - 32) * 5/9
                elif from_unit == "celsius" and to_unit == "kelvin":
                    return value + 273.15
                elif from_unit == "kelvin" and to_unit == "celsius":
                    return value - 273.15
                elif from_unit == "fahrenheit" and to_unit == "kelvin":
                    return (value - 32) * 5/9 + 273.15
                elif from_unit == "kelvin" and to_unit == "fahrenheit":
                    return (value - 273.15) * 9/5 + 32
            elif self.unit_type == "currency":
                 return "Currency conversion requires real-time data. Not yet implemented."
            elif self.unit_type == "time":
                times = {
                    "nanoseconds": 1e-9,
                    "microseconds": 1e-6,
                    "milliseconds": 1e-3,
                    "seconds": 1,
                    "minutes": 60,
                    "hours": 3600,
                    "days": 86400,
                    "weeks": 604800,
                    "months": 2629800, 
                    "calendar years": 31557600 
                }
                if from_unit in times and to_unit in times:
                    return value * times[from_unit] / times[to_unit]
            elif self.unit_type == "digital storage":
                digital_storage_units = {
                    "bits": 1 / 8,
                    "bytes": 1,
                    "kilobytes": 1000,
                    "kibibytes": 1024,
                    "megabytes": 1000**2,
                    "mebibytes": 1024**2,
                    "gigabytes": 1000**3,
                    "gibibytes": 1024**3,
                    "terabytes": 1000**4,
                    "tebibytes": 1024**4,
                    "petabytes": 1000**5,
                    "pebibytes": 1024**5,
                    "exabytes": 1000**6,
                    "exbibytes": 1024**6,
                    "zettabytes": 1000**7,
                    "zebibytes": 1024**7,
                    "yottabytes": 1000**8,
                    "yobibytes": 1024**8,
                }
                if from_unit in digital_storage_units and to_unit in digital_storage_units:
                    return value * digital_storage_units[from_unit] / digital_storage_units[to_unit]
            return "Conversion not yet implemented"
    def update_unit_options(event=None):
        selected_type = unit_type_dropdown.get()
        try:
            converter = UnitConvert(selected_type)
            available_units = converter.available_units()
            from_unit_dropdown["values"] = available_units
            to_unit_dropdown["values"] = available_units
            if available_units:
                from_unit_var.set(available_units[0])
                to_unit_var.set(available_units[0])
            else:
                from_unit_var.set("")
                to_unit_var.set("")
        except Exception as e:
            print(f"Error updating units: {e}")
            result_label.config(text=f"Error: {e}")
    def convert():
        try:
            value = float(value_var.get())
        except ValueError:
            result_label.config(text="Invalid input value.")
            return
        selected_type = unit_type_dropdown.get()
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()
        try:
            converter = UnitConvert(selected_type)
            result = converter.convert(from_unit, to_unit, value)
            result_label.config(text=f"{result} {to_unit}")
        except Exception as e:
            result_label.config(text=f"Conversion error: {e}")
    convert_button = tk.Button(converter_window, text="Convert", command=convert, bg="black", fg="lime")
    convert_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    unit_type_dropdown.bind("<<ComboboxSelected>>", update_unit_options)
    update_unit_options()
def explorer():
    root = tk.Tk()
    root.title("File Explorer")
    root.geometry("800x600")
    root.config(bg="black")
    file_listbox = tk.Listbox(root, bg="black", fg="green", selectmode=tk.SINGLE, font=("Courier", 12))
    file_listbox.pack(fill=tk.BOTH, expand=True)
    def update_file_list(path):
        file_listbox.delete(0, tk.END)
        try:
            files = os.listdir(path)
            for file in files:
                file_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not access path: {path}")
            log_action(f"Error accessing path {path}: {e}")
    def ask_for_drive():
        drive = simpledialog.askstring("Select Drive", "Type the drive letter (e.g., C:, D:, E:):")
        if drive and os.path.exists(drive + ":\\"):
            current_dir.set(drive + ":\\")
            update_file_list(drive + ":\\")
            log_action(f"Drive selected: {drive}")
        else:
            messagebox.showerror("Error", "Invalid drive. Try again.")
            log_action("Invalid drive entered.")
    def open_selected_file(event):
        selected_item = file_listbox.get(file_listbox.curselection())
        current_path = current_dir.get()
        selected_path = os.path.join(current_path, selected_item)
        if os.path.isdir(selected_path):
            current_dir.set(selected_path)
            update_file_list(selected_path)
            log_action(f"Entered folder: {selected_path}")
        else:
            log_action(f"Opened file: {selected_path}")
    def go_up():
        current_path = current_dir.get()
        parent_dir = os.path.dirname(current_path)
        if parent_dir != current_path:
            current_dir.set(parent_dir)
            update_file_list(parent_dir)
            log_action(f"Moved up to: {parent_dir}")
    def move_file():
        try:
            selected_item = file_listbox.get(file_listbox.curselection())
        except tk.TclError:
            messagebox.showerror("Error", "No file selected!")
            log_action("Attempted move but no file selected.")
            return
        current_path = current_dir.get()
        source_path = os.path.join(current_path, selected_item)
        destination = filedialog.askdirectory(title="Select Destination Directory")
        if destination:
            destination_path = os.path.join(destination, selected_item)
            try:
                os.rename(source_path, destination_path)
                update_file_list(current_dir.get())
                log_action(f"Moved {source_path} to {destination_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not move file: {str(e)}")
                log_action(f"Error moving {source_path}: {str(e)}")
    def rename_file():
        try:
            selected_item = file_listbox.get(file_listbox.curselection())
        except tk.TclError:
            messagebox.showerror("Error", "No file selected!")
            log_action("Attempted rename but no file selected.")
            return
        current_path = current_dir.get()
        source_path = os.path.join(current_path, selected_item)
        new_name = simpledialog.askstring("Rename File", f"Enter a new name for {selected_item}:")
        if new_name:
            new_path = os.path.join(current_path, new_name)
            try:
                os.rename(source_path, new_path)
                update_file_list(current_dir.get())
                log_action(f"Renamed {source_path} to {new_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename file: {str(e)}")
                log_action(f"Error renaming {source_path}: {str(e)}")
    def delete_file():
        try:
            selected_item = file_listbox.get(file_listbox.curselection())
        except tk.TclError:
            messagebox.showerror("Error", "No file selected!")
            log_action("Attempted delete but no file selected.")
            return
        current_path = current_dir.get()
        selected_path = os.path.join(current_path, selected_item)
        try:
            os.remove(selected_path)
            update_file_list(current_dir.get())
            log_action(f"Deleted {selected_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file: {str(e)}")
            log_action(f"Error deleting {selected_path}: {str(e)}")
    def create_file():
        file_name = simpledialog.askstring("Create File", "Enter the file name with extension (e.g., file.py, note.txt):")
        if file_name:
            current_path = current_dir.get()
            file_path = os.path.join(current_path, file_name)
            try:
                with open(file_path, "w") as f:
                    f.write("")
                update_file_list(current_dir.get())
                log_action(f"Created file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create file: {str(e)}")
                log_action(f"Error creating file {file_path}: {str(e)}")
    def create_folder():
        folder_name = simpledialog.askstring("Create Folder", "Enter the folder name:")
        if folder_name:
            current_path = current_dir.get()
            folder_path = os.path.join(current_path, folder_name)
            try:
                os.mkdir(folder_path)
                update_file_list(current_dir.get())
                log_action(f"Created folder: {folder_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create folder: {str(e)}")
                log_action(f"Error creating folder {folder_path}: {str(e)}")
    current_dir = tk.StringVar(root, value=os.getcwd())
    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(fill=tk.X)
    back_button = tk.Button(button_frame, text="Back", command=go_up, bg="black", fg="green", font=("Courier", 12))
    back_button.pack(side=tk.LEFT)
    action_menu_frame = tk.Frame(root, bg="black")
    action_menu_frame.pack(fill=tk.X)
    move_button = tk.Button(action_menu_frame, text="1. Move File", command=move_file, bg="black", fg="green", font=("Courier", 12))
    move_button.pack(side=tk.LEFT)
    rename_button = tk.Button(action_menu_frame, text="2. Rename File", command=rename_file, bg="black", fg="green", font=("Courier", 12))
    rename_button.pack(side=tk.LEFT)
    delete_button = tk.Button(action_menu_frame, text="3. Delete File", command=delete_file, bg="black", fg="green", font=("Courier", 12))
    delete_button.pack(side=tk.LEFT)
    create_file_button = tk.Button(action_menu_frame, text="4. Create File", command=create_file, bg="black", fg="green", font=("Courier", 12))
    create_file_button.pack(side=tk.LEFT)
    create_folder_button = tk.Button(action_menu_frame, text="5. Create Folder", command=create_folder, bg="black", fg="green", font=("Courier", 12))
    create_folder_button.pack(side=tk.LEFT)
    close_button = tk.Button(action_menu_frame, text="X", command=root.quit, bg="red", fg="white", font=("Courier", 14), bd=0, relief="flat")
    close_button.pack(side=tk.RIGHT)
    ask_for_drive()
    file_listbox.bind("<Double-1>", open_selected_file)
def find_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None
def kill_process(identifier, force=False):
    killed_processes = []
    try:
        pid = int(identifier)
        process_name = None
        try:
            process = psutil.Process(pid)
            process_name = process.name()
        except psutil.NoSuchProcess:
             display_output(f"Process with PID '{identifier}' not found.", animate=True)
             return
    except ValueError:
        process_name = identifier
        pid = None
    if process_name:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    try:
                        if force:
                            proc.send_signal(signal.SIGKILL)
                        else:
                            proc.send_signal(signal.SIGTERM)
                        killed_processes.append(proc.info['pid'])
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        display_output(f"Error: Could not terminate process {proc.info['pid']}.", animate=True)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    if killed_processes:
        if pid:
            display_output(f"Process {identifier} (PID: {pid}) {'force-' if force else ''}terminated.", animate=True)
        else:
            display_output(f"{'Force-' if force else ''}Terminated processes named {identifier}: {killed_processes}", animate=True)
    elif pid is not None:
        display_output(f"No processes found matching '{identifier}'.", animate=True)
def change_process_priority(identifier, priority):
    try:
        pid = int(identifier)
    except ValueError:
        pid = find_process_by_name(identifier)
        if pid is None:
            display_output(f"Process '{identifier}' not found.", animate=True)
            return
    try:
        process = psutil.Process(pid)
        if priority.lower() == "high":
            process.nice(psutil.HIGH_PRIORITY_CLASS) 
        elif priority.lower() == "normal":
            process.nice(psutil.NORMAL_PRIORITY_CLASS)
        else:
            display_output(f"Invalid priority. Use 'high', 'normal', etc.", animate=True)
            return
        display_output(f"Set priority of process {identifier} (PID: {pid}) to {priority}.", animate=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        display_output(f"Could not change priority of process {identifier}.", animate=True)
def suspend_resume_process(identifier, action):
    try:
        pid = int(identifier)
    except ValueError:
        pid = find_process_by_name(identifier)
        if pid is None:
            display_output(f"Process '{identifier}' not found.", animate=True)
            return
    try:
        process = psutil.Process(pid)
        if action == "suspend":
            process.suspend()
        elif action == "resume":
            process.resume()
        else:
            display_output("Invalid action. Use 'suspend' or 'resume'.", animate=True)
            return
        display_output(f"{action.title()}ed process {identifier} (PID: {pid}).", animate=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        display_output(f"Could not {action} process {identifier}.", animate=True)
def ping(host):
    try:
        response = subprocess.check_output(["ping", "-n", "4", host], text=True, stderr=subprocess.STDOUT)
        display_output(response)  
    except subprocess.CalledProcessError as e:
        display_output(f"Error: {e}")
def traceroute(host):
    target = host or "localhost"
    try:
        if platform.system() == "Windows":
            response = subprocess.check_output(["tracert", host])
            display_output(response.decode(), animate=True)
        else:  
            response = subprocess.check_output(["traceroute", host])
            display_output(response.decode(), animate=True)

    except subprocess.CalledProcessError as e:
        display_output(f"Traceroute to {host} failed: {e.returncode}", animate=True)
    except FileNotFoundError:
        display_output("traceroute/tracert command not found.", animate=True)
def show_clock():
    clock_window = tk.Toplevel(root)
    clock_window.title("Clock")
    city = tk.StringVar(clock_window, value="Local")
    city_entry = tk.Entry(clock_window, textvariable=city, bg="black", fg="lime", font=("default", 12))
    city_entry.pack(pady=5)
    clock_label = tk.Label(clock_window, font=("default", 48), bg="black", fg="lime")  # Initialize clock_label
    clock_label.pack(padx=20, pady=20)
    def update_clock():
        city_name = city.get().title().strip()
        try:
            if city_name.lower() == 'local':
                current_time = datetime.now().strftime("%H:%M:%S")
                clock_label.config(text=f"Local Time: {current_time}")  
            else:
                try:
                    timezone = pytz.timezone(city_name)
                except pytz.UnknownTimeZoneError:
                    try:
                        tf = TimezoneFinder()
                        geolocator = Nominatim(user_agent="geo_app")  
                        location = geolocator.geocode(city_name)
                        if location:
                            longitude = location.longitude
                            latitude = location.latitude
                            timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
                            if timezone_str:
                                timezone = pytz.timezone(timezone_str)
                            else:
                                raise pytz.UnknownTimeZoneError
                        else:
                            raise pytz.UnknownTimeZoneError
                    except pytz.UnknownTimeZoneError:
                        clock_label.config(text=f"Invalid City: {city_name}")
                        clock_label.after(1000, update_clock)
                        return
                current_time = datetime.now(timezone).strftime("%H:%M:%S")
                clock_label.config(text=f"{city_name}: {current_time}")
        except Exception as e:
            print(f"Error in update_clock: {e}")  
            clock_label.config(text="Error")  
        clock_label.after(1000, update_clock)
    update_clock()  
def get_wifi_name():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, shell=True
        )
        output = result.stdout
        for line in output.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
        return "N/A"
    except Exception:
        return "N/A"
def save_program_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(PROGRAMS, f)
def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        display_output(f"Hostname: {hostname}", animate=True)
        display_output(f"IP Address: {ip_address}", animate=True)
        interfaces = psutil.net_if_addrs()
        for interface_name, interface_addresses in interfaces.items():
            display_output(f"Interface: {interface_name}", animate=True)
            for address in interface_addresses:
                display_output(f"  - Family: {address.family.name}, Address: {address.address}", animate=True)
                if address.netmask:
                    display_output(f"    Netmask: {address.netmask}", animate=True)
                if address.broadcast:
                    display_output(f"    Broadcast: {address.broadcast}", animate=True)
    except Exception as e:
        display_output(f"Error getting network information: {e}", animate=True)
class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("SpacyOS Calculator")
        master.configure(bg="black")  
        self.display = tk.Entry(master, width=30, borderwidth=0, bg="black", fg="lime", font=("Consolas", 18), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sin', 'cos', 'tan', 'sqrt',
            'C', 'del', '(', ')'

        ]
        row = 1
        col = 0
        for button in buttons:
            command = lambda x=button: self.button_click(x)
            if button in ('=', '+', '-', '*', '/', 'sin', 'cos', 'tan', 'sqrt', '(', ')', 'C', 'del'): 
                tk.Button(master, text=button, width=5, height=2, command=command, bg="#2c3e50", fg="white", activebackground="#34495e", relief="flat").grid(row=row, column=col, padx=2, pady=2, sticky="nsew") 
            else: 
                tk.Button(master, text=button, width=5, height=2, command=command, bg="#3498db", fg="white", activebackground="#2980b9", relief="flat").grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
    def button_click(self, value):
        current = self.display.get()
        if value == '=':
            try:
                result = str(eval(current)) 
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
            except (SyntaxError, ZeroDivisionError, NameError, TypeError, ValueError) as e:  
                messagebox.showerror("Error", str(e))  
                self.display.delete(0, tk.END)  
        elif value == 'C':
            self.display.delete(0, tk.END)  
        elif value == 'del':
            self.display.delete(len(self.display.get()) - 1)  
        elif value in ('sin', 'cos', 'tan', 'sqrt'):
            try:
                if value == 'sin':
                    result = math.sin(math.radians(float(current)))
                elif value == 'cos':
                    result = math.cos(math.radians(float(current)))
                elif value == 'tan':
                    result = math.tan(math.radians(float(current)))
                elif value == 'sqrt':
                    result = math.sqrt(float(current))

                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))

            except (ValueError, TypeError): 
                messagebox.showerror("Error", "Invalid input for function")
                self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, value)
def open_calculator(): 
    calculator_window = tk.Toplevel(root)
    calculator = Calculator(calculator_window)
    log_action("Calculator Opened.")  
CALENDAR_DATA_FILE = "calendar_data.pkl"
def load_calendar_data():
    if os.path.exists(CALENDAR_DATA_FILE):
        try:
            with open(CALENDAR_DATA_FILE, "rb") as f:
                return pickle.load(f)
        except EOFError:
            return {}
    else:
        return {}
def save_calendar_data(calendar_data):
    with open(CALENDAR_DATA_FILE, "wb") as f:
        pickle.dump(calendar_data, f)
calendar_data = load_calendar_data()
def show_calendar():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    calendar_window = tk.Toplevel()
    calendar_window.title(f"Calendar for {calendar.month_name[month]} {year}")
    calendar_window.geometry("400x500")  
    header_frame = tk.Frame(calendar_window, bg="black")
    header_frame.pack(pady=10)
    def update_calendar(month, year):
        cal_str = calendar.month(year, month)
        cal_label.config(text=cal_str)
        calendar_window.title(f"Calendar for {calendar.month_name[month]} {year}")
    def prev_month():
        nonlocal month, year
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        update_calendar(month, year)
    def next_month():
        nonlocal month, year
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        update_calendar(month, year)
    prev_button = tk.Button(header_frame, text="<", command=prev_month, bg="black", fg="lime", relief="flat")
    prev_button.pack(side="left", padx=10)
    cal_label = tk.Label(header_frame, text=calendar.month(year, month), font=("Courier", 10), bg="black", fg="lime")
    cal_label.pack(side="left")
    next_button = tk.Button(header_frame, text=">", command=next_month, bg="black", fg="lime", relief="flat")
    next_button.pack(side="left", padx=10)
    days_frame = tk.Frame(calendar_window, bg="black")
    days_frame.pack(pady=10)
    def on_day_click(day):
        if (year, month, day) in calendar_data:
            display_output(f"Note for {year}-{month}-{day}: {calendar_data[(year, month, day)]}", animate=True)
        else:
            note = simpledialog.askstring("Input", f"Enter note for {year}-{month}-{day}:")
            if note:
                calendar_data[(year, month, day)] = note
                save_calendar_data(calendar_data)
                display_output(f"Note saved for {year}-{month}-{day}.", animate=True)
    def create_day_buttons():
        for widget in days_frame.winfo_children():
            widget.destroy()
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            day_button = tk.Button(days_frame, text=str(day), command=lambda d=day: on_day_click(d),
                                   bg="black", fg="lime", relief="flat", width=4)
            day_button.grid(row=(day-1)//7, column=(day-1)%7, padx=5, pady=5)  
    create_day_buttons()
    done_button = tk.Button(calendar_window, text="Done", command=calendar_window.destroy, bg="black", fg="lime", relief="flat")
    done_button.pack(pady=10)
    update_calendar(month, year)
def load_program_cache():
    global PROGRAMS
    if os.path.exists(CACHE_FILE):
        try:  
            with open(CACHE_FILE, "rb") as f:
                PROGRAMS.update(pickle.load(f))
        except EOFError:
            display_output("Cache file is corrupted or empty. Recreating...", speed=200, animate=True)
            save_program_cache() 
def update_metrics():
    while True:
        battery = psutil.sensors_battery()
        battery_percent = f"Battery: {battery.percent}%" if battery else "Battery: N/A"
        wifi_name = get_wifi_name()
        ram_usage = f"RAM: {psutil.virtual_memory().percent}%"
        cpu_usage = f"CPU: {psutil.cpu_percent()}%"
        disk_usage = f"Disk: {psutil.disk_usage('/').percent}%"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_label.config(
            text=f"{battery_percent}  |  Wi-Fi: {wifi_name}  |  {ram_usage}  |  {cpu_usage}  |  {disk_usage}  |  {current_time}",
            font=("Consolas", 14)  
        )
        time.sleep(1)
def scan_for_programs():
    global cancel_requested
    display_output("Scanning for programs... Please wait.", speed=200, animate=True)
    common_paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        os.path.expanduser("~\\AppData\\Local\\Programs"),
    ]
    for path in common_paths:
        for root, dirs, files in os.walk(path):
            if cancel_requested:
                cancel_requested = False
                return
            for file in files:
                if file.endswith(".exe"):
                    program_name = file.lower().replace(".exe", "")
                    full_path = os.path.join(root, file)
                    PROGRAMS[program_name] = full_path
    save_program_cache()
    display_output("Program scan complete.", speed=200, animate=True)
def async_scan():
    thread = threading.Thread(target=scan_for_programs, daemon=True)
    thread.start()
def display_hardware_info():
    display_output("Hardware Information:", animate=True)
    display_output(f"  OS: {platform.system()} {platform.release()} (SpacyOS V"+VERSION+")", animate=True)
    display_output(f"  System: {platform.system()}", animate=True) 
    display_output(f"  Node Name: {platform.node()}", animate=True)
    display_output(f"  Release: {platform.release()}", animate=True)
    display_output(f"  Version: {platform.version()}", animate=True)
    display_output(f"  Machine: {platform.machine()}", animate=True)
    display_output(f"  Processor: {platform.processor()}", animate=True)
    try:
        c = wmi.WMI()
        system_info = c.Win32_ComputerSystem()[0]
        model = system_info.Model
        display_output(f"  Model: {model}", animate=True)
    except ImportError:
        display_output("  Model: WMI not available (install 'wmi' package)", animate=True)
    except Exception as e:
        display_output(f"  Model: Error retrieving model info: {e}", animate=True)
    display_output("  CPU Cores:", animate=True)
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        display_output(f"    Core {i}: {percentage}%", animate=True)
    display_output(f"    Total CPU Usage: {psutil.cpu_percent()}%", animate=True)
    
    mem = psutil.virtual_memory()
    display_output(f"  RAM: {mem.total / (1024.0 ** 3):.1f}GB (Total)", animate=True)
    display_output(f"  Available RAM: {mem.available / (1024.0 ** 3):.1f}GB", animate=True)
    display_output(f"  Used RAM: {mem.used / (1024.0 ** 3):.1f}GB", animate=True)
def launch_program(command):
    match = find_closest_match(command)
    if match:
        try:
            display_output(f"Launching {match.title()}... Please wait.", speed=200, animate=True)
            subprocess.Popen(PROGRAMS[match], shell=True)
        except Exception as e:
            display_output(f"Error launching {match}: {e}", speed=200, animate=True)
    else:
        display_output(f"Program '{command}' not found. Consider refreshing the cache.", speed=200, animate=True)
        async_scan()
def find_closest_match(command):
    program_names = PROGRAMS.keys()
    matches = get_close_matches(command.lower(), program_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

def cancel_command():
    global cancel_requested
    cancel_requested = True
    display_output("Operation canceled.", speed=200, animate=True)
def list_programs():
    if PROGRAMS:
        display_output("Available Programs:", animate=True)
        for program in sorted(PROGRAMS.keys()):
            display_output(f" - {program}", animate=True)
    else:
        display_output("No programs found. Use 'refresh cache' to update the program list.", animate=True)
def display_help():
   commands = {
        "launch <program>": "Launches a program by name.",
        "list programs": "Lists all programs currently in the cache.",
        "refresh cache": "Scans the system for new programs and updates the cache.",
        "del": "Cancels the current operation, such as a scan.",
        "clear": "Clears the terminal output.",
        "browser": "Opens a built-in web browser.",
        "help": "Displays this help menu.",
        "f11": "Toggles fullscreen mode.",
        "exit": "Exits SpacyOS.",
        "shutdown": "Shuts down the computer after confirmation.",
        "restart": "Restarts the computer after confirmation.",
        "ps": "Lists running processes.",
        "editor": "Opens the built-in text editor.",
        "h-info": "Displays detailed hardware information (CPU, RAM, OS, etc.).",
        "netinfo": "Displays network information (IP address, hostname, etc.).",
        "setpriority <pid> <priority>": "Changes the priority of a process (priority: high, normal, etc.).", 
        "calendar": "Displays a calendar for a specified month and year.",                                       
        "terminal": "Opens the PC terminal (On Work)",
        "drawing.editor": "Opens the drawing editor (SpacyOS Built In)",   
        "kill <pid/process_name>": "Terminates a process by its ID or name.",
        "setpriority <pid/process_name> <priority>": "Changes process priority (high, normal).",
        "suspend <pid/process_name>": "Suspends a process.",
        "resume <pid/process_name>": "Resumes a process.",
        "ping [host]": "Pings a host (default: localhost).",
        "traceroute [host]": "Traces route to a host (default: localhost).",
        "clock": "Displays a simple clock." ,
        "explorer":"Opens built in File Explorer",
        "weather":"Opens built-in weather forecast.",
        "calculator":"Opens built-in calculator.",
        "converter":"Opens built-in converter" ,
        "ss":"Opens built-in screenshot system",
        "translator":"Opens built-in translator"
   }
   display_output("Available Commands:", animate=True)
   for cmd, desc in commands.items():
        display_output(f" - {cmd}: {desc}", animate=True)
def toggle_theme():
    global theme
    if theme == 'dark':
        root.config(bg="white")
        status_bar.config(bg="white")
        terminal_output.config(bg="white", fg="black")
        terminal_input.config(bg="white", fg="black")
        theme = 'light'
    else:
        root.config(bg="black")
        status_bar.config(bg="black")
        terminal_output.config(bg="black", fg="lime")
        terminal_input.config(bg="black", fg="lime")
        theme = 'dark'
def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pinfo = proc.info
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    display_output("Running Processes:", animate=True)
    for p in processes:
        cmdline = " ".join(p['cmdline']) if p['cmdline'] else ""  
        display_output(f"  PID: {p['pid']}, Name: {p['name']}, Command: {cmdline}", animate=True)
def open_text_editor():
    editor_window = tk.Toplevel(root)
    editor_window.title("SpacyOS Text Editor")
    editor_window.config(bg="black") 
    text_area = scrolledtext.ScrolledText(editor_window, wrap=tk.WORD, font=("Consolas", 12), bg="black", fg="lime", insertbackground="lime") # Green text, black bg, green cursor
    text_area.pack(fill="both", expand=True)
    def save_file():
        file_path = filedialog.asksaveasfilename(  
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(text_area.get("1.0", tk.END))
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    save_button = tk.Button(editor_window, text="Save", command=save_file, bg="black", fg="lime")  
    save_button.pack()
    editor_window.transient(root)
    log_action("SpacyOS Text Editor opened.")
def display_output(text, speed=200, animate=False):
    try:
        terminal_output.config(state="normal")
        if animate:
            terminal_output.insert(tk.END, text + "\n")
            terminal_output.update()
            time.sleep(1 / speed)
        else:
            terminal_output.insert(tk.END, text + "\n")
        terminal_output.config(state="disabled")
        terminal_output.see(tk.END)
    except tk.TclError:
        pass
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        log_action(f"Error getting IP: {str(e)}")
        return "Error"
ip_address = get_ip()
PASSWORD_FILE = "password.pkl"
SAFE_CODE = "Ghh18.uin" 
password_attempting_log = True
def create_password_file():
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "wb") as f:
            pickle.dump({}, f)  
def load_password():
    create_password_file()  
    with open(PASSWORD_FILE, "rb") as f:
        try:
            return pickle.load(f).get("password", None) 
        except EOFError: 
            return None
def save_password(password):
    with open(PASSWORD_FILE, "wb") as f:
        pickle.dump({"password": password}, f)
password_attempting_log = True
stored_password = load_password()
def check_password(command):
    global password_attempting_log, stored_password
    if command == SAFE_CODE:  
        new_password = simpledialog.askstring("Safe Code", "Enter a new password:")
        if new_password:
            save_password(new_password)
            stored_password = new_password
            password_attempting_log = False
            display_output("Password reset successfully!", speed=200, animate=True)
            log_action(f"Password reset using safe code. IP: {ip_address}")
            return True
        else:
            display_output("Password reset cancelled.", speed=200, animate=True)
            return False  
    elif stored_password is None: 
        display_output("Please sign up to get started. (Enter your password):", speed=200, animate=True)
        save_password(command)
        stored_password = command
        password_attempting_log = False
        display_output("Signup successful! You can now use commands.", speed=200, animate=True)
        log_action(f"User signed up. IP: {ip_address}")
        return True
    elif command == stored_password:  
        password_attempting_log = False
        display_output("Password accepted. You can now use commands.", speed=200, animate=True)
        log_action(f"User logged in. IP: {ip_address}")
        return True
    else:
        display_output("Invalid password. Please try again.", speed=200, animate=True)
        return False
def open_terminal(command):
    match = find_closest_match(command)  
    log_action("Opened PC terminal")
    try:
        os.startfile("cmd.exe")  
        display_output("Opening PC terminal...", speed=200, animate=True)
    except Exception as e: 
        display_output(f"Error opening terminal: {e}", speed=200, animate=True)
def log_action(action):
    log_filepath = os.path.join(os.getcwd(), "action_log.txt") 
    try:
        with open(log_filepath, "a") as log_file:  
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time}: {action}\n")
        print(f"Log entry added: {action}")  
    except OSError as e:
        print(f"Error writing to log file: {e}") 
def open_drawing_editor():
    try:
        drawing()
        display_output("Launching Drawing Editor... Please wait.", speed=200, animate=True)
        log_action("Drawing Editor launched.") 
    except Exception as e:
        display_output(f"Error launching Drawing Editor: {e}", speed=200, animate=True)
def handle_input(event=None):
    global history_index, confirm_command, password_attempting_log
    command = terminal_input.get().strip()
    if command:
        command_history.append(command)
        history_index = len(command_history)
    terminal_input.delete(0, tk.END)
    if password_attempting_log:
        if check_password(command):
            return  
        else:
            return  
    if confirm_command:
        if command.lower() == 'y':
            if confirm_command == "exit":
                display_output("Exiting SpacyOS...", speed=200, animate=True)
                log_action("Exited SpacyOS.")
                root.quit()
            elif confirm_command == "shutdown":
                display_output("Shutting down the computer...", speed=200, animate=True)
                log_action("Shut down the computer.")
                subprocess.run("shutdown /s /t 0", shell=True)  
            elif confirm_command == "restart":
                display_output("Restarting the computer...", speed=200, animate=True)
                log_action("Restarted the computer.")
                subprocess.run("shutdown /r /t 0", shell=True)  
            elif confirm_command=="browser":
             
                display_output("Launching SpacyBroswer...")
                browser()
                log_action("SpacyBroswer launched.")
            confirm_command = None  
        elif command.lower() == 'n':
            display_output("Operation canceled.", speed=200, animate=True)
            log_action("Operation canceled.")
            confirm_command = None 
        else:
            display_output("Invalid input. Please enter 'y' or 'n'.", speed=200, animate=True)
        return  
    if command.lower().startswith("launch "):
        program = command[7:]
        display_output(f"> {command}", speed=200, animate=True)
        threading.Thread(target=launch_program, args=(program,), daemon=True).start()
        log_action(f"Launch command executed for {program}")
    elif command.lower().startswith("ping "):
        host = command[5:].strip()
        ping("google.com")
        log_action(f"Pinged {host}")
    elif command.startswith("wifi"):
        if "connect" in command:  
            ssid = command.split("connect", 1)[1].strip()  
            connect_to_wifi(ssid)  
        else:
            wifi()  
    elif command.lower() == "browser":
        confirm_command = "browser"  
        display_output("Are you sure you want to proceed? This may cause blocking. Close SpacyBrowser tab afterwards. (y/n)", animate=True) 
    elif command.lower()=="translator":
        open_translator()
    elif command.lower().startswith("traceroute "):
        host = command[11:].strip()
        traceroute(host)
        log_action(f"Tracerouted {host}")
    elif command.lower() == "weather":
        try:
            display_output("Launching SpacyWeather... Please wait.", speed=200, animate=True)
            log_action("SpacyWeather launched.")
            weather()
        except Exception as e:
            display_output(f"Error launching SpacyWeather: {e}", speed=200, animate=True)
    elif command.lower() == "ss":
        log_action("Opened screenshot system.")
        screenshot()
    elif command.lower()=="converter":
        converter()
        display_output("Opening converter.")
    elif command.lower() == "clock":
        show_clock()
        log_action("Clock command executed.")
    elif command.lower() == "list programs":
        display_output("> list programs", speed=200, animate=True)
        list_programs()
        log_action("List programs command executed.")
    elif command.lower() == "refresh cache":
        display_output("> refresh cache", speed=200, animate=True)
        async_scan()
        log_action("Refresh cache command executed.")
    elif command.lower() == "clear":
        terminal_output.config(state="normal")
        terminal_output.delete(1.0, tk.END)
        terminal_output.config(state="disabled")
        log_action("Terminal cleared.")     
    elif command.lower() == "help":
        display_output("> help", speed=200, animate=True)
        display_help()
        log_action("Displayed help.")
    elif command.lower() == "del":
        cancel_command()
        log_action("Cancelled operation.")
    elif command.lower() == "drawing.editor": 
        display_output("Launching DrawingX...")
        log_action("DrawingX launched.")
        drawing()
    elif command.lower() == "exit":
        confirm_command = "exit"
        display_output("Are you sure you want to exit? (y/n)", animate=True)
        log_action("Exit command initiated.")
    elif command.lower() == "shutdown":
        confirm_command = "shutdown"
        display_output("Are you sure you want to shut down? (y/n)", animate=True)
        log_action("Shutdown command initiated.")
    elif command.lower() == "explorer":  
      display_output("> explorer", speed=200, animate=True)  
      explorer() 
      log_action("File explorer closed.") 
    elif command.lower() == "restart":
        confirm_command = "restart"
        display_output("Are you sure you want to restart? (y/n)", animate=True)
        log_action("Restart command initiated.")
    elif command.lower() == "h-info":
        display_hardware_info()
        log_action("Displayed hardware info.")
    elif command.lower().startswith("kill "):
        pid_str = command[5:] 
        display_output(f"> {command}", speed=200, animate=True)
        kill_process(pid_str)  
        log_action(f"Kill command executed for PID: {pid_str}")
    elif command.lower() == "ps":
        display_output("> ps", speed=200, animate=True)
        list_processes()
        log_action("List processes command executed.")
    elif command.lower() == "editor":
        display_output("> editor", speed=200, animate=True)
        open_text_editor()
        log_action("Open text editor command executed.")
    elif command.lower() == "netinfo":  
        get_network_info()
        log_action("Displayed network info")
    elif command.lower().startswith("setpriority "):
        parts = command.split()
        if len(parts) == 3:
            pid, priority = parts[1], parts[2]
            change_process_priority(pid, priority)
            log_action(f"Set priority of {pid} to {priority}")  
        else:
            display_output("Usage: setpriority <pid> <priority (high, normal)>", animate=True)
    elif command.lower().startswith("calendar"):
        show_calendar()
        log_action("Showed calendar")
    elif command.lower().startswith("suspend "):
        pid = command[8:]
        suspend_resume_process(pid, "suspend")
        log_action(f"Suspended process {pid}")  
    elif command.lower().startswith("resume "):
        pid = command[7:]
        suspend_resume_process(pid, "resume")
        log_action(f"Resumed process {pid}") 
    elif command.lower() == "calculator":
        open_calculator()
    elif command.lower()=="terminal":
        open_terminal(command)
    else:
        display_output(f"Unknown command: '{command}'", speed=200, animate=True)
        log_action(f"Unknown command executed: {command}")
def display_output(text, speed=200, animate=False):
    try:
        terminal_output.config(state="normal")
        if animate:
            terminal_output.insert(tk.END, text + "\n")
            terminal_output.update()
            time.sleep(1 / speed)
        else:
            terminal_output.insert(tk.END, text + "\n")
        terminal_output.config(state="disabled")
        terminal_output.see(tk.END)
    except tk.TclError:
        pass
root = tk.Tk()
root.title("SpacyOS V"+VERSION)
CACHE_FILE = "active_window_cache.pkl"
def load_cached_apps():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    return {}
def save_cached_apps(cached_apps):
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cached_apps, f)
def get_app_names():
    try:
        system_processes = {"explorer", "dwm", "svchost"}
        active_windows = Desktop(backend="uia").windows()
        process_map = {proc.pid: proc.name().replace(".exe", "").lower() for proc in psutil.process_iter(["pid", "name"])}

        current_apps = {
            win.process_id(): f"{process_map.get(win.process_id(), 'Unknown')} ({win.process_id()})"
            for win in active_windows
            if process_map.get(win.process_id(), "").lower() not in system_processes
        }
        return current_apps
    except Exception:
        return {}
def update_sidebar():
    new_apps = get_app_names()
    cached_apps = load_cached_apps()
    if new_apps != cached_apps:
        added = set(new_apps) - set(cached_apps)
        removed = set(cached_apps) - set(new_apps)
        for pid in added:
            listbox.insert(tk.END, new_apps[pid])
        for pid in removed:
            try:
                index = listbox.get(0, tk.END).index(cached_apps[pid])
                listbox.delete(index)
            except ValueError:
                pass
        save_cached_apps(new_apps)
    listbox.config(state=tk.NORMAL if new_apps else tk.DISABLED)
    root.after(5000, update_sidebar)
def activate_app(event):
    selection = listbox.curselection()
    if selection:
        try:
            pid = int(listbox.get(selection[0]).rsplit("(", 1)[-1][:-1])
            threading.Thread(target=activate_application, args=(pid,), daemon=True).start()
        except:
            pass
def activate_application(pid):
    try:
        app = application.Application(backend="uia").connect(process=pid)
        app.top_window().set_focus()
    except Exception as e:
        pass
sidebar_frame = tk.Frame(root, bg="grey", width=200)
sidebar_frame.grid(row=0, column=0, sticky="ns")  
listbox = tk.Listbox(sidebar_frame, width=20, bg="black", fg="lime", font=("Courier", 10), activestyle="none", selectmode=tk.SINGLE)
listbox.pack(fill=tk.BOTH, expand=True)
terminal_frame = tk.Frame(root, bg="black") 
terminal_frame.grid(row=0, column=1, sticky="nsew")  
root.grid_columnconfigure(1, weight=1)  
root.grid_rowconfigure(0, weight=1)
terminal_output = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, bg="black", fg="lime", font=("Consolas", 12), height=18)
terminal_output.pack(fill="both", expand=True, padx=5, pady=5)
terminal_input = tk.Entry(terminal_frame, bg="black", fg="lime", font=("Consolas", 12))
terminal_input.pack(fill="x", padx=5, pady=5)
terminal_input.bind("<Return>", handle_input)
status_bar = tk.Frame(root, bg="black")
status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
status_label = tk.Label(status_bar, text="Initializing system...", fg="lime", bg="black", font=("Consolas", 14))
status_label.pack(fill="x")
toggle_theme_button = tk.Button(status_bar, text="Toggle Theme", command=toggle_theme, bg="black", fg="lime", font=("Consolas", 10))
toggle_theme_button.pack(side="right")
root.bind("<F11>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
update_sidebar()
listbox.bind("<Double-1>", activate_app)
display_output("Welcome to SpacyOS V"+VERSION+"!", speed=200, animate=True)
display_output("Type 'help' for a list of commands.", speed=200, animate=True)
display_output("For launching Visual Studio Code please type >launch code because it is registred as code.exe not visualstudiocode.exe", speed=200, animate=True)
if stored_password is None:
    display_output("Welcome to SpacyOS! Please sign up to get started.", animate=True)
else:
    display_output("Welcome to SpacyOS! Please log in to get started.", animate=True)
load_program_cache()
async_scan()
metrics_thread = threading.Thread(target=update_metrics, daemon=True)
metrics_thread.start()
def set_focus():
    terminal_input.focus()
root.after(100, set_focus)
root.mainloop()
