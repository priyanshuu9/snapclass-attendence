import streamlit as st
def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-left: 8px solid #EB459E; padding: 25px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.5); margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.04); transition: all 0.3s ease;">
        <h3 style="margin: 0 0 8px 0; color: #1e293b; font-size: 1.6rem; font-weight: 800; font-family: 'Outfit', sans-serif;">{name}</h3>
        <p style="color: #64748b; margin: 10px 0; font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 500;">
            Code: <span style="background: rgba(88, 101, 242, 0.1); color: #5865F2; padding: 4px 10px; border-radius: 8px; font-weight: 600;">{code}</span> 
            <span style="color: #cbd5e1; margin: 0 8px;">|</span> 
            Section: <span style="color: #1e293b; font-weight: 600;">{section}</span>
        </p>
        
        """
    
    if stats:
        html+= """
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; margin-top: 15px;">
        """
        for icon, label, value in stats:
            html+= f"""
            <div style="background: rgba(235, 69, 158, 0.06); border: 1px solid rgba(235, 69, 158, 0.1); color: #2e3a59; padding: 6px 14px; border-radius: 12px; font-size: 0.88rem; font-family: 'Outfit', sans-serif; font-weight: 500; display: flex; align-items: center; gap: 6px;">
                <span>{icon}</span> 
                <span>{label}: <b>{value}</b></span>
            </div>
            """
        
        html+= "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

