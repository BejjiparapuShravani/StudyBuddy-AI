import os
import random
import pygame
import tkinter as tk
import speech_recognition as sr
import threading
import time
from tkinter import messagebox

# Load quotes
def load_quotes(filename="quotes.txt"):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return ["Stay focused. Keep learning!"]

# Play music
def play_music(folder, status_label):
    songs = [song for song in os.listdir(folder) if song.endswith(".mp3")]
    if not songs:
        status_label.config(text=f"No music found in {folder}")
        return
    song = random.choice(songs)
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(folder, song))
    pygame.mixer.music.play()
    status_label.config(text=f"🎵 Now Playing: {song}")

# Listen for mood
def listen_mood():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎤 Listening...")
        root.update()
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return None

# Analyze and respond to mood
def analyze_mood():
    mood = listen_mood()
    if not mood:
        status_label.config(text="Could not detect your mood. Try again.")
        return

    mood_label.config(text=f"🧠 Mood detected: {mood}")

    if mood in ['happy', 'neutral']:
        quote_label.config(text="")
        play_music("focus_music", status_label)
    elif mood in ['sad', 'stressed', 'emotional', 'tired']:
        quote = random.choice(quotes)
        quote_label.config(text=f"💬 {quote}")
        play_music("break_music", status_label)
    else:
        status_label.config(text="Unrecognized mood. Try again.")

# Reminder popup
def start_reminders(interval_minutes=30):
    def reminder_loop():
        while True:
            time.sleep(interval_minutes * 60)
            messagebox.showinfo("⏰ StudyBuddy Reminder", "Time to take a short break! Stretch, hydrate, or rest your eyes.")

    threading.Thread(target=reminder_loop, daemon=True).start()

# --- GUI SETUP ---
root = tk.Tk()
root.title("🎓 StudyBuddy AI")
root.geometry("700x500")
root.configure(bg="#e3f2fd")

quotes = load_quotes()

# Fonts
header_font = ("Segoe UI", 24, "bold")
text_font = ("Segoe UI", 12)
label_font = ("Segoe UI", 11)

# Layout
tk.Label(root, text="", bg="#e3f2fd", height=2).pack()  # Spacer

# Header
tk.Label(root, text="📚 StudyBuddy AI", font=header_font, bg="#e3f2fd", fg="#1a237e").pack(pady=20)

# Mood Button
tk.Button(root, text="🎙️ Speak Your Mood", font=text_font, bg="#3949ab", fg="white", command=analyze_mood, padx=10, pady=5).pack(pady=20)

# Mood display
mood_label = tk.Label(root, text="", font=text_font, bg="#e3f2fd", fg="#0d47a1")
mood_label.pack(pady=10)

# Quote display
quote_label = tk.Label(root, text="", font=label_font, wraplength=600, bg="#e3f2fd", fg="#004d40", justify="center")
quote_label.pack(pady=10)

# Status
status_label = tk.Label(root, text="", font=label_font, bg="#e3f2fd", fg="#1b5e20")
status_label.pack(pady=10)

# Footer
tk.Label(root, text="🎧 Say how you feel: happy, sad, neutral, stressed, tired, emotional", font=("Segoe UI", 10), bg="#e3f2fd", fg="#555").pack(pady=10)

# Start reminder popup loop (e.g., every 30 minutes)
start_reminders(30)

# Start the GUI event loop
root.mainloop()
