import streamlit as st

# Global monkeypatch to fix AttributeError in screen files calling st.space()
def _space(num=1):
    for _ in range(num):
        st.write("")
st.space = _space

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )
    
    # Sync theme from localStorage to URL query parameters silently without refreshing
    import streamlit.components.v1 as components
    components.html("""
        <script>
            try {
                const urlParams = new URLSearchParams(window.parent.location.search);
                const urlTheme = urlParams.get('theme');
                const localTheme = localStorage.getItem('theme');
                
                if (!urlTheme) {
                    const activeTheme = localTheme || 'dark';
                    urlParams.set('theme', activeTheme);
                    window.parent.history.replaceState({}, '', window.parent.location.pathname + '?' + urlParams.toString());
                    localStorage.setItem('theme', activeTheme);
                } else {
                    localStorage.setItem('theme', urlTheme);
                }
            } catch (e) {
                console.error("Theme sync error:", e);
            }
        </script>
    """, height=0, width=0)

    # Read and store current theme state
    theme_param = st.query_params.get('theme', 'dark')
    if theme_param not in ['dark', 'light']:
        theme_param = 'dark'
    st.session_state['theme'] = theme_param
    
    # Verify Supabase configuration and connectivity
    from src.database.config import check_db_connection
    db_success, db_error = check_db_connection()
    if not db_success:
        st.error("🔌 **Database Connection Error**")
        st.warning(db_error)
        st.info("👉 To run this application, make sure to configure a valid Supabase project URL and API key in `.streamlit/secrets.toml`.")
        st.stop()

    # Try to restore session from query parameters on startup
    from src.utils.session import restore_session
    restored = restore_session()
    if restored:
        role, uid = restored
        if role == 'student' and 'student_data' not in st.session_state:
            from src.database.db import get_student_by_id
            try:
                student = get_student_by_id(uid)
                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'student'
                    st.session_state.student_data = student
                    st.session_state.login_type = 'student'
            except Exception:
                pass
        elif role == 'teacher' and 'teacher_data' not in st.session_state:
            from src.database.db import get_teacher_by_id
            try:
                teacher = get_teacher_by_id(uid)
                if teacher:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'teacher'
                    st.session_state.teacher_data = teacher
                    st.session_state.login_type = 'teacher'
            except Exception:
                pass

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()


    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
main()