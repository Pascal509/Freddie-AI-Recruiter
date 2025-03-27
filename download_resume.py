# Import necessary libraries
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import io 
from googleapiclient.http import MediaIoBaseDownload

# Define the required Google Drive API scope (read-only access)
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Path to the Google service account credentials file
SERVICE_ACCOUNT_FILE = "credentials.json"

def download_resume(drive_link):
    """
    Downloads a resume from Google Drive if it hasn't been downloaded already.
    
    Args:
        drive_link (str): The Google Drive link to the resume.
    
    Returns:
        str: The local file path where the resume is saved, or None if an error occurs.
    """

    # Authenticate with Google Drive using service account credentials
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    # Initialize the Google Drive API client
    drive_service = build("drive", "v3", credentials=creds)

    # Extract the file ID from the Google Drive link
    try:
        file_id = drive_link.split("/d/")[1].split("/")[0] 
    except IndexError:
        print(f"⚠️ Invalid Google Drive link: {drive_link}")
        return None

    # Retrieve the file's metadata to get the original filename
    try:
        file_metadata = drive_service.files().get(fileId=file_id).execute()
        filename = file_metadata["name"] 
    except Exception as e:
        print(f"❌ Error fetching file metadata: {e}")
        return None

    # Ensure the "resumes" directory exists to store downloaded files
    os.makedirs("resumes", exist_ok=True)

    # Define the local path where the resume will be saved
    file_path = os.path.join("resumes", filename)

    # Check if the resume has already been downloaded to avoid duplicate downloads
    if os.path.exists(file_path):
        print(f"⚠️ Resume already downloaded: {filename}") 
        return file_path

    # Download the file from Google Drive
    try:
        # Request to download the file
        request = drive_service.files().get_media(fileId=file_id)

        # Open the local file in binary write mode to store the downloaded content
        with open(file_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            
            # Download pdfs in chunks
            while not done:
                status, done = downloader.next_chunk()
                print(f"📥 Download {int(status.progress() * 100)}% complete")  # Show download progress
        
        return file_path
    
    except Exception as e:
        print(f"❌ Failed to download {drive_link}: {e}")
        return None
