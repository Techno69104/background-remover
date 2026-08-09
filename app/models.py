from rembg import remove, new_session
import os

_session = None
_MODEL_NAME = os.getenv("REMBG_MODEL", "u2net")   # "u2net", "u2netp", "u2net_cloth_seg", etc.

def get_session():
    global _session
    if _session is None:
        # Force CPU (Render free tier has no GPU)
        _session = new_session(_MODEL_NAME, providers=["CPUExecutionProvider"])
    return _session

def remove_background(image_bytes: bytes) -> bytes:
    session = get_session()
    output = remove(image_bytes, session=session)
    return output
