import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_ai_art(prompt, output_dir="static/uploads/images", style="default"):
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Use a unique filename
        filename = f"ai_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(output_dir, filename)

        # Basic placeholder generation logic (for full AI generation, you would integrate Stable Diffusion, DALL·E, etc.)
        img = Image.new("RGB", (1024, 768), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)

        # Choose font
        font_path = "static/fonts/Roboto-Bold.ttf"
        try:
            font = ImageFont.truetype(font_path, 40)
        except:
            font = ImageFont.load_default()

        # Draw prompt text (placeholder for real AI-generated art)
        draw.text((50, 350), f"Prompt: {prompt}", fill="white", font=font)

        # Save image
        img.save(path)

        return {
            "status": "success",
            "path": path,
            "filename": filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
