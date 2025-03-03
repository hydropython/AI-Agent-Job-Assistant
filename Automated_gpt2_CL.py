import logging
from transformers import pipeline

logging.basicConfig(level=logging.INFO)

# Initialize the text generation model
generator = pipeline("text-generation", model="gpt2")

def generate_cover_letter(job_title, company, job_desc, skills, max_new_tokens=300, temperature=0.7, top_p=0.9):
    """
    Generates a professional and personalized cover letter.
    """
    logging.info("Inside the generate_cover_letter function...")

    # Create a refined prompt with more context and a clean structure
    prompt = (
        f"Dear Hiring Manager,\n\n"
        f"I am excited to apply for the {job_title} position at {company}. With a strong background in "
        f"{', '.join(skills)}, I am eager to contribute my expertise to your team.\n\n"
        f"Job Description: {job_desc}\n\n"
        f"I believe my skills in {', '.join(skills)} make me an excellent fit for this role. I am particularly excited "
        f"about the opportunity to work with big data and apply machine learning techniques to drive business insights. "
        f"I look forward to the possibility of discussing how I can contribute to {company}.\n\n"
        f"Thank you for your consideration, and I am excited about the opportunity to further discuss my application."
    )

    logging.info(f"Prompt:\n{prompt}")

    try:
        response = generator(prompt, 
                             max_new_tokens=max_new_tokens, 
                             do_sample=True, 
                             temperature=temperature, 
                             top_p=top_p,
                             repetition_penalty=1.2)  # Reduces redundancy
        generated_text = response[0]['generated_text']
        logging.info("Generated text successfully.")
    except Exception as e:
        logging.error(f"Error generating text: {e}")
        return "Error generating cover letter."

    return generated_text

# Example usage
if __name__ == "__main__":
    cover_letter = generate_cover_letter(
        job_title="Data Scientist", 
        company="Google", 
        job_desc="We're looking for a skilled data scientist to work on big data analytics and machine learning algorithms.",
        skills=["Python", "Machine Learning", "Data Analysis"]
    )

    # Final print to see the generated cover letter
    print("\nGenerated Cover Letter:")
    print(cover_letter)