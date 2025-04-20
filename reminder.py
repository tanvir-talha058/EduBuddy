import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import time
import webbrowser


def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 175)
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning ")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon ")
    else:
        speak("Good Evening ")

    speak("I am EduBuddy")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-us')
        command = command.lower()
        print("\n")
        print(command)
    except:
        print("Try Again")

    return command

def EduBuddy():
    while True:
        command = take_command()

        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak("It's " +time)

        elif 'tell me about' in command:
            command = command.replace("tell me about", "")
            results = wikipedia.summary(command, sentences=2)
            speak(results)

        elif 'set a reminder' in command:
            speak("What would you like me to remind you about?")
            reminder_text = take_command()
            speak("When should I remind you about " + reminder_text + "?")
            reminder_time_input = take_command()

            try:
                reminder_time = datetime.datetime.strptime(reminder_time_input, "%I:%M %p")
                current_time = datetime.datetime.now()
                if reminder_time > current_time:
                    delta_t = (reminder_time - current_time).total_seconds()
                    speak(f"Reminder set for {reminder_text} at {reminder_time.strftime('%I:%M %p')}.")
                    time.sleep(delta_t)
                    speak(f"Reminder: {reminder_text}")
                else:
                    speak("The specified time is already past.")
            except ValueError:
                speak("Invalid time format. Please specify the time in 'HH:MM AM/PM' format.")

        elif 'open google' in command:
            webbrowser.open("google.com")
        elif 'open youtube' in command:
            webbrowser.open("youtube.com")
        elif 'open facebook' in command:
            webbrowser.open("facebook.com")


greetings()
EduBuddy()