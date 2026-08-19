from flask import Flask, render_template, request
import os
import re
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------------
# Extract text from PDF
# -----------------------------------

def extract_text_from_pdf(pdf_path):

    text = ""

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# -----------------------------------
# Skill extraction
# -----------------------------------

def extract_skills(text):

    skills_list = [

        "python",
        "java",
        "c++",
        "c",
        "javascript",

        "html",
        "css",

        "react",
        "node.js",

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
        "data science",

        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",

        "power bi",
        "excel",

        "communication",
        "leadership",
        "problem solving"

    ]

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(set(found_skills))


# -----------------------------------
# Calculate match score
# -----------------------------------

def calculate_match_score(resume_skills, job_skills):

    if not job_skills:

        return 0

    matching_skills = set(resume_skills).intersection(
        set(job_skills)
    )

    score = (
        len(matching_skills)
        /
        len(set(job_skills))
    ) * 100

    return round(score, 2)


# -----------------------------------
# Home page
# -----------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        resume = request.files.get("resume")

        job_description = request.form.get(
            "job_description",
            ""
        )

        # Check resume

        if not resume:

            result = {
                "error": "Please upload a resume PDF."
            }

            return render_template(
                "index.html",
                result=result
            )


        # Check PDF

        if not resume.filename.lower().endswith(".pdf"):

            result = {
                "error": "Only PDF files are supported."
            }

            return render_template(
                "index.html",
                result=result
            )


        # Save resume

        filename = resume.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        resume.save(filepath)


        # Extract resume text

        resume_text = extract_text_from_pdf(
            filepath
        )


        # Extract resume skills

        resume_skills = extract_skills(
            resume_text
        )


        # Extract job skills

        job_skills = extract_skills(
            job_description
        )


        # Matching skills

        matching_skills = sorted(
            set(resume_skills).intersection(
                set(job_skills)
            )
        )


        # Missing skills

        missing_skills = sorted(
            set(job_skills).difference(
                set(resume_skills)
            )
        )


        # Calculate score

        score = calculate_match_score(
            resume_skills,
            job_skills
        )


        # Store results

        result = {

            "score": score,

            "resume_skills":
                resume_skills,

            "job_skills":
                job_skills,

            "matching_skills":
                matching_skills,

            "missing_skills":
                missing_skills

        }


    return render_template(
        "index.html",
        result=result
    )


# -----------------------------------
# Run application
# -----------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
