# Importing the required modules and libraries
import io
import requests
import configparser
import pytz

from PIL import Image, ImageTk
from tkinter import Tk, Label
from datetime import datetime
import os

class WeatherApp:
    # Define a method called set_configurations for the class.
    def set_configurations(self):
        # Create an instance of ConfigParser class.        
        self.configurations = configparser.ConfigParser()
        # Get the directory path of the current file and set it as a variable called loc.        
        loc = os.path.dirname(os.path.abspath(__file__))
        # Read the configuration file named 'config.ini' using the ConfigParser object and set it to the configurations instance variable. 
        self.configurations.read(loc+'\config.ini')
        # Get the value of the 'city' configuration setting from the 'configs' section of the configuration file and set it to the city instance variable.        
        self.city = self.configurations["configs"]["city"]
        # Get the value of the 'interval' configuration setting from the 'configs' section of the configuration file and convert it to an integer before setting it to the interval instance variable.        
        self.interval = int(self.configurations["configs"]["interval"])
        # Get the value of the 'api_key' configuration setting from the 'configs' section of the configuration file and set it to the api_key instance variable.        
        self.api_key = self.configurations["configs"]["api_key"]

    def get_weather_url(self):
        # Returns the URL for the OpenWeatherMap API to retrieve the weather information for the specified city.        
        return f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric'

    def get_icon_url(self, icon_code):
        # Returns the URL for the icon image corresponding to the given icon code from the OpenWeatherMap API.        
        return f'http://openweathermap.org/img/w/{icon_code}.png'

    def setup_location_label(self):
        # Create a label with the city name as text and a font size of 20               
        self.location_label = Label(self.initiator, text=self.city.title(), font=("Helvetica", 20))
        # Add the label to the parent frame        
        self.location_label.pack()

    def setup_icon_label(self):
        # Create a label to display the weather icon        
        self.icon_label = Label(self.initiator)
        # Add the label to the parent frame        
        self.icon_label.pack()

    def setup_icon_config(self):
        # Get the weather icon code from the API response
        icon_value = self.weather_details['weather'][0]['icon']
        # Download the icon image using the icon code and create a PhotoImage object from it
        icon = ImageTk.PhotoImage(Image.open(io.BytesIO(requests.get(self.get_icon_url(icon_value)).content)))
        # Set the PhotoImage as the icon label's image and keep a reference to it to prevent it from being garbage collected
        self.icon_label.config(image=icon)
        self.icon_label.image = icon

    def convert_farenheit(self, celsius_value):
         # Convert a temperature value from Celsius to Fahrenheit and round it to one decimal place
        return round(celsius_value * 1.8 + 32, 1)

    def setup_climate_label(self):
        # Create and pack climate label
        self.climate_label = Label(self.initiator, font=("Helvetica", 40))
        self.climate_label.pack()

    def setup_climate_config(self):
        # Get Celsius temperature from weather details and set climate label's text to include Fahrenheit
        celsius_value = self.weather_details['main']['temp']
        self.climate_label.config(text=f'{round(celsius_value, 1)} °C\n{self.convert_farenheit(celsius_value)} °F')

    def setup_description_label(self):
        # Create and pack description label
        self.description_label = Label(self.initiator, font=("Helvetica", 15))
        self.description_label.pack()

    def setup_description_config(self):
        # Get weather description from weather details and set description label's text
        self.description_label.config(text=self.weather_details['weather'][0]['description'].title())

    def setup_time_label(self):
        # Create and pack time label
        self.time_label = Label(self.initiator, font=("Helvetica", 20))
        self.time_label.pack()

    def setup_time_config(self):
        # Set time label's text to current time and update every second
        time_string = datetime.now(pytz.timezone('US/Eastern')).strftime("%a, %d %b %Y\n%H:%M:%S %Z")

# Update the label text with the formatted time
        self.time_label.config(text=time_string)

    def setup_labels(self):
        # Call functions to set up all labels
        self.setup_location_label()
        self.setup_climate_label()
        self.setup_icon_label()
        self.setup_description_label()
        self.setup_time_label()

    def setup_config_labels(self):
        # Call functions to set up all configurations
        self.setup_icon_config()
        self.setup_climate_config()
        self.setup_description_config()

    def setup_tkinter(self):
        # Create a new instance of the Tkinter window
        self.initiator = Tk()
        # Set the title of the window to "Weather App"
        self.initiator.title("Weather App")
        # Call the setup_labels() method to create the labels for weather information
        self.setup_labels()

    def fetch_weather(self):
        # Send a GET request to the OpenWeatherMap API to fetch weather data for the specified city
        self.weather_details = requests.get(self.get_weather_url()).json()
        # Call the setup_config_labels() method to update the labels with the new weather data
        self.setup_config_labels()

    def setup_timer(self):
        # Call the fetch_weather() method to fetch new weather data
        self.fetch_weather()
        # Set up a timer to call the setup_timer() method again after the specified interval
        self.initiator.after(self.interval * 60 * 1000, self.setup_timer)

    def end_tkinter(self):
        # Start the Tkinter event loop to display the window and handle user input
        self.initiator.mainloop()

    def __init__(self):
        # Call the set_configurations() method to set up the application configuration options
        self.set_configurations()
        # Call the setup_tkinter() method to set up the Tkinter window
        self.setup_tkinter()
        # Call the fetch_weather() method to fetch weather data for the first time
        self.fetch_weather()
        # Call the setup_time_config() method to set up the time configuration options
        self.setup_time_config()
         # Call the setup_timer() method to start the loop that fetches weather data at the specified interval
        self.setup_timer()
        # Call the end_tkinter() method to start the Tkinter event loop and display the window
        self.end_tkinter()

# This script creates an instance of the WeatherApp class and runs it.
# The WeatherApp class likely interacts with an external API to get weather data
# and displays it in a user-friendly format.
if __name__ == "__main__":
    WeatherApp() # Create an instance of the WeatherApp class and run it
