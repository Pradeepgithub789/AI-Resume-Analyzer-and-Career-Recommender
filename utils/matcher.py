from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocessing import clean_and_tokenize
from utils.skill_extractor import extract_skills, get_flat_skills
from typing import Dict, List, Any

def match_resume_to_jd(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Compare a resume and a Job Description (JD) using TF-IDF and Cosine Similarity.
    Also extracts matching and missing skills.
    
    Args:
        resume_text (str): Extracted text of the resume.
        jd_text (str): Text of the Job Description.
        
    Returns:
        Dict: Match details containing match percentage, matching/missing skills, etc.
    """
    # 1. Extract skills from both text fields
    resume_skills_dict = extract_skills(resume_text)
    resume_skills = get_flat_skills(resume_skills_dict)
    
    jd_skills_dict = extract_skills(jd_text)
    jd_skills = get_flat_skills(jd_skills_dict)
    
    # 2. Map overlapping and missing skills
    matching_skills = []
    missing_skills = []
    
    for skill in jd_skills:
        # Check if the skill matches (case-insensitive checking is handled by skill extractor,
        # but to be safe, we check if the exact string exists or check lowercases)
        # Note: both lists contain normalized names from our taxonomy
        if skill in resume_skills:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # 3. Calculate Text Similarity using TF-IDF and Cosine Similarity
    # Clean and join tokens to construct a space-separated string of root words for vectorization
    cleaned_resume_tokens = clean_and_tokenize(resume_text, remove_stopwords=True)
    cleaned_jd_tokens = clean_and_tokenize(jd_text, remove_stopwords=True)
    
    resume_corpus = " ".join(cleaned_resume_tokens)
    jd_corpus = " ".join(cleaned_jd_tokens)
    
    # Vectorize
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_corpus, jd_corpus])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Similarity score converted to percentage (0 - 100)
        semantic_match_pct = round(float(cosine_sim) * 100, 1)
    except Exception:
        # Fallback if vocabulary is empty or fit fails
        semantic_match_pct = 0.0
        
    # 4. Calculate a hybrid match score that weights semantic similarity (30%) and skill coverage (70%)
    # This prevents resumes with generic filler words but no matching skills from getting high scores, 
    # and vice versa. Matching core skills is the primary driver of job alignment.
    skill_coverage_pct = 0.0
    if len(jd_skills) > 0:
        skill_coverage_pct = (len(matching_skills) / len(jd_skills)) * 100
        
    # Weighted average: 30% semantic similarity + 70% hard skill matching coverage
    if len(jd_skills) > 0:
        overall_match_pct = (semantic_match_pct * 0.3) + (skill_coverage_pct * 0.7)
        
        # If all skills are possessed (100% coverage), ensure the compatibility score is at least 90%
        if skill_coverage_pct == 100.0:
            overall_match_pct = max(90.0, overall_match_pct)
        # If skill coverage is very high (>= 80%), ensure the score is at least 80% (Excellent Match tier)
        elif skill_coverage_pct >= 80.0:
            overall_match_pct = max(80.0, overall_match_pct)
            
        overall_match_pct = round(overall_match_pct, 1)
    else:
        overall_match_pct = semantic_match_pct
        
    # Limit score boundaries
    overall_match_pct = min(100.0, max(0.0, overall_match_pct))
    
    # 5. Define compatibility tier
    if overall_match_pct >= 80:
        compatibility_tier = "Excellent Match"
        compatibility_desc = "Your profile is highly aligned with this position. You possess most of the required skills and your experience closely mirrors the job requirements."
    elif overall_match_pct >= 60:
        compatibility_tier = "Strong Match"
        compatibility_desc = "You have a solid foundation for this role. Adding a few missing skills to your resume could significantly boost your visibility."
    elif overall_match_pct >= 40:
        compatibility_tier = "Moderate Match"
        compatibility_desc = "You meet several basic requirements but have notable skill gaps. Consider upskilling or rewriting sections of your resume to emphasize transferrable skills."
    else:
        compatibility_tier = "Low Match"
        compatibility_desc = "There is a significant gap between your profile and this role. We recommend tailoring your resume specifically for this position or building relevant skills."
        
    return {
        "overall_match_percentage": overall_match_pct,
        "semantic_similarity": semantic_match_pct,
        "skill_coverage_percentage": round(skill_coverage_pct, 1),
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "jd_skills": sorted(jd_skills),
        "compatibility_tier": compatibility_tier,
        "compatibility_description": compatibility_desc
    }
