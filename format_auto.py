"""
Bước 4+5 (v2 - Fixed): Dịch thuật + Format TTS chuẩn
- Chunk nhỏ hơn (max 2500 ký tự) để tránh lỗi API
- Cắt chunk thông minh tại ranh giới câu/đoạn
- Retry khi gặp lỗi
"""
import os
import re
import time
from deep_translator import GoogleTranslator
from num2words import num2words

BASE_DIR = r"D:\Solution\Audio-Book-Refactor\Kich-ban-clipchamp\Eat-that-frog"
MAX_CHUNK = 2500       # Giảm xuống 2500 để an toàn
TRANSLATE_DELAY = 1.5  # Delay giữa các lần gọi API
MAX_RETRIES = 3

# ==================== PHIÊN ÂM ====================
PHONETIC_MAP = {
    "Brian Tracy": "Brai-ân Tờ-rây-xi",
    "Napoleon Hill": "Na-pô-lê-ông Hil",
    "Napoleon": "Na-pô-lê-ông",
    "Abraham Lincoln": "Ây-bờ-ra-ham Lin-côn",
    "Abraham": "Ây-bờ-ra-ham",
    "Pareto": "Pa-rê-tô",
    "Vilfredo Pareto": "Vin-frê-đô Pa-rê-tô",
    "Peter Drucker": "Pi-tờ Đrắc-kờ",
    "Henry Ford": "Hen-ri Pho",
    "Thomas Edison": "Thô-mớt Ê-đi-xơn",
    "Mark Twain": "Mác Tuên",
    "Elbert Hubbard": "En-bợt Hắb-bợt",
    "Johann Wolfgang von Goethe": "Giô-han Vôn-gang phôn Gơ-tờ",
    "Goethe": "Gơ-tờ",
    "Alan Lakein": "Ây-lần Lê-kain",
    "Warren Buffett": "Wo-rần Bắp-phít",
    "Michael Jordan": "Mai-cồ Gióc-đan",
    "Stephen Covey": "Sti-vần Cô-vi",
    "ABCDE": "A B C D E",
}


# ==================== HELPER FUNCTIONS ====================
def replace_number(match):
    num_str = match.group()
    try:
        n = int(num_str)
        if n > 1_000_000_000:
            return num_str
        return num2words(n, lang='vi')
    except Exception:
        return num_str


def apply_phonetics(text):
    for eng, vi in sorted(PHONETIC_MAP.items(), key=lambda x: -len(x[0])):
        text = re.sub(r'\b' + re.escape(eng) + r'\b', vi, text, flags=re.IGNORECASE)
    return text


def split_into_chunks(text, max_size=MAX_CHUNK):
    """
    Chia text thành các chunk <= max_size ký tự.
    Ưu tiên cắt tại: đoạn văn (\\n\\n) > câu (.) > từ ( )
    """
    if len(text) <= max_size:
        return [text]

    chunks = []
    paragraphs = text.split('\n\n')
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Nếu đoạn này + current không vượt max
        if len(current) + len(para) + 2 <= max_size:
            current += para + '\n\n'
        else:
            # Lưu current trước nếu có
            if current.strip():
                chunks.append(current.strip())
                current = ""

            # Nếu 1 đoạn đơn đã > max_size → cắt theo câu
            if len(para) > max_size:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                sent_chunk = ""
                for sent in sentences:
                    if len(sent_chunk) + len(sent) + 1 <= max_size:
                        sent_chunk += sent + ' '
                    else:
                        if sent_chunk.strip():
                            chunks.append(sent_chunk.strip())
                        sent_chunk = sent + ' '
                if sent_chunk.strip():
                    chunks.append(sent_chunk.strip())
            else:
                current = para + '\n\n'

    if current.strip():
        chunks.append(current.strip())

    return [c for c in chunks if c.strip()]


def translate_chunk_safe(text, src='en', dest='vi'):
    """Dịch 1 chunk với retry."""
    for attempt in range(MAX_RETRIES):
        try:
            result = GoogleTranslator(source=src, target=dest).translate(text)
            return result
        except Exception as e:
            err_msg = str(e)
            if attempt < MAX_RETRIES - 1:
                print(f"    ⚠️  Retry {attempt+1}/{MAX_RETRIES}: {err_msg[:60]}")
                time.sleep(3 * (attempt + 1))
            else:
                print(f"    ❌ Bỏ qua chunk sau {MAX_RETRIES} lần thử: {err_msg[:60]}")
                return text  # Fallback: giữ nguyên
    return text


