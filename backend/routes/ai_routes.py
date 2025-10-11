from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.app import app
from backend.database import get_db
from backend.models import User, Prediction
import uuid
import os

# Directory to store uploaded images
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/getAge")
async def get_age(
    user_id: int,  # in future, you can get from JWT token
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint skeleton for age prediction:
    1. Receive an image from the user
    2. Save the image to disk
    3. Call your AI model to predict age
    4. Store the prediction in the database
    5. Return predicted age and confidence
    """

    # Step 1: Save uploaded file
    try:
        file_ext = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Step 2: Call your AI model (placeholder)
    # TODO: Replace with actual AI prediction logic
    predicted_age = 25
    confidence = 0.92

    # Step 3: Store prediction in database
    try:
        prediction = Prediction(
            user_id=user_id,
            image_path=file_path,
            predicted_age=predicted_age,
            confidence=confidence
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    # Step 4: Return response
    return JSONResponse({
        "user_id": user_id,
        "predicted_age": predicted_age,
        "confidence": confidence,
        "image_path": file_path
    })
