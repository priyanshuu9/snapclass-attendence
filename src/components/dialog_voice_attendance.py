import streamlit as st

from src.pipelines.voice_pipeline import process_bulk_audio

from src.database.db import get_client

import pandas as pd


from src.components.dialog_attendance_results import show_attendance_result
from datetime import datetime


@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):
    is_student = st.session_state.get('user_role') == 'student'
    if is_student:
        st.write('Record your voice saying "I am present". Then AI will recognize you.')
        audio_data = st.audio_input("Record your voice")
    else:
        st.write('Record audio of students saying "I am present". Then AI will recognize the students.')
        audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio', type='primary', use_container_width=True):
        # Guard: user must record audio first
        if not audio_data:
            st.warning('⚠️ Please record audio before analyzing.')
            return

        with st.spinner('Processing audio data...'):
            # Use admin client to bypass RLS on subject_students
            client = get_client(admin=True)

            if is_student:
                student_id = st.session_state.student_data['student_id']
                # Fetch student's data
                res = client.table('students').select("name, student_id, voice_embedding").eq('student_id', student_id).execute()
                student_data = res.data[0] if res.data else None

                if not student_data or not student_data.get('voice_embedding'):
                    st.error('You do not have a voice profile registered. Please register a voice sample first.')
                    return

                candidates_dict = {student_id: student_data['voice_embedding']}
            else:
                enrolled_res = client.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course.')
                    return

                candidates_dict = {
                    s['students']['student_id']: s['students']['voice_embedding']
                    for s in enrolled_students if s['students'].get('voice_embedding')
                }

            if not candidates_dict:
                st.error('No voice profiles registered.')
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            if is_student:
                score = detected_scores.get(student_id, 0.0)
                is_present = bool(score > 0)

                if not is_present:
                    st.error("Voice not recognized. Please speak clearly or re-record.")
                    return

                results.append({
                    "Name": student_data['name'],
                    "ID": student_id,
                    "Score": round(score, 3),
                    "Status": "✅ Present"
                })

                attendance_to_log.append({
                    'student_id': student_id,
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': True
                })
            else:
                for node in enrolled_students:
                    student = node['students']
                    score = detected_scores.get(student['student_id'], 0.0)
                    is_present = bool(score > 0)

                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Score": round(score, 3) if is_present else "-",
                        "Status": "✅ Present" if is_present else "❌ Absent"
                    })

                    attendance_to_log.append({
                        'student_id': student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present)
                    })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)

