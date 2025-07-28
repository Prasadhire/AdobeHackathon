import fitz  # PyMuPDF
import os
import json

INPUT_FOLDER = "sample_pdfs"
OUTPUT_FOLDER = "outputs"

def get_heading_structure(pdf_path):
    doc = fitz.open(pdf_path)
    all_spans = []

    # Collect spans from all pages in a single pass
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if len(text) < 3 or not text.isprintable():
                            continue

                        span_data = {
                            "text": text,
                            "size": round(span["size"], 2),
                            "flags": span["flags"],
                            "font": span["font"],
                            "x": span["bbox"][0],
                            "y": span["bbox"][1],
                            "page": page_num + 1,
                            "is_bold": bool(span["flags"] & 2)
                        }
                        all_spans.append(span_data)

    # Get top unique font sizes
    sizes = sorted(list(set([s["size"] for s in all_spans])), reverse=True)
    size_to_level = {}
    for i, size in enumerate(sizes):
        if i == 0:
            size_to_level[size] = "Title"
        elif i == 1:
            size_to_level[size] = "H1"
        elif i == 2:
            size_to_level[size] = "H2"
        else:
            size_to_level[size] = "H3"

    title = None
    headings = []

    for span in all_spans:
        level = size_to_level.get(span["size"])
        if not level:
            continue

        if level == "Title" and not title:
            # Extra check: likely title is at top 25% of first page
            if span["page"] == 1 and span["y"] < 200:
                title = span["text"]
        elif level in ["H1", "H2", "H3"]:
            headings.append({
                "level": level,
                "text": span["text"],
                "page": span["page"]
            })

    # Sort by page then vertical position
    headings = sorted(headings, key=lambda h: (h["page"], next(
        (s["y"] for s in all_spans if s["text"] == h["text"] and s["page"] == h["page"]), 0)))

    return {
        "title": title or "Untitled Document",
        "outline": headings
    }

def main():
    print("🚀 Starting PDF parsing...")
    print("📂 Checking folder:", INPUT_FOLDER)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            print(f"📄 Processing: {filename}")
            filepath = os.path.join(INPUT_FOLDER, filename)
            try:
                result = get_heading_structure(filepath)
                outname = filename.rsplit(".", 1)[0] + ".json"
                outpath = os.path.join(OUTPUT_FOLDER, outname)
                with open(outpath, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2)
                print(f"✅ Saved: {outname}")
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
