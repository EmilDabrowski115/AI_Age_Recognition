import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import mobilenet_v2
import os
from typing import Tuple, Optional

class AgePredictionService:
    """
    Service for predicting age from face images using a pre-trained model.
    """

    def __init__(self, model_path: str = None):
        """
        Initialize the age prediction service.

        Args:
            model_path: Path to the trained model (.h5 file)
        """
        if model_path is None:
            # Default path relative to this file
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(backend_dir, "models", "best_age_model_opt_224.h5")

        self.model_path = model_path
        self.model = None
        self.face_cascade = None
        self.IMG_SIZE = (224, 224)
        self.MAX_AGE = 116.0

        # Load model and face detector
        self._load_model()
        self._load_face_detector()

    def _load_model(self):
        """Load the trained age prediction model."""
        try:
            # Try loading with compile=False to avoid optimizer issues
            self.model = tf.keras.models.load_model(
                self.model_path,
                compile=False,
                safe_mode=False  # Disable safe mode for legacy models
            )
            print(f"✓ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"⚠️ First load attempt failed, trying legacy format...")
            try:
                # Try with legacy loading for older Keras models
                import h5py
                self.model = tf.keras.models.load_model(
                    self.model_path,
                    compile=False
                )
                print(f"✓ Model loaded with legacy support from {self.model_path}")
            except Exception as e2:
                raise RuntimeError(f"Failed to load model from {self.model_path}: {e2}")

    def _load_face_detector(self):
        """Load the Haar Cascade face detector."""
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            if self.face_cascade.empty():
                raise RuntimeError("Failed to load face cascade classifier")
            print("✓ Face detector loaded")
        except Exception as e:
            raise RuntimeError(f"Failed to load face detector: {e}")

    def _preprocess_face(self, face: np.ndarray) -> np.ndarray:
        """
        Preprocess a face image for the model.

        Args:
            face: BGR face image array

        Returns:
            Preprocessed face tensor ready for model input
        """
        # Resize to model input size
        face = cv2.resize(face, self.IMG_SIZE)

        # Convert BGR to RGB
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        # Normalize pixel values to [0, 1]
        face = face.astype(np.float32) / 255.0

        # Apply MobileNetV2 preprocessing
        face = mobilenet_v2.preprocess_input(face)

        # Add batch dimension
        face = np.expand_dims(face, axis=0)

        return face

    def predict_from_file(self, image_path: str) -> dict:
        """
        Predict age from an image file.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with prediction results:
            {
                'success': bool,
                'predicted_age': float,
                'confidence': float,
                'error': str (if success is False)
            }
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return {
                'success': False,
                'error': 'Cannot load image file'
            }

        return self.predict_from_array(img)

    def predict_from_bytes(self, image_bytes: bytes) -> dict:
        """
        Predict age from image bytes.

        Args:
            image_bytes: Image data as bytes

        Returns:
            Dictionary with prediction results
        """
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {
                'success': False,
                'error': 'Cannot decode image bytes'
            }

        return self.predict_from_array(img)

    def predict_from_array(self, img: np.ndarray) -> dict:
        """
        Predict age from a numpy array image.

        Args:
            img: BGR image as numpy array

        Returns:
            Dictionary with prediction results
        """
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # Handle detection errors
        if len(faces) == 0:
            return {
                'success': False,
                'error': 'No face detected in the image. Please ensure the image contains a clear, frontal face.'
            }

        if len(faces) > 1:
            return {
                'success': False,
                'error': f'Multiple faces detected ({len(faces)} faces). Please provide an image with only one face.'
            }

        # Extract face region
        x, y, w, h = faces[0]
        face = img[y:y+h, x:x+w]

        # Preprocess face
        face_tensor = self._preprocess_face(face)

        # Predict
        pred_norm = self.model.predict(face_tensor, verbose=0)[0][0]

        # De-normalize prediction
        # Model outputs normalized age in range [-1, 1]
        # Convert to actual age: ((pred + 1) / 2) * MAX_AGE
        pred_age = ((pred_norm + 1) / 2) * self.MAX_AGE
        pred_age = float(np.clip(pred_age, 0, self.MAX_AGE))

        # Calculate confidence (for now, use a simple heuristic)
        # You can improve this based on your model's characteristics
        confidence = float(1.0 - abs(pred_norm))  # Higher confidence when prediction is further from 0
        confidence = max(0.5, min(0.99, confidence))  # Clamp between 0.5 and 0.99

        return {
            'success': True,
            'predicted_age': round(pred_age, 1),
            'confidence': round(confidence, 3),
            'face_coordinates': {
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h)
            }
        }


# Global instance to be used across the application
_age_service_instance: Optional[AgePredictionService] = None

def get_age_service() -> AgePredictionService:
    """
    Get or create the singleton instance of AgePredictionService.

    Returns:
        AgePredictionService instance
    """
    global _age_service_instance
    if _age_service_instance is None:
        _age_service_instance = AgePredictionService()
    return _age_service_instance
