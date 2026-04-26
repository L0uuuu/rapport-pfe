import fitz  # PyMuPDF

def extract_text(pdf_path, output_path="output.txt"):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Text saved to {output_path}")

if __name__ == "__main__":
    import sys
    pdf = sys.argv[1] if len(sys.argv) > 1 else "input.pdf"
    out = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    extract_text(pdf, out)