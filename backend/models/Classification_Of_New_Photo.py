import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import mobilenet_v2

# ==============================
# CONFIG
# ==============================
MODEL_PATH = r"C:\Users\agnie\Documents\Studia\Face_Recognition_APP_Team_Project\best_age_model_opt_224.h5"
IMG_SIZE = (224, 224)
MAX_AGE = 116.0

test_images = [
    r"C:\Users\agnie\Downloads\R.jpg",
    r"C:\Users\agnie\Downloads\mankey.jpg",
    r"C:\Users\agnie\Downloads\Infants_Winter_hat_Glance_555750_2560x1708.jpg",
    r"C:\Users\agnie\Downloads\177862_mala_dziewczynka.jpg",
    r"C:\Users\agnie\Downloads\cute-happy-poor-black-child-home_21730-14533.jpeg",
    r"C:\Users\agnie\Downloads\super-closeup-portrait-wonderful-african-woman_923209-2467.avif",
    r"C:\Users\agnie\Downloads\images.jpg",
    r"C:\Users\agnie\Downloads\OIP.jpeg"
]

# ==============================
# Load model
# ==============================
model = tf.keras.models.load_model(MODEL_PATH)
print("✓ Model loaded")

# ==============================
# Face detector (Haar Cascade)
# ==============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ==============================
# Helper: preprocess face
# ==============================
def preprocess_face(face):
    print("  > Original face shape:", face.shape, "dtype:", face.dtype)
    face = cv2.resize(face, IMG_SIZE)
    print("  > Resized face shape:", face.shape)
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    print("  > Converted BGR->RGB")
    face = face.astype(np.float32) / 255.0
    print("  > Normalized face pixel values (0-1)")
    face = mobilenet_v2.preprocess_input(face)
    print("  > Applied MobileNetV2 preprocessing")
    face = np.expand_dims(face, axis=0)
    print("  > Expanded dims for batch:", face.shape)
    return face

# ==============================
# Inference loop
# ==============================
for img_path in test_images:
    print("\n==============================")
    print("Image:", img_path)

    img = cv2.imread(img_path)
    if img is None:
        print("❌ Cannot load image")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )

    # ==============================
    # Detection error handling
    # ==============================
    if len(faces) == 0:
        print("Detection error. No human face recognized.")
        continue

    if len(faces) > 1:
        print("Detection error. More than one face recognized.")
        continue

    # ==============================
    # Single face → predict age
    # ==============================
    x, y, w, h = faces[0]
    face = img[y:y+h, x:x+w]

    print("  > Detected face coordinates: x={}, y={}, w={}, h={}".format(x, y, w, h))
    print("  > Face pixel value range: min={}, max={}".format(face.min(), face.max()))
    
    face_tensor = preprocess_face(face)

    print("  > Feeding face to model...")
    pred_norm = model.predict(face_tensor, verbose=0)[0][0]
    print("  > Model raw output (normalized age):", pred_norm)

    # de-normalization
    pred_age = ((pred_norm + 1) / 2) * MAX_AGE
    pred_age = np.clip(pred_age, 0, MAX_AGE)
    print("  > De-normalized predicted age:", pred_age)

    # ==============================
    # Draw bounding box & prediction
    # ==============================
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(
        img,
        f"Age: {pred_age:.1f}",
        (x, y-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    # ==============================
    # Display image
    # ==============================
    cv2.imshow("Face Age Prediction", img)
    print("  > Displaying image window. Press any key to continue...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
