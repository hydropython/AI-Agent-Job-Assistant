import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

def generate_cover_letter(job_title, company, job_desc, skills, max_length=100, temperature=0.7, top_p=0.9):
    """
    Generates a professional and personalized cover letter using the Mistral-7B-Instruct-v0.1 model.
    """
    logging.info("Loading the Mistral-7B-Instruct-v0.1 model...")

    # Load the model and tokenizer from Hugging Face
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    try:
        start_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        loading_time = time.time() - start_time
        logging.info(f"Model loaded successfully in {loading_time:.2f} seconds.")
    except Exception as e:
        logging.error(f"Error loading the model: {e}")
        return "Error loading model"

    # Create a refined prompt
    prompt = (
        f"Dear Hiring Manager,\n\n"
        f"I am excited to apply for the {job_title} position at {company}. With a strong background in "
        f"{', '.join(skills)}, I am eager to contribute my expertise to your team.\n\n"
        f"Job Description: {job_desc}\n\n"
        f"Please craft a professional, structured, and compelling cover letter highlighting my qualifications.\n"
    )

    logging.info(f"Prompt:\n{prompt}")

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    logging.info("Prompt tokenized successfully.")

    # Generate text using the model
    try:
        generation_start_time = time.time()
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            pad_token_id=tokenizer.eos_token_id,
        )

        # Decode and return the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generation_time = time.time() - generation_start_time
        logging.info(f"Generated cover letter successfully in {generation_time:.2f} seconds.")
        logging.info(f"Generated text length: {len(generated_text)}")
    except Exception as e:
        logging.error(f"Error generating cover letter: {e}")
        return "Error generating cover letter."

    return generated_text

# Example usage
if __name__ == "__main__":
    logging.info("Starting cover letter generation...")
    cover_letter = generate_cover_letter(
        job_title="Data Scientist", 
        company="Google", 
        job_desc="We're looking for a skilled data scientist to work on big data analytics and machine learning algorithms.",
        skills=["Python", "Machine Learning", "Data Analysis"]
    )

    # Final print to see the generated cover letter
    logging.info("Cover letter generated:")
    print("\nGenerated Cover Letter:")
    print(cover_letter)