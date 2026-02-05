import time
import pytesseract
from PIL import Image
import io
import os
from fastapi import FastAPI, File, UploadFile, HTTPException

# --- CONFIGURATION ---
# We point Python to the folder you verified in Phase 1

path_to_tesseract = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

app = FastAPI(title="Flexbone OCR Challenge")

@app.get("/")
def home():
    return {"message": "OCR API is running locally."}

@app.post("/extract-text")
async def extract_text(image: UploadFile = File(...)):
    # 1. Start Timer 
    start_time = time.time()

    # 2. Validation 
    if image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file. Only JPG allowed.")

    try:
        # 3. Read Image
        contents = await image.read()
        image_obj = Image.open(io.BytesIO(contents))

        # 4. Perform OCR 
        # We get detailed data to calculate confidence
        data = pytesseract.image_to_data(image_obj, output_type=pytesseract.Output.DICT)
        
        extracted_text_list = []
        confidences = []

        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > -1:
                text = data['text'][i].strip()
                if text:
                    extracted_text_list.append(text)
                    confidences.append(float(data['conf'][i]))

        final_text = " ".join(extracted_text_list)
        
        # Calculate Average Confidence 
        avg_confidence = 0.0
        if confidences:
            # Convert 0-100 scale to 0.0-1.0
            avg_confidence = sum(confidences) / len(confidences) / 100.0

        # 5. Calculate Time
        processing_time = (time.time() - start_time) * 1000

        # 6. Return JSON 
        return {
            "success": True,
            "text": final_text,
            "confidence": round(avg_confidence, 2),
            "processing_time_ms": int(processing_time)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }