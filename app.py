from flask import Flask, render_template, request
import os
import re
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills that the analyzer can detect
SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "data analysis",
    "data science",
    "excel",
    "communication",
    "problem solving",
    "leadership",
    "teamwork"
]


def extract_text_from_pdf(file_path):
    """Extract text from uploaded PDF."""
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_skills(text):
    """Find known skills in text."""
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check resume
    if "resume" not in request.files:
        return "Please upload a resume PDF."

    resume = request.files["resume"]

    if resume.filename == "":
        return "Please select a resume PDF."

    # Get job description
    job_description = request.form.get("job_description", "")

    if not job_description.strip():
        return "Please enter a job description."

    # Save uploaded resume
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    resume.save(file_path)

    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(file_path)

        # Extract skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        # Matching skills
        matching_skills = [
            skill for skill in job_skills
            if skill in resume_skills
        ]

        # Missing skills
        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_skills
        ]

        # Calculate score
        if len(job_skills) > 0:
            score = round(
                (len(matching_skills) / len(job_skills)) * 100
            )
        else:
            score = 0

        return render_template(
            "result.html",
            score=score,
            resume_skills=resume_skills,
            job_skills=job_skills,
            matching_skills=matching_skills,
            missing_skills=missing_skills
        )

    except Exception as e:
        return f"Error while analyzing resume: {str(e)}"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
