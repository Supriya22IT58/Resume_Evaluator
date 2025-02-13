import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load Dataset (Ensure 'UpdatedResumeDataSet.csv' is in the same folder)
df = pd.read_csv("UpdatedResumeDataSet.csv")

# Check for missing values
df.dropna(inplace=True)

# Extract Resume Text and Categories
X = df["Resume"]  # Resume Text
y = df["Category"]  # Job Category

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create Pipeline (TF-IDF + Naive Bayes Classifier)
pipeline = Pipeline([
    ("vectorizer", TfidfVectorizer(stop_words="english")),
    ("classifier", MultinomialNB())
])

# Train Model
pipeline.fit(X_train, y_train)

# Save Model
joblib.dump(pipeline, "resume_evaluator_model.pkl")
print("✅ Model training completed and saved as resume_evaluator_model.pkl")
