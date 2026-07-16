import os
from flask import request

def get_streamlit_url():
    # Priority 1: Explicit environment variables
    env_url = os.environ.get('STREAMLIT_URL') or os.environ.get('VITE_STREAMLIT_URL')
    if env_url:
        return env_url
    
    # Priority 2: Host header inspection to detect Local Development vs Production Vercel
    host = request.headers.get('Host', '')
    if 'localhost' in host or '127.0.0.1' in host:
        return 'http://localhost:8501'
    
    # Priority 3: Fallback Production default
    return 'https://snapclass-attendence.streamlit.app'
