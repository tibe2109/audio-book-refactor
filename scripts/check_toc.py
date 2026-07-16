import fitz

pdf_path = '/mnt/d/Solution/Audio-Book-Refactor/Docs/Nghe-thuat-quyen-ru.pdf'
doc = fitz.open(pdf_path)
toc = doc.get_toc()
for t in toc:
    print(t)
