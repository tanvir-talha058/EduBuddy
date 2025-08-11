import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import webbrowser

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm Listening Dear...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that. Please say that again.")
        return "none"
    except sr.RequestError as e:
        speak(f"Could not request results; {e}")
        return "none"
    return query


def wish():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good Morning")
    elif hour == 12:
        speak("Good Noon")
    elif 12 < hour < 18:
        speak("Good Afternoon")
    elif 18 <= hour < 22:
        speak("Good Evening")
    else:
        speak("Good Night")

    speak("I'm EduBuddy. Please tell me how I can help you.")





if __name__ == "__main__":
    speak("Hi Tanvir, This is Edu-Buddy")
    wish()
    while True:
        query = take_command().lower()

        if "open notepad" in query:
            speak("Openning nodepad...")
            path= "C:\\Windows\\system32\\notepad.exe"
            os.startfile(path)

        elif "open google chrome" in query:
            speak("Opening google chrome...")
            path = "C:\\Program Files\\Google\Chrome\\Application\\chrome.exe"
            os.startfile(path)

        elif "open microsoft word" in query:
            speak("Opening microsoft word....")
            path = "C:\\Program Files\Microsoft Office\\root\Office16\\WINWORD.EXE"
            os.startfile(path)

        elif "open command prompt" in query:
            speak("Opening command prompt...")
            os.system("start cmd")

        elif "open camera" in query:
            speak("Opening camera, be ready....")
            cap= cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam',img)
                k= cv2.waitKey(30)
                if k==6:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "time" in query:
            time= datetime.datetime.now().strftime('%I:%M %p')
            speak("the time right now is: " + time)

            print(time)


        elif "play music" in query:
            speak("Playing your favourite music...")
            music_dir = "D:\\Music"
            songs= os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[0]))


        elif "do you know" in query:
            query= query.replace("wikipedia"," ")
            result= wikipedia.summary(query, sentences=2)
            speak("According to my knowledge..")
            speak(result)
            print(result)


        elif "open youtube" in query:
            speak("Opening youtube...")
            webbrowser.open("www.youtube.com")


        elif "open facebook" in query:
            speak("Opening facebook...")
            webbrowser.open("www.facebook.com")


        elif "open chat gpt" in query:
            speak("Opening chat gpt...")
            webbrowser.open("https://chat.openai.com")


        elif "open google" in query:
            speak("Opening google..What should I search in google Sir?")
            cm = take_command().lower()
            webbrowser.open(f"{cm}")


        elif "learn python" in query:
            speak("You can easily learn python programming language from here..")
            webbrowser.open("https://www.w3schools.com/python/")


        elif "learn java" in query:
            speak("You can easily learn java programming language from here..")
            webbrowser.open("https://www.w3schools.com/java/default.asp")


        elif "learn html" in query:
            speak("You can easily learn html from here..")
            webbrowser.open("https://www.w3schools.com/html/default.asp")


        elif "learn c" in query:
            speak("You can easily learn c programming language from here..")
            webbrowser.open("https://www.w3schools.com/c/index.php")


        elif "learn php" in query:
            speak("You can easily learn php from here..")
            webbrowser.open("https://www.w3schools.com/php/default.asp")


        elif "learn django" in query:
            speak("You can easily learn django from here..")
            webbrowser.open("https://www.w3schools.com/django/index.php")


        elif "learn web development" in query:
            speak("You can easily learn web development from here..")
            webbrowser.open("https://www.w3schools.com/whatis/default.asp")


        elif "ethical hacking" in query:
            speak("You can easily learn ethical hacking from here..")
            webbrowser.open("https://youtube.com/playlist?list=PL82D6HIBQ199l1XGskGj-_H9c8Fr-5hr4&si=2MJ_euwZHZYuu5NF")


        elif "set reminder" in query:
            speak("Setting reminder for you..")
            webbrowser.open("https://vclock.com/")


        elif "learn python" in query:
            speak("You can easily learn python programming language from here..")
            webbrowser.open("https://www.w3schools.com/python/")


        elif "learn python" in query:
            speak("You can easily learn python programming language from here..")
            webbrowser.open("https://www.w3schools.com/python/")


        elif "learn python" in query:
            speak("You can easily learn python programming language from here..")
            webbrowser.open("https://www.w3schools.com/python/")


        elif "learn python" in query:
            speak("You can easily learn python programming language from here..")
            webbrowser.open("https://www.w3schools.com/python/")


        elif "course teacher" in query:
            speak("""Md. Monarul Islam Sir.
                     Currently he is working as a Lecturer at Daffodil International University.
                     He had completed his B.Sc in Computer Science and Engineering from Khulna University of Engineering
                     and Technology and
                     M.Sc from Bangladesh University of Engineering and Technology.""")

        elif "Suggest movie" in query:
            speak("You must should watch  the movie named The Pursuit of Happiness")

        if 'exit' in query:
            speak("Goodbye")
            break

