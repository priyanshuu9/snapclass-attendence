import dlib
import numpy as np
import face_recognition_models
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    try:
        detector, sp, facerec = load_dlib_models()
        faces = detector(image_np, 1)

        encodings = []
        for face in faces:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) # 128 embedding
            encodings.append(np.array(face_descriptor))
        return encodings
    except Exception as e:
        st.error(f"Face extraction error: {str(e)}")
        return []

@st.cache_resource
def get_trained_model():
    """
    Loads student templates from the database and caches them.
    We return a dictionary containing lists of embeddings and student IDs.
    """
    X = []
    y = []

    try:
        student_db = get_all_students()
    except Exception as e:
        st.warning(f"Database unavailable for loading face templates: {str(e)}")
        return None

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None

    return {'X': X, 'y': y}


def train_classifier():
    """
    Clears the cached student templates so that any newly registered students are loaded.
    """
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    """
    Detects faces in class_image_np and identifies them using nearest-neighbor matching
    against the face embeddings stored in the database.
    Returns:
        detected_students: dict of student_id -> True
        all_students: list of all registered student IDs (with templates)
        num_detected_faces: total number of faces found in the image
    """
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    model_data = get_trained_model()
    if not model_data:
        return detected_students, [], len(encodings)
    
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))
    resemblance_threshold = 0.6  # Standard threshold for dlib face recognition (lower is more strict)

    for encoding in encodings:
        best_match_score = float('inf')
        best_match_id = None

        # Compare this query encoding against all registered student embeddings
        for i, student_embedding in enumerate(X_train):
            score = np.linalg.norm(student_embedding - encoding)
            if score < best_match_score:
                best_match_score = score
                best_match_id = y_train[i]

        # If the closest template matches within our threshold, record the student as present
        if best_match_id is not None and best_match_score <= resemblance_threshold:
            detected_students[best_match_id] = True

    return detected_students, all_students, len(encodings)
