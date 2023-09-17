import speech_recognition as sr
from gtts import gTTS
import os
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import requests

listener = sr.Recognizer()

def talk(text):
    try:
        tts = gTTS(text=text, lang='en-us', tld='us', slow=False)
        tts.save('output.mp3')
        os.system('afplay output.mp3')  # For macOS. Use 'aplay output.mp3' for Linux.
        os.remove('output.mp3')

    except Exception as e:
        print("Exception: {}".format(e))

def take_command():
    try:
        with sr.Microphone() as source:

            print('\nListening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if 'infinity' in command:
                command = command.replace('infinity', '')
                print("Input command: " + command)
                return command
            
            else:
                print("No command received.")
                talk('Are you there, Boss?')

                print("Listening...")
                voice = listener.listen(source, timeout=3)  # Listen for an additional 3 seconds
                if voice:
                    print("Voice Received.")
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    print("Input command: " + command)
                    return command
                else:
                    print("No response. Going to sleep mode.")
                    talk('Going to sleep mode.')
                    return None
        
    except Exception as e:
        print("Exception:"+ str(e))

# Code that tells about weather of any city 
# Fetches API with "openweathermap"
def get_weather(city):
    api_key = "1ea8dda1005b9287b2e996d6f9be9b7a"  # Replace with your OpenWeatherMap API key
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        main_weather = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        
        weather_info = f"The weather in {city} is {main_weather}. Description: {description}. Temperature: {temperature}°C. Humidity: {humidity}%."
        return weather_info
    else:
        return "Sorry, I couldn't retrieve the weather information for that city."

def get_news(topic):
    # Define the API endpoint URL and parameters
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": "75f1babdb00c4a0cbf3ede3bc885950e",  # Replace with your News API key
        "q": topic,  # Query parameter for the topic
        "language": "en",  # Language parameter (English)
        "pageSize": 3,  # Number of articles to retrieve
    }

    try:
        # Send a GET request to the API
        response = requests.get(url, params=params)
        data = response.json()

        # Check if the response was successful
        if response.status_code == 200 and data["status"] == "ok":
            articles = data["articles"]
            if len(articles) > 0:
                return articles
            else:
                return None
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print("Exception:", e)
        return None

# Function that returns what to greet depending on the time of the day
def get_greetings():
    current_time = datetime.datetime.now()

    if current_time.hour < 12:
        return "Good Morning Sir!"
    
    elif 12 <= current_time.hour < 18:
        return "Good Afternoon Sir!"
    
    else:
        return "Good Evening Sir!"

def run_alexa():
    command = take_command()

    if 'play' in  command or 'can you please play on youtube' in command:
        song = command.replace('play', '')
        talk('Sure, Playing' + song)
        print('Playing' + song)
        pywhatkit.playonyt(song)
        talk("Is there anything else I can assist you with?")

    elif 'who are you' in command:
        talk('I am INFINITY, a virtual AI assistant. I was created by Rishabh Mathur.')
        talk("Do you have any other questions or requests?")

    elif 'date' in command or "today\'s date" in command:
        date = datetime.date.today().strftime(" %B %d, %Y")
        print(date)
        talk("Today's date is: " + date)
        talk("Is there anything else I can help you with?")

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M %p') # %p is used for AM/PM 
        print(time)
        talk('Current time is' + time)
        talk("Anything else Sir?")

    elif 'who is' in command:
        person = command.replace('Who is', '')
        try:
            info = wikipedia.summary(person, 2)
            print(info)
            talk(info)
        except wikipedia.exceptions.PageError:
            message = "Sorry, I couldn't find information about {person}."
            print("Sorry, I couldn't find information about {person}.")
            talk(message)
        talk("Do you have any other questions or requests?")

    elif 'go for a date' in command:
        talk('I have a headache!')
        talk("I'm really sorry. Anything else I can help you with?")

    elif 'are you single' in command:
        talk('I am in relationship with WIFI.')
        talk("Ahm... sorry about that.")
        talk("By the way, do you need any sort of help? I'm here to asssist you.")

    elif 'tell me a joke' in command:
        talk(pyjokes.get_joke())
        talk("By the way, do you need any sort of help? I'm here to asssist you.")
    
    # User asks for weather of particular city.
    elif 'weather' in command:
        city = command.replace('weather', '').strip()
        weather_info = get_weather(city)
        talk(weather_info)
        talk("Is there anything else I can help you with?")

    # User asks to read some news.
    # It asks for news for some particular topic.
    elif 'read some news' in command:

        topic = None  # Initialize topic variable

        while True:

            if topic is None:
                talk("What topic would you like to read news about?")
                topic = take_command()
            else:
                talk("Anything else Sir?")
                response = take_command()

                if response and ("yes" in response or "sure" in response):
                    talk("What topic would you like to read news about?")
                    topic = take_command()
                else:
                    talk("Alright. Have a great day!")
                    break

            if topic:
                articles = get_news(topic)

                if articles is not None:
                    talk(f"Here are the top news articles on {topic}:")
                    for article in articles:
                        title = article["title"]
                        description = article["description"]
                        print(title)
                        talk(title)
                        print(description)
                        talk(description)
                else:
                    talk(f"Sorry, I couldn't find any news articles on {topic}.")
                    talk("Anything else you would like me to do sir?")
                    break

                topic = None 

    elif 'good morning' in command:
        greetings = ['Good morning Sir!', 'Good morning! Sir, how can I assist you?', 'Good morning Sir! Happy to see you back.']
        talk(random.choice(greetings) +  "How may I help you?")

    elif 'good afternoon' in command:
        greetings = ['Good afternoon Sir!', 'Good afternoon Boss! How can I assist you?', 'Good afternoon Boss! What is your todays plan?']
        talk(random.choice(greetings) +  "How may I help you?")

    elif 'good night' in command:
        greetings = ['Good night Sir!', 'Good night Sir! Have a restful sleep!', 'Nighty night!','Good night, see you tomorrow!']
        talk(random.choice(greetings))
        return -1

    # If user says "No" it would stop exectuing
    elif ('no' or 'nothing' or 'bye') in command:
        talk('Let me know if you need any help. Have a great day Sir!')
        return -1
    
    else:
        talk('Sir, would you please say that again?')

# Main function
if __name__ == "__main__":
    greetings = get_greetings()
    talk(greetings + "How may i assist you?")

    while True:
        x = run_alexa()
        if x == -1:
            break
