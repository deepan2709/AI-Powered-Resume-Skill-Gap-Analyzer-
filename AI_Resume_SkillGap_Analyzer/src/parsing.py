import re
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def text_from_file(file_path):
    """Read text content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_skills(text):
    """Extract skills from text using keyword matching and NLP."""
    # Common technical skills and keywords
    common_skills = {
        'python', 'java', 'javascript', 'c++', 'ruby', 'php', 'sql', 'nosql',
        'mongodb', 'postgresql', 'mysql', 'oracle', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'machine learning', 'deep learning', 'ai',
        'artificial intelligence', 'data science', 'data analysis',
        'statistics', 'mathematics', 'pytorch', 'tensorflow', 'keras',
        'scikit-learn', 'pandas', 'numpy', 'scipy', 'matplotlib',
        'data visualization', 'power bi', 'tableau', 'git', 'agile',
        'scrum', 'jira', 'confluence'
    }
    
    # Normalize text
    text = text.lower()
    
    # Extract skills using simple keyword matching
    found_skills = set()
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill)
    
    return list(found_skills)
