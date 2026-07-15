import streamlit as st
import base64
import os
from PIL import Image
import io


def get_logo_url():
    # Served by Streamlit from static/images/priyanshu_singh.png when enableStaticServing is true
    return "/app/static/images/priyanshu_singh.png"


def footer_home():
    logo_url = get_logo_url()
    
    st.markdown(f"""
        <div style="margin-top: 2rem; display: flex; gap: 6px; justify-content: center; align-items: center;">
        <p style="font-weight: bold; color: var(--text-primary); margin: 0; font-family: 'Outfit';">Created with ❤️ by</p>  
        <img src="{logo_url}" style="max-height: 30px; border-radius: 4px;" />
        </div>
        """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = get_logo_url()
    
    st.markdown(f"""
        <div style="margin-top: 2rem; display: flex; gap: 6px; justify-content: center; align-items: center;">
        <p style="font-weight: bold; color: var(--text-primary); margin: 0; font-family: 'Outfit';">Created with ❤️ by</p>  
        <img src="{logo_url}" style="max-height: 30px; border-radius: 4px;" />
        </div>
        """, unsafe_allow_html=True)
