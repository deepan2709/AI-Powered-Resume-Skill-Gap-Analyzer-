# app.py
import streamlit as st
import pandas as pd
from src.parsing import extract_skills
from src.matching import compare_skills
from PyPDF2 import PdfReader  # for PDF text extraction

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
st.title("🤖 AI Resume & Skill Gap Analyzer (PDF Version)")

# --- Upload PDF Resume ---
uploaded = st.file_uploader("Upload resume (PDF)", type=["pdf"])

# --- Target Role Input ---
role = st.text_input("Target role (e.g. Data Scientist)", value="Data Scientist")

# --- Role-to-Skills Mapping ---
ROLE_SKILLS = {
    "data scientist": ["python", "sql", "machine learning", "statistics", "pandas", "data visualization"],
    "ml engineer": ["python", "pytorch", "tensorflow", "docker", "kubernetes", "aws"],
    "data analyst": ["excel", "sql", "power bi", "tableau", "python", "statistics"]
}

# --- Resume Processing ---
if uploaded is not None:
    with st.spinner("Extracting text from PDF..."):
        pdf_reader = PdfReader(uploaded)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text() or ""

    if not content.strip():
        st.error("❌ Could not extract text from PDF. Please upload a text-based resume (not scanned).")
        st.stop()

    # --- Extract Skills from Resume Text ---
    with st.spinner("Analyzing resume skills..."):
        candidate_skills = extract_skills(content)
        
    # Display found skills
    st.subheader("📋 Skills Found in Resume")
    if candidate_skills:
        st.write(", ".join(candidate_skills))
    else:
        st.warning("No relevant skills were detected in the resume.")

    # Compare with role requirements
    role_key = role.lower()
    role_skills = ROLE_SKILLS.get(role_key, [])
    
    if not role_skills:
        st.error(f"❌ Role '{role}' not found in our database. Please choose from: {', '.join(ROLE_SKILLS.keys())}")
        st.stop()
        
    result = compare_skills(candidate_skills, role_skills)
    
    # Display results
    st.subheader(f"🎯 Role Analysis: {role}")
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Match Score", f"{result['score']}%")
    with col2:
        matched_count = len(result['matched'])
        st.metric("Skills Matched", f"{matched_count}")
    with col3:
        missing_count = len(result['missing'])
        st.metric("Skills to Develop", f"{missing_count}")

    # Detailed breakdown
    st.subheader("✅ Matched Skills")
    if result["matched"]:
        st.write(", ".join(result["matched"]))
    else:
        st.write("No direct skill matches found.")

    st.subheader("🎯 Skills to Develop")
    if result["missing"]:
        for skill in result["missing"]:
            st.write(f"- {skill}")
    else:
        st.write("You have all the required skills for this role!")

    # Recommendations section
    if result["missing"]:
        st.subheader("📚 Learning Recommendations")
        st.write("To improve your profile, consider these learning resources:")
        for skill in result["missing"]:
            with st.expander(f"Learn {skill}"):
                st.write(f"""
                ### Resources to learn {skill}:
                1. Online Courses:
                   - Search on Coursera for "{skill} certification"
                   - Check Udemy for "{skill} for beginners"
                   - Look up LinkedIn Learning "{skill} essential training"
                
                2. Practice Projects:
                   - Create a portfolio project using {skill}
                   - Contribute to open source projects using {skill}
                   
                3. Communities:
                   - Join {skill}-related Discord servers
                   - Participate in {skill} discussions on Stack Overflow
                """)
