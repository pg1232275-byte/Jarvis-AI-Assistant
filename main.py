import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
newsapi= "NEWS_API_KEY"

#for better sound results go for  gtts speak allows a lot of things.
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiprocess(command):
    client = OpenAI(api_key = "YOUR_API_KEY")
    completion = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system","content": "You are a virtual assistant named jarvis skilled kn gemral tasks like Alexa and google cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

    return completion.choices[0].message.content



def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif"open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif"open Linkdien" in c.lower():
        webbrowser.open("https://linkdien.com")
    elif"open instagram" in c.lower():
        webbrowser.open("https://instagram.com")


    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        print("Song =", repr(song))
        print("Available keys =", musicLibrary.music.keys())
        link = musicLibrary.music[song]
        webbrowser.open(link)


    elif "news" in c.lower():
        
        r = requests.get("https://api.mediastack.com/v1/news?access_key=f1d0370ca14c00965828c444272e048d&countries=in&limit=5")

        news = r.json()

        for article in news["data"]:
            print(article["title"])
            speak(article["title"])
    else:
        #Let openai handle the request.
        output = aiprocess(c)
        speak(output)



if __name__ == ("__main__") :
    speak("Initializing Jarvis.... ")
    while True:
       #listen for the wake word "jarvis".
       #obtaining audio from microphone.
        r = sr.Recognizer()
        

        #recognize speech using google
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)
            if( word.lower() == "jarvis"):
                speak("Hello Boss....")
                
                #listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                processCommand(command)
           
        except Exception as e:
            print("Error ; {0}".format(e))

