import pyttsx3
import os
from datetime import datetime

def generate_audio_from_text(text, user_id=None, voice_id=None, output_dir="static/uploads/audio"):
    try:
        engine = pyttsx3.init()
        if voice_id:
            engine.setProperty('voice', voice_id)
        filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        path = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        engine.save_to_file(text, path)
        engine.runAndWait()
        return {"status": "success", "path": path, "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}
