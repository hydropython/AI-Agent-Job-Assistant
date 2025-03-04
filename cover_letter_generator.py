from nlp_processing import extract_skills_from_description

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