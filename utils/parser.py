import pdfplumber
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_input) -> str:
    """
    Extract text content from an uploaded PDF file or a file path.
    
    Args:
        file_input: Can be a file path (str) or a file-like object (e.g., BytesIO from streamlit file_uploader).
        
    Returns:
        str: Extracted raw text from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(file_input) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text(layout=False)
                if page_text:
                    text += page_text + "\n"
        
        # Clean up any potential formatting issues or corrupted characters
        text = clean_extracted_text(text)
        return text
    except Exception as e:
        logger.error(f"Error during PDF text extraction: {str(e)}")
        raise ValueError(f"Could not parse the PDF file. Please ensure it is a valid, unencrypted PDF. Error: {str(e)}")

def clean_extracted_text(text: str) -> str:
    """
    Apply standard cleaning to the extracted raw PDF text.
    
    Args:
        text (str): Raw text content.
        
    Returns:
        str: Cleaned text content.
    """
    if not text:
        return ""
    
    # 1. Normalize line endings and remove weird control characters
    text = text.replace('\r', '\n')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    
    # 2. Fix ligature characters common in PDFs (e.g., 'fi', 'fl', 'ffi', etc.)
    ligatures = {
        'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl',
        'ﬆ': 'st', 'Œ': 'OE', 'œ': 'oe', 'Æ': 'AE', 'æ': 'ae'
    }
    for ligature, replacement in ligatures.items():
        text = text.replace(ligature, replacement)
        
    # 3. Standardize multiple consecutive spaces to a single space, but preserve single newlines
    lines = []
    for line in text.split('\n'):
        # Strip trailing/leading spaces and replace multi-spaces with single space
        line = re.sub(r'\s+', ' ', line).strip()
        if line:
            lines.append(line)
            
    return '\n'.join(lines)

def parse_pdf_with_metadata(file_input) -> dict:
    """
    Extract text and count pages from a PDF.
    
    Args:
        file_input: Can be a file path or file-like object.
        
    Returns:
        dict: Containing 'text' (cleaned text) and 'page_count' (int).
    """
    text = ""
    pages_count = 0
    try:
        with pdfplumber.open(file_input) as pdf:
            pages_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text(layout=False)
                if page_text:
                    text += page_text + "\n"
        text = clean_extracted_text(text)
        return {
            "text": text,
            "page_count": pages_count
        }
    except Exception as e:
        logger.error(f"Error parsing PDF with metadata: {str(e)}")
        raise ValueError(f"Could not parse the PDF file. Error: {str(e)}")

