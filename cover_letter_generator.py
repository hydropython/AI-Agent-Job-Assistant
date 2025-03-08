import os
import PyPDF2
from docx import Document
from nlp_processing import extract_skills_from_description
from datetime import datetime

def generate_cover_letter(job_title, company, job_desc, cv_file):
    # Extract skills from job description
    skills = extract_skills_from_description(job_desc)
    
    # Extract relevant experience from CV
    experience = extract_experience_from_cv(cv_file)

    # Extract name and contact info from the CV
    name, contact_info = extract_name_and_contact_from_cv(cv_file)

    # Create the cover letter template
    cover_letter = f"""
    Dear Hiring Manager,

    I am excited to apply for the {job_title} position at {company}. With a strong background in {', '.join(skills)}, 
    I am eager to contribute my expertise to your team.

    Currently, I am a {experience}. I have successfully contributed to optimizing experimental workflows, improving predictive accuracy, and co-authoring research papers. Furthermore, I have disseminated AI/ML research publications to a community of over 200 data scientists, helping foster collaboration and drive advancements in the field.

    I am excited about the opportunity to apply my technical skills, analytical expertise, and academic background to the {job_title} role at {company}, where I can leverage my experience to help drive positive change in the advertising industry. The opportunity to work on flexible hours and contribute to a team that ensures responsible advertising resonates with my professional values and long-term career goals.

    I look forward to the opportunity to further discuss how my background and skills can contribute to the continued success of {company}. Thank you for your consideration.

    Sincerely,  
    {name}  
    {contact_info}
    """
    
    return cover_letter

# Helper functions for extracting information from CV (if necessary)
def extract_experience_from_cv(cv_file):
    """
    Extracts relevant experience and skills from the uploaded CV.
    This function works for both PDF and DOCX files.
    """
    experience = ""

    # If the CV is a PDF
    if cv_file.name.lower().endswith('.pdf'):
        reader = PyPDF2.PdfReader(cv_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        experience = extract_experience_from_text(text)

    # If the CV is a DOCX
    elif cv_file.name.lower().endswith('.docx'):
        doc = Document(cv_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        experience = extract_experience_from_text(text)

    return experience


def extract_experience_from_text(text):
    """
    Processes the raw text from the CV to extract experience and responsibilities.
    """
    # Simple processing to find sections related to experience
    experience_section = ""
    experience_keywords = ['experience', 'work', 'role', 'responsibilities']

    for line in text.split('\n'):
        for keyword in experience_keywords:
            if keyword in line.lower():
                experience_section += line.strip() + "\n"
                break

    return experience_section


def extract_name_and_contact_from_cv(cv_file):
    """
    Extracts name and contact information from the CV (works for both PDF and DOCX files).
    This assumes the name is at the top and contact information follows.
    """
    name = ""
    contact_info = ""

    # If the CV is a PDF
    if cv_file.name.lower().endswith('.pdf'):
        reader = PyPDF2.PdfReader(cv_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        name, contact_info = extract_name_and_contact_from_text(text)

    # If the CV is a DOCX
    elif cv_file.name.lower().endswith('.docx'):
        doc = Document(cv_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        name, contact_info = extract_name_and_contact_from_text(text)

    return name, contact_info


def extract_name_and_contact_from_text(text):
    """
    Processes the raw text from the CV to extract name and contact information.
    Assumes name is the first line and contact info follows.
    """
    lines = text.split("\n")
    
    # Assuming the first line is the name and second line contains contact information
    name = lines[0] if len(lines) > 0 else "Your Full Name"
    contact_info = lines[1] if len(lines) > 1 else "Your Contact Information"
    
    return name, contact_info


# Save the CV and Cover Letter to Files
def save_to_files(cv_file, cover_letter, name):
    # Define directory to store files
    output_dir = "generated_documents"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the file names based on the user's name
    cover_letter_filename = f"Cover_letter_{name}.txt"
    cv_filename = f"CV_{name}.txt"
    
    # Save Cover Letter to file
    with open(os.path.join(output_dir, cover_letter_filename), "w") as f:
        f.write(cover_letter)
    
    # Save CV to file (assuming CV is text extracted from the PDF or DOCX)
    with open(os.path.join(output_dir, cv_filename), "w") as f:
        f.write("CV content goes here...")  # You could extract the content from the CV file (e.g., from text)

    print(f"Cover letter saved as {cover_letter_filename}")
    print(f"CV saved as {cv_filename}")

    return os.path.join(output_dir, cover_letter_filename), os.path.join(output_dir, cv_filename)


def main():
    # Define job details and CV path
    job_title = "Data Scientist"
    company = "Tech Company"
    job_desc = "We are looking for a Data Scientist with strong skills in machine learning and data analysis."
    cv_path = 'path_to_cv.pdf'  # Replace with actual CV path
    
    # Simulating opening the CV file
    with open(cv_path, "rb") as cv_file:
        # Generate Cover Letter
        cover_letter = generate_cover_letter(job_title, company, job_desc, cv_file)

        # Extract name from the CV for filename purposes
        name, contact_info = extract_name_and_contact_from_cv(cv_file)

        # Save the Cover Letter and CV to files
        cover_letter_filename, cv_filename = save_to_files(cv_file, cover_letter, name)

        print(f"Cover letter and CV saved successfully.")

if __name__ == "__main__":
    main()

