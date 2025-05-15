#  ATS Resume Checker

This is a Flask-based web application that analyzes your resume against a job description to assess how well it matches, helping you improve your chances with Applicant Tracking Systems (ATS).

---

## Features

- Upload resume (PDF/DOCX supported)
- Paste or upload job description
- Compare and score resume based on job relevance
- Uses NLP to extract and match skills
- User-friendly interface with modal feedback
- Backend built with Flask | Frontend with HTML, CSS, JS

---

## Tech Stack

- **Frontend:** HTML, JavaScript (Modals)
- **Backend:** Python, Flask
- **Libraries:** `spaCy`, `PyPDF2`, `python-docx`, `re`, `nltk`
- **AI:** LangChain + Groq (LLaMA 3 model)


##  Installation

1. **Clone the repository**

  git clone https://github.com/Kavita201/ATS-MatchScore.git
  
  cd ATS-MatchScore

2. **Create a virtual environment**

   python -m venv venv

   source venv/bin/activate

   venv\Scripts\activate


3. **Run the Flask app**

   python app.py
   
