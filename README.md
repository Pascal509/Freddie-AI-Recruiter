# **Freddie AI Recruiter**
An automated AI-powered recruitment system that fetches candidate data, downloads resumes, ranks candidates using OpenAI, stores results, and sends emails to selected candidates.

---

## **Table of Contents**
- [Overview](#overview)  
- [Features](#features)  
- [Project Architecture](#project-architecture)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [File Structure](#file-structure)  
- [API Endpoints](#api-endpoints)  
- [Technologies Used](#technologies-used)  
- [Contributing](#contributing)  
- [License](#license)  

---

## **Overview**
The **Freddie AI Recruiter** automates the candidate screening process by:  
✅ Fetching candidate details from Google Sheets.  
✅ Downloading resumes from Google Drive.  
✅ Extracting text from resumes using PDF parsing.  
✅ Ranking candidates based on AI evaluation (GPT-4 Turbo).  
✅ Storing ranked results in a Google Sheet.  
✅ Sending emails to shortlisted candidates.  

---

## **Features**
✔️ Fetches candidates from a Google Sheet.  
✔️ Downloads resumes from Google Drive.  
✔️ Extracts text from PDFs.  
✔️ Uses AI to rank candidates based on resumes & answers.  
✔️ Stores results in Google Sheets.  
✔️ Sends emails to qualified candidates.  
✔️ Exposes an API to retrieve candidate rankings.  

---

## **Project Architecture**

```
Freddie AI Recruiter
│── main.py                 # Main Flask API
│── fetch_candidates.py      # Fetches candidates from Google Sheets
│── download_resume.py       # Downloads resumes from Google Drive
│── rank_candidates.py       # Uses OpenAI to rank candidates
│── store_results.py         # Stores results in Google Sheets
│── send_email.py            # Sends emails to shortlisted candidates
│── requirements.txt         # Python dependencies
│── .env.variables           # Environment variables (API keys, credentials)
│── credentials.json         # Google API service account credentials
│── README.md                # Project documentation
```

---

## **Installation**

### **1️ Clone the Repository**  
```bash
git clone https://github.com/yourusername/freddie-ai-recruiter.git
cd freddie-ai-recruiter
```

### **2️ Create a Virtual Environment (Optional but Recommended)**  
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scriptsctivate     # On Windows
```

### **3️ Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## **Configuration**

1 **Set Up Google API Credentials**  
- Generate a service account key (`credentials.json`) from Google Cloud Console.  
- Enable **Google Sheets API** and **Google Drive API**.  

2 **Set Up `.env.variables`**  
Create a `.env.variables` file with the following:  
```env
OPENAI_API_KEY=your-openai-api-key
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password
```

3 **Update Google Sheet & Drive Links**  
Modify `fetch_candidates.py` and `store_results.py` with **your Google Sheet ID**.  

---

## **Usage**

### **Run the Flask API**  
```bash
python main.py
```

### **Process Candidates Manually**  
If needed, run the ranking and email-sending process separately:  
```bash
python -c "import main; main.process_candidates()"
```

---

## **API Endpoints**

| Endpoint        | Method | Description |
|---------------|--------|-------------|
| `/`           | GET    | Check if API is running. |
| `/rankings`   | GET    | Retrieve ranked candidates. |

---

## **Technologies Used**
- **Backend:** Flask (Python)  
- **Data Storage:** Google Sheets (gspread)  
- **Resume Handling:** PyMuPDF (fitz)  
- **AI Ranking:** OpenAI GPT-4 Turbo  
- **Emailing:** SMTP (smtplib)  
- **Google API:** Google Drive & Google Sheets API  

---

## **Contributing**
1️⃣ Fork the repository.  
2️⃣ Create a new branch: `git checkout -b feature-branch`.  
3️⃣ Make changes & commit: `git commit -m "Your message"`.  
4️⃣ Push changes: `git push origin feature-branch`.  
5️⃣ Open a Pull Request.  

---

## **License**  
This project is licensed under the **MIT License**.  

---
**Happy Coding!** 
