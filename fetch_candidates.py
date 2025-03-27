# Import necessary libraries
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets document ID
SHEET_ID = "1TPntAcoFPZVCFp-4kYgnqcaWGn5BGeuadU0okc6yWvs"

def fetch_candidates(sheet_id=SHEET_ID):
    """
    Fetches candidate data from a Google Sheets document.

    Args:
        sheet_id (str): The ID of the Google Sheets document (default: SHEET_ID).

    Returns:
        list: A list of dictionaries containing candidate data, or an empty list on error.
    """
    try:
        # Authenticate using the service account credentials
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        # Connect to Google Sheets
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1  # Access the first sheet

        # Fetch all records as a list of dictionaries
        return sheet.get_all_records()
    
    except Exception as e:
        print(f"❌ Error fetching candidates: {e}") 
        return []
