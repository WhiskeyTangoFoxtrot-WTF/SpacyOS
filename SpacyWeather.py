import tkinter as tk
from tkinter import ttk
import requests
import time
from threading import Thread
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
    weather_label.config(text=f"{city}\nTemperature: {temp}°C\n{desc}\nWind Speed: {wind} m/s")
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
        forecast_entry = tk.Label(forecast_frame, text=f"{time_text}\n{temp}°C, {desc}", font=("Courier", 12), bg="black", fg="lime", justify="center")
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
