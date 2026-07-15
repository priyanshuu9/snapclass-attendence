import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
            <img src='{logo_url}' style='height:100px;' />
            <h1 style='text-align:center; color: var(--text-primary); text-shadow: 0 4px 12px var(--primary-glow);'>SNAP<br/>CLASS</h1>
        </div>   
        """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px">
            <img src='{logo_url}' style='height:75px;' />
            <h2 style='text-align:left; color: var(--primary); font-family: "Outfit", sans-serif; font-weight: 800;'>SNAP<br/>CLASS</h2>
        </div>   
        """, unsafe_allow_html=True)
