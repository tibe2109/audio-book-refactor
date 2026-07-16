import fitz
import sys

def extract_pdf(pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted {len(doc)} pages to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <input.pdf> <output.txt>")
    else:
        extract_pdf(sys.argv[1], sys.argv[2])
