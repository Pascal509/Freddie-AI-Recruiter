# Import required libraries
import openai 
import os
import re
from dotenv import load_dotenv

# Load environment variables from the .env file (specified as ".env.variables")
load_dotenv(".env.variables")

# Retrieve OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OpenAI API Key. Set it in the environment variable or .env.variables file.")

# Configure OpenAI API key for authentication
openai.api_key = OPENAI_API_KEY


def rank_candidate(name, resume_text, screening_answers):
    """
    Uses OpenAI's GPT model to evaluate and rank a candidate for a Marketing Officer role.

    Args:
        name (str): The candidate's full name.
        resume_text (str): Extracted text from the candidate's resume.
        screening_answers (str): Candidate's answers to screening questions.

    Returns:
        int: A ranking score between 0 and 100, where higher scores indicate a better fit.
    """

    # Construct a prompt for OpenAI GPT-4 to evaluate the candidate
    prompt = f"""
    Candidate Name: {name}
    Resume: {resume_text}
    Screening Answers: {screening_answers}

    Rate this candidate's fit for a marketing officer role on a scale of 0-100.
    Consider experience, skills, and cultural fit.
    Respond **only** with a number between 0 and 100.
    """

    try:
        # Send the prompt to OpenAI's GPT-4 model
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Use regex to extract the numeric score (0-100) from the response
        match = re.search(r"\b\d+\b", response_text)
        if match:
            return int(match.group(0))
        else:
            print(f"⚠️ Unexpected OpenAI response: {response_text}")
            return 0
        
     # Handle API errors
    except Exception as e:
        print(f"❌ OpenAI API error: {e}") 
        return 0