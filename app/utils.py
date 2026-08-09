import io
from PIL import Image

def validate_image(file_bytes: bytes) -> bool:
    try:
        Image.open(io.BytesIO(file_bytes)).verify()
        return True
    except Exception:
        return False
