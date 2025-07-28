# 📘 Adobe PDF Intelligence - Round 1B Submission

This project is the official solution for **Adobe India Hackathon 2025 - Round 1B: Connecting the Dots Challenge**.

It processes multiple PDF documents and returns a ranked, structured JSON output based on a given persona and job-to-be-done. The tool is optimized for clarity, performance, and Docker-based execution.

---

## 📁 Project Structure

```
adobe-pdf-project/
└── 1B Round/
    ├── input/         # Place your PDF files here
    ├── persona.json   # Defines persona & job-to-be-done
    ├── output/        # Final output JSON saved here
    ├── main.py        # Main processing logic
    ├── utils.py       # Helper functions (scoring, parsing)
    ├── Dockerfile     # Docker container definition
    └── README.md      # You're reading it!
```

---

## 🧠 How It Works

1. Loads `persona.json` file, which should contain:
    ```json
    {
      "persona": "AI Researcher",
      "job_to_be_done": "Understand transformer architectures, attention mechanisms, and efficient model training techniques."
    }
    ```
2. Parses all PDFs in the `input/` folder, splits them into sections based on heading structure.
3. Applies NLP techniques (embedding, similarity scoring).
4. Ranks sections across PDFs and saves top matches to `output/` as structured JSON.

---

## ⚙️ Step-by-Step Execution (Docker)

### 1️⃣ Step 1: Move into the working directory

```powershell
cd "adobe-pdf-project\1B Round"
```

### 2️⃣ Step 2: Build the Docker Image

Make sure Docker Desktop is running.

```powershell
docker build -t adobe-pdf-ranker .
```

### 3️⃣ Step 3: Add Input Files

- Place your PDF files inside the `input/` folder.
- Create or modify `persona.json` in the same folder with the structure shown above.

### 4️⃣ Step 4: Run the Docker Container

```powershell
docker run --rm `
  -v "${PWD}/input:/app/input" `
  -v "${PWD}/output:/app/output" `
  -v "${PWD}/persona.json:/app/persona.json" `
  adobe-pdf-ranker
```

### 5️⃣ Step 5: View Results

- After execution, the ranked JSON output will be saved in the `output/` folder as `result.json`.

---

## 📝 Notes

- The system uses fast embedding and similarity scoring for accurate ranking.
- Handles large PDFs and multiple documents efficiently.
- Output includes PDF file name, page, heading, snippet, and similarity score.

---

## ✅ Ready for Evaluation

Made with focus and precision by Team 🚀 **Team Dominators**