# SnapClass - AI-Powered Attendance Management System

SnapClass is a modern, integrated SaaS-style classroom attendance system that leverages biometric artificial intelligence (Face Recognition and Voice Verification) to automate roll calls. By scanning a class photo or recording class audio responses, SnapClass identifies present students in seconds, eliminating manual tracking, administrative overhead, and student proxy attendance.

---

## 🌟 Core Features

### 👤 AI Biometric Attendance
- **Face Scanner**: Processes class photos using deep 128-dimensional facial descriptors to detect and recognize multiple students simultaneously (powered by `dlib` and `face_recognition_models`).
- **Voice ID Verification**: Discriminative vocal voiceprints (powered by `Resemblyzer`) split bulk classroom recordings, cross-referencing speakers with stored vocal embeddings. Perfect biometric backup.

### 📚 Course Enrollment & QR codes
- **Join Codes & QR**: Teachers generate dynamic enrollment links and QR codes for subjects.
- **Auto-Enrollment**: Students open links with join codes, log in/sign up, and are enrolled instantly in the corresponding course (URL session remains persistent on reload).

### 🏫 Teacher Dashboard
- **Subject Control**: Create, update, or safely delete subjects and review enrolled registries.
- **Taking Attendance**: Run Face scanning or Voice ID verification directly from the dashboard and review a detailed results sheet.
- **Log Management**: Manually correct student present/absent logs, delete sessions, or export structured attendance sheets to CSV.
- **Course Analytics**: Interactive charts showing attendance rates per student, low-presence alerts (< 75%), and session charts.

### 👤 Student Dashboard
- **Activity Metrics**: Visual overall and subject-wise metrics and low-attendance warnings.
- **Biometric Registrations**: Manage, view, and update face and voice templates directly using webcam/microphone.
- **History Logs**: Real-time updates of marked class presence.

---

## 📁 Repository Directory Structure

```text
├── .streamlit/
│   └── secrets.toml           # Streamlit secrets (DB URLs & Keys)
├── src/
│   ├── components/            # UI components and popups (dialogs)
│   ├── database/              # DB connection config & queries (db.py, schema.sql)
│   ├── pipelines/             # ML face & voice processing pipelines
│   ├── screens/               # Main pages (home, teacher, student screens)
│   ├── ui/                    # Base styles and glassmorphism themes
│   └── utils/                 # Utilities (secure session signatures)
├── app.py                     # Main Streamlit application entry point
├── packages.txt               # Streamlit Cloud native packages checklist
├── requirements.txt           # Python package dependencies
├── .env.example               # Template for environment configurations
└── README.md                  # Project documentation
```

---

## 🛠️ Local Installation & Setup

### 1. Prerequisites
- **Python**: version `3.10` is highly recommended.
- **C++ Compiler**: To compile the native `dlib` package:
  - **Windows**: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the "Desktop development with C++" workload.
  - **macOS/Linux**: Ensure `cmake` and `g++` are installed in your shell.

### 2. Configure Virtual Environment
```bash
# Clone the repository and navigate inside
git clone https://github.com/your-username/snapclass.git
cd snapclass

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Setup Database Schema
SnapClass uses **Supabase** (PostgreSQL) as its backend database. 
1. Create a free project on [Supabase](https://supabase.com/).
2. Navigate to the **SQL Editor** on your Supabase dashboard.
3. Copy the contents of the reference schema file: `src/database/schema.sql` and run them to set up all tables, indexes, and Row Level Security (RLS) policies.

### 4. Configure Secrets
Create a file named `.streamlit/secrets.toml` in the project root:
```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
SUPABASE_SERVICE_KEY = "your-supabase-service-role-key"
```
*(Get these values from your Supabase Project Settings -> API page).*

### 5. Run Locally
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🚀 Cloud Deployment (Streamlit Cloud)

1. Push your codebase to a GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and click **New app**.
3. Select your repository, branch, and set the Main file path to `app.py`.
4. Open **Advanced Settings** -> **Secrets** and paste the variables from your `secrets.toml`.
5. SnapClass includes `packages.txt` in the root which instructs the build server to install native binaries (`cmake`, `build-essential`, `libgl1`, etc.) required to compile `dlib` and initialize `OpenCV/Pillow`.
6. Click **Deploy**. The server will install libraries, compile dependencies, and launch your live URL.

---

## 🔒 Security Architecture
- **Password Protection**: Passwords are securely hashed using `bcrypt` before storage.
- **API Protection**: No privileged database keys are exposed. Normal student/teacher database actions respect PostgreSQL query patterns, and logins/signups use the service-role client on the server-side to guarantee credentials validation.
- **Row Level Security (RLS)**: Policies restrict access so students can only view their own attendance details, and teachers can manage courses and logs.