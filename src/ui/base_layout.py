import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #5865F2 !important;
                }

                .stApp div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding:2.5rem !important;
                    border-radius: 3rem !important;
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    


def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: radial-gradient(at 0% 0%, rgba(224, 227, 255, 1) 0px, transparent 50%),
                                radial-gradient(at 100% 0%, rgba(235, 69, 158, 0.15) 0px, transparent 50%),
                                radial-gradient(at 50% 100%, rgba(88, 101, 242, 0.1) 0px, transparent 50%),
                                #f8fafc !important;
                    background-attachment: fixed !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

                
         /* Hide Top Bar of streamlit */
                
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top:2.5rem !important;    
                max-width: 1000px !important;
            }

            h1 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 3.5rem !important;
                font-weight: 800 !important;
                line-height: 1.15 !important;
                margin-bottom: 0rem !important;
                background: linear-gradient(135deg, #1e293b 0%, #4752c4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
                

            h2 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 2.25rem !important;
                font-weight: 800 !important;
                line-height: 1.2 !important;
                margin-bottom: 0rem !important;
                color: #1e293b;
            }
                
            h3, h4, p, span, li {
                font-family: 'Outfit', sans-serif !important;    
            }
                

            /* Primary Button style */
            button {
                border-radius: 14px !important;
                background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%) !important;
                color: white !important;
                padding: 12px 24px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 15px rgba(88, 101, 242, 0.25) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(88, 101, 242, 0.4) !important;
                background: linear-gradient(135deg, #4752C4 0%, #3b45a9 100%) !important;
            }

            button:active {
                transform: translateY(0px) !important;
            }

            /* Secondary Button */
            button[kind="secondary"] {
                border-radius: 14px !important;
                background: linear-gradient(135deg, #EB459E 0%, #d82c85 100%) !important;
                color: white !important;
                padding: 12px 24px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 15px rgba(235, 69, 158, 0.25) !important;
            }

            button[kind="secondary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(235, 69, 158, 0.4) !important;
                background: linear-gradient(135deg, #d82c85 0%, #be1b70 100%) !important;
            }

            /* Tertiary Button */
            button[kind="tertiary"] {
                border-radius: 14px !important;
                background: rgba(15, 23, 42, 0.05) !important;
                color: #1e293b !important;
                padding: 10px 20px !important;
                border: 1px solid rgba(15, 23, 42, 0.1) !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
                box-shadow: none !important;
            }

            button[kind="tertiary"]:hover {
                transform: translateY(-2px) !important;
                background: rgba(15, 23, 42, 0.08) !important;
                color: black !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
            }

            /* Custom input styling */
            div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stTextArea"] textarea {
                background: rgba(255, 255, 255, 0.7) !important;
                border-radius: 12px !important;
                border: 1px solid rgba(88, 101, 242, 0.2) !important;
                font-family: 'Outfit', sans-serif !important;
                color: #1e293b !important;
                padding: 12px 16px !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.01) !important;
                transition: all 0.3s ease !important;
            }
            div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
                border-color: #5865F2 !important;
                box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.01) !important;
                background: white !important;
            }

            /* Tabs styling */
            div[data-testid="stTabBar"] {
                gap: 8px !important;
                background: rgba(255, 255, 255, 0.6) !important;
                backdrop-filter: blur(8px) !important;
                padding: 6px !important;
                border-radius: 16px !important;
                border: 1px solid rgba(255, 255, 255, 0.5) !important;
                margin-bottom: 20px !important;
            }
            div[data-testid="stTabBar"] button {
                border-radius: 12px !important;
                background: transparent !important;
                color: #4b5563 !important;
                box-shadow: none !important;
                padding: 8px 16px !important;
                font-weight: 600 !important;
                transition: all 0.25s ease !important;
                border: none !important;
            }
            div[data-testid="stTabBar"] button[aria-selected="true"] {
                background: white !important;
                color: #5865F2 !important;
                box-shadow: 0 4px 12px rgba(88, 101, 242, 0.15) !important;
            }
            div[data-testid="stTabBar"] button:hover {
                color: #5865F2 !important;
                transform: none !important;
            }

            /* Metrics styling */
            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.7) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.5) !important;
                border-radius: 20px !important;
                padding: 20px !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.02) !important;
                text-align: center !important;
                transition: transform 0.3s ease !important;
            }
            div[data-testid="stMetric"]:hover {
                transform: translateY(-3px) !important;
            }
            div[data-testid="stMetricLabel"] {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                color: #64748b !important;
                font-size: 0.95rem !important;
            }
            div[data-testid="stMetricValue"] {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                color: #5865F2 !important;
                font-size: 2.25rem !important;
            }

            /* Glassmorphic border wrapper for login/register */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(255, 255, 255, 0.6) !important;
                backdrop-filter: blur(15px) !important;
                border: 1px solid rgba(255, 255, 255, 0.5) !important;
                border-radius: 28px !important;
                padding: 2.5rem !important;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.03) !important;
                margin-top: 10px !important;
            }

            /* Biometric scan cards */
            .biometric-card {
                background: rgba(255, 255, 255, 0.65) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.4) !important;
                border-radius: 24px !important;
                padding: 24px !important;
                text-align: center !important;
                margin-bottom: 12px !important;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.02) !important;
                transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            }
            .biometric-card:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 15px 30px rgba(88, 101, 242, 0.08) !important;
                background: rgba(255, 255, 255, 0.75) !important;
            }
            .biometric-card h4 {
                color: #1e293b !important;
                font-weight: 700 !important;
            }
        </style>  

                """
            ,unsafe_allow_html=True)