import cv2
import os
from datetime import datetime

def apply_anime_filter(input_image_path, output_dir="static/uploads/images"):
    try:
        img = cv2.imread(input_image_path)
        if img is None:
            return {"status": "error", "message": "Image not found."}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

        color = cv2.bilateralFilter(img, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)

        filename = f"anime_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        cv2.imwrite(output_path, cartoon)

        return {"status": "success", "path": output_path, "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}
