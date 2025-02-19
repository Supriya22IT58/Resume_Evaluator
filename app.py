import streamlit as st
import joblib
import fitz  # PyMuPDF
import docx
import io
import time
import random
import re

# Load Trained Model
model = joblib.load("resume_evaluator_model.pkl")

# Function to Extract Text from Various File Types
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def extract_text_from_docx(file):
    doc = docx.Document(io.BytesIO(file.read()))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    else:
        return None

# Function to Extract Name, Email, and Experience from Resume Text
def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        words = line.strip().split()
        if 1 < len(words) <= 4:  # Assuming name consists of 2 to 4 words
            return line.strip()
    return "Not Found"

def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text)
    return match.group(0) if match else "Not Found"

def extract_experience(text):
    exp_pattern = r"(\d+)\s*(?:years?|yrs?|year|yr)"
    matches = re.findall(exp_pattern, text, re.IGNORECASE)
    if matches:
        return f"{max(map(int, matches))} years"
    return "Fresher"

# Streamlit UI Setup
st.set_page_config(page_title="Resume Evaluator", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #e6f3ff, #f0e6ff, #ffe6f0, #e6fff0);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    .floating-title {
        animation: float 3s ease-in-out infinite;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='floating-title' style='text-align: center; color: #6c63ff;'>✨ Resume Evaluator ✨</h1>", unsafe_allow_html=True)

fun_messages = [
    "Let's make your resume sparkle! ✨",
    "Time to shine bright! 🌟",
    "Ready to impress? 🚀",
    "Let's make magic happen! 🎭",
    "Your success story starts here! 📈",
    "Transforming resumes into opportunities! 🎯"
]
st.markdown(f"<h3 style='text-align: center; color: black;'>{random.choice(fun_messages)}</h3>", unsafe_allow_html=True)

# Resume Upload
resume = st.file_uploader("📜 Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# Submit Button
if st.button("🌟 Reveal Your Resume's Potential"):
    if not resume:
        st.error("❌ Please upload your resume before proceeding!")
    else:
        with st.spinner(random.choice(["Summoning career opportunities... 🌟", "Analyzing your professionalism... 🔮", "Unleashing your potential... 🚀"])):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)

        resume_text = extract_text_from_file(resume)
        
        if resume_text:
            name = extract_name(resume_text)
            email = extract_email(resume_text)
            experience = extract_experience(resume_text)
            
            st.subheader("Extracted Information")
            st.write(f"**👤 Name:** {name}")
            st.write(f"**📧 Email:** {email}")
            st.write(f"**📅 Experience:** {experience}")
            
            # Predict Category
            prediction = model.predict([resume_text])[0]
            
            # Skill Recommendations
            skill_suggestions = {
                "Data Science": ["Deep Learning", "SQL", "Big Data"],
                "Web Development": ["React.js", "Node.js", "Database Management"],
                "Software Engineering": ["System Design", "Data Structures", "Algorithms"],
                "AI/ML": ["TensorFlow", "NLP", "Reinforcement Learning"],
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
            
            # Display Results
            st.success(f"✅ **Predicted Category:** {prediction}")
            if suggestions:
                st.info(f"🔹 **Suggested Skills to Improve:** {', '.join(suggestions)}")
        else:
            st.error("❌ Could not extract text from the uploaded file.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: black;'>
        <p style='font-size: 12px;'>✨ Making dreams come true, one resume at a time ✨</p>
    </div>
""", unsafe_allow_html=True)
