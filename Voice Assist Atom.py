import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import random
import socket

server_esp32 = ('ESP32_IP_ADDRESS', ESP32_PORT) #Replace the Port Number and the IP of the ESP32

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your Atom. How may I help you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, please say that again...")
        query = None
    return query

intro = "<your intro here>"
grt = ["hai","hello", "hi", "hey"]

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        
        if query is None:
            continue
        elif 'what is your name' in query.lower():
            speak("My name is Atom. How can I assist you?")

        elif "intro your self" in query or "introduce yourself" in query:
            try :
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect(server_esp32)

                        client_socket.send("40".encode())
                     
                        client_socket.close()  
            except:
                print("out of server !")
                
            speak(intro)
            try :
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect(server_esp32)

                        client_socket.send("75".encode())
                     
                        client_socket.close()
            except:
                print("out of server !")
                
            print("Intro given ....")
            
   
        elif query.lower() in grt:
            greetings = ['hai', 'hello', 'hey there', 'hi',"yes"]
            speak(random.choice(greetings))

        elif 'open youtube' in query.lower():
            webbrowser.open("https://www.youtube.com/")
            speak("opening youtube")
        elif 'open google' in query.lower():
            webbrowser.open("https://www.google.com/")
            speak("opening google")
        elif 'what is the time' in query.lower() or "time now" in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'exit' in query.lower():
            speak("Thank you for using me. Have a good day!")
            break
        elif  "search for" in query or 'search' in query :
            if "search for" in query:
                search_query = query.split("search for")[-1]
                
            elif 'search' in query:
                search_query = query.split('search')[-1]
            
            url = f'https://www.google.com/search?q={search_query}'
            webbrowser.open(url)
            print(f'Searching for "{search_query}" on Google...')

        elif 'open website' in query:
            website_url = query.split('open website')[-1]
            webbrowser.open(website_url)
            print(f'Opening website: {website_url}')

        elif 'what is the weather' in query:
            location = query.split('the weather in')[-1]
            url = f'https://www.google.com/search?q=weather+{location}'
            webbrowser.open(url)
            print(f'Getting weather information for {location}...')


        elif "hey atom" in query:
            speak('yes how can i help you')

        elif 'who is' in query or 'what is' in query or 'who are' in query or "what are" in query:
            person = query.replace('who is', '').replace('what is', '').replace('who are', '').replace('what are', '')
            try:    
                info = wikipedia.summary(person, sentences=2)
                # Use text-to-speech to speak the answer
                engine.say(info)
                engine.runAndWait()
            except:
                speak("Sorry, I could not find information on that topic.")
        elif "do you know "in query:
            person = query.replace('do you know', '')
            try:    
                info = wikipedia.summary(person, sentences=2)
                # Use text-to-speech to speak the answer
                engine.say(f"yes, {info}")
                engine.runAndWait()
            except:
                speak("Sorry, I could not find information on that topic.")
                

        else:
                  speak("Sorry, I could not understand.")      
      
