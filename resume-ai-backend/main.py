import os
import io
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import docx
import pdfplumber
from dotenv import load_dotenv
import re             # <-- MAKE SURE THIS LINE IS HERE
import json           # <-- And this one
import traceback      # <-- And this one

load_dotenv() # Load environment variables from .env file
# --- Configuration ---
# Load your API key from an environment variable for security
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

app = FastAPI()

# --- CORS Middleware ---
# This allows your frontend (on a different URL) to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper Function to Parse Resumes ---
def parse_resume(file: UploadFile) -> str:
    content = file.file.read()
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages)
    elif file.filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join(para.text for para in doc.paragraphs)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or DOCX.")

# --- The AI Prompt ---
def get_optimization_prompt(resume_text: str, job_description: str) -> str:
    return f"""
    You are an expert AI resume assistant and career coach.
    Your task is to optimize the provided resume to perfectly match the given job description.

    Analyze the following:
    - Resume Text: "{resume_text}"
    - Job Description: "{job_description}"

    Based on your analysis, you MUST provide a response in a valid JSON format.
    The JSON object should have two keys:
    1. "optimized_resume_text": A complete, rewritten version of the resume. Incorporate relevant keywords and action verbs from the job description naturally. Rephrase bullet points to highlight achievements and measurable outcomes that align with the job's requirements. Maintain a professional tone. Do not invent new experiences.
    2. "explanation_of_changes": A brief, bulleted list in a single string explaining the key changes made. This should cover:
        - Keywords Added: Important keywords from the job description that were integrated.
        - Action Verbs: How action verbs were improved to be more impactful.
        - ATS Friendliness: General advice on why the new format is better for Applicant Tracking Systems (ATS).

    Example for "explanation_of_changes":
    "- **Keywords Added:** Integrated terms like 'Agile Methodologies', 'Project Lifecycle Management', and 'Stakeholder Communication' from the job description.\\n- **Impactful Language:** Replaced passive phrases with strong action verbs like 'Orchestrated', 'Spearheaded', and 'Quantified' to demonstrate achievements.\\n- **ATS Optimization:** The resume now uses a clean, single-column format with standard headings, which is easily parsed by applicant tracking systems."

    Provide ONLY the JSON object in your response.
    """

# --- API Endpoint ---
@app.post("/optimize-resume/")
async def optimize_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    try:
        resume_text = parse_resume(resume_file)

        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = get_optimization_prompt(resume_text, job_description)
        response = model.generate_content(prompt)

        raw_text = response.text
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)

        if match:
            json_str = match.group(0)
            return JSONResponse(content=json.loads(json_str))
        else:
            raise HTTPException(status_code=500, detail="AI response did not contain valid JSON.")

    except Exception as e:
        # --- NEW DEBUGGING LINE ---
        # This will force the full error to be printed in your terminal
        traceback.print_exc()
        # --- END OF NEW LINE ---
        raise HTTPException(status_code=500, detail=str(e))
        # --- END OF NEW LOGIC ---

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))