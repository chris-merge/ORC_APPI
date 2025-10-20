from PIL import Image
import pytesseract
from io import BytesIO

def ocr_local(image_bytes):
    """
    Recibe bytes de imagen y devuelve el texto extraído
    """
    image = Image.open(BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text.strip()
