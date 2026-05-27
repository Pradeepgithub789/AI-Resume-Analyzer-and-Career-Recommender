import re
from typing import Dict, List, Any, Tuple

# Section synonyms for detection
SECTION_PATTERNS = {
    "Education": [r'\beducation\b', r'\bacacademic\b', r'\bqualifications\b', r'\bdegree\b', r'\bschooling\b'],
    "Experience": [r'\bexperience\b', r'\bwork\s+history\b', r'\bprofessional\s+experience\b', r'\bemployment\b', r'\bcareer\b'],
    "Skills": [r'\bskills\b', r'\btechnical\s+skills\b', r'\bexpertise\b', r'\bcompetencies\b', r'\bcore\s+strengths\b'],
    "Projects": [r'\bprojects\b', r'\bacademics?\s+projects\b', r'\bpersonal\s+projects\b', r'\bkey\s+projects\b'],
    "Contact Info": [r'\bcontact\b', r'\bemail\b', r'\bphone\b', r'\baddress\b', r'\blinkedin\b']
}

# Strong action verbs for ATS screening
ACTION_VERBS = {
    "developed", "led", "managed", "designed", "implemented", "created", 
    "automated", "optimized", "built", "engineered", "facilitated", 
    "increased", "reduced", "delivered", "coordinated", "analyzed", 
    "resolved", "integrated", "monitored", "deployed", "refactored", 
    "mentored", "championed", "formulated", "leveraged", "pioneered"
}

def analyze_sections(text: str) -> Dict[str, bool]:
    """
    Check for the presence of standard resume sections.
    Uses robust line-start header patterns for sections (Education, Experience, Skills, Projects)
    to avoid middle-of-sentence false positives, while falling back to general search for inline Contact Info.
    """
    found_sections = {}
    text_lower = text.lower()
    
    for section, patterns in SECTION_PATTERNS.items():
        found = False
        if section == "Contact Info":
            # Contact info fields are typically inline, so check anywhere
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    found = True
                    break
        else:
            # Main sections must appear as standalone headers at the beginning of a line
            for pattern in patterns:
                clean_pat = pattern.replace(r'\b', '')
                # Matches patterns starting a line (allowing markdown headers, bullets, spaces)
                header_regex = rf'(?:^|\n)\s*[#=*•-]*\s*{clean_pat}\b'
                if re.search(header_regex, text_lower):
                    found = True
                    break
                    
        found_sections[section] = found
        
    return found_sections

