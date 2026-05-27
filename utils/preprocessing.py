import re
import logging
import spacy
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy loaded spacy model
_nlp = None

def get_spacy_nlp():
    """
    Get or download the spaCy NLP model lazily.
    """
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy 'en_core_web_sm' model not found. Attempting to download...")
            try:
                from spacy.cli import download
                download("en_core_web_sm")
                _nlp = spacy.load("en_core_web_sm")
                logger.info("Successfully downloaded and loaded 'en_core_web_sm'")
            except Exception as e:
                logger.error(f"Could not download 'en_core_web_sm'. Fallbacks will be used. Error: {str(e)}")
                _nlp = None
    return _nlp

def extract_contact_info(text: str) -> Dict[str, Any]:
    """
    Extract email, phone number, and professional links (LinkedIn, GitHub) from resume text.
    """
    contact_info = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "other_links": []
    }
    
    # 1. Email Regex
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        email = email_match.group(0)
        # Remove any leading 'envelope', 'email', 'mail' prefixes caused by layout extraction errors
        email = re.sub(r'^(?:envelope|email|mail|address)\s*[:\-\s]*', '', email, flags=re.IGNORECASE)
        contact_info["email"] = email
        
    # 2. Phone Regex (various formats: +1-234-567-8900, (123) 456-7890, 1234567890, etc.)
    # Standard Indian & US formats
    phone_pattern = r'(?:(?:\+|00)?[1-9]\d{0,3}[-.\s]?)?(?:\(?\d{2,5}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}(?:[-.\s]?\d{1,4})?'
    # We find all matches, but filter for valid lengths of numbers to avoid matching random years or ids
    phone_matches = re.findall(phone_pattern, text)
    for match in phone_matches:
        cleaned_num = re.sub(r'[-.\s\(\)\+]', '', match)
        # Typically phone numbers are between 8 and 14 digits
        if 8 <= len(cleaned_num) <= 15:
            contact_info["phone"] = match.strip()
            break
            
    # 3. Socials/Links Regex
    linkedin_match = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+/?', text, re.IGNORECASE)
    if linkedin_match:
        contact_info["linkedin"] = linkedin_match.group(0)
        
    github_match = re.search(r'(?:https?://)?(?:www\.)?github\.com/[\w\-]+/?', text, re.IGNORECASE)
    if github_match:
        contact_info["github"] = github_match.group(0)
        
    # Find all general links, exclude email matches, linkedin, and github
    all_links = re.findall(r'(?:https?://)?(?:www\.)?[\w\-]+\.[\w\-]{2,}(?:/[\w\-./?%&=]*)?', text, re.IGNORECASE)
    for link in all_links:
        link_lower = link.lower()
        if "linkedin.com" not in link_lower and "github.com" not in link_lower and "@" not in link_lower:
            # Simple heuristic to avoid matching email subsegments or random file paths
            if not link_lower.endswith(('.pdf', '.doc', '.docx', '.png', '.jpg')):
                contact_info["other_links"].append(link.strip())
                
    # Deduplicate other links
    contact_info["other_links"] = list(set(contact_info["other_links"]))[:3] # Limit to 3 other links
    
    return contact_info

def extract_candidate_name(text: str) -> str:
    """
    Attempt to extract the candidate's name from the top section of the resume.
    """
    nlp = get_spacy_nlp()
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "Candidate"
        
    # Try using NER on the first 5 lines
    if nlp:
        header_text = " ".join(lines[:5])
        doc = nlp(header_text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # Ensure the extracted name does not contain common keywords
                name = ent.text.strip()
                if len(name.split()) >= 2 and not any(kw in name.lower() for kw in ["resume", "curriculum", "vitae", "profile", "contact", "email", "phone"]):
                    return name
                    
    # Fallback heuristic: Check the first 2 lines for 2 or 3 capitalised words
    for line in lines[:3]:
        # Skip if line contains email, phone, or symbols
        if "@" in line or any(char.isdigit() for char in line) or ":" in line or len(line) > 30:
            continue
        words = line.split()
        if 2 <= len(words) <= 3:
            # Check if all words are capitalised
            if all(w[0].isupper() for w in words if w[0].isalpha()):
                return line
                
    return lines[0] # Return the first line if all heuristics fail

# Common english stopwords to use in case spaCy is not available
BASIC_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def clean_and_tokenize(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Preprocess, tokenize, lowercase, and optionally remove stopwords from text.
    """
    # Lowercase and clean characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#\-\.]', ' ', text) # Retain +, #, -, . for skills like C++, C#, CI/CD, .NET
    
    nlp = get_spacy_nlp()
    tokens = []
    
    if nlp:
        # Process text using spaCy (disable parser and NER for speed)
        doc = nlp(text, disable=["parser", "ner"])
        for token in doc:
            # Check for punctuation, whitespace, and optionally stopwords
            if token.is_punct or token.is_space:
                continue
            if remove_stopwords and token.is_stop:
                continue
            tokens.append(token.lemma_)
    else:
        # Fallback split-based cleaning
        raw_words = text.split()
        for w in raw_words:
            # Clean symbols at boundaries but keep internal (e.g. C++ or .net)
            w_cleaned = w.strip('.,:-()[]{}')
            if not w_cleaned:
                continue
            if remove_stopwords and w_cleaned in BASIC_STOPWORDS:
                continue
            tokens.append(w_cleaned)
            
    return tokens
