import re
import logging
from typing import Dict, List, Set, Tuple

logger = logging.getLogger(__name__)

# Complete structured taxonomy of tech skills
SKILL_TAXONOMY = {
    "Programming Languages": [
        "Python", "Java", "C++", "C", "C#", "Go", "Rust", "Ruby", "PHP", 
        "Swift", "Kotlin", "TypeScript", "JavaScript", "R", "Scala", "Bash", 
        "SQL", "HTML", "CSS", "Dart", "MATLAB", "Perl", "Julia"
    ],
    "Web Development": [
        "React", "Angular", "Vue", "Vue.js", "Next.js", "Nuxt.js", "Svelte", 
        "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot", 
        "Ruby on Rails", "Laravel", "ASP.NET", "TailwindCSS", "Bootstrap", 
        "jQuery", "Redux", "GraphQL", "REST APIs", "gRPC", "Webpack", "Vite"
    ],
    "Databases & Cache": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra", 
        "Elasticsearch", "Neo4j", "Firebase", "DynamoDB", "MariaDB", "Oracle",
        "SQL Server", "Memcached"
    ],
    "AI, Machine Learning & Data Science": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP",
        "Natural Language Processing", "Computer Vision", "TensorFlow", 
        "PyTorch", "Keras", "Scikit-Learn", "Pandas", "NumPy", "SciPy", 
        "Matplotlib", "Seaborn", "XGBoost", "Hugging Face", "LLMs", 
        "Generative AI", "LangChain", "OpenCV", "Tableau", "PowerBI", 
        "Data Visualization", "Data Analytics", "Data Mining", "Statistics",
        "Feature Engineering", "A/B Testing"
    ],
    "Cloud & DevOps": [
        "AWS", "Google Cloud Platform", "GCP", "Microsoft Azure", "Azure",
        "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD", "Jenkins",
        "GitHub Actions", "Git", "GitHub", "GitLab", "Linux", "Unix", "Bash Scripting",
        "Nginx", "Apache", "Kubectl", "CircleCI", "Prometheus", "Grafana"
    ],
    "Mobile & Systems": [
        "Flutter", "React Native", "SwiftUI", "Android Development", "iOS Development", 
        "Android Studio", "Kotlin", "Xamarin", "Cordova", "Electron"
    ],
    "Software Engineering Concepts": [
        "Data Structures", "Algorithms", "DSA", "System Design", "Microservices",
        "OOP", "Object Oriented Programming", "Design Patterns", "Agile", 
        "Scrum", "Kanban", "SDLC", "GitFlow", "Unit Testing", "PyTest", 
        "JUnit", "TDD", "Test Driven Development", "CI/CD", "RESTful APIs",
        "API Design", "Authentication", "JWT", "OAuth"
    ],
    "Soft Skills & Management": [
        "Project Management", "Leadership", "Communication", "Problem Solving",
        "Teamwork", "Agile Management", "Product Management", "Critical Thinking",
        "Time Management", "Collaboration", "Mentoring"
    ]
}

def compile_skill_regex(skill: str) -> re.Pattern:
    """
    Compile a case-insensitive regex for a skill that avoids false substring matches.
    Specially handles skills with custom symbols like C++, C#, .NET, Node.js.
    """
    # Escape special characters
    escaped_skill = re.escape(skill)
    
    # Custom boundary checks for special characters
    # If the skill starts or ends with symbols like + or # or ., standard \b (word boundary) won't work.
    
    # 1. Starts with special character (e.g. .NET)
    if skill.startswith('.'):
        pattern = rf'(?:\s|^){escaped_skill}(?:\b|\s|$)'
    # 2. Ends with special characters (e.g. C++, C#)
    # We ensure they are not followed by letters, +, or # to allow punctuation like commas or periods
    elif skill.endswith('+') or skill.endswith('#'):
        pattern = rf'\b{escaped_skill}(?![a-zA-Z+#])'
    # 3. Simple short letters (e.g. C, R, Go) - require strict full word boundary
    elif len(skill) <= 2:
        # Special case for 'C' to avoid false matches in 'C++' or 'C#'
        if skill.lower() == 'c':
            pattern = rf'\b{escaped_skill}\b(?![+#])'
        else:
            pattern = rf'\b{escaped_skill}\b'
    # 4. Standard multi-word or single-word skills
    else:
        # Match boundaries but allow internal spaces/hyphens
        pattern = rf'\b{escaped_skill}\b'
        
    return re.compile(pattern, re.IGNORECASE)

# Compile all regexes once during module import
SKILL_REGEXES: Dict[str, List[Tuple[str, re.Pattern]]] = {}
for category, skills in SKILL_TAXONOMY.items():
    SKILL_REGEXES[category] = []
    for skill in skills:
        SKILL_REGEXES[category].append((skill, compile_skill_regex(skill)))

def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract skills from the resume text based on the predefined skill taxonomy.
    
    Returns:
        Dict[str, List[str]]: A dictionary of extracted skills grouped by category.
    """
    extracted = {}
    normalized_text = " " + text + " "  # Wrap in spaces to simplify regex boundary checks at start/end
    
    for category, skill_list in SKILL_REGEXES.items():
        found_in_category = set()
        for skill_name, pattern in skill_list:
            if pattern.search(normalized_text):
                # Extra validation: Make sure "Go" is not matched inside "Google", or "C" is not matched in "CV"
                # If short skill, double check boundaries
                if len(skill_name) <= 2:
                    # R and C can have false matches in section bullet indices, e.g., "C. Projects"
                    # Let's perform a strict clean check
                    matches = pattern.findall(normalized_text)
                    if matches:
                        # Ensure it's not a bullet like "C. Projects" or "c/o"
                        valid_match = False
                        for match in matches:
                            # Search in original text with surrounding context to avoid false indices
                            idx = normalized_text.lower().find(match.lower())
                            if idx != -1:
                                surrounding = normalized_text[max(0, idx-2):min(len(normalized_text), idx+len(match)+2)]
                                # If surrounded by dot or slash, ignore
                                if not re.search(r'[A-Za-z]\.\s|[0-9]\.\s|/|\\', surrounding):
                                    valid_match = True
                                    break
                        if valid_match:
                            found_in_category.add(skill_name)
                else:
                    found_in_category.add(skill_name)
                    
        if found_in_category:
            # Sort the found skills to maintain consistency
            extracted[category] = sorted(list(found_in_category))
            
    # Resolve aliases/synonyms
    # Vue and Vue.js -> keep Vue
    # NLP and Natural Language Processing -> keep NLP
    # OOP and Object Oriented Programming -> keep OOP
    # CI/CD and Continuous Integration/Continuous Deployment -> keep CI/CD
    for cat in extracted:
        items = extracted[cat]
        if "Vue.js" in items and "Vue" in items:
            items.remove("Vue.js")
        if "Natural Language Processing" in items and "NLP" in items:
            items.remove("Natural Language Processing")
        if "Object Oriented Programming" in items and "OOP" in items:
            items.remove("Object Oriented Programming")
        extracted[cat] = sorted(items)
        
    return extracted

def get_flat_skills(extracted_skills: Dict[str, List[str]]) -> List[str]:
    """
    Get a flat list of all extracted skills.
    """
    flat = []
    for skills in extracted_skills.values():
        flat.extend(skills)
    return sorted(list(set(flat)))
