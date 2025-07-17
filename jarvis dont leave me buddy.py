import tkinter as tk
import datetime
import webbrowser
import os
import pyttsx3
import speech_recognition as sr

# === Voice Engine Setup ===
try:
    engine = pyttsx3.init()
except Exception as e:
    engine = None
    print("Voice engine not available:", e)

def speak(text):
    if engine:
        engine.say(text)
        engine.runAndWait()

def take_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        chat.insert(tk.END, "Listening...\n")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            entry.insert(0, command)
            respond()
        except sr.UnknownValueError:
            chat.insert(tk.END, "Could not understand audio.\n")
            speak("I couldn't understand that.")
        except sr.RequestError:
            chat.insert(tk.END, "Could not connect to recognition service.\n")
            speak("There was an error with the speech service.")

def respond(event=None):
    cmd = entry.get().strip().lower()
    entry.delete(0, tk.END)
    chat.insert(tk.END, f"You: {cmd}\n")

    if "time" in cmd:
        reply = "Current time is " + datetime.datetime.now().strftime("%I:%M %p")

    elif "date" in cmd:
        reply = "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y")

    elif "open youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        reply = "Opening YouTube"

    elif "open google" in cmd:
        webbrowser.open("https://www.google.com")
        reply = "Opening Google"

    elif "open notepad" in cmd:
        try:
            os.startfile("notepad.exe")
            reply = "Opening Notepad"
        except:
            reply = "Could not open Notepad"

    elif "help" in cmd:
        reply = "Try: time, date, open youtube, open google, open notepad, help, exit"

    elif cmd in ["exit", "quit", "bye"]:
        reply = "Goodbye!"
        chat.insert(tk.END, "JARVIS: " + reply + "\n")
        speak(reply)
        root.destroy()
        return

    else:
        reply = "I don't understand. Type 'help' to see commands."

    chat.insert(tk.END, "JARVIS: " + reply + "\n")
    speak(reply)

# === GUI Setup ===
root = tk.Tk()
root.title("JARVIS with Voice Input")
root.geometry("500x450")

chat = tk.Text(root, bg="black", fg="lime", font=("Consolas", 12))
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Consolas", 12))
entry.pack(padx=10, pady=5, fill=tk.X)
entry.bind("<Return>", respond)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

voice_btn = tk.Button(button_frame, text="🎤 Speak", font=("Arial", 10), command=take_voice_command)
voice_btn.pack(side=tk.LEFT, padx=5)

help_btn = tk.Button(button_frame, text="❓ Help", font=("Arial", 10), command=lambda: entry.insert(0, "help"))
help_btn.pack(side=tk.LEFT)

chat.insert(tk.END, "JARVIS: Hello! Type or speak a command. Try 'help'.\n")
speak("Hello! I am JARVIS. Type or speak a command.")

root.mainloop()
