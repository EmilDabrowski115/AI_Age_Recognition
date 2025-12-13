# Setup and Testing Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Test User (Required for age verification)
```bash
cd /home/ogchaotic/School/AI_Age_Recognition
python3 create_test_user.py
```

This creates a test user with:
- Username: `testuser`
- Password: `password123`
- User ID: `1`

### 3. Start the Backend Server
```bash
cd /home/ogchaotic/School/AI_Age_Recognition
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

The backend should start at: `http://localhost:8000`

**Test the API:**
```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response: {"status":"ok","message":"API is running"}
```

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd frontend/age_recognition
npm install
```

### 2. Start the Development Server
```bash
npm run dev
```

The frontend should start at: `http://localhost:5173`

## Testing the Age Verification Flow

### Option 1: Using the Frontend UI

1. Open your browser to `http://localhost:5173`
2. Navigate to the Age Verification page
3. Click "Upload your photo" and select an image with a clear, frontal face
4. Click "Verify Age"
5. The system will:
   - Detect the face in the image
   - Predict the age using the AI model
   - Show the predicted age and confidence score
   - Allow registration if age >= 18

### Option 2: Using cURL (Backend Only)

```bash
# Test with an image file
curl -X POST "http://localhost:8000/getAge?user_id=1" \
  -F "file=@/path/to/your/image.jpg"
```

**Expected Success Response:**
```json
{
  "success": true,
  "user_id": 1,
  "predicted_age": 25.3,
  "confidence": 0.876,
  "image_path": "data/uploads/abc-123.jpg",
  "prediction_id": 1
}
```

**Expected Error Responses:**

No face detected:
```json
{
  "detail": "No face detected in the image. Please ensure the image contains a clear, frontal face."
}
```

Multiple faces detected:
```json
{
  "detail": "Multiple faces detected (2 faces). Please provide an image with only one face."
}
```

## Key Implementation Details

### Backend (`/getAge` endpoint)
- **Location:** `backend/routes/ai_routes.py:16`
- **Method:** POST
- **Parameters:**
  - `user_id` (query parameter): ID of the user
  - `file` (multipart/form-data): Image file
- **Returns:** Predicted age, confidence score, and prediction ID

### Age Prediction Service
- **Location:** `backend/services/age_prediction_service.py`
- **Model:** `backend/models/best_age_model_opt_224.h5`
- **Features:**
  - Face detection using Haar Cascade
  - Image preprocessing (224x224, MobileNetV2)
  - Age prediction (0-116 years)
  - Confidence scoring

### Frontend Integration
- **Location:** `frontend/age_recognition/src/views/AgeVerifyPage.vue`
- **Features:**
  - Image file selection with preview
  - Real-time age verification via API
  - Error handling for face detection issues
  - Confidence score display
  - Age threshold check (18+ for registration)

## Troubleshooting

### "No module named 'cv2'"
```bash
pip install opencv-python
```

### "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### CORS Errors
The backend is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000`
- `http://localhost:8000`

If you're using a different port, update `backend/app.py:18`

### "Database error"
Make sure you've created the test user:
```bash
python3 create_test_user.py
```

### Model Loading Error
Verify the model file exists:
```bash
ls -lh backend/models/best_age_model_opt_224.h5
```

## Production Deployment

For production, you'll want to:

1. **Remove test user creation** - Use real authentication
2. **Update CORS origins** - Only allow your production domain
3. **Add authentication** - Get `user_id` from JWT token instead of query parameter
4. **Environment variables** - Store sensitive config in `.env` file
5. **Build frontend** - Run `npm run build` and serve static files
6. **Use production server** - Deploy with gunicorn or similar

## API Endpoints Summary

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/health` | GET | Health check | ✓ Working |
| `/signup` | POST | User registration | ✓ Working |
| `/login` | POST | User login | ✓ Working |
| `/getAge` | POST | Age prediction | ✓ Working |
