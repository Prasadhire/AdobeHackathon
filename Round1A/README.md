📘 Adobe PDF Parser - Round 1A Submission

This project is a solution for Adobe India Hackathon 2025 - Round 1A: Connecting the Dots Challenge.

It processes PDF files and extracts structured heading information including:

📌 Document Title

📌 Headings (H1, H2, H3)

📌 Page numbers

The output is saved in a clean JSON format for each PDF.

📂 Project Structure

├── input/                 # Input folder for PDFs (mounted into Docker)
├── output/                # Output folder for JSON files (mounted into Docker)
├── app/
│   ├── main.py            # Main script to extract headings
│   └── requirements.txt   # Python dependencies
├── Dockerfile             # Dockerfile for containerization
└── README.md              # This file

🛠️ Tech Stack

Python 3.10

PyMuPDF (fitz) for PDF parsing

Docker for packaging and portability

🚀 How to Run (Using Docker)

🧱 Step 1: Build Docker Image & Go to right directory of Round1A using "cd Round1A"

# In PowerShell (Windows):
docker build -t adobe-pdf-parser .

📂 Step 2: Place PDFs

Place all your .pdf files inside the input folder (same directory as this project).

▶️ Step 3: Run Parser

# Windows PowerShell

docker run --rm -v "${PWD}/input:/app/sample_pdfs" -v "${PWD}/output:/app/outputs" adobe-pdf-parser


✅ After running, JSON files will be saved inside the output folder.

🧠 How It Works

The script uses font sizes to estimate heading levels:

Largest font → Title

Next → H1

Then → H2

Then → H3

It loops through all pages and spans to extract these into structured JSON.

Example Output:

{
  "title": "Understanding AI",
  "outline": [
    {"level": "H1", "text": "What is AI?", "page": 1},
    {"level": "H2", "text": "Applications", "page": 2}
  ]
}

📌 Notes

Assumes that PDF headings follow a size hierarchy (larger fonts = higher level).

Ignores very short texts (less than 3 characters) to avoid noise.

🏁 Final Status

This project is Dockerized, fully aligned with the Adobe Round 1A prompt, and has been successfully tested.

✅ Ready for submission.

🙌 Made with effort by Team 🚀

Team Domintors