import os
from flask import Flask, render_template, request, jsonify, make_response
from ats import extract_text, clean_text, analyze_resume
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash



app = Flask(__name__)

# Define folder for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    response = make_response(render_template('index.html', result=None))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/check_resume', methods=['POST'])
def check_resume():
    resume_file = request.files.get('resume')
    jd_file = request.files.get('jobdesc-file')
    jd_text_input = request.form.get('jobdesc')  # textarea JD

    if not resume_file or resume_file.filename == '':
        return jsonify({"error": "No resume file uploaded."})

    if (not jd_file or jd_file.filename == '') and not jd_text_input.strip():
        return jsonify({"error": "Please upload a JD file or paste the JD text."})

    if not allowed_file(resume_file.filename):
        return jsonify({"error": "Invalid resume file type."})

    resume_filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    resume_file.save(resume_path)

    if jd_file and jd_file.filename != '' and allowed_file(jd_file.filename):
        jd_filename = secure_filename(jd_file.filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        jd_file.save(jd_path)
        jd_text = extract_text(jd_path)
    else:
        jd_text = jd_text_input

    resume_text = extract_text(resume_path)

    if not resume_text or not jd_text:
        return jsonify({"error": "Failed to extract text from resume or job description."})

    cleaned_resume_text = clean_text(resume_text)
    cleaned_jd_text = clean_text(jd_text)

    result = analyze_resume(cleaned_resume_text, cleaned_jd_text)
    return render_template('result.html', result=result)



if __name__ == '__main__':
    app.run(debug=True)
