📄 Resume Evaluator
🚀 AI-powered Resume Evaluator that analyzes resumes, predicts job categories, and provides skill improvement suggestions to help users land their dream job.

🔹 Features
✔ Upload resumes in PDF, DOCX, or TXT format.
✔ AI-powered classification of resumes into job categories.
✔ Personalized skill improvement suggestions for better career growth.
✔ Interactive UI with smooth animations and professional design.
✔ Supports freshers to 25+ years of experience.

📌 Tech Stack
Frontend: Streamlit, HTML, CSS
Backend: FastAPI
ML Model: Naïve Bayes Classifier (trained using TF-IDF)
Libraries Used: Pandas, NumPy, Scikit-learn, Joblib, PyMuPDF, python-docx
🛠 How to Run the Project
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/Resume-Evaluator.git
cd Resume-Evaluator
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Train the ML Model
bash
Copy
Edit
python model.py
This will create resume_evaluator_model.pkl.

4️⃣ Run the Web App
bash
Copy
Edit
streamlit run app.py
📂 Project Structure
php
Copy
Edit
📁 Resume-Evaluator
│── 📄 model.py          # Machine Learning Model for Resume Classification
│── 📄 app.py            # Streamlit Web Application
│── 📄 requirements.txt  # Dependencies
│── 📂 data              # Dataset folder (Ensure dataset is inside)
│── 📂 models            # Trained model files
│── 📂 static            # CSS/Images for UI
│── 📂 templates         # HTML templates (if used)
│── 📄 README.md         # Project Documentation
📊 Dataset Used
The model is trained using UpdatedResumeDataSet.csv, which contains resume text and job categories.

🛠 Future Enhancements
🔹 Resume Scoring System
🔹 Integration with Job Portals
🔹 More Advanced NLP-based Resume Analysis

🤝 Contributing
Contributions are welcome! Feel free to fork the repository, create a pull request, or open an issue.

📜 License
This project is licensed under the MIT License.

