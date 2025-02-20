import streamlit as st
import joblib
import fitz  # PyMuPDF
import docx
import io
import time
import random
import textstat  # Readability Check
import spacy
from collections import Counter
from fpdf import FPDF

# Load Trained Model & NLP Model
model = joblib.load("resume_evaluator_model.pkl")
nlp = spacy.load("en_core_web_sm")

# Function to Extract Text from Various File Types
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
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

# Grammar & Readability Check
def grammar_readability_check(text):
    return textstat.flesch_reading_ease(text)

# Extract Keywords for ATS Optimization
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return dict(Counter(keywords).most_common(10))

# Generate PDF Report
def generate_pdf(name, email, role, category, suggestions, readability, keywords):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume Evaluation Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Role Applied For: {role}", ln=True)
    pdf.cell(200, 10, txt=f"Predicted Category: {category}", ln=True)
    pdf.cell(200, 10, txt=f"Readability Score: {readability}", ln=True)
    pdf.cell(200, 10, txt=f"Suggested Skills: {', '.join(suggestions)}", ln=True)
    pdf.cell(200, 10, txt=f"Top Keywords: {', '.join(keywords.keys())}", ln=True)
    pdf.ln(10)
    return pdf.output(dest='S').encode('latin1')

# Streamlit UI Custom Styling
st.set_page_config(page_title="Resume Evaluator", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #e6f3ff, #f0e6ff, #ffe6f0, #e6fff0); background-size: 400% 400%; }
    .floating-title { animation: float 3s ease-in-out infinite; display: inline-block; }
    .stButton > button { background: linear-gradient(45deg, #6c63ff, #836fff); color: white !important; border-radius: 25px; padding: 15px 30px; font-size: 18px; transition: all 0.3s ease; }
    .stButton > button:hover { transform: scale(1.05); background: linear-gradient(45deg, #836fff, #6c63ff); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='floating-title' style='text-align: center; color: #6c63ff;'>✨ Resume Evaluator ✨</h1>", unsafe_allow_html=True)

fun_messages = [
    "Let's make your resume sparkle! ✨", "Time to shine bright! 🌟",
    "Ready to impress? 🚀", "Let's make magic happen! 🎭",
    "Your success story starts here! 📈", "Transforming resumes into opportunities! 🎯"
]
st.markdown(f"<h3 style='text-align: center; color: black;'>{random.choice(fun_messages)}</h3>", unsafe_allow_html=True)

# Input Fields
name = st.text_input("👤 Your Name", placeholder="e.g., Harry Potter")
email = st.text_input("📧 Your Email", placeholder="e.g., wizard@hogwarts.com")
role = st.selectbox("🎯 Role Applying For", ["Select Role", "Data Science", "Web Development", "Software Engineering", "AI/ML", "Cloud Computing", "Cybersecurity"])
experience = st.selectbox("📅 Years of Experience", ["Select Experience"] + ["Fresher"] + [f"{i} years" for i in range(1, 26)])
resume = st.file_uploader("📜 Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# Submit Button
if st.button("🌟 Reveal Your Resume's Potential"):
    if not name or not email or role == "Select Role" or experience == "Select Experience" or not resume:
        st.error("❌ Please fill in all required fields before proceeding!")
    else:
        with st.spinner(random.choice(["Summoning career opportunities... 🌟", "Analyzing your professionalism... 🔮", "Unleashing your potential... 🚀"])):  
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)

        resume_text = extract_text_from_file(resume)

        if resume_text:
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

            # Readability & Keywords
            readability_score = grammar_readability_check(resume_text)
            keywords = extract_keywords(resume_text)

            # Display Results
            st.success(f"✅ **Predicted Category:** {prediction}")
            st.info(f"📖 **Readability Score:** {readability_score:.2f}")
            st.info(f"🔹 **Suggested Skills to Improve:** {', '.join(suggestions)}")
            st.info(f"📌 **Top Keywords for ATS:** {', '.join(keywords.keys())}")

            # Generate PDF Report
            pdf_data = generate_pdf(name, email, role, prediction, suggestions, readability_score, keywords)
            st.download_button(label="📥 Download Report", data=pdf_data, file_name="Resume_Evaluation_Report.pdf", mime="application/pdf")

        else:
            st.error("❌ Could not extract text from the uploaded file.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>✨ Making dreams come true, one resume at a time ✨</p>", unsafe_allow_html=True)
