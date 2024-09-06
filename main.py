import speech_recognition as sr
import pyttsx3
import requests
import datetime
import os  # For executing system commands
import subprocess  # Alternative to os for better control over system commands

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, there was an issue with the request.")
            return None

def get_weather():
    api_key = "your_openweathermap_api_key"
    city = "London"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    data = response.json()
    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
        return f"The weather in {city} is {weather} with a temperature of {temperature:.2f}°C."
    else:
        return "I could not get the weather information."

def open_application(app_name):
    """Function to open specified applications."""
    try:
        if "spotify" in app_name:
            # Replace the path below with the actual path of Spotify on your system
            subprocess.Popen(["C:\\Users\\<YourUsername>\\AppData\\Roaming\\Spotify\\Spotify.exe"])
            return "Opening Spotify."
        elif "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
            return "Opening Notepad."
        elif "calculator" in app_name:
            subprocess.Popen(["calc.exe"])
            return "Opening Calculator."
        else:
            return f"Sorry, I cannot open {app_name} at the moment."
    except Exception as e:
        return f"Failed to open {app_name}. Error: {str(e)}"

def handle_command(command):
    if "weather" in command:
        return get_weather()
    elif "time" in command:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."
    elif "hello" in command:
        return "Hello! How can I assist you today?"
    elif "open" in command:
        # Extract app name from the command and try to open it
        app_name = command.replace("open", "").strip()
        return open_application(app_name)
    else:
        return "Sorry, I didn't understand that command."

def main():
    while True:
        command = listen()
        if command:
            response = handle_command(command.lower())
            speak(response)

if __name__ == "__main__":
    main()