def calculate_ats_score(
    text: str, 
    extracted_skills: List[str], 
    contact_info: Dict[str, Any],
    is_fresher: bool = None
) -> Dict[str, Any]:
    """
    Compute ATS score out of 100 based on multiple parameters:
    1. Section Completeness (30%)
    2. Skill Density (30%)
    3. Word Count / Length (20%)
    4. Keyword Density & Formatting (Action Verbs, Social Links) (20%)
    
    Returns:
        Dict: Complete score breakdown, deductions, and actionable improvements.
    """
    score = 0
    breakdown = {}
    recommendations = []
    
    # Pre-calculate word count for auto-detection and scoring
    word_list = [w for w in re.findall(r'\b\w+\b', text.lower())]
    word_count = len(word_list)
    
    sections = analyze_sections(text)
    
    # 0. Student / Fresher Auto-Detection (if not explicitly passed from UI)
    if is_fresher is None:
        has_no_experience_section = not sections.get("Experience", False)
        has_edu_and_proj = sections.get("Education", False) and sections.get("Projects", False)
        has_recent_year = bool(re.search(r'\b(202[2-7])\b', text))
        
        # User refined logic: No Experience, both Edu + Proj present, and either recent grad year or small word count
        is_fresher = has_no_experience_section and has_edu_and_proj and (word_count < 350 or has_recent_year)
    
    # ---------------------------------------------
    # 1. Section Completeness (Max 30 points)
    # ---------------------------------------------
    # Adjust section completeness for freshers: projects can substitute for experience
    experience_substituted = False
    if is_fresher and sections.get("Projects") and not sections.get("Experience"):
        sections["Experience"] = True
        experience_substituted = True

    sections_found = sum(1 for found in sections.values() if found)
    section_score = sections_found * 6 # 5 sections * 6 = 30 points max
    score += section_score
    breakdown["Section Completeness"] = {
        "score": section_score,
        "max": 30,
        "details": sections
    }
    
    # Generate section recommendations
    for sec, found in sections.items():
        if not found:
            recommendations.append(
                f"⚠️ **Missing Section**: Could not detect a clear '{sec}' section. Make sure to add a standard header like '{sec}'."
            )
            
    # ---------------------------------------------
    # 2. Skill Density Check (Max 30 points)
    # ---------------------------------------------
    skill_count = len(extracted_skills)
    skill_score = 0
    if 12 <= skill_count <= 22:
        skill_score = 30
        skill_status = "Optimal"
    elif 8 <= skill_count <= 11 or 23 <= skill_count <= 28:
        skill_score = 20
        skill_status = "Good, but could be adjusted"
    elif 5 <= skill_count <= 7 or 29 <= skill_count <= 35:
        skill_score = 10
        skill_status = "Suboptimal (too few or too many)"
    else:
        skill_score = 5
        skill_status = "Critical (very few or cluttered)"
        
    score += skill_score
    breakdown["Skill Density"] = {
        "score": skill_score,
        "max": 30,
        "details": {
            "count": skill_count,
            "status": skill_status
        }
    }
    
    if skill_count < 10:
        recommendations.append(
            f"💡 **Increase Skill Count**: You listed only {skill_count} skills. Aim to include 12-22 relevant technical skills to pass ATS filters."
        )
    elif skill_count > 25:
        recommendations.append(
            f"💡 **Reduce Skill Clutter**: You listed {skill_count} skills. Having too many skills can dilute your profile and look like keyword stuffing. Keep it focused between 12-22 skills."
        )
        
    # ---------------------------------------------
    # 3. Word Count / Length (Max 20 points)
    # ---------------------------------------------
    word_score = 0
    if is_fresher:
        # Optimized brackets for freshers/students (concise 1-page resume is optimal)
        if 180 <= word_count <= 600:
            word_score = 20
            word_status = "Optimal for Fresher (Ideal 1-page format)"
        elif 120 <= word_count < 180 or 600 < word_count <= 850:
            word_score = 15
            word_status = "Good, but can be slightly refined"
        elif 80 <= word_count < 120 or 850 < word_count <= 1100:
            word_score = 8
            word_status = "Suboptimal length for Fresher"
        else:
            word_score = 2
            word_status = "Critically Short/Long"
    else:
        # Standard brackets for experienced roles
        if 400 <= word_count <= 900:
            word_score = 20
            word_status = "Optimal (ideal 1-page format)"
        elif 250 <= word_count < 400 or 900 < word_count <= 1200:
            word_score = 15
            word_status = "Acceptable, but can be improved"
        elif 150 <= word_count < 250 or 1200 < word_count <= 1500:
            word_score = 8
            word_status = "Short or Wordy"
        else:
            word_score = 2
            word_status = "Critically Short/Long"
        
    score += word_score
    breakdown["Resume Length"] = {
        "score": word_score,
        "max": 20,
        "details": {
            "word_count": word_count,
            "status": word_status
        }
    }
    
    if is_fresher:
        if word_count < 150:
            recommendations.append(
                f"📏 **Resume Too Short**: Your resume has only {word_count} words. Try to add a bit more detail about your academic coursework, projects, or achievements to reach at least 180 words."
            )
        elif word_count > 700:
            recommendations.append(
                f"📏 **Resume Too Wordy**: Your resume has {word_count} words. For student profiles, a highly focused single-page layout (under 600 words) is recommended."
            )
    else:
        if word_count < 300:
            recommendations.append(
                f"📏 **Resume Too Short**: Your resume has only {word_count} words. Standard resumes should be at least 350-400 words to show sufficient depth."
            )
        elif word_count > 1000:
            recommendations.append(
                f"📏 **Resume Too Wordy**: Your resume has {word_count} words. An overly wordy resume can easily be discarded. Try to condense it, focusing on impact."
            )
        
    # ---------------------------------------------
    # 4. Keyword Formatting & Actions (Max 20 points)
    # ---------------------------------------------
    format_score = 0
    format_details = {}
    
    # A. Check for Email & Phone (5 pts)
    has_contact = contact_info.get("email") is not None and contact_info.get("phone") is not None
    format_score += 5 if has_contact else (2.5 if (contact_info.get("email") or contact_info.get("phone")) else 0)
    format_details["Contact Info Present"] = has_contact
    
    if not contact_info.get("email"):
        recommendations.append("📧 **Missing Email**: Ensure your professional email is clearly visible at the top of your resume.")
    if not contact_info.get("phone"):
        recommendations.append("📞 **Missing Phone Number**: Add your phone number so recruiters can easily reach out to you.")
        
    # B. Professional Profile Links (LinkedIn / GitHub) (5 pts)
    has_links = (contact_info.get("linkedin") is not None) + (contact_info.get("github") is not None)
    link_points = has_links * 2.5 # 2.5 pts each
    format_score += link_points
    format_details["LinkedIn Provided"] = contact_info.get("linkedin") is not None
    format_details["GitHub Provided"] = contact_info.get("github") is not None
    
    if not contact_info.get("linkedin"):
        recommendations.append("🔗 **Missing LinkedIn**: Adding a customized LinkedIn URL increases recruiter views and builds trust.")
    if not contact_info.get("github"):
        recommendations.append("💻 **Missing GitHub**: For tech roles, linking to your GitHub profile demonstrates hands-on coding experience.")
        
    # C. Strong Action Verbs Density (10 pts)
    # Count unique action verbs present in the text
    found_verbs = [v for v in ACTION_VERBS if re.search(rf'\b{v}\b', text.lower())]
    verb_count = len(found_verbs)
    
    # Score out of 10
    verb_score = min(10, verb_count * 1.25) # 8 verbs -> 10 pts
    format_score += verb_score
    format_details["Action Verbs Found"] = verb_count
    
    score += format_score
    breakdown["Formatting & Verbs"] = {
        "score": round(format_score, 1),
        "max": 20,
        "details": format_details
    }
    
    if verb_count < 5:
        recommendations.append(
            f"🚀 **Use Action Verbs**: Found only {verb_count} strong action verbs. Use impactful verbs like 'engineered', 'streamlined', 'automated', and 'optimized' to describe your accomplishments rather than 'responsible for'."
        )
        
    # Clean up recommendations (ensure limit or keep only top ones)
    if not recommendations:
        recommendations.append("🎉 **Outstanding Formatting!** Your resume is in excellent shape and meets standard ATS guidelines.")
        
    return {
        "overall_score": min(100, round(score)),
        "breakdown": breakdown,
        "recommendations": recommendations,
        "action_verbs_found": sorted(found_verbs)
    }
