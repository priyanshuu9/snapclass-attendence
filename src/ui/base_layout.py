import streamlit as st

def get_theme_css():
    theme = st.session_state.get('theme', 'dark')
    if theme == 'dark':
        return """
        :root {
            --bg-main: #0B0B0B;
            --bg-sidebar: rgba(17, 17, 17, 0.95);
            --bg-card: #181818;
            --bg-secondary: #111111;
            --border: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.25);
            --text-primary: #ffffff;
            --text-muted: #9ca3af;
            --text-on-accent: #ffffff;
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-glow: rgba(99, 102, 241, 0.2);
            --secondary: #8b5cf6;
            --secondary-dark: #7c3aed;
            --secondary-glow: rgba(139, 92, 246, 0.15);
            --bg-gradient: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
                            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.08) 0px, transparent 50%),
                            radial-gradient(at 50% 100%, rgba(99, 102, 241, 0.05) 0px, transparent 50%),
                            #0B0B0B;
            --input-bg: rgba(255, 255, 255, 0.02);
            --input-border: rgba(255, 255, 255, 0.08);
            --input-focus-border: #6366f1;
            --tab-bg: rgba(255, 255, 255, 0.02);
            --tab-border: rgba(255, 255, 255, 0.06);
            --tab-selected: rgba(255, 255, 255, 0.08);
            --metric-bg: rgba(255, 255, 255, 0.02);
            --metric-border: rgba(255, 255, 255, 0.04);
            --card-border-glow: rgba(99, 102, 241, 0.12);
            --shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
            --success-bg: rgba(16, 185, 129, 0.1);
            --success-text: #34d399;
            --card-bg-glass: rgba(24, 24, 24, 0.6);
            --bg-navbar: rgba(11, 11, 11, 0.75);
        }
        """
    else:
        return """
        :root {
            --bg-main: #f8fafc;
            --bg-sidebar: rgba(248, 250, 252, 0.85);
            --bg-card: #ffffff;
            --bg-secondary: #f1f5f9;
            --border: rgba(15, 23, 42, 0.08);
            --border-glow: rgba(99, 102, 241, 0.15);
            --text-primary: #0f172a;
            --text-muted: #64748b;
            --text-on-accent: #ffffff;
            --primary: #4f46e5;
            --primary-dark: #4338ca;
            --primary-glow: rgba(79, 70, 229, 0.15);
            --secondary: #d946ef;
            --secondary-dark: #c084fc;
            --secondary-glow: rgba(217, 70, 239, 0.15);
            --bg-gradient: radial-gradient(at 0% 0%, rgba(224, 227, 255, 0.6) 0px, transparent 50%),
                            radial-gradient(at 100% 0%, rgba(235, 69, 158, 0.12) 0px, transparent 50%),
                            radial-gradient(at 50% 100%, rgba(88, 101, 242, 0.08) 0px, transparent 50%),
                            #f8fafc;
            --input-bg: rgba(255, 255, 255, 0.7);
            --input-border: rgba(88, 101, 242, 0.2);
            --input-focus-border: #4f46e5;
            --tab-bg: rgba(255, 255, 255, 0.6);
            --tab-border: rgba(255, 255, 255, 0.5);
            --tab-selected: #ffffff;
            --metric-bg: rgba(255, 255, 255, 0.7);
            --metric-border: rgba(255, 255, 255, 0.5);
            --card-border-glow: rgba(99, 102, 241, 0.08);
            --shadow: 0 4px 20px rgba(99, 102, 241, 0.05);
            --success-bg: rgba(16, 185, 129, 0.15);
            --success-text: #059669;
            --card-bg-glass: rgba(255, 255, 255, 0.7);
            --bg-navbar: rgba(248, 250, 252, 0.75);
        }
        """

