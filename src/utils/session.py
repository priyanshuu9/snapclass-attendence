import hashlib
import streamlit as st

def get_session_signature(role: str, uid: str) -> str:
    """
    Generates a secure signature based on user role, ID, and the Supabase API Key.
    This prevents users from manually changing query parameters to access other accounts.
    """
    secret = st.secrets.get("SUPABASE_KEY", "default-fallback-secret-key-12345")
    payload = f"{role}:{uid}:{secret}"
    return hashlib.sha256(payload.encode()).hexdigest()

def save_session(role: str, uid: int | str):
    """
    Saves the user session details securely in the URL query parameters.
    """
    uid_str = str(uid)
    sig = get_session_signature(role, uid_str)
    st.query_params["role"] = role
    st.query_params["uid"] = uid_str
    st.query_params["sig"] = sig

def clear_session():
    """
    Clears the session parameters from the URL.
    """
    # Streamlit query_params supports dict operations
    for key in ["role", "uid", "sig"]:
        if key in st.query_params:
            del st.query_params[key]

def restore_session() -> tuple[str, int] | None:
    """
    Validates and restores the user session from URL query parameters.
    Returns (role, uid) if valid, otherwise None.
    """
    role = st.query_params.get("role")
    uid = st.query_params.get("uid")
    sig = st.query_params.get("sig")
    
    if not role or not uid or not sig:
        return None
        
    expected_sig = get_session_signature(role, uid)
    if sig == expected_sig:
        try:
            return role, int(uid)
        except ValueError:
            return None
            
    # Signature mismatch: clear invalid parameters
    clear_session()
    return None
