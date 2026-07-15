import streamlit as st
from datetime import datetime
import pandas as pd
import time
import numpy as np
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog

from src.database.config import supabase
from src.database.db import (
    check_teacher_exists, 
    create_teacher, 
    teacher_login, 
    get_teacher_subjects, 
    get_attendance_for_teacher,
    get_client,
    delete_subject,
    update_subject,
    delete_attendance_session,
    create_attendance,
    unenroll_student_to_subject
)
from src.pipelines.face_pipeline import predict_attendance
from src.pipelines.voice_pipeline import process_bulk_audio


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        # Redesigned Premium Glassmorphic Sidebar
        teacher_data = st.session_state.teacher_data
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
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;">Professor Account</p>
                    <h4 style="margin: 4px 0; font-family: 'Outfit'; font-weight: 700; color: var(--text-primary);">🏫 Prof. {teacher_data['name']}</h4>
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted);">@{teacher_data['username']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Theme toggle
            st.markdown("### 🌓 Appearance")
            theme_toggled = st.toggle("Dark Mode", value=(st.session_state.get('theme', 'dark') == 'dark'), key='teacher_sidebar_theme_toggle')
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
            if st.button("Logout", type='secondary', key='teacher_sidebar_logout_btn', use_container_width=True):
                from src.utils.session import clear_session
                clear_session()
                st.session_state['is_logged_in'] = False
                if 'teacher_data' in st.session_state:
                    del st.session_state.teacher_data 
                if 'login_type' in st.session_state:
                    st.session_state['login_type'] = None
                if 'active_teacher_subject' in st.session_state:
                    del st.session_state.active_teacher_subject
                st.rerun()

        # Check if teacher has selected a course to drill down
        if st.session_state.get("active_teacher_subject"):
            teacher_subject_details_dashboard()
        else:
            teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data['teacher_id']

    # Clean header presentation
    header_dashboard()
    st.space()

    # Tabs inside general dashboard
    tab_courses, tab_all_logs = st.tabs(["📚 My Subjects", "📋 Global Attendance Records"])

    with tab_courses:
        col1, col2 = st.columns([3, 1], vertical_alignment='center')
        with col1:
            st.subheader("Manage Subjects")
        with col2:
            if st.button('Create New Subject', type='primary', use_container_width=True, key='create_new_sub_btn'):
                create_subject_dialog(teacher_id)

        st.space()

        # LIST all SUBJECTS
        subjects = get_teacher_subjects(teacher_id)
        if subjects:
            cols = st.columns(2)
            for i, sub in enumerate(subjects):
                stats = [
                    ("🫂", "Enrolled Students", sub['total_students']),
                    ("🕰️", "Class Sessions", sub['total_classes']),
                ]
                
                # Make dynamic callback to capture loop variable correctly
                def make_card_footer(s=sub):
                    fc1, fc2 = st.columns(2)
                    with fc1:
                        if st.button(f"Share", key=f"share_{s['subject_code']}", icon=":material/share:", use_container_width=True):
                            share_subject_dialog(s['name'], s['subject_code'])
                    with fc2:
                        if st.button(f"Manage Course", key=f"manage_{s['subject_code']}", type="primary", use_container_width=True):
                            st.session_state.active_teacher_subject = s
                            st.rerun()

                with cols[i % 2]:
                    subject_card(
                        name=sub['name'],
                        code=sub['subject_code'],
                        section=sub['section'],
                        stats=stats,
                        footer_callback=make_card_footer
                    )
        else:
            st.info("No courses found. Create one above to get started!")

    with tab_all_logs:
        st.subheader("Global Attendance Logs")
        records = get_attendance_for_teacher(teacher_id)

        if not records:
            st.info("No attendance logs recorded yet.")
        else:
            data = []
            for r in records:
                ts = r.get('timestamp')
                data.append({
                    "ts_group": ts.split(".")[0] if ts else None,
                    "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
                    "Subject": r['subjects']['name'],
                    "Subject Code": r['subjects']['subject_code'],
                    "is_present": bool(r.get('is_present', False))
                })

            df = pd.DataFrame(data)
            summary = (
                df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
                .agg(
                    Present_Count=('is_present', 'sum'),
                    Total_Count=('is_present', 'count')
                ).reset_index()
            )
            summary['Attendance Stats'] = (
                "✅ " + summary['Present_Count'].astype(str) + " / "
                + summary['Total_Count'].astype(str) + ' Present'
            )
            display_df = (
                summary.sort_values(by='ts_group', ascending=False)
                [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
            )
            st.dataframe(display_df, use_container_width=True, hide_index=True)

    footer_dashboard()


def teacher_subject_details_dashboard():
    subject = st.session_state.active_teacher_subject
    subject_id = subject['subject_id']

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        st.subheader(f"📘 {subject['name']} ({subject['subject_code']})")
        st.caption(f"Section: {subject['section']}")
    with c2:
        if st.button("← Back to Subjects", type='secondary', use_container_width=True, key='back_to_subjects_list_btn'):
            del st.session_state.active_teacher_subject
            st.rerun()

    # Tabs inside Subject Details Drilldown
    tab_students, tab_take, tab_logs, tab_analytics, tab_settings = st.tabs([
        "📋 Enrolled Students",
        "📸 Take Attendance (AI)",
        "📝 Attendance Logs",
        "📊 Analytics & Trends",
        "⚙️ Course Settings"
    ])

    client = get_client(admin=True)

    with tab_students:
        st.subheader("Enrolled Student Registry")
        st.write("Below are all the students enrolled in this course.")

        enrolled_res = client.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute()
        enrolled_students = enrolled_res.data

        if not enrolled_students:
            st.info("No students enrolled in this course yet.")
        else:
            student_list = []
            for i, es in enumerate(enrolled_students):
                s = es['students']
                face_status = "✅ Registered" if s.get('face_embedding') else "❌ Missing"
                voice_status = "✅ Registered" if s.get('voice_embedding') else "❌ Missing"

                student_list.append({
                    "Student ID": s['student_id'],
                    "Name": s['name'],
                    "Username": s['username'],
                    "Face Template": face_status,
                    "Voice Template": voice_status,
                })
            
            s_df = pd.DataFrame(student_list)
            st.dataframe(s_df, use_container_width=True, hide_index=True)

            # Manual Unenroll form
            st.markdown("#### Unenroll Student")
            to_unenroll = st.selectbox("Select student to unenroll", options=[f"{s['Name']} (ID: {s['Student ID']})" for s in student_list], key='unenroll_selectbox')
            if st.button("Remove Selected Student", type="secondary", key='btn_unenroll_student_submit'):
                selected_id = int(to_unenroll.split("ID: ")[1].split(")")[0])
                try:
                    unenroll_student_to_subject(selected_id, subject_id)
                    st.toast(f"Removed student from subject registry.", icon="🗑️")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to unenroll: {str(e)}")

    with tab_take:
        st.subheader("Start Smart Attendance Session")
        st.write("Scan class biometrics to record present/absent students automatically.")

        if not enrolled_students:
            st.warning("You must have students enrolled in this class to take attendance.")
        else:
            mode = st.radio("Attendance Biometric Mode", ["Face Recognition (Class Photo)", "Voice Recognition (Class Audio)"], key='teacher_take_mode')

            if mode == "Face Recognition (Class Photo)":
                st.write("Upload a class photo or take a picture using the classroom webcam.")
                
                face_source = st.radio("Photo Input Source", ["Upload Image File", "Use Webcam Camera"], key='face_input_src_radio')
                img_data = None
                if face_source == "Upload Image File":
                    img_data = st.file_uploader("Upload Class Image", type=['png', 'jpg', 'jpeg'], key='class_photo_uploader')
                else:
                    img_data = st.camera_input("Take snapshot of the class", key='class_photo_camera')

                if img_data:
                    st.image(img_data, caption="Loaded class photo", use_container_width=True)
                    if st.button("Run AI Face Analysis", type="primary", use_container_width=True, key='teacher_run_face_btn'):
                        with st.spinner("AI is scanning face templates..."):
                            img = Image.open(img_data)
                            img_np = np.array(img.convert('RGB'))
                            
                            detected_students, all_students_with_bio, num_faces = predict_attendance(img_np)
                            
                            results = []
                            logs_to_save = []
                            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                            for node in enrolled_students:
                                s = node['students']
                                s_id = s['student_id']
                                is_present = s_id in detected_students
                                
                                results.append({
                                    "Student ID": s_id,
                                    "Name": s['name'],
                                    "Status": "✅ Present" if is_present else "❌ Absent"
                                })
                                logs_to_save.append({
                                    "student_id": s_id,
                                    "subject_id": subject_id,
                                    "timestamp": current_timestamp,
                                    "is_present": is_present
                                })

                            st.session_state.pending_attendance = (pd.DataFrame(results), logs_to_save)
                            st.toast(f"Face scanner completed. Found {num_faces} face(s) in image.", icon="🧠")

            else:
                st.write("Record class audio where students speak their attendance phrase, or upload a pre-recorded clip.")
                audio_source = st.radio("Audio Input Source", ["Upload Audio File", "Record Classroom Mic"], key='audio_input_src_radio')
                audio_data = None
                if audio_source == "Upload Audio File":
                    audio_data = st.file_uploader("Upload Classroom Audio", type=['wav', 'mp3', 'ogg', 'm4a'], key='class_audio_uploader')
                else:
                    try:
                        audio_data = st.audio_input("Record classroom voice responses", key='class_audio_mic')
                    except Exception:
                        st.warning("Microphone access is not enabled or supported.")

                if audio_data:
                    if st.button("Run AI Speaker Identification", type="primary", use_container_width=True, key='teacher_run_voice_btn'):
                        with st.spinner("Processing audio embeddings..."):
                            # Retrieve student templates
                            candidates_dict = {
                                es['students']['student_id']: es['students']['voice_embedding']
                                for es in enrolled_students if es['students'].get('voice_embedding')
                            }

                            if not candidates_dict:
                                st.error("None of the enrolled students have voice templates registered in their profiles.")
                            else:
                                raw_bytes = audio_data.read()
                                detected_scores = process_bulk_audio(raw_bytes, candidates_dict)

                                results = []
                                logs_to_save = []
                                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                                for node in enrolled_students:
                                    s = node['students']
                                    s_id = s['student_id']
                                    score = detected_scores.get(s_id, 0.0)
                                    is_present = bool(score > 0.0)

                                    results.append({
                                        "Student ID": s_id,
                                        "Name": s['name'],
                                        "Confidence Score": f"{score:.3f}" if is_present else "-",
                                        "Status": "✅ Present" if is_present else "❌ Absent"
                                    })
                                    logs_to_save.append({
                                        "student_id": s_id,
                                        "subject_id": subject_id,
                                        "timestamp": current_timestamp,
                                        "is_present": is_present
                                    })

                                st.session_state.pending_attendance = (pd.DataFrame(results), logs_to_save)
                                st.toast("Vocal biometric processor completed.", icon="🧠")

            # Structured Review & Save Screen for taken attendance
            if st.session_state.get("pending_attendance"):
                st.divider()
                st.markdown("### Review Captured Attendance")
                df_rev, logs_rev = st.session_state.pending_attendance
                st.dataframe(df_rev, use_container_width=True, hide_index=True)

                rc1, rc2 = st.columns(2)
                with rc1:
                    if st.button("Discard Results", type="secondary", use_container_width=True, key='btn_discard_pending'):
                        del st.session_state.pending_attendance
                        st.rerun()
                with rc2:
                    if st.button("Confirm and Save Logs", type="primary", use_container_width=True, key='btn_save_pending'):
                        try:
                            create_attendance(logs_rev)
                            st.success("Attendance sheet synced to database successfully!")
                            del st.session_state.pending_attendance
                            time.sleep(1.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Database sync failed: {str(e)}")

    with tab_logs:
        st.subheader("Attendance Log Registry")
        
        # Load logs for this subject
        subj_logs_res = client.table('attendance_logs').select("*, students(*)").eq('subject_id', subject_id).execute()
        subj_logs = subj_logs_res.data

        if not subj_logs:
            st.info("No attendance records found for this course yet.")
        else:
            # Group records by timestamp
            session_groups = {}
            for row in subj_logs:
                ts = row['timestamp']
                if ts not in session_groups:
                    session_groups[ts] = []
                session_groups[ts].append(row)

            # Map timestamps to selectbox option labels
            session_options = {}
            for ts in sorted(session_groups.keys(), reverse=True):
                dt_str = datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p")
                p_count = sum(1 for r in session_groups[ts] if r['is_present'])
                tot_count = len(session_groups[ts])
                session_options[f"{dt_str} ({p_count}/{tot_count} Present)"] = ts

            selected_sess_label = st.selectbox("Select Class Session", options=list(session_options.keys()), key='session_selectbox')
            selected_timestamp = session_options[selected_sess_label]
            session_rows = session_groups[selected_timestamp]

            # Display student statuses inside selected session
            st.markdown("#### Student Attendance Sheet")
            
            # Form-like toggles
            updated_states = {}
            for row in session_rows:
                student = row['students']
                s_id = row['student_id']
                
                col_name, col_status = st.columns([3, 1], vertical_alignment='center')
                with col_name:
                    st.write(student['name'])
                with col_status:
                    updated_states[s_id] = st.toggle("Present", value=bool(row['is_present']), key=f"toggle_att_{s_id}_{selected_timestamp}")

            # Save manual updates
            uc1, uc2 = st.columns(2)
            with uc1:
                if st.button("Save Manual Corrections", type="primary", use_container_width=True, key='save_manual_corrections_btn'):
                    with st.spinner("Updating logs..."):
                        try:
                            # 1. Delete existing records for this session
                            delete_attendance_session(subject_id, selected_timestamp)
                            # 2. Insert corrected records
                            corrected_logs = []
                            for s_id, is_pres in updated_states.items():
                                corrected_logs.append({
                                    "student_id": s_id,
                                    "subject_id": subject_id,
                                    "timestamp": selected_timestamp,
                                    "is_present": is_pres
                                })
                            create_attendance(corrected_logs)
                            st.toast("Manual attendance overrides saved successfully!", icon="✅")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Correction failed: {str(e)}")
            with uc2:
                if st.button("Delete Session Record", type="secondary", use_container_width=True, key='delete_session_btn'):
                    try:
                        delete_attendance_session(subject_id, selected_timestamp)
                        st.toast("Deleted class session attendance sheet.", icon="🗑️")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Deletion failed: {str(e)}")

            # Export to CSV section
            st.divider()
            st.markdown("#### Export Report")
            export_data = []
            for ts in sorted(session_groups.keys()):
                dt_str = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")
                for r in session_groups[ts]:
                    export_data.append({
                        "Date": dt_str,
                        "Student Name": r['students']['name'],
                        "Username": r['students']['username'],
                        "Is Present": "Yes" if r['is_present'] else "No"
                    })
            export_df = pd.DataFrame(export_data)
            csv_bytes = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Structured CSV Report",
                data=csv_bytes,
                file_name=f"Attendance_{subject['subject_code']}.csv",
                mime="text/csv",
                use_container_width=True,
                key='download_csv_report_btn'
            )

    with tab_analytics:
        st.subheader("Attendance Analytics")

        if not subj_logs:
            st.info("No logs available for charts yet.")
        else:
            # Prepare data
            chart_data = []
            student_stats = {}
            total_sess = len(session_groups)

            for row in subj_logs:
                ts = row['timestamp']
                dt_short = datetime.fromisoformat(ts).strftime("%m-%d")
                is_pres = bool(row['is_present'])

                chart_data.append({
                    "Date": dt_short,
                    "is_present": 1 if is_pres else 0
                })

                s_id = row['student_id']
                s_name = row['students']['name']
                if s_id not in student_stats:
                    student_stats[s_id] = {"name": s_name, "attended": 0}
                if is_pres:
                    student_stats[s_id]['attended'] += 1

            c_df = pd.DataFrame(chart_data)
            
            # 1. Bar Chart: Present student count per session
            sess_trends = c_df.groupby("Date").sum().reset_index()
            st.markdown("##### Present Student Counts per Class Session")
            st.bar_chart(sess_trends, x="Date", y="is_present")

            # 2. Alerts for low attendance
            st.markdown("##### Students with Low Attendance Alert (< 75%)")
            low_att_list = []
            for s_id, stats in student_stats.items():
                rate = (stats['attended'] / total_sess * 100) if total_sess > 0 else 100.0
                if rate < 75.0:
                    low_att_list.append({
                        "Student Name": stats['name'],
                        "Attended Sessions": f"{stats['attended']} / {total_sess}",
                        "Attendance Rate": f"{rate:.1f}%"
                    })
            
            if low_att_list:
                st.warning("⚠️ The following students are currently matching flags for low class presence:")
                st.table(pd.DataFrame(low_att_list))
            else:
                st.success("🎉 Excellent! All students are currently maintaining attendance rates >= 75%.")

    with tab_settings:
        st.subheader("Course Controls & Actions")
        
        # Course Edit Form
        st.write("Update general details for this course.")
        new_sub_name = st.text_input("Subject Name", value=subject['name'], key='edit_sub_name_input')
        new_sub_section = st.text_input("Section", value=subject['section'], key='edit_sub_sect_input')
        new_sub_code = st.text_input("Subject Code", value=subject['subject_code'], key='edit_sub_code_input')

        ec1, ec2 = st.columns(2)
        with ec1:
            if st.button("Save Course Settings", type="primary", use_container_width=True, key='btn_update_subject_submit'):
                if new_sub_name and new_sub_section and new_sub_code:
                    try:
                        update_subject(subject_id, new_sub_name.strip(), new_sub_section.strip(), new_sub_code.strip())
                        # Update session reference
                        st.session_state.active_teacher_subject['name'] = new_sub_name
                        st.session_state.active_teacher_subject['section'] = new_sub_section
                        st.session_state.active_teacher_subject['subject_code'] = new_sub_code
                        st.success("Course details updated successfully!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Update failed: {str(e)}")
                else:
                    st.warning("Fields cannot be empty!")
        with ec2:
            st.write("") # placeholder
            
        st.divider()

        # Archive/Delete course
        st.markdown("#### ⚠️ Danger Zone")
        st.warning("Archiving or deleting a course will permanently delete all enrollments and historical attendance logs from the database. This action is irreversible.")
        
        confirm_del_text = st.text_input("To confirm, type the course code below:", placeholder=subject['subject_code'], key='delete_confirm_text_input')
        
        if st.button("Delete Course Permanently", type="secondary", use_container_width=True, key='btn_delete_course_submit'):
            if confirm_del_text.strip() == subject['subject_code']:
                try:
                    delete_subject(subject_id)
                    st.toast(f"Course permanently deleted.", icon="🗑️")
                    del st.session_state.active_teacher_subject
                    time.sleep(1.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Deletion failed: {str(e)}")
            else:
                st.error("Confirmation text mismatch! Course was not deleted.")


def login_teacher(username, password):
    if not username or not password:
        return False, "Username and password cannot be empty."
    
    try:
        teacher = teacher_login(username.strip(), password)
        if teacher:
            from src.utils.session import save_session
            save_session('teacher', teacher['teacher_id'])
            st.session_state.user_role = 'teacher'
            st.session_state.teacher_data = teacher
            st.session_state.is_logged_in = True
            return True, ""
        return False, "Invalid username and password combination."
    except Exception as e:
        return False, f"Login error: {str(e)}"


def teacher_screen_login():
    # Screen Header
    c1, c2 = st.columns([3.5, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to Home", type='secondary', key='teacher_back_to_home', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()

    with st.container(border=True):
        st.markdown("<h2 style='text-align: center; color: var(--primary); margin-top: 0; font-family: Outfit;'>Teacher Login</h2>", unsafe_allow_html=True)
        st.space()

        teacher_username = st.text_input("Username", placeholder='Enter your username', key='t_login_username_input')
        teacher_pass = st.text_input("Password", type='password', placeholder="Enter your password", key='t_login_pwd_input')

        st.divider()
        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Log in', shortcut='control+enter', type='primary', use_container_width=True, key='teacher_submit_login_btn'):
                # Call local helper login_teacher defined in this file
                success, error_msg = login_teacher(teacher_username, teacher_pass)
                if success:
                    st.toast("Welcome back, Professor!", icon="👋")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(error_msg)

        with btnc2:
            if st.button('Register Teacher Account', use_container_width=True, key='teacher_go_to_reg_btn'):
                st.session_state.teacher_login_type = 'register'
                st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match!"
    
    try:
        if check_teacher_exists(teacher_username.strip()):
            return False, "Username already taken! Please choose another one."
        create_teacher(teacher_username.strip(), teacher_pass, teacher_name.strip())
        return True, "Successfully created profile! You can login now."
    except Exception as e:
        return False, f"Registration error: {str(e)}"
    
 
def teacher_screen_register():
    c1, c2 = st.columns([3.5, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to Home", type='secondary', key='teacher_reg_back_to_home', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()

    with st.container(border=True):
        st.markdown("<h2 style='text-align: center; color: var(--primary); margin-top: 0; font-family: Outfit;'>Register Teacher Profile</h2>", unsafe_allow_html=True)
        st.space()
        
        teacher_username = st.text_input("Choose Username", placeholder='ananyaroy', key='t_reg_username')
        teacher_name = st.text_input("Full Name", placeholder='Ananya Roy', key='t_reg_name')
        teacher_pass = st.text_input("Password", type='password', placeholder="Enter password", key='t_reg_pwd')
        teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="Confirm password", key='t_reg_pwd_confirm')

        st.divider()

        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Register Now', shortcut='control+enter', type='primary', use_container_width=True, key='teacher_submit_reg_btn'):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    time.sleep(1.5)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button('Login to Existing Account', use_container_width=True, key='teacher_reg_back_to_login_btn'):
                st.session_state.teacher_login_type = 'login'
                st.rerun()

    footer_dashboard()