def style_background_home():
    theme = st.session_state.get('theme', 'dark')
    bg_color = "#0B0B0B" if theme == 'dark' else "#f8fafc"
    col_bg = "#181818" if theme == 'dark' else "#ffffff"
    col_border = "rgba(255,255,255,0.08)" if theme == 'dark' else "rgba(0,0,0,0.06)"
    
    st.markdown(f"""
        <style>
                .stApp {{
                    background: {bg_color} !important;
                    background-image: var(--bg-gradient) !important;
                }}
                .stApp div[data-testid="stHorizontalBlock"]:nth-of-type(2) div[data-testid="stColumn"]{{
                    background-color: {col_bg} !important;
                    border: 1px solid {col_border} !important;
                    padding: 2.5rem !important;
                    border-radius: 2rem !important;
                    box-shadow: var(--shadow) !important;
                }}
        </style>  
        """, unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown("""
        <style>
                .stApp {
                    background: var(--bg-gradient) !important;
                    background-attachment: fixed !important;
                }
        </style>  
        """, unsafe_allow_html=True)

def style_base_layout():
    theme_vars = get_theme_css()
    
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
            
            {theme_vars}
            
            /* Global text styling overrides */
            body, .stApp {{
                color: var(--text-primary) !important;
            }}
            
            /* Hide Streamlit Header elements */
            #MainMenu, footer, header {{
                visibility: hidden;
            }}
            
            .block-container {{
                padding-top: 2.5rem !important;    
                max-width: 1000px !important;
            }}

            h1 {{
                font-family: 'Outfit', sans-serif !important;
                font-size: 3.5rem !important;
                font-weight: 800 !important;
                line-height: 1.15 !important;
                margin-bottom: 0rem !important;
                background: linear-gradient(135deg, var(--text-primary) 0%, var(--primary) 100%);
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
            }}
            
            h2 {{
                font-family: 'Outfit', sans-serif !important;
                font-size: 2.25rem !important;
                font-weight: 800 !important;
                line-height: 1.2 !important;
                margin-bottom: 0rem !important;
                color: var(--text-primary) !important;
            }}
            
            h3, h4, p, span, li, label, div[data-testid="stMarkdown"] {{
                font-family: 'Outfit', sans-serif !important;    
                color: var(--text-primary);
            }}
            
            /* Subtitle/caption */
            .stCaption, caption, figcaption, div[data-testid="caption"] {{
                color: var(--text-muted) !important;
            }}

            /* Primary Button style */
            button {{
                border-radius: 14px !important;
                background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
                color: white !important;
                padding: 12px 24px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                box-shadow: var(--shadow) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }}

            button:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px var(--primary-glow) !important;
                background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%) !important;
            }}

            button:active {{
                transform: translateY(0px) !important;
            }}

            /* Secondary Button */
            button[kind="secondary"] {{
                border-radius: 14px !important;
                background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%) !important;
                color: white !important;
                padding: 12px 24px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 15px var(--secondary-glow) !important;
            }}

            button[kind="secondary"]:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px var(--secondary-glow) !important;
                background: linear-gradient(135deg, var(--secondary-dark) 0%, var(--secondary) 100%) !important;
            }}

            /* Tertiary Button */
            button[kind="tertiary"] {{
                border-radius: 14px !important;
                background: var(--input-bg) !important;
                color: var(--text-primary) !important;
                padding: 10px 20px !important;
                border: 1px solid var(--border) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
                box-shadow: none !important;
            }}

            button[kind="tertiary"]:hover {{
                transform: translateY(-2px) !important;
                background: rgba(255, 255, 255, 0.08) !important;
                color: var(--text-primary) !important;
                box-shadow: var(--shadow) !important;
            }}

            /* Inputs & Dropdowns */
            div[data-testid="stTextInput"] input, 
            div[data-testid="stNumberInput"] input, 
            div[data-testid="stTextArea"] textarea,
            div[data-testid="stSelectbox"] div[role="combobox"] {{
                background: var(--input-bg) !important;
                border-radius: 12px !important;
                border: 1px solid var(--input-border) !important;
                font-family: 'Outfit', sans-serif !important;
                color: var(--text-primary) !important;
                padding: 12px 16px !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.01) !important;
                transition: all 0.3s ease !important;
            }}
            div[data-testid="stTextInput"] input:focus, 
            div[data-testid="stNumberInput"] input:focus,
            div[data-testid="stSelectbox"] div[role="combobox"]:focus {{
                border-color: var(--input-focus-border) !important;
                box-shadow: 0 0 0 3px var(--primary-glow) !important;
                background: var(--bg-card) !important;
            }}
            
            /* Labels */
            div[data-testid="stWidgetLabel"] p {{
                color: var(--text-muted) !important;
                font-weight: 500 !important;
            }}

            /* Tabs styling */
            div[data-testid="stTabBar"] {{
                gap: 8px !important;
                background: var(--tab-bg) !important;
                backdrop-filter: blur(8px) !important;
                -webkit-backdrop-filter: blur(8px) !important;
                padding: 6px !important;
                border-radius: 16px !important;
                border: 1px solid var(--tab-border) !important;
                margin-bottom: 20px !important;
            }}
            div[data-testid="stTabBar"] button {{
                border-radius: 12px !important;
                background: transparent !important;
                color: var(--text-muted) !important;
                box-shadow: none !important;
                padding: 8px 16px !important;
                font-weight: 600 !important;
                transition: all 0.25s ease !important;
                border: none !important;
            }}
            div[data-testid="stTabBar"] button[aria-selected="true"] {{
                background: var(--tab-selected) !important;
                color: var(--primary) !important;
                box-shadow: var(--shadow) !important;
            }}
            div[data-testid="stTabBar"] button:hover {{
                color: var(--primary) !important;
                transform: none !important;
            }}

            /* Metrics styling */
            div[data-testid="stMetric"] {{
                background: var(--metric-bg) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                border: 1px solid var(--metric-border) !important;
                border-radius: 20px !important;
                padding: 20px !important;
                box-shadow: var(--shadow) !important;
                text-align: center !important;
                transition: transform 0.3s ease !important;
            }}
            div[data-testid="stMetric"]:hover {{
                transform: translateY(-3px) !important;
                border-color: var(--border-glow) !important;
            }}
            div[data-testid="stMetricLabel"] {{
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                color: var(--text-muted) !important;
                font-size: 0.95rem !important;
            }}
            div[data-testid="stMetricValue"] {{
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                color: var(--primary) !important;
                font-size: 2.25rem !important;
            }}

            /* Glassmorphic border wrapper for login/register */
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                background: var(--bg-card) !important;
                backdrop-filter: blur(15px) !important;
                -webkit-backdrop-filter: blur(15px) !important;
                border: 1px solid var(--border) !important;
                border-radius: 28px !important;
                padding: 2.5rem !important;
                box-shadow: var(--shadow) !important;
                margin-top: 10px !important;
            }}

            /* Biometric scan cards */
            .biometric-card {{
                background: var(--metric-bg) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                border: 1px solid var(--border) !important;
                border-radius: 24px !important;
                padding: 24px !important;
                text-align: center !important;
                margin-bottom: 12px !important;
                box-shadow: var(--shadow) !important;
                transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            }}
            .biometric-card:hover {{
                transform: translateY(-4px) !important;
                box-shadow: 0 15px 30px var(--primary-glow) !important;
                background: var(--bg-card) !important;
                border-color: var(--border-glow) !important;
            }}
            .biometric-card h4 {{
                color: var(--text-primary) !important;
                font-weight: 700 !important;
            }}
            
            /* Sidebar glassmorphism override */
            section[data-testid="stSidebar"] {{
                background-color: var(--bg-sidebar) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border-right: 1px solid var(--border) !important;
            }}
            
            /* Dataframe/Table overrides */
            div[data-testid="stDataFrame"] {{
                border-radius: 12px !important;
                overflow: hidden !important;
                border: 1px solid var(--border) !important;
            }}
            
            /* Custom alert styling overrides for student alert */
            .attendance-alert-container {{
                background-color: var(--success-bg) !important;
                border-left: 6px solid var(--success) !important;
                padding: 15px !important;
                border-radius: 12px !important;
                margin-bottom: 20px !important;
            }}
            
            .warning-alert-container {{
                background-color: rgba(239, 68, 68, 0.1) !important;
                border-left: 6px solid #EF4444 !important;
                padding: 15px !important;
                border-radius: 12px !important;
                margin-bottom: 20px !important;
            }}
            
            /* Radio layout customization */
            div[data-testid="stRadio"] {{
                background: var(--input-bg) !important;
                border-radius: 12px !important;
                padding: 10px 16px !important;
                border: 1px solid var(--border) !important;
            }}
            
            /* Spacing overrides */
            .stSpace {{
                margin-bottom: 1.5rem !important;
            }}
        </style>  
        """, unsafe_allow_html=True)