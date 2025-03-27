import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills_from_description(job_desc):
    skills = ["Python", "Machine Learning", "Data Analysis", "AI", "Deep Learning", "SQL", "Java", "Cloud Computing"]
    doc = nlp(job_desc)
    extracted_skills = set()
    for token in doc:
        if token.text.lower() in [skill.lower() for skill in skills]:
            extracted_skills.add(token.text)
    return list(extracted_skills)


# cover_letter_generator.py
from src.nlp_processing import extract_skills_from_description

def generate_cover_letter(job_title, company, job_desc):
    skills = extract_skills_from_description(job_desc)
    cover_letter = f"""
    Dear Hiring Manager,

    I am excited to apply for the {job_title} position at {company}. With a strong background in {', '.join(skills)}, 
    I am eager to contribute my expertise to your team.

    Job Description: {job_desc}

    I look forward to the opportunity to discuss my application.
    Thank you for your consideration.
    """
    return cover_letter