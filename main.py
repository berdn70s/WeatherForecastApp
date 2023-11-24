import tkinter as tk
from tkinter import ttk
import requests
import os


class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")

        master.configure(bg="lightblue")

        # City selection dropdown list
        self.city_label = tk.Label(master, text="Select a city:", font=("Helvetica", 16), fg="blue", bg="lightblue")
        self.city_label.pack(padx=10, pady=10)

        self.city_var = tk.StringVar()
        self.city_dropdown = ttk.Combobox(master, textvariable=self.city_var, font=("Helvetica", 14), state="readonly")
        self.city_dropdown["values"] = ("Ankara", "Izmir", "Istanbul", "Antalya", "Bursa")
        self.city_dropdown.current(0)
        self.city_dropdown.pack(padx=10, pady=10)

        # Weather information display area
        self.weather_info_label = tk.Label(master, text="Weather Information:", font=("Helvetica", 16), fg="blue",
                                           bg="lightblue")
        self.weather_info_label.pack(padx=10, pady=10)

        self.weather_info_text = tk.Text(master, height=20, width=60, font=("Helvetica", 14))
        self.weather_info_text.pack(padx=10, pady=10)

        # Temperature unit toggle button
        self.temp_unit_var = tk.StringVar(value="Celsius")
        self.temp_unit_button = tk.Button(master, textvariable=self.temp_unit_var, command=self.toggle_temp_unit,
                                          font=("Helvetica", 14), bg="yellow", activebackground="green")
        self.temp_unit_button.pack(padx=10, pady=10)

        # Current weather button
        self.current_weather_button = tk.Button(master, text="Show Current Weather", command=self.show_current_weather,
                                                font=("Helvetica", 14), bg="yellow", activebackground="green")
        self.current_weather_button.pack(padx=10, pady=10)

        # 3-day forecast button
        self.forecast_button = tk.Button(master, text="Show 3-Day Forecast", command=self.show_forecast,
                                         font=("Helvetica", 14), bg="yellow", activebackground="green")
        self.forecast_button.pack(padx=10, pady=10)

        # Show current weather or 3-day forecast
        self.show_forecast = False

        # Load user preferences
        if os.path.exists("Settings.txt"):
            with open("Settings.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    city = lines[0].strip()
                    temp_unit = lines[1].strip()
                    show_forecast = lines[2].strip()
                    self.city_var.set(city)
                    self.temp_unit_var.set(temp_unit)
                    self.show_forecast = show_forecast == "True"
                    if temp_unit == "Fahrenheit":
                        self.temp_unit_button.configure(bg="green", activebackground="yellow")
                    self.get_weather_data(show_forecast=self.show_forecast)

    def get_weather_data(self, show_forecast=False):
        try:
            city = self.city_var.get()
            city = city.replace(" ", "-")

            api_key = "d14bd97a2016de74a13dd57deb9157a8"
            base_url = "http://api.openweathermap.org/data/2.5"

            if not show_forecast:
                # Send request to OpenWeatherMap API to get current weather data for selected city
                url = f"{base_url}/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                temp = data["main"]["temp"]
                wind_speed = data["wind"]["speed"]
                weather_description = data["weather"][0]["description"]

                if self.temp_unit_var.get() == "Fahrenheit":
                    temp_fahrenheit = temp * 9 / 5 + 32
                    temp_str = f"{temp_fahrenheit:.1f}°F"
                else:
                    temp_str = f"{temp:.1f}°C"

                if temp < 10:
                    temp_icon = "❄"
                elif temp < 25:
                    temp_icon = "☀"
                else:
                    temp_icon = "🔥"

                if wind_speed < 2:
                    wind_speed_icon = "🍃"
                elif wind_speed < 10:
                    wind_speed_icon = "🌬"
                else:
                    wind_speed_icon = "💨"

                # Update weather information display area with current weather data
                weather_info = f"City: {city}\n\nCurrent Weather:\nTemperature: {temp_str} {temp_icon}\nWind Speed: {wind_speed} m/s {wind_speed_icon}\nDescription: {weather_description}\n"

                self.weather_info_text.delete(1.0, tk.END)
                self.weather_info_text.insert(tk.END, weather_info)
            else:
                # Send request to OpenWeatherMap API to get 3-day forecast data for selected city
                url = f"{base_url}/forecast?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                # 3-day forecast
                day_count = 0
                weather_info = f"City: {city}\n\n3-Day Forecast:\n"
                for forecast in data["list"]:
                    dt_txt = forecast["dt_txt"]
                    if "12:00:00" in dt_txt or "00:00:00" in dt_txt:
                        temp = forecast["main"]["temp"]
                        weather_description = forecast["weather"][0]["description"]

                        if self.temp_unit_var.get() == "Fahrenheit":
                            temp_fahrenheit = temp * 9 / 5 + 32
                            temp_str = f"{temp_fahrenheit:.1f}°F"
                        else:
                            temp_str = f"{temp:.1f}°C"

                        if temp < 10:
                            temp_icon = "❄"
                        elif temp < 25:
                            temp_icon = "☀"
                        else:
                            temp_icon = "🔥"

                        if "12:00:00" in dt_txt:
                            weather_info += f"{dt_txt.split()[0]} Day: {temp_str} {temp_icon}, {weather_description}\n"
                        else:
                            weather_info += f"{dt_txt.split()[0]} Night: {temp_str} {temp_icon}, {weather_description}\n"

                        if "00:00:00" in dt_txt:
                            day_count += 1

                        if day_count == 3:
                            break

                self.weather_info_text.delete(1.0, tk.END)
                self.weather_info_text.insert(tk.END, weather_info)

        except requests.exceptions.ConnectionError:
            self.weather_info_text.delete(1.0, tk.END)
            self.weather_info_text.insert(tk.END, "Error: No internet connection")

    def toggle_temp_unit(self):
        if self.temp_unit_var.get() == "Celsius":
            self.temp_unit_var.set("Fahrenheit")
            self.temp_unit_button.configure(bg="green", activebackground="yellow")

        else:
            self.temp_unit_var.set("Celsius")
            self.temp_unit_button.configure(bg="yellow", activebackground="green")

        self.get_weather_data(show_forecast=self.show_forecast)

    def show_current_weather(self):
        self.show_forecast = False
        self.get_weather_data(show_forecast=False)

    def show_forecast(self):
        self.show_forecast = True
        self.get_weather_data(show_forecast=True)

    def save_preferences(self):
        with open("Settings.txt", "w") as f:
            f.write(f"{self.city_var.get()}\n")
            f.write(f"{self.temp_unit_var.get()}\n")
            f.write(f"{self.show_forecast}\n")


root = tk.Tk()
app = WeatherApp(root)
root.protocol("WM_DELETE_WINDOW", lambda: (app.save_preferences(), root.destroy()))
root.mainloop()
