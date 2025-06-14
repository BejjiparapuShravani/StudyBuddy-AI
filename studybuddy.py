import os
import random
import time
import pygame
import speech_recognition as sr

def play_music(folder):
    songs = [song for song in os.listdir(folder) if song.endswith('.mp3')]
    if not songs:
        print(f"No music files found in {folder}")
        return
    song = random.choice(songs)
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(folder, song))
    pygame.mixer.music.play()
    print(f"Playing {song}...")
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def load_quotes(filename="quotes.txt"):
    with open(filename, 'r') as file:
        quotes = [line.strip() for line in file if line.strip()]
    return quotes

def listen_mood():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say how you feel while studying:")
        audio = recognizer.listen(source)
    try:
        mood_text = recognizer.recognize_google(audio)
        print(f"You said: {mood_text}")
        return mood_text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
        return None
    except sr.RequestError:
        print("Sorry, speech service is down.")
        return None

def main():
    quotes = load_quotes()
    mood = listen_mood()
    if mood is None:
        print("No valid mood detected, exiting.")
        return

    if mood == 'happy' or mood == 'neutral':
        print(f"Mood detected: {mood}")
        print("Playing focus music...")
        play_music('focus_music')

    elif mood == 'sad' or mood == 'stressed':
        print(f"Mood detected: {mood}")
        quote = random.choice(quotes)
        print("Motivational quote:", quote)
        print("Playing break music...")
        play_music('break_music')

    else:
        print(f"Mood detected: {mood}")
        print("No specific music or quotes for this mood.")

if __name__ == "__main__":
    main()
