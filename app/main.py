import os
import io
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import Response
from dotenv import load_dotenv

from .utils import validate_image
from .models import remove_background

load_dotenv()

API_KEY = os.getenv("API_KEY")  # optional security

app = FastAPI(title="Background Remover API", version="1.0")

def verify_api_key(api_key: str = Depends(lambda: None)):
    # If API_KEY is not set, no auth required
    if not API_KEY:
        return True
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True

@app.post("/remove-background")
async def remove_bg(
    file: UploadFile = File(...),
    api_key: str = None,
    _=Depends(verify_api_key)
):
    # 1. Validate file type
    if file.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(400, "Only PNG, JPEG and WEBP are supported")

    # 2. Read and validate image
    contents = await file.read()
    if not validate_image(contents):
        raise HTTPException(400, "Invalid image file")

    # 3. Remove background
    try:
        result_bytes = remove_background(contents)
    except Exception as e:
        raise HTTPException(500, f"Background removal failed: {str(e)}")

    # 4. Return the result as PNG
    return Response(content=result_bytes, media_type="image/png")
