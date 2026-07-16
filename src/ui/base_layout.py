import streamlit as st

def get_theme_css():
    theme = st.session_state.get('theme', 'dark')
    if theme == 'dark':
        return """
        :root {
            --bg-main: #0B0B0B;
            --bg-sidebar: #111111;
            --bg-card: #161616;
            --bg-secondary: #121212;
            --border: #222222;
            --border-glow: #333333;
            --text-primary: #ffffff;
            --text-muted: #8e8e93;
            --text-on-accent: #ffffff;
            --primary: #4f46e5;
            --primary-dark: #3730a3;
            --primary-glow: transparent;
            --secondary: #7c3aed;
            --secondary-dark: #5b21b6;
            --secondary-glow: transparent;
            --bg-gradient: #0B0B0B;
            --input-bg: #1a1a1a;
            --input-border: #2c2c2e;
            --input-focus-border: #4f46e5;
            --tab-bg: #111111;
            --tab-border: #222222;
            --tab-selected: #1a1a1a;
            --metric-bg: #161616;
            --metric-border: #222222;
            --card-border-glow: #222222;
            --shadow: none;
            --success-bg: rgba(16, 185, 129, 0.1);
            --success-text: #10b981;
            --card-bg-glass: #161616;
            --bg-navbar: #0B0B0B;
        }
        """
    else:
        return """
        :root {
            --bg-main: #f8fafc;
            --bg-sidebar: #ffffff;
            --bg-card: #ffffff;
            --bg-secondary: #f1f5f9;
            --border: #e2e8f0;
            --border-glow: #cbd5e1;
            --text-primary: #0f172a;
            --text-muted: #64748b;
            --text-on-accent: #ffffff;
            --primary: #4f46e5;
            --primary-dark: #3730a3;
            --primary-glow: transparent;
            --secondary: #7c3aed;
            --secondary-dark: #5b21b6;
            --secondary-glow: transparent;
            --bg-gradient: #f8fafc;
            --input-bg: #ffffff;
            --input-border: #cbd5e1;
            --input-focus-border: #4f46e5;
            --tab-bg: #f1f5f9;
            --tab-border: #e2e8f0;
            --tab-selected: #ffffff;
            --metric-bg: #ffffff;
            --metric-border: #e2e8f0;
            --card-border-glow: #e2e8f0;
            --shadow: none;
            --success-bg: rgba(16, 185, 129, 0.1);
            --success-text: #059669;
            --card-bg-glass: #ffffff;
            --bg-navbar: #ffffff;
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
            
            /* Hide only specific Streamlit Header actions and footer, keeping header itself visible for the sidebar toggle */
            #MainMenu, footer, [data-testid="stHeaderActionButton"], [data-testid="stDecoration"] {{
                visibility: hidden !important;
            }}
            
            header {{
                background-color: transparent !important;
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
                color: var(--text-primary) !important;
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

            /* Primary Button style - scoped only to developer-defined buttons */
            div[data-testid="stButton"] button, 
            div[data-testid="stFormSubmitButton"] button {{
                border-radius: 12px !important;
                background: var(--primary) !important;
                color: white !important;
                padding: 12px 24px !important;
                border: 1px solid var(--border) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                box-shadow: none !important;
                transition: background-color 0.2s ease, border-color 0.2s ease !important;
            }}

            div[data-testid="stButton"] button:hover, 
            div[data-testid="stFormSubmitButton"] button:hover {{
                background: var(--primary-dark) !important;
                border-color: var(--primary) !important;
            }}

            div[data-testid="stButton"] button:active, 
            div[data-testid="stFormSubmitButton"] button:active {{
                background: var(--primary-dark) !important;
            }}

            /* Style Streamlit's sidebar toggle buttons (expand & collapse) to render flat 2D icons and completely hide raw icon texts */
            div[data-testid="collapsedControl"] {{
                visibility: visible !important;
                z-index: 999999 !important;
            }}

            header button,
            button[data-testid="stSidebarCollapseButton"],
            section[data-testid="stSidebar"] button,
            button.e12tamyi15 {{
                visibility: visible !important;
                z-index: 999999 !important;
                width: 40px !important;
                height: 40px !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                cursor: pointer !important;
                border-radius: 50% !important;
                transition: background-color 0.2s ease !important;
                padding: 0 !important;
                margin: 8px !important;
                font-size: 0px !important;
                color: transparent !important;
                line-height: 0 !important;
                position: relative !important;
            }}

            header button:hover,
            button[data-testid="stSidebarCollapseButton"]:hover,
            section[data-testid="stSidebar"] button:hover,
            button.e12tamyi15:hover {{
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: none !important;
                transform: none !important;
            }}

            /* Hide all child elements containing raw icon texts inside any sidebar toggle button */
            header button *,
            button[data-testid="stSidebarCollapseButton"] *,
            section[data-testid="stSidebar"] button *,
            button.e12tamyi15 * {{
                font-size: 0px !important;
                color: transparent !important;
                line-height: 0 !important;
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                width: 0 !important;
                height: 0 !important;
            }}

            /* Custom 2D flat icons on the buttons directly */
            header button::before,
            div[data-testid="collapsedControl"] button::before {{
                content: "☰" !important;
                font-size: 1.5rem !important;
                color: var(--text-primary) !important;
                font-family: 'Outfit', sans-serif !important;
                visibility: visible !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                height: 100% !important;
            }}

            button[data-testid="stSidebarCollapseButton"]::before,
            section[data-testid="stSidebar"] button::before {{
                content: "✕" !important;
                font-size: 1.3rem !important;
                color: var(--text-primary) !important;
                font-family: 'Outfit', sans-serif !important;
                visibility: visible !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                height: 100% !important;
            }}

            header button svg,
            button[data-testid="stSidebarCollapseButton"] svg,
            section[data-testid="stSidebar"] button svg,
            button.e12tamyi15 svg {{
                display: none !important;
            }}

            /* Secondary Button */
            button[kind="secondary"] {{
                border-radius: 12px !important;
                background: var(--secondary) !important;
                color: white !important;
                padding: 12px 24px !important;
                border: 1px solid var(--border) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                box-shadow: none !important;
                transition: background-color 0.2s ease, border-color 0.2s ease !important;
            }}

            button[kind="secondary"]:hover {{
                background: var(--secondary-dark) !important;
                border-color: var(--secondary) !important;
            }}

            /* Tertiary Button */
            button[kind="tertiary"] {{
                border-radius: 12px !important;
                background: var(--input-bg) !important;
                color: var(--text-primary) !important;
                padding: 10px 20px !important;
                border: 1px solid var(--border) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
                box-shadow: none !important;
                transition: background-color 0.2s ease, border-color 0.2s ease !important;
            }}

            button[kind="tertiary"]:hover {{
                background: var(--tab-selected) !important;
                border-color: var(--primary) !important;
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
                box-shadow: none !important;
                transition: border-color 0.2s ease !important;
            }}
            div[data-testid="stTextInput"] input:focus, 
            div[data-testid="stNumberInput"] input:focus,
            div[data-testid="stSelectbox"] div[role="combobox"]:focus {{
                border-color: var(--input-focus-border) !important;
                box-shadow: none !important;
                background: var(--input-bg) !important;
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
                padding: 6px !important;
                border-radius: 12px !important;
                border: 1px solid var(--tab-border) !important;
                margin-bottom: 20px !important;
            }}
            div[data-testid="stTabBar"] button {{
                border-radius: 8px !important;
                background: transparent !important;
                color: var(--text-muted) !important;
                box-shadow: none !important;
                padding: 8px 16px !important;
                font-weight: 600 !important;
                transition: all 0.2s ease !important;
                border: none !important;
            }}
            div[data-testid="stTabBar"] button[aria-selected="true"] {{
                background: var(--tab-selected) !important;
                color: var(--primary) !important;
                box-shadow: none !important;
            }}
            div[data-testid="stTabBar"] button:hover {{
                color: var(--primary) !important;
                transform: none !important;
            }}

            /* Metrics styling */
            div[data-testid="stMetric"] {{
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
                padding: 20px !important;
                box-shadow: none !important;
                text-align: center !important;
                transition: border-color 0.2s ease !important;
            }}
            div[data-testid="stMetric"]:hover {{
                border-color: var(--primary) !important;
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

            /* Flat border wrapper for login/register */
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                background: var(--bg-card) !important;
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                padding: 2.5rem !important;
                box-shadow: none !important;
                margin-top: 10px !important;
            }}

            /* Biometric scan cards */
            .biometric-card {{
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                padding: 24px !important;
                text-align: center !important;
                margin-bottom: 12px !important;
                box-shadow: none !important;
                transition: border-color 0.2s ease, background-color 0.2s ease !important;
            }}
            .biometric-card:hover {{
                background: var(--bg-card) !important;
                border-color: var(--primary) !important;
            }}
            .biometric-card h4 {{
                color: var(--text-primary) !important;
                font-weight: 700 !important;
            }}
            
            /* Sidebar glassmorphism override */
            section[data-testid="stSidebar"] {{
                background-color: var(--bg-sidebar) !important;
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