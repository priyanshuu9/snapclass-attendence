import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background: var(--bg-card); border-left: 4px solid var(--secondary); padding: 20px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 20px; transition: border-color 0.2s ease;">
        <h3 style="margin: 0 0 8px 0; color: var(--text-primary); font-size: 1.5rem; font-weight: 800; font-family: 'Outfit', sans-serif;">{name}</h3>
        <p style="color: var(--text-muted); margin: 10px 0; font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 500;">
            Code: <span style="background: var(--bg-secondary); border: 1px solid var(--border); color: var(--primary); padding: 4px 10px; border-radius: 8px; font-weight: 600;">{code}</span> 
            <span style="color: var(--border); margin: 0 8px;">|</span> 
            Section: <span style="color: var(--text-primary); font-weight: 600;">{section}</span>
        </p>
        
        """
    
    if stats:
        html+= """
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; margin-top: 15px;">
        """
        for icon, label, value in stats:
            html+= f"""
            <div style="background: var(--bg-secondary); border: 1px solid var(--border); color: var(--text-primary); padding: 6px 14px; border-radius: 8px; font-size: 0.88rem; font-family: 'Outfit', sans-serif; font-weight: 500; display: flex; align-items: center; gap: 6px;">
                <span>{icon}</span> 
                <span>{label}: <b>{value}</b></span>
            </div>
            """
        
        html+= "</div>"

    html += "</div>"

    import re
    clean_html = re.sub(r'\s+', ' ', html).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
