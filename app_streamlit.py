# app_streamlit.py

import streamlit as st
import fitz  # PyMuPDF
from matcher import get_match_score, is_match
from job_roles import job_descriptions

st.set_page_config(page_title="Resume Matcher", layout="centered")
st.title("📌 Resume Match Checker")

st.markdown("Upload your **PDF resume** and choose a job role to check your fit!")

# Step 1: Upload Resume (PDF Only)
uploaded_file = st.file_uploader("📄 Upload your resume (.pdf only)", type=["pdf"])

# Step 2: Select Job Role
selected_role = st.selectbox("🎯 Choose a job role", list(job_descriptions.keys()))

def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

if uploaded_file and selected_role:
    # Extract and clean text
    try:
        resume_text = extract_text_from_pdf(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read PDF: {e}")
        st.stop()

    job_desc = job_descriptions[selected_role]

    # Step 3: Match Score
    with st.spinner("Analyzing..."):
        score = get_match_score(resume_text, job_desc)
        match = is_match(score)

    # Step 4: Output
    st.success("✅ Analysis Complete!")
    st.metric(label="Match Score", value=f"{score:.2f}", delta="Pass" if match else "Fail")

    if match:
        st.markdown("🎉 **Strong match! Your resume aligns well with this job role.**")
    else:
        st.markdown("⚠️ **Some mismatch. Consider improving your resume for this role.**")
