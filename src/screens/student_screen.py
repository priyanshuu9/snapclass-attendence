import streamlit as st
from PIL import Image
import numpy as np
import time
from datetime import datetime
import pandas as pd

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.dialog_attendance_results import attendance_result_dialog

from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import (
    get_all_students, 
    create_student, 
    get_student_subjects, 
    get_student_attendance, 
    unenroll_student_to_subject,
    check_student_exists,
    student_login,
    update_student_embeddings
)
from src.utils.session import save_session, clear_session


def student_dashboard():
    # Load session student details
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    # Refresh student data from DB to reflect any bio changes
    from src.database.db import get_student_by_id
    try:
        updated_student = get_student_by_id(student_id)
        if updated_student:
            st.session_state.student_data = updated_student
            student_data = updated_student
    except Exception:
        pass

    # Dashboard Header
    header_dashboard()

    st.space()

    # Load subjects and attendance logs
    with st.spinner('Loading dashboard data...'):
        try:
            subjects = get_student_subjects(student_id)
            logs = get_student_attendance(student_id)
        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")
            subjects, logs = [], []

    # Process overall metrics
    total_subjects = len(subjects)
    
    # Calculate attendance counts per subject
    stats_map = {}
    total_classes_across_all = 0
    total_present_across_all = 0

    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        total_classes_across_all += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1
            total_present_across_all += 1

    overall_pct = (total_present_across_all / total_classes_across_all * 100) if total_classes_across_all > 0 else 100.0

    # Layout Dashboard Overview Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="📚 Enrolled Subjects", value=total_subjects)
    with m2:
        st.metric(label="📅 Total Class Sessions", value=total_classes_across_all)
    with m3:
        st.metric(label="📈 Overall Attendance Rate", value=f"{overall_pct:.1f}%")

    # Display Warning Banner for low attendance (< 75%)
    low_attendance_warnings = []
    for sub_node in subjects:
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        if stats['total'] > 0:
            pct = (stats['attended'] / stats['total']) * 100
            if pct < 75.0:
                low_attendance_warnings.append(f"**{sub['name']}** ({pct:.1f}%)")

    if low_attendance_warnings:
        st.markdown(f"""
            <div class="warning-alert-container">
                <span style="color: #ef4444; font-weight: 700; font-size: 1.1rem; font-family: 'Outfit'">⚠️ Attendance Alert</span>
                <p style="color: var(--text-primary); margin: 5px 0 0 0; font-family: 'Outfit'; font-size: 0.95rem">
                    Your attendance is currently below the required 75.0% in: {', '.join(low_attendance_warnings)}. Please attend classes to prevent debarment.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Core Navigation Tabs
    tab_subjects, tab_mark, tab_profile = st.tabs([
        "📚 Enrolled Subjects", 
        "✅ Mark Attendance", 
        "⚙️ AI Profile & Biometrics"
    ])

    with tab_subjects:
        c_sub1, c_sub2 = st.columns([3, 1], vertical_alignment='center')
        with c_sub1:
            st.subheader("Your Enrolled Courses")
        with c_sub2:
            if st.button('Enroll in New Course', type='primary', use_container_width=True, key='enroll_new_course_btn'):
                enroll_dialog()

        st.space()

        if subjects:
            cols = st.columns(2)
            for i, sub_node in enumerate(subjects):
                sub = sub_node['subjects']
                sid = sub['subject_id']
                stats = stats_map.get(sid, {"total": 0, "attended": 0})
                
                attendance_rate = (stats['attended'] / stats['total'] * 100) if stats['total'] > 0 else 100.0
                rate_color = "#22C55E" if attendance_rate >= 75.0 else "#EF4444"

                def make_unenroll_callback(sid_to_remove=sid, sname=sub['name']):
                    def callback():
                        if st.button("Unenroll", type='tertiary', key=f"unenroll_{sid_to_remove}", use_container_width=True):
                            try:
                                unenroll_student_to_subject(student_id, sid_to_remove)
                                st.toast(f"Unenrolled from {sname}!", icon="🗑️")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Unenrollment failed: {str(e)}")
                    return callback

                with cols[i % 2]:
                    subject_card(
                        name=sub['name'],
                        code=sub['subject_code'],
                        section=sub['section'],
                        stats=[
                            ('📅', 'Classes Total', stats['total']),
                            ('✅', 'Attended', stats['attended']),
                            ('📈', 'Attendance Rate', f"<span style='color: {rate_color}; font-weight: bold;'>{attendance_rate:.1f}%</span>")
                        ],
                        footer_callback=make_unenroll_callback(sid, sub['name'])
                    )
        else:
            st.info("You are not enrolled in any subjects. Click 'Enroll in New Course' above to join.")

    with tab_mark:
        st.subheader("Mark Your Classroom Attendance")
        st.write("Scan your biometric profile to mark yourself present for the class session.")

        if not subjects:
            st.warning("Please enroll in a subject first before marking attendance.")
        else:
            # Map subjects to selectbox
            subject_options = {f"{s['subjects']['name']} ({s['subjects']['subject_code']})": s['subjects']['subject_id'] for s in subjects}
            
            # Select subject
            sel_sub_label = st.selectbox('Select Course', options=list(subject_options.keys()), key='mark_subject_select')
            selected_subject_id = subject_options[sel_sub_label]

            # Trigger dialogs
            bc1, bc2 = st.columns(2)
            with bc1:
                st.markdown("""
                    <div class="biometric-card">
                        <span style="font-size: 2.2rem;">👤</span>
                        <h4>Face ID Scanner</h4>
                        <p style="font-size: 0.95rem; color: var(--text-muted); min-height: 48px; margin: 8px 0 16px 0;">Scan your face using the webcam to mark attendance automatically.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button('Use Face Scanning', type='primary', use_container_width=True, icon=':material/photo_prints:', key='btn_launch_face'):
                    add_photos_dialog()

            with bc2:
                st.markdown("""
                    <div class="biometric-card">
                        <span style="font-size: 2.2rem;">🎙️</span>
                        <h4>Voice ID Authentication</h4>
                        <p style="font-size: 0.95rem; color: var(--text-muted); min-height: 48px; margin: 8px 0 16px 0;">Record your unique voice signature to verify attendance.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button('Use Voice Verification', type='primary', use_container_width=True, icon=':material/mic:', key='btn_launch_voice'):
                    voice_attendance_dialog(selected_subject_id)

            # Handle Face Recognition Results if images are uploaded in the session state
            if 'attendance_images' not in st.session_state:
                st.session_state.attendance_images = []

            if st.session_state.attendance_images:
                st.divider()
                st.write("📷 **Captured Attendance Images:**")
                gallery_cols = st.columns(4)
                for idx, img in enumerate(st.session_state.attendance_images):
                    with gallery_cols[idx % 4]:
                        st.image(img, use_container_width=True, caption=f'Capture {idx+1}')

                fc1, fc2 = st.columns(2)
                with fc1:
                    if st.button('Clear Photos', type='secondary', use_container_width=True, icon=':material/delete:', key='clear_photos_btn'):
                        st.session_state.attendance_images = []
                        st.rerun()
                with fc2:
                    if st.button('Run Face Verification', type='primary', use_container_width=True, icon=':material/analytics:', key='run_verification_btn'):
                        with st.spinner('AI checking your face...'):
                            is_detected = False
                            for img in st.session_state.attendance_images:
                                img_np = np.array(img.convert('RGB'))
                                detected, _, _ = predict_attendance(img_np)
                                if detected and student_id in detected:
                                    is_detected = True
                                    break
                            
                            if is_detected:
                                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                                results = [{
                                    "Name": student_data['name'],
                                    "ID": student_id,
                                    "Status": "✅ Present"
                                }]
                                attendance_to_log = [{
                                    'student_id': student_id,
                                    'subject_id': selected_subject_id,
                                    'timestamp': current_timestamp,
                                    'is_present': True
                                }]
                                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
                            else:
                                st.error("Verification failed: Face not matched. Please ensure your capture is clear and well-lit!")

    with tab_profile:
        st.subheader("Manage Biometric Profiles")
        st.write("Ensure your facial and vocal profiles are registered properly to support smart scanning.")

        has_face = student_data.get('face_embedding') is not None
        has_voice = student_data.get('voice_embedding') is not None

        # Display Biometric Status Info
        bioc1, bioc2 = st.columns(2)
        with bioc1:
            if has_face:
                st.success("✅ **Face Embedding Profile:** Registered")
            else:
                st.error("❌ **Face Embedding Profile:** Not Registered (Required)")
        with bioc2:
            if has_voice:
                st.success("✅ **Voice Embedding Profile:** Registered")
            else:
                st.warning("⚠️ **Voice Embedding Profile:** Not Registered (Optional backup)")

        st.divider()

        # Update Face Embedding Section
        st.markdown("### Update Face Template")
        profile_face_src = st.radio("Photo Input Source", ["Upload Image File", "Use Webcam Camera"], key='std_profile_face_src_radio')
        face_source = None
        if profile_face_src == "Upload Image File":
            face_source = st.file_uploader("Upload Profile Image", type=['png', 'jpg', 'jpeg'], key='student_profile_photo_uploader')
        else:
            face_source = st.camera_input("Capture photo to refresh your face template", key='profile_face_cam')
        if face_source:
            if st.button('Save New Face Template', type='primary', key='btn_save_face_template'):
                with st.spinner('Extracting face embedding...'):
                    img = np.array(Image.open(face_source))
                    encodings = get_face_embeddings(img)
                    if encodings:
                        try:
                            update_student_embeddings(student_id, face_embedding=encodings[0].tolist())
                            train_classifier() # Retrain local cached mappings
                            st.toast("Face biometric template updated successfully!", icon="✅")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save face profile: {str(e)}")
                    else:
                        st.error("Could not locate facial features. Make sure your face is centered and fully lit!")

        st.divider()

        # Update Voice Embedding Section
        st.markdown("### Update Voice Template")
        voice_source = None
        try:
            voice_source = st.audio_input("Record voice to register/refresh voice template", key='profile_voice_mic')
        except Exception:
            st.warning("Microphone access is not supported or blocked by browser settings.")
        
        if voice_source:
            if st.button('Save New Voice Template', type='primary', key='btn_save_voice_template'):
                with st.spinner('Extracting vocal features...'):
                    try:
                        voice_emb = get_voice_embedding(voice_source.read())
                        if voice_emb:
                            update_student_embeddings(student_id, voice_embedding=voice_emb)
                            st.toast("Voice biometric template updated successfully!", icon="✅")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to extract voice embedding. Try speaking louder or re-recording.")
                    except Exception as e:
                        st.error(f"Voice update failed: {str(e)}")


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_data = st.session_state.student_data
        with st.sidebar:
            st.markdown("""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px; padding-top: 10px;">
                    <img src="https://i.ibb.co/YTYGn5qV/logo.png" style="height:45px;" />
                    <h3 style="margin:0; font-family:'Outfit'; font-weight:800; color: var(--primary);">SnapClass</h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # User profile summary
            st.markdown(f"""
                <div style="padding: 10px 0;">
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;">Student Account</p>
                    <h4 style="margin: 4px 0; font-family: 'Outfit'; font-weight: 700; color: var(--text-primary);">👤 {student_data['name']}</h4>
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted);">@{student_data['username']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Theme toggle
            st.markdown("### 🌓 Appearance")
            theme_toggled = st.toggle("Dark Mode", value=(st.session_state.get('theme', 'dark') == 'dark'), key='student_sidebar_theme_toggle')
            new_theme = 'dark' if theme_toggled else 'light'
            if new_theme != st.session_state.get('theme', 'dark'):
                st.session_state['theme'] = new_theme
                st.query_params['theme'] = new_theme
                import streamlit.components.v1 as components
                components.html(f"""
                    <script>
                        localStorage.setItem('theme', '{new_theme}');
                    </script>
                """, height=0, width=0)
                st.rerun()
                
            st.divider()
            
            # Logout
            if st.button("Logout", type='secondary', key='student_sidebar_logout_btn', use_container_width=True):
                clear_session()
                st.session_state['is_logged_in'] = False
                if 'student_data' in st.session_state:
                    del st.session_state.student_data 
                if 'login_type' in st.session_state:
                    st.session_state['login_type'] = None
                st.rerun()

        student_dashboard()
        return
    
    if "student_login_type" not in st.session_state:
        st.session_state.student_login_type = "login"

    # Screen header
    c1, c2 = st.columns([3.5, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to Home", type='secondary', key='student_back_to_home', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()

    # Routing Login vs Register
    if st.session_state.student_login_type == "login":
        student_screen_login()
    else:
        student_screen_register()


def student_screen_login():
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center; color: var(--primary); margin-top: 0; font-family: Outfit;'>Student Login</h2>", unsafe_allow_html=True)
        st.space()

        login_method = st.radio("Select Authentication Method", ["Password Login", "FaceID Login"], horizontal=True, key='student_login_method_select')

        if login_method == "Password Login":
            username = st.text_input("Username", placeholder='Enter your username', key='std_login_username_input')
            password = st.text_input("Password", type='password', placeholder='Enter your password', key='std_login_pwd_input')
            
            st.divider()
            btnc1, btnc2 = st.columns(2)
            with btnc1:
                if st.button('Log in', shortcut='control+enter', type='primary', use_container_width=True, key='student_password_login_btn'):
                    if not username or not password:
                        st.warning("Please fill in both fields!")
                    else:
                        try:
                            student = student_login(username.strip(), password)
                            if student:
                                save_session('student', student['student_id'])
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = student
                                st.toast(f"Welcome back, {student['name']}!", icon="👋")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Invalid username and password combination.")
                        except Exception as e:
                            st.error(f"Login failed: {str(e)}")
            with btnc2:
                if st.button('Register New Account', use_container_width=True, key='student_go_to_reg_btn'):
                    st.session_state.student_login_type = 'register'
                    st.rerun()

        else:
            st.markdown("<h3 style='font-family: Outfit; font-weight: 700; margin-top: 10px;'>Verify Face to Login</h3>", unsafe_allow_html=True)
            st.info("Look directly into the camera to log in.")
            photo_source = st.camera_input("Verify face", key='student_face_login_cam')

            if photo_source:
                img = np.array(Image.open(photo_source))
                with st.spinner('Scanning...'):
                    try:
                        detected, all_ids, num_faces = predict_attendance(img)
                        if num_faces == 0:
                            st.warning('No face found in camera viewport.')
                        elif num_faces > 1:
                            st.warning('Multiple faces detected. Please make sure only one face is visible.')
                        else:
                            if detected:
                                student_id = list(detected.keys())[0]
                                all_students = get_all_students()
                                student = next((s for s in all_students if s['student_id'] == student_id), None)

                                if student:
                                    save_session('student', student['student_id'])
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = student
                                    st.toast(f"Welcome Back, {student['name']}!", icon="👋")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Face matches a template, but no matching DB record was found.")
                            else:
                                st.error('Face not recognized. If you are a new student, please register first.')
                    except Exception as e:
                        st.error(f"Face scanner error: {str(e)}")

            st.divider()
            if st.button('Register New Account', type="primary", use_container_width=True, key='student_go_to_reg_face_btn'):
                st.session_state.student_login_type = 'register'
                st.rerun()

    footer_dashboard()


def student_screen_register():
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center; color: var(--primary); margin-top: 0; font-family: Outfit;'>Register Student Profile</h2>", unsafe_allow_html=True)
        st.space()

        # Input elements with fixed keys to survive camera inputs
        new_name = st.text_input("Full Name", placeholder='E.g. Hamza Rizvi', key='reg_name_text_input')
        username = st.text_input("Choose Username", placeholder='E.g. hamzarizvi', key='reg_username_text_input')
        password = st.text_input("Password", type='password', placeholder='Enter password', key='reg_pwd_text_input')
        password_confirm = st.text_input("Confirm Password", type='password', placeholder='Confirm password', key='reg_pwd_confirm_text_input')

        st.markdown("<h3 style='font-family: Outfit; font-weight: 700; margin-top: 15px;'>Required: Face Profile Capture</h3>", unsafe_allow_html=True)
        st.info("Capture or upload a clear, bright picture to enable face recognition logins and scans.")
        face_src = st.radio("Photo Input Source", ["Upload Image File", "Use Webcam Camera"], key='std_reg_face_src_radio')
        photo_source = None
        if face_src == "Upload Image File":
            photo_source = st.file_uploader("Upload Profile Image", type=['png', 'jpg', 'jpeg'], key='student_reg_photo_uploader')
        else:
            photo_source = st.camera_input("Center your face", key='student_registration_cam')

        st.markdown("<h3 style='font-family: Outfit; font-weight: 700; margin-top: 15px;'>Optional: Voice Profile Enrollment</h3>", unsafe_allow_html=True)
        st.info("Record a short phrase to register your voice backup (e.g. \"I am present, student profile enrollment.\")")
        audio_data = None
        try:
            audio_data = st.audio_input('Record voice template', key='student_registration_mic')
        except Exception:
            st.warning('Microphone connection not allowed or supported by this browser.')

        st.divider()
        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Create Student Account', type='primary', use_container_width=True, key='student_submit_registration_btn'):
                if not new_name or not username or not password:
                    st.warning('Name, username, and password fields are required!')
                elif password != password_confirm:
                    st.error('Passwords do not match!')
                elif not photo_source:
                    st.error('Face profile capture is required to create a student account.')
                else:
                    try:
                        if check_student_exists(username.strip()):
                            st.error('This username is already taken! Please choose another one.')
                        else:
                            with st.spinner('Creating student profile...'):
                                img = np.array(Image.open(photo_source))
                                encodings = get_face_embeddings(img)
                                if encodings:
                                    face_emb = encodings[0].tolist()

                                    voice_emb = None
                                    if audio_data:
                                        voice_emb = get_voice_embedding(audio_data.read())

                                    response_data = create_student(
                                        username=username.strip(),
                                        password=password,
                                        name=new_name.strip(),
                                        face_embedding=face_emb,
                                        voice_embedding=voice_emb
                                    )

                                    if response_data:
                                        train_classifier()  # Re-evaluate local cached face classifiers
                                        student = response_data[0]
                                        save_session('student', student['student_id'])
                                        st.session_state.is_logged_in = True
                                        st.session_state.user_role = 'student'
                                        st.session_state.student_data = student
                                        st.toast(f'Account created successfully! Welcome, {new_name}!')
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error('Database connection failed. Account could not be created.')
                                else:
                                    st.error('Failed to extract facial vectors from the capture. Ensure your lighting is good and try again.')
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")

        with btnc2:
            if st.button('Login to Existing Account', use_container_width=True, key='student_back_to_login_btn'):
                st.session_state.student_login_type = 'login'
                st.rerun()

    footer_dashboard()