def translate_text(text):
    """Dịch toàn bộ text, chia nhỏ nếu cần."""
    if not text.strip():
        return ""

    chunks = split_into_chunks(text, MAX_CHUNK)
    print(f"    → Chia thành {len(chunks)} chunk(s)", end="", flush=True)

    translated_parts = []
    for i, chunk in enumerate(chunks):
        result = translate_chunk_safe(chunk)
        translated_parts.append(result)
        print(".", end="", flush=True)
        if i < len(chunks) - 1:
            time.sleep(TRANSLATE_DELAY)

    print()  # newline
    return '\n\n'.join(translated_parts)


# ==================== GOLDEN RULES (Bước 5) ====================
def apply_golden_rules(text):
    """Format TTS chuẩn theo quy tắc vàng."""
    # 1. Xóa dấu ngoặc kép
    text = text.replace('\u201c', '').replace('\u201d', '').replace('"', '').replace('"', '').replace("'", '')

    # 2. Thay thế ký tự đặc biệt bằng dấu phẩy
    text = re.sub(r'[\(\)\-\u2014\u2013:;]', ', ', text)

    # 3. Xóa ký tự lạ
    text = re.sub(r'[*#@~`^|\\<>{}]', '', text)
    text = re.sub(r'\.{2,}', '', text)

    # 4. Phiên âm tên nước ngoài
    text = apply_phonetics(text)

    # 5. Chuyển số thành chữ tiếng Việt
    text = re.sub(r'\b\d+\b', replace_number, text)

    # 6. Dọn dấu phẩy thừa
    text = re.sub(r',\s*,+', ',', text)
    text = re.sub(r',\s*\.', '.', text)

    # 7. Chuẩn hóa khoảng trắng
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 8. Thêm ngắt nghỉ `. ......` cuối mỗi đoạn
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    formatted = []
    for para in paragraphs:
        lines = [l.strip() for l in para.split('\n') if l.strip()]
        if not lines:
            continue

        if len(lines) == 1 and len(lines[0]) < 120:
            # Có thể là tiêu đề hoặc câu ngắn
            line = lines[0]
            if not re.search(r'[.?!,]$', line):
                line += '. ......'
            else:
                line += ' ......'
            formatted.append(line)
        else:
            # Đoạn văn thông thường
            joined = ' '.join(lines)
            if not re.search(r'[.?!]$', joined):
                joined += '.'
            joined += ' ......'
            formatted.append(joined)

    return '\n\n'.join(formatted)


# ==================== PROCESS CHAPTER ====================
def process_chapter(chapter_dir):
    chapter_name = os.path.basename(chapter_dir)
    raw_path = os.path.join(chapter_dir, "raw_original.txt")
    translated_path = os.path.join(chapter_dir, "translated.txt")
    output_path = os.path.join(chapter_dir, "Kich-ban-1.txt")

    if not os.path.exists(raw_path):
        print(f"  ⚠️  Không có raw_original.txt: {chapter_name}")
        return

    if os.path.exists(output_path):
        print(f"  ⏭️  Đã có Kich-ban-1.txt: {chapter_name}")
        return

    print(f"\n{'─'*55}")
    print(f"📖 {chapter_name}")

    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    if not raw_text.strip():
        print(f"  ⚠️  File trống, bỏ qua.")
        return

    # --- Bước 4: Dịch thuật ---
    if os.path.exists(translated_path):
        print(f"  ✓ Đọc lại bản dịch đã có...")
        with open(translated_path, 'r', encoding='utf-8') as f:
            translated = f.read()
    else:
        print(f"  🌐 Dịch EN→VI ({len(raw_text):,} ký tự)...")
        translated = translate_text(raw_text)
        with open(translated_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        print(f"  ✓ Dịch xong ({len(translated):,} ký tự)")

    # Kiểm tra nếu bản dịch vẫn là tiếng Anh (heuristic: < 5% ký tự tiếng Việt)
    vi_chars = len(re.findall(r'[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]', translated, re.IGNORECASE))
    if vi_chars < 10 and len(translated) > 200:
        print(f"  ⚠️  Bản dịch có vẻ vẫn là tiếng Anh! ({vi_chars} ký tự VI). Kiểm tra lại.")

    # --- Bước 5: Format TTS ---
    print(f"  ⚙️  Format TTS...")
    formatted = apply_golden_rules(translated)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted)

    print(f"  ✅ Kich-ban-1.txt ({len(formatted):,} ký tự)")


# ==================== MAIN ====================
def main():
    print("=" * 55)
    print("BƯỚC 4+5 (v2): Dịch thuật + Format TTS")
    print("=" * 55)

    chapter_dirs = sorted([
        os.path.join(BASE_DIR, d)
        for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ])

    print(f"Tìm thấy {len(chapter_dirs)} chương cần xử lý.\n")

    for chapter_dir in chapter_dirs:
        process_chapter(chapter_dir)

    print(f"\n{'='*55}")
    print("✅ HOÀN THÀNH BƯỚC 4+5!")


if __name__ == "__main__":
    main()
