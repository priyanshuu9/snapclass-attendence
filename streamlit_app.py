import streamlit as st
import sys
import os

st.title("SnapClass AI - Diagnostics Page")

st.write("### Python & Environment Info")
st.write(f"Python Version: `{sys.version}`")
st.write(f"Working Directory: `{os.getcwd()}`")

st.write("### Diagnostics Logs")

def test_import(module_name):
    try:
        __import__(module_name)
        st.success(f"✓ `{module_name}` imported successfully!")
        return True
    except Exception as e:
        import traceback
        st.error(f"✗ `{module_name}` failed to import!")
        st.code(traceback.format_exc())
        return False

# Test imports sequentially
test_import("numpy")
test_import("pandas")
test_import("dlib")
test_import("face_recognition_models")
test_import("supabase")
test_import("bcrypt")
test_import("segno")
test_import("PIL")
test_import("librosa")
test_import("resemblyzer")
test_import("flask")

st.write("Diagnostics complete.")