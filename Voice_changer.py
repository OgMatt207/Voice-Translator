import pygame
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator

# Set up text to speech
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)  # 0 for male, 1 for female

def text_to_speech_japanese(text):
    tts = gTTS(text, lang='fr')
    tts.save('output.mp3')
    
    # Initialize pygame mixer if not already initialized
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    # Load and play the generated MP3 file
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Cleanup resources after audio is played
    pygame.mixer.quit()

# Converting text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to record the user's speech
def record_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Recording started")
        audio = r.listen(source)
        print("Recording finished.")

    try:
        text = r.recognize_google(audio)
        if text.strip() == "":
            print("No speech detected. Try again.")
            return record_speech()
        return text
    except sr.UnknownValueError:
        print("Unable to recognize speech")
        return record_speech()
    except sr.RequestError as e:
        print("Error occurred during speech recognition:", str(e))
        return record_speech()

# Main loop
if __name__ == "__main__":
    while True:
        prompt = record_speech().lower()
        print(prompt)
        if "goodbye" in prompt:
            speak("Goodbye")
            break
        else:
            # Translate the recognized text to Japanese
            target_language = "ja"  # Language code for Japanese
            translated_text = GoogleTranslator(source='auto', target=target_language).translate(prompt)
            text_to_speech_japanese(translated_text)

            # Save the translated text to a text file
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(translated_text)

            # Print the translated text
            print(translated_text)
