import os
import speech_recognition as sr
from datetime import datetime

def convert_voice_to_text(audio_file_path, language="en-US"):
    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language=language)
        return {
            "status": "success",
            "text": text
        }

    except sr.UnknownValueError:
        return {
            "status": "error",
            "message": "Could not understand the audio."
        }

    except sr.RequestError as e:
        return {
            "status": "error",
            "message": f"Could not request results; {e}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
