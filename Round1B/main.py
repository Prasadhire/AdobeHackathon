import os
import fitz  # PyMuPDF
import re
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdfs(input_dir):
    pdfs = {}
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            path = os.path.join(input_dir, file)
            try:
                pdfs[file] = fitz.open(path)
            except Exception as e:
                print(f"⚠️ Failed to open {file}: {e}")
    return pdfs

def extract_sections(pdfs):
    section_list = []
    for filename, doc in pdfs.items():
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        text = " ".join([span["text"] for span in line["spans"]]).strip()
                        if is_potential_heading(text):
                            section_text = extract_section_text(doc, page_num)
                            if len(section_text.strip()) > 20:
                                section_list.append({
                                    "document": filename,
                                    "page_number": page_num,
                                    "section_title": text,
                                    "section_text": section_text
                                })
    return section_list

def is_potential_heading(text):
    return (
        5 < len(text) < 100 and
        text.isprintable() and
        text[0].isupper() and
        not re.match(r"^\d+$", text.strip()) and
        not text.lower().endswith(".pdf")
    )

def extract_section_text(doc, start_page):
    collected_text = ""
    for i in range(start_page - 1, min(start_page + 1, len(doc))):
        try:
            page = doc[i]
            text = page.get_text()
            collected_text += text + "\n"
        except Exception as e:
            print(f"⚠️ Error extracting text from page {i+1}: {e}")
    return collected_text.strip()

def compute_similarity(sections, query):
    try:
        section_texts = [s["section_text"] for s in sections]
        section_embeddings = model.encode(section_texts)
        query_embedding = model.encode([query])

        sims = cosine_similarity(query_embedding, section_embeddings)[0]
        for i, score in enumerate(sims):
            sections[i]["similarity"] = float(score)

        ranked = sorted(sections, key=lambda x: x["similarity"], reverse=True)
        for i, sec in enumerate(ranked, start=1):
            sec["importance_rank"] = i
        return ranked[:5]
    except Exception as e:
        print(f"❌ Error in similarity computation: {e}")
        return []

def generate_output(ranked_sections, persona, job):
    timestamp = datetime.utcnow().isoformat() + "Z"

    return {
        "metadata": {
            "documents": list({s["document"] for s in ranked_sections}),
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": timestamp
        },
        "extracted_sections": [
            {
                "document": s["document"],
                "page_number": s["page_number"],
                "section_title": s["section_title"],
                "importance_rank": s["importance_rank"]
            }
            for s in ranked_sections
        ],
        "subsection_analysis": [
            {
                "document": s["document"],
                "page_number": s["page_number"],
                "refined_text": s["section_text"]
            }
            for s in ranked_sections
        ]
    }
