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
        /* Modern Fonts and Variables overrides */
        .navbar-brand {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.5rem;
            color: var(--text-primary);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .navbar-links {
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }
        .navbar-link {
            color: var(--text-muted);
            text-decoration: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            transition: color 0.2s ease;
        }
        .navbar-link:hover {
            color: var(--primary);
        }

        /* Flat Navbar Wrapper Selector Hack */
        div[data-testid="stHorizontalBlock"]:first-of-type {
            background: var(--bg-navbar) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border) !important;
            padding: 12px 24px !important;
            margin-bottom: 3rem !important;
            box-shadow: none !important;
        }

        /* Hero Text & Layout */
        .hero-section {
            text-align: center;
            padding: 2rem 1rem 4rem 1rem;
            color: var(--text-primary);
        }
        .hero-title {
            font-family: 'Outfit', sans-serif !important;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            line-height: 1.15 !important;
            color: var(--text-primary) !important;
            margin-bottom: 1.5rem !important;
        }
        .hero-title span {
            color: var(--primary) !important;
        }
        .hero-subtitle {
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.25rem !important;
            color: var(--text-muted) !important;
            max-width: 760px;
            margin: 0 auto !important;
            line-height: 1.6 !important;
        }
        
        /* Features Section */
        .section-title {
            text-align: center;
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            margin-top: 5rem !important;
            margin-bottom: 2.5rem !important;
        }
        .feature-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 2.25rem;
            border: 1px solid var(--border);
            border-left: 5px solid var(--primary);
            color: var(--text-primary);
            box-shadow: none;
            margin-bottom: 1.5rem;
            transition: border-color 0.2s ease;
        }
        .feature-card:hover {
            border-color: var(--primary);
        }
        .feature-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.3rem;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            font-family: 'Outfit', sans-serif;
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* How It Works Card Styling */
        .how-card {
            background: var(--bg-card) !important;
            border-radius: 12px !important;
            padding: 2.5rem !important;
            border: 1px solid var(--border) !important;
            height: 100% !important;
            box-shadow: none !important;
        }
        .how-card h3 {
            color: var(--text-primary) !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            margin-top: 0 !important;
            margin-bottom: 1.25rem !important;
            border-bottom: 1px solid var(--border) !important;
            padding-bottom: 0.5rem !important;
        }
        .how-card ol {
            font-family: 'Outfit', sans-serif !important;
            line-height: 1.8 !important;
            padding-left: 1.2rem !important;
            color: var(--text-muted) !important;
        }
        .how-card li {
            margin-bottom: 0.75rem !important;
            font-weight: 500 !important;
        }

        /* FAQ Accordion Styling */
        .faq-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.75rem;
            margin-bottom: 1.25rem;
            color: var(--text-primary);
            box-shadow: none;
            transition: border-color 0.2s ease;
        }
        .faq-card:hover {
            border-color: var(--primary);
        }
        .faq-question {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            margin-bottom: 0.5rem;
            color: var(--primary);
        }
        .faq-answer {
            font-family: 'Outfit', sans-serif;
            font-size: 0.98rem;
            color: var(--text-muted);
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. Glassmorphism Navigation Bar with Streamlit layout
    nav_c1, nav_c2 = st.columns([4, 1.2], vertical_alignment='center')
    with nav_c1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 20px; padding: 0.2rem 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="https://i.ibb.co/YTYGn5qV/logo.png" style="height:36px;" />
                    <span style="font-family: 'Outfit'; font-weight: 800; font-size: 1.4rem; color: var(--text-primary);">SnapClass</span>
                </div>
                <div style="display: flex; gap: 1.5rem; margin-left: 2.5rem; align-items: center;">
                    <a href="#features" class="navbar-link">Features</a>
                    <a href="#how-it-works" class="navbar-link">Process</a>
                    <a href="#faq" class="navbar-link">FAQ</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with nav_c2:
        # Real-time Theme toggle widget inside Navbar
        theme_toggled = st.toggle("Dark Mode", value=(st.session_state.get('theme', 'dark') == 'dark'), key='home_theme_toggle_widget')
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

    # 2. Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">AI Attendance System<br><span>Built for Smart Classrooms</span></h1>
            <p class="hero-subtitle">
                Automate roll-calls in seconds using computer vision facial scanning and backup voice biometrics. 
                Say goodbye to proxies and administration overhead.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Portals / CTAs (Side by Side)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style="text-align: center;">
                <h2 style="color: var(--text-primary); margin-bottom: 1rem;">Student Portal</h2>
                <p style="color: var(--text-muted); font-family: 'Outfit', sans-serif; font-size: 1.05rem; margin-bottom: 1.5rem; line-height:1.4">
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
                <h2 style="color: var(--text-primary); margin-bottom: 1rem;">Teacher Portal</h2>
                <p style="color: var(--text-muted); font-family: 'Outfit', sans-serif; font-size: 1.05rem; margin-bottom: 1.5rem; line-height:1.4">
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
    st.markdown("<br><hr style='border: 1px solid var(--border)'><br>", unsafe_allow_html=True)

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