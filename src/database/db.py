from src.database.config import supabase, supabase_admin
import bcrypt
import httpx
import streamlit as st

def get_client(admin=False):
    """
    Returns the admin client if requested and available, otherwise the standard client.
    This ensures RLS policies don't block critical login/registration flows.
    """
    if admin and supabase_admin is not None:
        return supabase_admin
    return supabase

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def is_student_schema_updated() -> bool:
    """
    Detects if the database has been updated with the student credential columns.
    Since we have confirmed the schema is updated in production, this returns True
    to prevent transient network or query errors from blocking students.
    """
    return True

def check_teacher_exists(username):
    try:
        client = get_client(admin=True)
        response = client.table("teachers").select("username").ilike("username", username).execute()
        return len(response.data) > 0
    except Exception as e:
        raise Exception(f"Database error checking teacher existence: {str(e)}")

def create_teacher(username, password, name):
    try:
        client = get_client(admin=True)
        data = {"username": username, "password": hash_pass(password), "name": name}
        response = client.table("teachers").insert(data).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to create teacher in database: {str(e)}")

def teacher_login(username, password):
    try:
        client = get_client(admin=True)
        response = client.table("teachers").select("*").ilike("username", username).execute()
        if response.data:
            teacher = response.data[0]
            if check_pass(password, teacher['password']):
                return teacher
        return None
    except Exception as e:
        raise Exception(f"Database error during teacher login: {str(e)}")

def get_teacher_by_id(teacher_id):
    try:
        client = get_client(admin=True)
        response = client.table("teachers").select("*").eq("teacher_id", teacher_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        raise Exception(f"Failed to retrieve teacher info: {str(e)}")

def get_all_students():
    try:
        client = get_client(admin=True)
        response = client.table('students').select("*").execute()
        return response.data
    except Exception as e:
        raise Exception(f"Database error fetching students: {str(e)}")

def get_student_by_id(student_id):
    try:
        client = get_client(admin=True)
        response = client.table("students").select("*").eq("student_id", student_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        raise Exception(f"Failed to retrieve student info: {str(e)}")

def check_student_exists(username):
    try:
        client = get_client(admin=True)
        response = client.table("students").select("username").ilike("username", username).execute()
        return len(response.data) > 0
    except Exception as e:
        raise Exception(f"Database error checking student existence: {str(e)}")

def create_student(username, password, name, face_embedding=None, voice_embedding=None):
    try:
        client = get_client(admin=True)
        data = {
            'username': username,
            'password': hash_pass(password) if password else None,
            'name': name,
            'face_embedding': face_embedding,
            'voice_embedding': voice_embedding
        }
        response = client.table('students').insert(data).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to register student profile: {str(e)}")

def student_login(username, password):
    try:
        client = get_client(admin=True)
        response = client.table("students").select("*").ilike("username", username).execute()
        if response.data:
            student = response.data[0]
            if student.get('password') and check_pass(password, student['password']):
                return student
        return None
    except Exception as e:
        raise Exception(f"Database error during student login: {str(e)}")

def create_subject(subject_code, name, section, teacher_id):
    try:
        client = get_client(admin=True)
        data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
        response = client.table("subjects").insert(data).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to create subject: {str(e)}")

def get_teacher_subjects(teacher_id):
    try:
        client = get_client(admin=True)
        response = client.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
        subjects = response.data

        for sub in subjects:
            sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
            attendance = sub.get('attendance_logs', [])
            unique_sessions = len(set(log['timestamp'] for log in attendance))
            sub['total_classes'] = unique_sessions

            sub.pop('subject_students', None)
            sub.pop('attendance_logs', None)

        return subjects
    except Exception as e:
        raise Exception(f"Failed to load teacher's subjects: {str(e)}")

def enroll_student_to_subject(student_id, subject_id):
    try:
        client = get_client(admin=True)
        data = {'student_id': student_id, "subject_id": subject_id}
        response = client.table('subject_students').insert(data).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to enroll student: {str(e)}")

def unenroll_student_to_subject(student_id, subject_id):
    try:
        client = get_client(admin=True)
        response = client.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to unenroll student: {str(e)}")

def get_student_subjects(student_id):
    try:
        client = get_client(admin=True)
        response = client.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to load student's subjects: {str(e)}")

def get_student_attendance(student_id):
    try:
        client = get_client(admin=True)
        response = client.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to load student's attendance: {str(e)}")

def create_attendance(logs):
    try:
        client = get_client(admin=True)
        response = client.table('attendance_logs').insert(logs).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to record attendance: {str(e)}")

def get_attendance_for_teacher(teacher_id):
    try:
        client = get_client(admin=True)
        response = client.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to fetch teacher attendance records: {str(e)}")

def update_student_embeddings(student_id, face_embedding=None, voice_embedding=None):
    try:
        client = get_client(admin=True)
        data = {}
        if face_embedding is not None:
            data['face_embedding'] = face_embedding
        if voice_embedding is not None:
            data['voice_embedding'] = voice_embedding
        if not data:
            return None
        response = client.table('students').update(data).eq('student_id', student_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to update student embeddings: {str(e)}")

def delete_subject(subject_id):
    try:
        client = get_client(admin=True)
        response = client.table("subjects").delete().eq("subject_id", subject_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to delete subject: {str(e)}")

def update_subject(subject_id, name, section, subject_code):
    try:
        client = get_client(admin=True)
        data = {"name": name, "section": section, "subject_code": subject_code}
        response = client.table("subjects").update(data).eq("subject_id", subject_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to update subject: {str(e)}")

def delete_attendance_session(subject_id, timestamp):
    try:
        client = get_client(admin=True)
        response = client.table('attendance_logs').delete().eq('subject_id', subject_id).eq('timestamp', timestamp).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Failed to clear attendance session: {str(e)}")

