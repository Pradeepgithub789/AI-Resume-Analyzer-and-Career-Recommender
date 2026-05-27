# 💼 AI-Powered Resume Analyzer & Career Recommender

A production-grade, highly aesthetic **AI-Powered Resume Analyzer and Career Recommendation System** designed to boost placement readiness. Built with **Flask**, **spaCy**, and **Scikit-Learn**, this application performs deep semantic parsing, scores resumes against strict ATS parameters, predicts career pathways, and maps skill gaps with guided roadmaps.

## 🚀 Core Features

### 1. 📄 ATS Resume Scorer & Analyzer
* **Automated Text Extraction:** Uses `pdfplumber` to extract and clean text from uploaded PDF resumes (handles custom ligature letters and formatting issues).
* **Multi-Factor Scoring (Out of 100):** Measures resume strength across four categories:
  1. *Section Completeness (30%):* Detects crucial sections (Education, Experience, Skills, Projects, Contact).
  2. *Skill Density (30%):* Checks if listed technologies fall within an optimal range (12-22 skills).
  3. *Word Count / Length (20%):* Analyzes length and checks for wordy or critically short resumes.
  4. *Formatting & Action Verbs (20%):* Checks for strong business action verbs (e.g. *engineered, optimized, refactored*) and checks for active portfolio URLs (LinkedIn, GitHub).
* **Actionable Recommendations:** Provides standard, dynamic bullet points explaining exactly why deductions occurred and how to fix them.

### 2. 🎯 Semantic Job Description Matcher
* **TF-IDF Vectorization:** Transforms resume and target job descriptions into a vector space of word importance scores.
* **Cosine Similarity Overlap:** Calculates the semantic match percentage between your resume and a target job.
* **Hybrid Match Scorer:** Combines text similarity (50%) and physical skill coverage (50%) to prevent false-positive matching on filler words.
* **Overlaps & Gap Mapping:** Divides job keywords into *Matching Skills Possessed* and *Missing Skills (Skill Gap)*.

### 3. 💼 Intelligent Career Planner & Skill Gap Roadmaps
* **Category Classification:** Predicts the primary resume profile (e.g., *Frontend Development*, *Data Science & AI*, *Cloud DevOps*, etc.) based on parsed skill concentrations.
* **Pathway Matching:** Displays the top 3 best matching career tracks with compatibility progress bars.
* **Interactive Upskilling Roadmaps:** For every missing career skill, the engine suggests curated next-steps, recommended courses, and topics to study.

### 4. 📂 Reference Skill Taxonomy Browser
* Displays all 200+ technology keywords tracked by the custom Regex engine, divided into 8 distinct technical sectors.

### 5. 📥 Professional PDF Report Export
* Generates and downloads a beautifully styled, print-ready PDF analysis report using **ReportLab** containing the full compatibility scorecard, actionable items, and career roadmap highlights.

---

## 📂 Project Architecture

```
resume_analyzer/
│
├── app.py                      # Flask main entrypoint (Routing and APIs)
├── requirements.txt            # Project Python dependencies
├── README.md                   # Installation & documentation
│
├── templates/
│   └── index.html              # Custom HTML5 responsive cockpit layout
│
├── static/
│   ├── css/
│   │   └── styles.css          # Sleek glassmorphism custom stylesheets
│   └── js/
│       └── main.js             # Client SPA controller, fetch APIs, and SVG gauges
│
├── data/
│   └── sample_jds.json         # Predefined high-quality Job Descriptions for testing
│
└── utils/
    ├── parser.py               # Extract and clean text from PDF resumes (pdfplumber)
    ├── preprocessing.py        # Tokenization, cleaning, spacy downloader, contact parsing
    ├── skill_extractor.py      # Skill taxonomies & custom Regex-based matchers
    ├── ats_scorer.py           # ATS scoring calculations, action verbs, and criteria
    ├── matcher.py              # TF-IDF + Cosine Similarity matching engine
    ├── recommender.py          # Career mapping, skill gap analysis, and course paths
    └── pdf_generator.py        # ReportLab PDF print-out layout manager
```

---

## 🛠️ Installation & Setup

Follow these steps to run the application locally on your computer:

### Prerequisites
Make sure you have **Python 3.8+** installed.

### 1. Clone or Move to Workspace
Open your terminal and navigate to the project directory:
```bash
cd c:/Users/paras/OneDrive/Documents/AI_Resume_Project
```

### 2. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```
*(The application will automatically download the spaCy `en_core_web_sm` model on first launch. If you face any issues, you can run `python -m spacy download en_core_web_sm` manually).*

### 3. Launch the Flask Server
Start the local server:
```bash
python app.py
```

### 4. Open in Browser
Once launched, open your web browser and navigate to:
```
http://localhost:5000
```
Open it in your preferred web browser to explore the dashboard!

---

## 🚀 How to Test the System

1. **Step 1: Get Scored**
   - Upload any sample tech resume (in `.pdf` format) inside the **ATS Resume Scorer** tab.
   - Click **Analyze Uploaded Resume**.
   - Review your overall compatibility gauge, extracted contact information, and skill distribution charts.
   - Click **Download Detailed PDF Report** to save a physical copy of your scorecard.

2. **Step 2: Match against a Job Description (JD)**
   - Navigate to the **Job Description Matcher** tab.
   - Select one of the pre-loaded jobs from the dropdown (e.g. *DeepMinded AI Labs - AI/ML Engineer* or *TechNova Solutions - Backend Software Engineer*).
   - Alternatively, paste a custom job description from LinkedIn or Indeed.
   - Click **Run Compatibility Comparison** to view matching/missing badges and semantic similarity metrics.

3. **Step 3: Roadmap Upskilling**
   - Go to the **Career Recommender** tab.
   - Check your primary resume category prediction.
   - Expand the recommended careers to view tailored roadmap milestones and links to master missing skills.

---

## 🧑‍💻 Technical Highlights (For Portfolio/Resume)
* **Hybrid Matcher Architecture:** Developed a specialized scoring metric combining structural text representation (TF-IDF bag-of-words vectorization) with discrete set theory logic (Hard Skill token intersection ratio).
* **Word-Boundary Symbol Parser:** Crafted case-insensitive Regular Expressions to accurately detect specialized programming syntax (`C++`, `C#`, `.NET`, `Node.js`) while maintaining strict word boundary safety to eliminate substrings and bullet indexing errors.
* **Preserved App State:** Built an active `st.session_state` architecture ensuring parsed resume metadata persists securely as users cycle between parsing, matching, and upskilling pages.
