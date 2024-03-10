import os
import pygame
import speech_recognition as sr
import openai
from config import apikey
import random
import pyautogui


def speak(text):
    voice ="en-US-AriaNeural"
    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "output.mp3"'

    os.system(command)
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(e)
    finally:
         pygame.mixer.music.stop()
         pygame.mixer.quit()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognizing..")
        query = r.recognize_google(audio, language="en-in")
        print(f"you said :{query}")
        return query
    except Exception as e:
        return "some error occured. sorry for inconvinience please repeat again."
chatstr: str= ""
def chat(query):
    global chatstr
    print(chatstr)
    openai.api_key = apikey
    chatstr += f"you: {query} \n Desktop:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatstr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speak(response['choices'][0]['text'])
    chatstr += f"{response['choices'][0]['text']}\n"
    return response['choices'][0]['text']

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt : {prompt} \n*****************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"] [0] ["text"] )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/prompt- {random.randint(1,556666553344333)}", "w") as f:
        f.write(text)

if __name__ == '__main__':
    print('PyCharm')
    say("hello I am desktop A.I")
while True:
    print("listening....")
    query = take_command()
    sites = [["youtube","https://www.youtube.com/"], ["wikipedia","https://www.wikipedia.org/"],
             ["google","https://www.google.com/"],["instagram","https://www.instagram.com/"],
             ["whatsapp","https://www.web.whatsapp.com/"],
             ["youtube music","https://www.music.youtube.com/"],["flipkart","https://www.flipkart.com/"],
             ["Amazon","https://www.amazon.com/"],["Gmail","https://www.mail.gooogle.com/"],]
    for site in sites:
        if f"open {site[0]}".lower() in query.lower():
            speak(f"opeing {site[0]} sir")
            webbrowser.open(site[1])

    if  "play music" in query or "open music" in query:
        musicpath = "/Users/sakshamgoyal/Downloads/music.mp3"
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener,musicpath])

    elif "the time" in query or "current time" in query:
        strfTime = datetime.datetime.now().strftime("%H:%M")
        say(f"sir the time is {strfTime}")

    elif 'open' in query:
        app_name= query.replace('open','')
        speak('opening' +app_name)
        pyautogui.press('Command')
        pyautogui.press('spacebar')
        pyautogui.typewrite(app_name)
        pyautogui.sleep(0.7)
        pyautogui.press('return')

    elif 'close' in query:
        pyautogui.hotkey('command',)



    elif "using artificial intelligence".lower() in query or "using AI".lower() in query:
        ai(prompt=query)

    elif "exit".lower() in query or "bye".lower() in query or "quit".lower() in query or "stop".lower() in query or "end".lower() in query or "close".lower() in query or "close the program".lower() in query or "close the program".lower() in query:
        say("bye sir")
        exit()

    elif "reset".lower() in query or "clear chat".lower() in query:
        chatstr = ""
        say("chat has been reset sir")
    else:
        print("Chatting...")
        chat(query)

    speak(query)
