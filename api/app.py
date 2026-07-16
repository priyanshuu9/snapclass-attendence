import os
from flask import Flask, render_template

try:
    from api.config import get_streamlit_url
except ImportError:
    from config import get_streamlit_url

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(current_dir, "../templates"),
    static_folder=os.path.join(current_dir, "../static")
)

@app.route('/')
def home():
    # Dynamically detect and render the correct Streamlit URL
    streamlit_url = get_streamlit_url()
    return render_template('index.html', streamlit_url=streamlit_url)

@app.route('/connect')
def connect():
    # Render the waking loader screen
    streamlit_url = get_streamlit_url()
    return render_template('connect.html', streamlit_url=streamlit_url)

@app.route('/api/health')
def health_check():
    # Server-to-server check to verify if the Streamlit app is awake and responsive
    streamlit_url = get_streamlit_url()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        import requests
        # Check standard Streamlit health check endpoint
        res = requests.get(f"{streamlit_url.rstrip('/')}/_stcore/health", headers=headers, timeout=4)
        if res.status_code == 200:
            return {"status": "online"}
    except Exception:
        pass
        
    try:
        import requests
        # Fallback check on the root page
        res = requests.get(streamlit_url, headers=headers, timeout=4)
        content = res.text.lower()
        
        # If redirected to share.streamlit.io auth or contains sleep text, it is sleeping
        if "share.streamlit.io" in res.url or "get this app back up" in content or "zzzz" in content or "sleeping" in content:
            return {"status": "sleeping"}
            
        if res.status_code == 200:
            if "sleeping" not in content and "waking up" not in content:
                return {"status": "online"}
    except Exception:
        pass
        
    return {"status": "offline"}

if __name__ == '__main__':
    app.run(debug=True, port=5002)
