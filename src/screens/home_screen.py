import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Setup background and styles
    style_background_home()
    style_base_layout()

    # Custom SaaS Styling overrides for home screen
    st.markdown("""
        <style>
        /* Modern Fonts and Variables */
        :root {
            --primary: #5865F2;
            --primary-dark: #4752C4;
            --accent: #EB459E;
            --bg-light: #F3F4F6;
            --text-dark: #1F2937;
        }

        /* Glassmorphism Navigation Bar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.25);
            margin-bottom: 2rem;
        }
        .navbar-brand {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.5rem;
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .navbar-links {
            display: flex;
            gap: 1.5rem;
        }
        .navbar-link {
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            transition: color 0.2s ease;
        }
        .navbar-link:hover {
            color: #EB459E;
        }

        /* Hero Text & Layout */
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            color: white;
        }
        .hero-title {
            font-family: 'Outfit', sans-serif !important;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            line-height: 1.15 !important;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
            margin-bottom: 1.5rem !important;
        }
        .hero-subtitle {
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.35rem !important;
            color: rgba(255, 255, 255, 0.9) !important;
            max-width: 800px;
            margin: 0 auto 3rem auto !important;
            line-height: 1.6 !important;
        }

        /* Portal Cards */
        .portal-card {
            background: white !important;
            border-radius: 24px !important;
            padding: 2.5rem !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            border: 2px solid rgba(255, 255, 255, 0.5) !important;
            text-align: center;
            height: 100%;
        }
        
        /* Features Section */
        .section-title {
            text-align: center;
            color: white;
            font-family: 'Outfit', sans-serif !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            margin-top: 4rem !important;
            margin-bottom: 2.5rem !important;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 18px;
            padding: 1.75rem;
            border-left: 6px solid #EB459E;
            color: #1F2937;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }
        .feature-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.25rem;
            color: #111827;
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            font-family: 'Outfit', sans-serif;
            color: #4B5563;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* How It Works Card Styling */
        .how-card {
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%) !important;
            border-radius: 24px !important;
            padding: 2.25rem !important;
            border: 2px solid #EB459E !important;
            height: 100% !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(235, 69, 158, 0.25) !important;
        }
        .how-card h3 {
            color: #ffffff !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            margin-top: 0 !important;
            margin-bottom: 1.25rem !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding-bottom: 0.5rem !important;
        }
        .how-card ol {
            font-family: 'Outfit', sans-serif !important;
            line-height: 1.8 !important;
            padding-left: 1.2rem !important;
            color: #E2E8F0 !important;
        }
        .how-card li {
            margin-bottom: 0.75rem !important;
            font-weight: 500 !important;
        }

        /* FAQ Accordion Styling */
        .faq-card {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            color: white;
        }
        .faq-question {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #E0E3FF;
        }
        .faq-answer {
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.85);
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. Glassmorphism Navigation Bar
    st.markdown("""
        <div class="navbar">
            <a href="#" class="navbar-brand">
                <img src="https://i.ibb.co/YTYGn5qV/logo.png" style="height:40px;" />
                <span>SnapClass</span>
            </a>
            <div class="navbar-links">
                <a href="#features" class="navbar-link">Features</a>
                <a href="#how-it-works" class="navbar-link">How It Works</a>
                <a href="#faq" class="navbar-link">FAQ</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">AI-Powered Attendance<br>for Modern Classrooms</h1>
            <p class="hero-subtitle">
                Automate class attendance in seconds using facial recognition and voice authentication. 
                Say goodbye to proxy attendance and manual roll calls.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Portals / CTAs (Side by Side)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style="text-align: center;">
                <h2 style="color: white; margin-bottom: 1rem;">Student Portal</h2>
                <p style="color: #E0E3FF; font-family: 'Outfit', sans-serif; font-size: 1.05rem; margin-bottom: 1.5rem; line-height:1.4">
                    Join a class, register your AI templates (Face and Voice), and view your real-time attendance scorecards.
                </p>
                <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
                    <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" style="width:110px;" />
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button('Student Portal', type='primary', use_container_width=True, key='btn_student_portal'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h2 style="color: white; margin-bottom: 1rem;">Teacher Portal</h2>
                <p style="color: #E0E3FF; font-family: 'Outfit', sans-serif; font-size: 1.05rem; margin-bottom: 1.5rem; line-height:1.4">
                    Create subjects, generate enrollment QR codes, launch smart scanning, and download structured attendance sheets.
                </p>
                <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
                    <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" style="width:130px;" />
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button('Teacher Portal', type='primary', use_container_width=True, key='btn_teacher_portal'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # Divider
    st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.2)'><br>", unsafe_allow_html=True)

    # 4. Features Section
    st.markdown("<h2 class='section-title' id='features'>Core AI Capabilities</h2>", unsafe_allow_html=True)
    fcol1, fcol2 = st.columns(2, gap="medium")

    with fcol1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">👤 Face Biometric Scanner</div>
                <div class="feature-desc">
                    Uses deep 128-dimensional facial descriptors to scan and recognize students directly from a class photo or webcam capture. Resolves multiple faces instantly.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-title">🔗 QR & Join Code Auto-Enrollment</div>
                <div class="feature-desc">
                    Teachers can generate dynamic course QR codes. Students scan to log in and automatically enroll in the subject instantly.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with fcol2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🎙️ Voice Verification</div>
                <div class="feature-desc">
                    Uses speaker-discriminative embeddings (powered by Resemblyzer) to verify voice identity when class photos aren't optimal. Perfect backup auth.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-title">📊 Analytics Dashboard</div>
                <div class="feature-desc">
                    Visualizes attendance trends, flags students falling below minimum requirements (75%), and lets teachers export reports to CSV.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # How it Works Section
    st.markdown("<h2 class='section-title' id='how-it-works'>How It Works</h2>", unsafe_allow_html=True)
    
    hcol1, hcol2 = st.columns(2)
    with hcol1:
        st.markdown("""
            <div class="how-card">
                <h3>For Teachers</h3>
                <ol>
                    <li>Create your teacher profile with secure credentials.</li>
                    <li>Add your subjects/courses to your dashboard.</li>
                    <li>Display the generated enrollment link or QR code in class.</li>
                    <li>Start a scanning session (Face/Voice) to record attendance instantly!</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    with hcol2:
        st.markdown("""
            <div class="how-card">
                <h3>For Students</h3>
                <ol>
                    <li>Create your profile and enroll your Face (via camera) and Voice templates.</li>
                    <li>Enter the join code shared by your teacher.</li>
                    <li>Scan your face/voice to mark attendance during class sessions.</li>
                    <li>Check your records and class attendance metrics anytime.</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("<h2 class='section-title' id='faq'>Frequently Asked Questions</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="faq-card">
            <div class="faq-question">❓ How accurate is the face recognition scanner?</div>
            <div class="faq-answer">
                It uses deep neural network embeddings mapped through dlib. By projecting facial layouts into a 128D metric space, it matches templates with Euclidean distances. Setting resemblance boundaries (0.6 threshold) prevents simple proxies.
            </div>
        </div>
        <div class="faq-card">
            <div class="faq-question">❓ What if the camera is unavailable?</div>
            <div class="faq-answer">
                Students or teachers can use the high-fidelity Voice Attendance tool as an audio-biometric backup. Alternatively, teachers can correct logs manually.
            </div>
        </div>
        <div class="faq-card">
            <div class="faq-question">❓ Is our data secure in Supabase?</div>
            <div class="faq-answer">
                Yes. Passwords are salted and hashed using bcrypt. Access policies are protected via PostgreSQL Row Level Security (RLS), restricting private data to authorized roles.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    footer_home()