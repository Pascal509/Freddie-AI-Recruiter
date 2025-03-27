# Import necessary libraries
import gspread  
from google.oauth2.service_account import Credentials

# Google Sheet ID where results will be stored
RESULT_SHEET_ID = "1Wc_VaZiQDVn0gkMp3O1ST5qvVqSA2kNuCaE_IPPf984"


def store_results(candidate_scores):
    """
    Stores candidate ranking results in a Google Sheet.

    Args:
        candidate_scores (list): A list of dictionaries containing candidate details:
            - "name" (str): Candidate's name
            - "score" (int): Candidate's ranking score
            - "email" (str): Candidate's email address

    Returns:
        None
    """
    try:
        # Authenticate with Google Sheets using service account credentials
        creds = Credentials.from_service_account_file(
            "credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(creds)

        # Open the Google Sheet
        sheet = client.open_by_key(RESULT_SHEET_ID).sheet1

        # Ensure headers exist in the first row
        if not sheet.row_values(1):  # Check if the first row is empty
            sheet.append_row(["Name", "Score", "Email"])  # Add column headers

        # Retrieve existing records (avoid duplicate entries)
        existing_records = {row[0]: row for row in sheet.get_all_values()[1:]}  # Store existing names

        # Append new candidates who are not already in the sheet
        for candidate in candidate_scores:
            if candidate["name"] not in existing_records:
                sheet.append_row([candidate["name"], candidate["score"], candidate["email"]])

    except Exception as e:
        print(f"❌ Error storing results: {e}")  # Handle errors gracefully
