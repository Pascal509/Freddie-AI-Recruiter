# Import necessary libraries
from flask import Flask, jsonify
from fetch_candidates import fetch_candidates
from download_resume import download_resume
from rank_candidates import rank_candidate
from store_results import store_results
from send_email import send_email
import fitz
import threading

# Initialize Flask application
app = Flask(__name__)

# Global variable to store ranked candidates
ranked_candidates = []  

def extract_text_from_pdf(pdf_path):
    """
    Extracts text content from a given PDF resume.

    Args:
        pdf_path (str): The file path to the candidate's resume.

    Returns:
        str: The extracted text from the PDF, or an empty string if an error occurs.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text("text") + "\n" for page in doc)
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""


def process_candidates():
    """
    Fetches candidate data, processes their resumes, ranks them using AI,
    stores the results, and sends emails to qualified candidates.
    """
    global ranked_candidates

    print("🚀 Fetching candidates...")
    candidates = fetch_candidates()
    ranked_candidates = []

    # Iterate through each candidate
    for candidate in candidates:
        print(f"📄 Processing: {candidate.get('Full Name', 'Unknown')}")

        # Extract candidate details
        name = candidate.get("Full Name", "Unknown")
        email = candidate.get("Email", "Unknown")
        screening_answers = candidate.get("Screening Answers", "")
        resume_link = candidate.get("Resume Link", "")

        # Download Resume from Google Drive
        resume_path = download_resume(resume_link)
        resume_text = extract_text_from_pdf(resume_path) if resume_path else ""

        # Rank the candidate using AI (OpenAI GPT)
        score = rank_candidate(name, resume_text, screening_answers)

        # Store ranked candidate information
        ranked_candidates.append({"name": name, "score": score, "email": email})

    print("📊 Storing results...")
    store_results(ranked_candidates)  # Save results to storage

    # Send interview emails to candidates scoring 70 or above
    for candidate in ranked_candidates:
        if candidate["score"] >= 70:
            print(f"✉️ Sending email to {candidate['name']}...")
            send_email(candidate["email"], candidate["name"])

    print("✅ Process Completed!")


@app.route("/", methods=["GET"])
def home():
    """
    API root endpoint.

    Returns:
        JSON: Message confirming that the API is running.
    """
    return jsonify({"message": "Freddie AI Recruiter API is running!"})


@app.route("/rankings", methods=["GET"])
def get_rankings():
    """
    API endpoint to retrieve ranked candidates.

    Returns:
        JSON: A list of ranked candidates with their scores.
    """
    return jsonify({"rankings": ranked_candidates})


if __name__ == "__main__":
    # Run `process_candidates` in a background thread to prevent blocking Flask
    threading.Thread(target=process_candidates).start()

    # Start Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)
