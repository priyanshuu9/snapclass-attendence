# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from supabase import create_client, Client
# pyrefly: ignore [missing-import]
import httpx

def check_db_connection() -> tuple[bool, str]:
    """
    Checks if Supabase credentials are configured correctly and the database is reachable.
    Returns (success, error_message).
    """
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    
    if not url or url == "https://your-project-id.supabase.co":
        return False, "Supabase URL is not configured. Please edit `.streamlit/secrets.toml` and configure your own Supabase URL."
    if not key or key == "your-supabase-anon-key":
        return False, "Supabase API Key is not configured. Please edit `.streamlit/secrets.toml` and configure your own Supabase Key."
        
    try:
        # Create client and attempt a fast check (GET request to supabase rest endpoint)
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}"
        }
        # Just check if we can resolve the host and get a response
        response = httpx.get(f"{url}/rest/v1/", headers=headers, timeout=5.0)
        # Any status code from the server (even 401/404/200) means the host is reachable and DNS resolved
        return True, ""
    except httpx.ConnectError:
        return False, f"Could not connect to Supabase at '{url}'. Please check your internet connection or verify the URL is correct."
    except Exception as e:
        return False, f"Failed to initialize or connect to Supabase: {str(e)}"

# Read secrets
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")
service_key = st.secrets.get("SUPABASE_SERVICE_KEY")

# Initialize clients if not placeholder (will be verified fully in app.py)
if url and key and url != "https://your-project-id.supabase.co" and key != "your-supabase-anon-key":
    try:
        supabase: Client = create_client(url, key)
    except Exception:
        supabase = None
else:
    supabase = None

if url and service_key:
    try:
        supabase_admin: Client = create_client(url, service_key)
    except Exception:
        supabase_admin = None
else:
    supabase_admin = None