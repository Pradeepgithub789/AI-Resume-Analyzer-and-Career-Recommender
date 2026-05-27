from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import io
import tempfile
import logging

# Core utilities
from utils.parser import extract_text_from_pdf, parse_pdf_with_metadata
from utils.preprocessing import get_spacy_nlp, extract_contact_info, extract_candidate_name
from utils.skill_extractor import extract_skills, get_flat_skills, SKILL_TAXONOMY
from utils.ats_scorer import calculate_ats_score
from utils.matcher import match_resume_to_jd
from utils.recommender import recommend_jobs
from utils.pdf_generator import generate_pdf_report

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Limit file upload to 16MB

# Pre-load spaCy model lazily on server boot
logger.info("Pre-warming NLP Engine...")
get_spacy_nlp()
logger.info("NLP Engine is ready.")

# Load sample Job Descriptions
SAMPLE_JDS = []
try:
    jd_path = os.path.join(os.path.dirname(__file__), "data", "sample_jds.json")
    if os.path.exists(jd_path):
        with open(jd_path, "r") as f:
            SAMPLE_JDS = json.load(f)
except Exception as e:
    logger.error(f"Error loading sample job descriptions: {str(e)}")

# ----------------------------------------------------
# HTML Template Route
# ----------------------------------------------------
@app.route("/")
def index():
    """
    Render main dashboard landing page.
    """
    return render_template("index.html")

# ----------------------------------------------------
# JSON API Endpoints
# ----------------------------------------------------
@app.route("/api/sample-jds", methods=["GET"])
def get_sample_jds():
    """
    Get the list of predefined sample Job Descriptions.
    """
    return jsonify(SAMPLE_JDS)

@app.route("/api/skill-taxonomy", methods=["GET"])
def get_skill_taxonomy():
    """
    Get the predefined system skill taxonomy.
    """
    return jsonify(SKILL_TAXONOMY)

@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    """
    Accept an uploaded PDF resume, parse, clean, score, and recommend careers.
    """
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file was uploaded"}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400
        
    try:
        # Create a temporary file to save the uploaded file stream
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, next(tempfile._get_candidate_names()) + ".pdf")
        file.save(temp_path)
        
        # 1. Parse Text & Metadata
        parsed_pdf = parse_pdf_with_metadata(temp_path)
        resume_text = parsed_pdf["text"]
        page_count = parsed_pdf["page_count"]
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if not resume_text.strip():
            return jsonify({"error": "The resume appeared to contain no extractable text. Please ensure it is not scanned/image-only."}), 422
            
        # 2. Extract Candidate Information
        candidate_name = extract_candidate_name(resume_text)
        contact_info = extract_contact_info(resume_text)
        
        # 3. Extract Skills
        extracted_skills = extract_skills(resume_text)
        flat_skills = get_flat_skills(extracted_skills)
        
        # Get student/fresher toggle preference (None if not provided, for auto-detection fallback)
        is_fresher_raw = request.form.get("is_fresher")
        is_fresher_val = None
        if is_fresher_raw is not None:
            is_fresher_val = is_fresher_raw.lower() == "true"
            
        # 4. Calculate ATS Scoring
        ats_results = calculate_ats_score(resume_text, flat_skills, contact_info, is_fresher=is_fresher_val)
        
        # 5. Career Path Recommendation
        recommender_results = recommend_jobs(flat_skills)
        
        # Return complete details package
        return jsonify({
            "resume_text": resume_text,
            "page_count": page_count,
            "candidate_name": candidate_name,
            "contact_info": contact_info,
            "extracted_skills": extracted_skills,
            "flat_skills": flat_skills,
            "ats_results": ats_results,
            "recommender_results": recommender_results
        })
        
    except Exception as e:
        logger.error(f"Error during API resume analysis: {str(e)}")
        return jsonify({"error": f"Failed to parse resume: {str(e)}"}), 500

@app.route("/api/match", methods=["POST"])
def match_resume():
    """
    Compare resume text vs custom/preloaded Job Description text.
    """
    data = request.get_json() or {}
    resume_text = data.get("resume_text", "")
    jd_text = data.get("jd_text", "")
    
    if not resume_text.strip():
        return jsonify({"error": "Missing resume text context"}), 400
    if not jd_text.strip():
        return jsonify({"error": "Missing job description text context"}), 400
        
    try:
        match_results = match_resume_to_jd(resume_text, jd_text)
        return jsonify(match_results)
    except Exception as e:
        logger.error(f"Error during Job Description matching: {str(e)}")
        return jsonify({"error": f"Failed to execute job matching: {str(e)}"}), 500

@app.route("/api/download-report", methods=["POST"])
def download_pdf_report():
    """
    Accepts resume metrics payload and generates/streams the downloadable ReportLab PDF.
    """
    try:
        data = request.get_json() or {}
        candidate_name = data.get("candidate_name", "Candidate")
        contact_info = data.get("contact_info", {})
        ats_results = data.get("ats_results", {})
        recommender_results = data.get("recommender_results", {})
        
        # Generate on-the-fly PDF bytes
        pdf_bytes = generate_pdf_report(
            candidate_name=candidate_name,
            contact_info=contact_info,
            ats_results=ats_results,
            recommender_results=recommender_results
        )
        
        # Stream file to browser
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"ATS_Report_{candidate_name.replace(' ', '_')}.pdf"
        )
        
    except Exception as e:
        logger.error(f"Error compiling PDF report: {str(e)}")
        return jsonify({"error": f"Could not export PDF report: {str(e)}"}), 500

if __name__ == "__main__":
    # Start on standard port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)
