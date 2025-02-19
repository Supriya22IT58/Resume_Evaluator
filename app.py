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

# Function to Extract Name, Email, Experience, and Skills from Resume Text
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

def extract_skills(text):
    skills_keywords = ["Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning", "Cloud Computing", "React", "Node.js", "Data Science", "Cybersecurity"]
    found_skills = [skill for skill in skills_keywords if skill.lower() in text.lower()]
    return found_skills if found_skills else ["Not Found"]

# Suggested Learning Courses
learning_resources = {
    "Python": "https://www.coursera.org/specializations/python",
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "Data Science": "https://www.udacity.com/course/data-scientist-nanodegree--nd025",
    "React": "https://react.dev/",
    "Cloud Computing": "https://aws.amazon.com/training/"
}

# Streamlit UI Setup
st.set_page_config(page_title="Resume Evaluator", page_icon="📄", layout="centered")

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
            skills = extract_skills(resume_text)
            
            st.subheader("Extracted Information")
            st.write(f"**👤 Name:** {name}")
            st.write(f"**📧 Email:** {email}")
            st.write(f"**📅 Experience:** {experience}")
            st.write(f"**💡 Extracted Skills:** {', '.join(skills)}")
            
            # Suggested Courses
            st.subheader("📚 Suggested Learning Resources")
            for skill in skills:
                if skill in learning_resources:
                    st.markdown(f"- [{skill} Course]({learning_resources[skill]})")
            
            # Predict Category
            prediction = model.predict([resume_text])[0]
            
            # Display Results
            st.success(f"✅ **Predicted Category:** {prediction}")
        else:
            st.error("❌ Could not extract text from the uploaded file.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: black;'><p style='font-size: 12px;'>✨ Making dreams come true, one resume at a time ✨</p></div>", unsafe_allow_html=True)
