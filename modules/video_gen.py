from moviepy.editor import TextClip, concatenate_videoclips
import os
from datetime import datetime

def generate_text_video(text, output_dir="static/uploads/videos", font="Arial", fontsize=48, color='white', bg_color='black', duration=3):
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        lines = text.strip().split('.')
        clips = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            clip = TextClip(line, fontsize=fontsize, font=font, color=color, bg_color=bg_color, size=(1280, 720))
            clip = clip.set_duration(duration)
            clips.append(clip)

        final_clip = concatenate_videoclips(clips, method="compose")
        filename = f"text_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        path = os.path.join(output_dir, filename)
        final_clip.write_videofile(path, fps=24)

        return {"status": "success", "path": path, "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}
