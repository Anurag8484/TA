import base64
from io import BytesIO
from PIL import Image
import pytesseract


def extract_text_from_base64_image(base64_string: str) -> str:
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"[OCR Error] {str(e)}"
