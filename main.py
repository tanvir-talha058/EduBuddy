import pyaudio
import pyttsx3
import speech_recognition as sr

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone as source:
        print("I'm Listening Dear...")
        r.pause_threshold=1
        audio = r.listen(source,timeout=1, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query= r.recognize_google_cloud(audio, language='en-in')
        print(f"user said:{query}")

    except Exception as e:
        speak("Please say that again please...")
        return "none"
    return query


if __name__=="__main__":
    takecommand()
    speak("Hi Tanvir , This is Edu-Buddy.. How can i help you?")


