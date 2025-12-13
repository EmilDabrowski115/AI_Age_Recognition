from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.models import Prediction
from backend.services.age_prediction_service import get_age_service
import uuid
import os
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Directory to store uploaded images
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Test endpoint to verify file upload works
@router.post("/testUpload")
async def test_upload(file: UploadFile = File(...)):
    """Simple test endpoint to verify file upload is working"""
    logger.info("🧪 Test upload endpoint called")
    logger.info(f"File: {file.filename}, Type: {file.content_type}")
    content = await file.read()
    logger.info(f"File size: {len(content)} bytes")
    return {"status": "ok", "filename": file.filename, "size": len(content)}

@router.post("/getAge")
async def get_age(
    image: UploadFile = File(...),
):
    """
    Endpoint for age prediction:
    1. Receive an image from the user
    2. Save the image to disk
    3. Call AI model to predict age
    4. Store the prediction in the database
    5. Return predicted age and confidence
    """

    logger.info("=" * 60)
    logger.info("🚀 /getAge endpoint called")
    logger.info(f"📁 File received: {image.filename}")
    logger.info(f"📝 Content type: {image.content_type}")
    logger.info(f"📏 File size: {image.size if hasattr(image, 'size') else 'unknown'}")

    # Step 1: Read uploaded file bytes
    try:
        logger.info("📖 Reading file bytes...")
        image_bytes = await image.read()
        logger.info(f"✓ File read successfully - {len(image_bytes)} bytes")
    except Exception as e:
        logger.error(f"❌ Failed to read file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read file: {e}")

    # Step 2: Call AI model for age prediction
    try:
        logger.info("🤖 Initializing AI service...")
        age_service = get_age_service()
        logger.info("✓ AI service initialized")

        logger.info("🔮 Running age prediction...")
        result = age_service.predict_from_bytes(image_bytes)
        logger.info(f"📊 Prediction result: {result}")

        if not result['success']:
            logger.warning(f"⚠️ Prediction unsuccessful: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=400, detail=result.get('error', 'Prediction failed'))

        predicted_age = result['predicted_age']
        confidence = result['confidence']
        logger.info(f"✓ Age predicted: {predicted_age} years (confidence: {confidence:.2%})")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ AI prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"AI prediction error: {e}")

    # Step 3: Save uploaded file to disk (after successful prediction)
    try:
        logger.info("💾 Saving uploaded file to disk...")
        file_ext = os.path.splitext(image.filename)[1] if image.filename else '.jpg'
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        logger.info(f"📍 File path: {file_path}")

        with open(file_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"✓ File saved successfully")
    except Exception as e:
        logger.error(f"⚠️ Failed to save file: {e}")
        # Continue even if file save fails - we still have the prediction
        file_path = f"error_saving_file_{uuid.uuid4()}"

    # Step 4: Return response
    response_data = {
        "success": True,
        "predicted_age": predicted_age,
        "confidence": confidence,
        "image_path": file_path
    }
    logger.info(f"📤 Returning response: {response_data}")
    logger.info("=" * 60)
    return JSONResponse(response_data)
