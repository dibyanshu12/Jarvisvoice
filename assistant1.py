import sys
import threading
from neuralintents import BasicAssistant
import speech_recognition as sr
import pyttsx3 as tts
import tkinter as tk

class Assistant():
    def __init__(self):
        self.recog=sr.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate",150)
        self.assistant = BasicAssistant("venv/intent.json", method_mappings={"file" : self.create_file})
        self.assistant.fit_model()

        self.root = tk.Tk()
        self.label= tk.Label(text="🤖", font=("Arial",120,"bold"))
        self.label.pack()
        threading.Thread(target=self.run_assistant).start()
        self.root.mainloop()

    def create_file(self):
        with open("test.txt","w") as f:
            f.write("Jai Shree Ram")

    def run_assistant(self):
        while True:
            try:
                with (sr.Microphone() as mic):
                    self.recog.adjust_for_ambient_noise(mic, duration=0.2)
                    au = self.recog.listen(mic)
                    txt= self.recog.recognize_google(au,language='en')
                    txt= txt.lower()

                    if "jarvis" in txt:
                        self.label.config(fg="red")
                        au = self.recog.listen(mic)
                        txt = self.recog.recognize_google(au, language='en')
                        txt = txt.lower()

                        if txt == "stop":
                            print("stop")
                            self.speaker.say("bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()

                        else:

                            if txt is not None:
                                res= self.assistant.process_input(txt)
                                if res is not None:
                                    self.speaker.say(res)
                                    self.speaker.runAndWait()
                                self.label.config(fg="black")
            except sr.UnknownValueError:
                self.recog = sr.Recognizer()
                self.label.config(fg="black")
                continue
Assistant()