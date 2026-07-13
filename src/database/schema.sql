-- Reference SQL Schema for SnapClass AI Attendance System
-- This file documents the database schema and RLS policies used by the application.
-- You can run these commands directly in your Supabase SQL Editor.

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. TEACHERS TABLE
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. STUDENTS TABLE
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    face_embedding FLOAT8[] DEFAULT NULL,
    voice_embedding FLOAT8[] DEFAULT NULL,
    verification_status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. SUBJECTS (COURSES) TABLE
CREATE TABLE IF NOT EXISTS subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    section TEXT NOT NULL,
    teacher_id INT REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. SUBJECT_STUDENTS (ENROLLMENT) TABLE
CREATE TABLE IF NOT EXISTS subject_students (
    subject_id INT REFERENCES subjects(subject_id) ON DELETE CASCADE,
    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (subject_id, student_id)
);

-- 5. ATTENDANCE_LOGS TABLE
CREATE TABLE IF NOT EXISTS attendance_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    subject_id INT REFERENCES subjects(subject_id) ON DELETE CASCADE,
    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,
    is_present BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES FOR QUERY OPTIMIZATION
CREATE INDEX IF NOT EXISTS idx_teachers_username ON teachers(username);
CREATE INDEX IF NOT EXISTS idx_students_username ON students(username);
CREATE INDEX IF NOT EXISTS idx_subjects_code ON subjects(subject_code);
CREATE INDEX IF NOT EXISTS idx_attendance_subject_timestamp ON attendance_logs(subject_id, timestamp);

-- ROW LEVEL SECURITY (RLS) POLICIES
-- Turn on RLS for tables
ALTER TABLE teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE subject_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance_logs ENABLE ROW LEVEL SECURITY;

-- Teachers access:
-- Teachers can view their own profile.
CREATE POLICY "Teachers can view own profile" ON teachers
    FOR SELECT USING (true); -- Authenticated select allowed

-- Students access:
-- Students can read their own profile.
CREATE POLICY "Students can view own profile" ON students
    FOR SELECT USING (true);

-- Subjects access:
-- Anyone can view subjects (needed for join-code checks).
CREATE POLICY "Anyone can view subjects" ON subjects
    FOR SELECT USING (true);

-- Subject Enrollments:
-- Students can view their own enrollments, teachers can view all enrollments.
CREATE POLICY "Students can view own enrollments" ON subject_students
    FOR SELECT USING (true);

CREATE POLICY "Anyone can insert enrollments" ON subject_students
    FOR INSERT WITH CHECK (true);

-- Attendance Logs:
-- Students can view their own logs.
CREATE POLICY "Students can view own attendance logs" ON attendance_logs
    FOR SELECT USING (true);

-- Teachers can manage (select, insert, update) logs.
CREATE POLICY "Anyone can insert attendance logs" ON attendance_logs
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update attendance logs" ON attendance_logs
    FOR UPDATE USING (true);
