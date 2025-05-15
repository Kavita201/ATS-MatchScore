import os
import json
from pypdf import PdfReader
from docx import Document
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLaMA model
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key=GROQ_API_KEY 
)

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT files"""
    try:
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            return " ".join(page.extract_text() or "" for page in reader.pages)
        elif file_path.lower().endswith(".docx"):
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        elif file_path.lower().endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Error: Unsupported file format '{file_path}'"
    except Exception as e:
        return f"Error extracting text: {e}"

def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def analyze_resume(resume_text, jd_text):
    """Analyze resume against job description using LLM"""
    # Create a prompt directly as a message instead of using PromptTemplate
    prompt = f"""
Analyze the following resume for ATS (Applicant Tracking System) compatibility by comparing Resume and Job Description.
Evaluate and provide a percentage contribution for each of the following categories toward the overall ATS score:

- compare Key Responsibilities of JD and  Resume 
- Skills relevance 
- Education relevence
- Experience relevance
- Grammar and spelling
- Designation or Position

Based on these, calculate a final ATS_score and return ONLY a valid JSON object in the following format:

{{
  "ATS_score": "XX%",
  "score_breakdown": {{
    "skills": "XX%",
    "education": "XX%",
    "experience": "XX%",
    "grammar": "XX%"
  }},
  "missing_requirements": ["skill1", "skill2", "skill3"],
  "improvement_suggestion": ["suggestion1", "suggestion2", "suggestion3"]
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    
    # Use the messages API instead of chains
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    
    # Extract the content from the response
    content = response.content
    
    # Clean the response to ensure it's valid JSON
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response", "raw_response": content}
    else:
        return {"error": "No JSON found in response", "raw_response": content}

if __name__ == '__main__':
    resume_path = input("Enter the path to the resume file (pdf/docx/txt): ")
    jd_input = input("Enter path to job description file or type JD text directly: ")

    # Extract Job Description
    if jd_input.lower().endswith(('.pdf', '.docx', '.txt')):
        jd_text = extract_text(jd_input)
        if jd_text.startswith("Error"):
            print("Failed to extract JD:\n", jd_text)
            jd_text = ""
    else:
        lines = [jd_input]
        while True:
            line = input()
            if line.strip() == '':
                break
            lines.append(line)
        jd_text = "\n".join(lines)

    resume_text = extract_text(resume_path)
    if not isinstance(resume_text, str) or resume_text.startswith("Error"):
        print("Failed to extract text from Resume.\n", resume_text)
        resume_text = ""

    if not resume_text or not jd_text:
        print("Missing resume or job description text.")
    else:
        cleaned_resume_text = clean_text(resume_text)
        cleaned_jd_text = clean_text(jd_text)

        print("\nAnalyzing resume vs job description...\n")
        result = analyze_resume(cleaned_resume_text, cleaned_jd_text)
        
        # Format and print the result as JSON
        try:
            print("\nResult:")
            print(json.dumps(result, indent=4))
        except Exception as e:
            print("Error formatting output:", e)
            print("Raw output:", result)
# with open("ats_result.json", "w") as f:
#     json.dump(result, f, indent=4)