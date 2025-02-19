import streamlit as st
import joblib
import fitz  # PyMuPDF
import docx
import io
import os
import time
import random

# Check if the model file exists
MODEL_PATH = "resume_evaluator_model.pkl"
if not os.path.exists(MODEL_PATH):
    st.error("🚨 Model file not found! Please ensure `resume_evaluator_model.pkl` is available.")
    st.stop()

# Load Trained Model
model = joblib.load(MODEL_PATH)

# Function to Extract Text from Various File Types
def extract_text_from_pdf(file):
    try:
        text = ""
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
        return text
    except Exception as e:
        return None

def extract_text_from_docx(file):
    try:
        doc = docx.Document(io.BytesIO(file.read()))
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return None

def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        return None

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    else:
        return None

# Streamlit UI
st.set_page_config(page_title="Resume Evaluator", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f7f8fc; }
    .stButton > button {
        background: linear-gradient(45deg, #6c63ff, #836fff);
        color: white !important;
        border-radius: 25px;
        padding: 12px 28px;
        font-size: 16px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #6c63ff;'>✨ Resume Evaluator ✨</h1>", unsafe_allow_html=True)

# User Input Fields
name = st.text_input("👤 Your Name", placeholder="e.g., John Doe")
email = st.text_input("📧 Your Email", placeholder="e.g., john.doe@example.com")
role = st.selectbox("🎯 Role Applying For", ["Select Role", "Data Science", "Web Development", "Software Engineering", "AI/ML", "Cloud Computing", "Cybersecurity"])
experience = st.selectbox("📅 Years of Experience", ["Select Experience", "Fresher"] + [f"{i} years" for i in range(1, 26)])
resume = st.file_uploader("📜 Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# Submit Button
if st.button("🌟 Evaluate My Resume"):
    if not name or not email or role == "Select Role" or experience == "Select Experience" or not resume:
        st.error("❌ Please complete all fields before proceeding!")
    else:
        with st.spinner("Analyzing your resume... 🔍"):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)

        resume_text = extract_text_from_file(resume)

        if resume_text:
            prediction = model.predict([resume_text])[0]
            
            # Skill Recommendations
            skill_suggestions = {
                "Data Science": ["SQL", "Big Data", "Machine Learning"],
                "Web Development": ["React.js", "Node.js", "Database Management"],
                "Software Engineering": ["System Design", "Data Structures", "Algorithms"],
                "AI/ML": ["Deep Learning", "NLP", "TensorFlow"],
                "Cloud Computing": ["AWS", "Azure", "Kubernetes"],
                "Cybersecurity": ["Network Security", "Ethical Hacking", "Cryptography"]
            }

            suggestions = skill_suggestions.get(prediction, [])
            if experience == "Fresher":
                suggestions.append("Internship Experience")
            elif "years" in experience:
                years = int(experience.split()[0])
                if years > 5:
                    suggestions.append("Advanced Certifications")
                if years > 10:
                    suggestions.append("Leadership & Mentoring")

            st.success(f"✅ **Predicted Category:** {prediction}")
            if suggestions:
                st.info(f"🔹 **Suggested Skills to Improve:** {', '.join(suggestions)}")
        else:
            st.error("❌ Could not extract text from the uploaded file.")
