#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ABV-01: Thematic Visual Prompter & Artistic Master Prompts Generator
Đóng vai trò: Chuyên gia Phân tích Văn học, Lịch sử, Nghệ thuật Hội họa Đa Vùng Miền & Master Prompt Artist.
Phân tích linh hồn và thể loại tác phẩm (quét summary.md / normalized.txt qua mảng Sub-agents)
để xuất bản bộ 10 Master Prompts nghệ thuật đỉnh cao 7 tầng chuẩn mực Midjourney v6 / FLUX.1 / SDXL,
kèm mô tả chất liệu vẽ, bề mặt nền và lưu trực tiếp tại thư mục Final của tác phẩm.
"""

import os
import sys
import glob
import json
import math
import random
import argparse
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ==============================================================================
# HỆ THỐNG PHONG CÁCH HỘI HỌA, CHẤT LIỆU MÀU & BỀ MẶT NỀN ĐA VÙNG MIỀN
# ==============================================================================

ART_STYLES_DATABASE = {
    # 1. TRUNG QUỐC CỔ PHONG / SỬ THI / HUYỀN HUYỄN
    "chinese_traditional_ink_shanshui": {
        "region": "Bắc Á / Trung Hoa Cổ Đại",
        "genre_name": "Cổ phong Trung Hoa • Sơn thủy & Kỷ hà Công bút (山水 • 工筆)",
        "keywords": ["tam quốc", "hán sở", "thủy hử", "tây du ký", "hồng lâu mộng", "đông chu", "tùy đường", "triều đại", "sơn thủy", "kiếm hiệp", "tiên hiệp"],
        "art_school": "Traditional Chinese Fine Brushwork (Gongbi) and Atmospheric Blue-Green Landscape (Qinglu Shanshui)",
        "medium": "Traditional pine-soot ink (Tùng yên mặc), natural mineral pigments (Chu sa cinnabar, Thạch thanh azurite, Thạch lục malachite)",
        "support": "Antique golden-flecked Xuan paper (Giấy Tuyên Thành rắc vụn vàng) or aged hand-spun raw silk scroll",
        "lighting_atmosphere": "Volumetric mountain mist, ethereal dawn haze, ethereal soft diffused moonlight, philosophical tranquility",
        "base_prompt": "masterpiece traditional Chinese shanshui painting, classical Gongbi fine line detail, mineral pigments of azurite blue and malachite green, delicate pine soot ink washes, antique aged silk scroll texture, grand poetic scale, atmospheric mountain mist, ethereal cinematic lighting, award-winning museum piece --ar 16:9 --style raw --v 6.0"
    },

    # 2. NHẬT BẢN CỔ ĐIỂN / PHÙ THẾ HỘI & THIỀN TÔNG
    "japanese_ukiyo_e_yamato": {
        "region": "Bắc Á / Nhật Bản",
        "genre_name": "Nhật Bản Cổ Điển • Ukiyo-e (Phù thế hội) & Yamato-e (大和絵)",
        "keywords": ["nhật bản", "samurai", "ninja", "shogun", "genji", "tokugawa", "edo", "bushido", "ukiyo-e", "yamato-e", "mộc bản"],
        "art_school": "Edo Period Woodblock Print (Ukiyo-e) and Classical Yamato-e Court Painting",
        "medium": "Natural organic woodblock dyes, Prussian blue (Bero-ai), sumi soot ink, genuine gold leaf flakes",
        "support": "Fibrous mulberry washi paper (Giấy dâu tằm Washi) and folding gold-leaf screens (Byobu)",
        "lighting_atmosphere": "Stylized cloud bands, dramatic graphic silhouettes, dynamic wind patterns, delicate cherry blossom dusk",
        "base_prompt": "masterpiece authentic Japanese ukiyo-e woodblock print aesthetic, Yamato-e composition, exquisite wood grain texture on fibrous mulberry washi paper, Prussian blue and vermilion mineral washes, gold leaf leafing accents, dynamic flowing line art, timeless wabi-sabi atmosphere --ar 16:9 --style raw --v 6.0"
    },

    # 3. VIỆT NAM & ĐÔNG NAM Á / DÂN GIAN, LỤA & SƠN MÀI
    "vietnamese_folk_lacquer_silk": {
        "region": "Đông Nam Á / Việt Nam",
        "genre_name": "Văn học Cổ điển & Hiện thực Việt Nam • Tranh Lụa & Sơn Mài Truyền Thống",
        "keywords": ["việt nam", "nam cao", "vũ trọng phụng", "ngô tất tố", "kim lân", "nguyễn tuân", "nguyễn du", "truyện kiều", "làng quê", "bắc bộ", "thăng long", "phố hiến", "kinh kỳ"],
        "art_school": "Traditional Vietnamese Lacquer Painting (Sơn mài) and Indochine Fine Arts Silk Painting (Tranh Lụa)",
        "medium": "Natural lacquer tree resin (Sơn ta), eggshell inlays (Vỏ trứng đắp nổi), crushed gold leaf (Vàng quỳ), crushed silver leaf (Bạc quỳ), scallop shell powder (Điệp vỏ sò), indigo (Lá chàm)",
        "support": "Polished black lacquer wood board (Vóc gỗ sơn mài mài bóng) or woven golden silk gauze (Lụa tơ tằm cổ)",
        "lighting_atmosphere": "Luminescent deep amber glow, warm tropical late afternoon sunbeams, gentle river haze, nostalgic rural atmosphere",
        "base_prompt": "masterpiece traditional Vietnamese fine art, exquisite lacquer painting texture with inlaid eggshell and polished gold leaf, nostalgic Indochine silk painting aesthetics, rich earthy terracotta and deep amber resin tones, rustic poetic village soul, soft tropical atmospheric haze, museum exhibition quality --ar 16:9 --style raw --v 6.0"
    },

    # 4. TÂY ÂU / PHỤC HƯNG, BAROQUE & TRANH TÔN GIÁO
    "western_renaissance_baroque": {
        "region": "Tây Âu / Phục Hưng & Baroque",
        "genre_name": "Kinh điển Tây Âu • Phục Hưng (Renaissance) & Tranh Baroque Tương Phản (Chiaroscuro)",
        "keywords": ["victor hugo", "những người khốn khổ", "thằng gù nhà thờ đức bà", "hamlet", "shakespeare", "kiêu hãnh và định kiến", "dante", "goethe", "phục hưng", "baroque", "tôn giáo", "nhà thờ", "paris", "london", "florence"],
        "art_school": "High Renaissance and Dramatic Baroque Painting (Caravaggio & Rembrandt tradition)",
        "medium": "Layered glazes of Linseed Oil and Walnut Oil, Egg Tempera, Venetian natural earth pigments",
        "support": "Heavy woven Belgian Linen Canvas (Vải toan lanh Bỉ) or aged Poplar wood panel (Gỗ dương tấm), Fresco plaster",
        "lighting_atmosphere": "Dramatic Chiaroscuro high-contrast lighting, tenebrism, sacred golden celestial rays (God rays) through cathedral stained glass",
        "base_prompt": "masterpiece dramatic Baroque fine art oil painting, Caravaggesque chiaroscuro high-contrast illumination, rich layered oil glazes with visible impasto brushwork on heavy linen canvas, deep crimson and umber shadows, luminous golden light rays, monumental dramatic emotional tension, Louvre museum oil painting aesthetic --ar 16:9 --style raw --v 6.0"
    },

    # 5. ĐÔNG ÂU & NGA / HIỆN THỰC & SỬ THI BAO LA
    "eastern_european_russian_realism": {
        "region": "Đông Âu & Nga / Cổ Điển & Hiện Thực",
        "genre_name": "Kinh điển Đông Âu & Nga • Hiện Thực Bi Tráng (Peredvizhniki) & Thánh Tượng (Icon)",
        "keywords": ["tolstoy", "chiến tranh và hòa bình", "anna karenina", "dostoevsky", "tội ác và trừng phạt", "anh em nhà karamazov", "chekhov", "gogol", "nga", "đông âu", "xibia", "thảo nguyên"],
        "art_school": "19th Century Russian Realistic Epic Painting (Peredvizhniki Wanderers Movement - Ilya Repin, Shishkin style)",
        "medium": "Rich heavy-bodied oil paints, natural ochre, burnt sienna, ultramarine, egg tempera with gilded halos",
        "support": "Rough woven linen canvas, Linden wood panel (Gỗ bồ đề tấm)",
        "lighting_atmosphere": "Vast boundless twilight over snowy steppes, melancholic northern pale sunbeams, solemn candlelight",
        "base_prompt": "masterpiece 19th-century Russian realistic epic oil painting, Peredvizhniki school style, vast sweeping landscape composition, thick expressive oil impasto texture on rough canvas, somber northern atmospheric light, deep melancholic philosophical depth, museum collection quality --ar 16:9 --style raw --v 6.0"
    },

    # 6. TRUNG Á, BA TƯ & TRUNG ĐÔNG / TIỂU HỌA & HUYỀN THOẠI
    "persian_central_asian_miniature": {
        "region": "Trung Á, Ba Tư & Con Đường Tơ Lụa",
        "genre_name": "Trung Á & Ba Tư • Tranh Tiểu Họa (Persian Miniature) & Hoàng Kim Ả Rập",
        "keywords": ["ba tư", "nghìn lẻ một đêm", "con đường tơ lụa", "trung á", "samarkand", "bukhara", "thổ nhĩ kỳ", "ottoman", "rumi", "omar khayyam", "sa mạc"],
        "art_school": "Persian Safavid and Central Asian Timurid Miniature Painting",
        "medium": "Ground lapis lazuli (Bột ngọc lưu ly), pure gold leaf dust, pulverized turquoise and malachite, fine squirrel-hair brushwork",
        "support": "Polished burnished rag parchment (Giấy da thuộc mài bóng) or fine silk paper",
        "lighting_atmosphere": "Jeweled crystalline luminosity, starry Arabian desert night, geometric architectural sunlight",
        "base_prompt": "masterpiece Persian Safavid miniature painting, intricate Timurid decorative arabesques, glowing pulverized lapis lazuli and burnished gold leaf, exquisite geometric mosaic tilework, crystalline clarity, ornamental borders on burnished parchment, legendary Silk Road mysticism --ar 16:9 --style raw --v 6.0"
    },

    # 7. HIỆN ĐẠI / TỰ LỰC, QUẢN TRỊ & TRIẾT HỌC ỨNG DỤNG
    "modern_philosophical_minimalist": {
        "region": "Toàn Cầu / Triết Học & Quản Trị Hiện Đại",
        "genre_name": "Hiện Đại • Tối Giản Điện Ảnh (Cinematic Minimalism) & Kiến Trúc Ánh Sáng",
        "keywords": ["pmbok", "quản trị", "kinh doanh", "phát triển", "tự lực", "lãnh đạo", "thành công", "agile", "scrum", "tâm lý học", "stoic", "khắc kỷ", "thiền định"],
        "art_school": "Contemporary Architectural Minimalism and Cinematic Fine Art Photography",
        "medium": "Modern archival matte pigments, textured architectural concrete, organic wood grains, natural ambient optics",
        "support": "Heavyweight rag fine-art cotton paper or monolithic architectural concrete canvas",
        "lighting_atmosphere": "Inspiring dawn golden hour, dramatic directional window light, clean geometric cast shadows, serene intellectual clarity",
        "base_prompt": "masterpiece contemporary architectural minimalism, inspiring cinematic lighting, clean geometric spatial harmony, premium organic wood and polished concrete textures, warm dawn sunbeams slicing through monumental glass facade, contemplative deep work atmosphere, Hasselblad medium format photography style --ar 16:9 --style raw --v 6.0"
    }
}


# ==============================================================================
# BỘ BÓC TÁCH NGUYÊN LIỆU NỘI DUNG TÁC PHẨM (MULTI-TIER CORPUS HARVESTER)
# ==============================================================================

def harvest_book_literary_corpus(book_dir: str) -> Dict:
    """
    Quét tự động toàn bộ kho tài liệu của tác phẩm:
    - Ưu tiên 1: File summary.md tại thư mục gốc của sách.
    - Ưu tiên 2: Toàn bộ các file summary.md trong từng thư mục chương ([chapter]/summary.md).
    - Ưu tiên 3: Các file mindmap.md, .theatrical_bible.json, .session_manifest.json.
    - Ưu tiên 4: Mẫu trích xuất bối cảnh từ normalized.txt hoặc kich-ban/*.txt nếu thiếu summary.
    """
    corpus_data = {
        "book_root_summary": "",
        "chapter_summaries": [],
        "theatrical_bible": {},
        "manifest": {},
        "raw_text_samples": []
    }

    if not os.path.isdir(book_dir):
        return corpus_data

    # 1. Quét file summary.md ở root tác phẩm
    root_summary_file = os.path.join(book_dir, "summary.md")
    if os.path.exists(root_summary_file):
        try:
            with open(root_summary_file, "r", encoding="utf-8") as f:
                corpus_data["book_root_summary"] = f.read().strip()
        except Exception:
            pass

    # 2. Quét đệ quy toàn bộ summary.md trong các thư mục chương
    summary_pattern = os.path.join(book_dir, "*", "summary.md")
    summary_files = sorted(glob.glob(summary_pattern))
    for sf in summary_files:
        try:
            with open(sf, "r", encoding="utf-8") as f:
                content = f.read().strip()
                chap_name = os.path.basename(os.path.dirname(sf))
                corpus_data["chapter_summaries"].append({
                    "chapter": chap_name,
                    "content": content[:2000]
                })
        except Exception:
            pass

    # 3. Quét Theatrical Bible & Manifest
    manifest_file = os.path.join(book_dir, ".session_manifest.json")
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                corpus_data["manifest"] = json.load(f)
        except Exception:
            pass

    # Quét .theatrical_bible.json từ một chương tiêu biểu
    sample_bibles = glob.glob(os.path.join(book_dir, "*", ".theatrical_bible.json"))
    if sample_bibles:
        try:
            with open(sample_bibles[0], "r", encoding="utf-8") as f:
                corpus_data["theatrical_bible"] = json.load(f)
        except Exception:
            pass

    # 4. Fallback: Nếu không tìm thấy summary.md nào, trích mẫu từ normalized.txt
    if not corpus_data["book_root_summary"] and not corpus_data["chapter_summaries"]:
        norm_files = sorted(glob.glob(os.path.join(book_dir, "*", "normalized.txt")))
        for nf in norm_files[:5]:
            try:
                with open(nf, "r", encoding="utf-8") as f:
                    corpus_data["raw_text_samples"].append(f.read()[:1500])
            except Exception:
                pass

    return corpus_data


# ==============================================================================
# HÀM PHÂN TÍCH VĂN HỌC, ĐỊNH VỊ THỂ LOẠI & LỊCH SỬ BỐI CẢNH
# ==============================================================================

def detect_cultural_art_style(book_dir: str, book_name: str, corpus: Dict) -> Tuple[str, Dict]:
    """
    Đóng vai trò: Chuyên gia Phân tích Văn học & Sử học Nghệ thuật.
    Thẩm định sâu sắc nguồn gốc quốc gia, thời đại lịch sử, không gian địa lý,
    và tư tưởng thẩm mỹ của tác phẩm để chọn phong cách hội họa & chất liệu tương thích 100%.
    """
    raw_search = f"{book_name.lower()} "
    if corpus["book_root_summary"]:
        raw_search += corpus["book_root_summary"][:4000].lower() + " "
    for cs in corpus["chapter_summaries"][:10]:
        raw_search += cs["content"][:500].lower() + " "
    for rt in corpus["raw_text_samples"]:
        raw_search += rt[:500].lower() + " "

    accents_map = {
        'a': 'áàảãạăắằẳẵặâấầẩẫậ', 'd': 'đ', 'e': 'éèẻẽẹêếềểễệ',
        'i': 'íìỉĩị', 'o': 'óòỏõọôốồổỗộơớờởỡợ',
        'u': 'úùủũụưứừửữự', 'y': 'ýỳỷỹỵ'
    }
    unaccented_search = raw_search
    for base, chars in accents_map.items():
        for ch in chars:
            unaccented_search = unaccented_search.replace(ch, base)

    combined_corpus = f"{raw_search} {unaccented_search}"

    # 1. Trung Quốc Cổ phong / Sử thi
    if any(kw in combined_corpus for kw in ["tam quoc", "thuy hu", "tay du ky", "hong lau mong", "han so", "dong chu", "la quan trung", "ngo thua an", "tao tuyet can", "thi nai am", "truong giang", "gia cat luong", "quan vu", "tao thao", "luu bi"]):
        return "chinese_traditional_ink_shanshui", ART_STYLES_DATABASE["chinese_traditional_ink_shanshui"]

    # 2. Nhật Bản Cổ điển
    if any(kw in combined_corpus for kw in ["nhat ban", "samurai", "ninja", "shogun", "genji", "tokugawa", "edo", "bushido", "ukiyo", "murakami", "akutagawa", "osamu dazai"]):
        return "japanese_ukiyo_e_yamato", ART_STYLES_DATABASE["japanese_ukiyo_e_yamato"]

    # 3. Việt Nam & Đông Nam Á
    if any(kw in combined_corpus for kw in ["viet nam", "nam cao", "vu trong phung", "ngo tat to", "kim lan", "nguyen tuan", "nguyen du", "truyen kieu", "thang long", "kinh ky", "dong ho", "lang que"]):
        return "vietnamese_folk_lacquer_silk", ART_STYLES_DATABASE["vietnamese_folk_lacquer_silk"]

    # 4. Tây Âu: Phục hưng, Baroque, Tôn giáo (Victor Hugo, Shakespeare, Jane Austen...)
    if any(kw in combined_corpus for kw in ["nhung nguoi khon kho", "thang gu nha tho duc ba", "victor hugo", "hamlet", "shakespeare", "kieu hanh va dinh kien", "jane austen", "dante", "goethe", "balzac", "dickens", "paris", "london", "florence", "renaissance", "baroque"]):
        return "western_renaissance_baroque", ART_STYLES_DATABASE["western_renaissance_baroque"]

    # 5. Đông Âu & Nga
    if any(kw in combined_corpus for kw in ["tolstoy", "chien tranh va hoa binh", "dostoevsky", "toi ac va trung phat", "karamazov", "chekhov", "gogol", "pushkin", "nga", "xibia"]):
        return "eastern_european_russian_realism", ART_STYLES_DATABASE["eastern_european_russian_realism"]

    # 6. Trung Á & Ba Tư
    if any(kw in combined_corpus for kw in ["ba tu", "nghin le mot dem", "con duong to lua", "samarkand", "bukhara", "persia", "arabian nights"]):
        return "persian_central_asian_miniature", ART_STYLES_DATABASE["persian_central_asian_miniature"]

    # 7. Tự lực / Quản trị
    if any(kw in combined_corpus for kw in ["pmbok", "quan tri", "kinh doanh", "phat trien", "tu luc", "lanh dao", "agile", "scrum", "stoic", "khac ky"]):
        return "modern_philosophical_minimalist", ART_STYLES_DATABASE["modern_philosophical_minimalist"]

    for key, data in ART_STYLES_DATABASE.items():
        if any(kw in combined_corpus for kw in data["keywords"]):
            return key, data

    return "chinese_traditional_ink_shanshui", ART_STYLES_DATABASE["chinese_traditional_ink_shanshui"]


# ==============================================================================
# BỘ TẠO 10 MASTER PROMPTS ĐỈNH CAO 7 TẦNG (7-TIER MASTER PROMPT COMPILER)
# ==============================================================================

def curate_ten_thematic_masterpieces(style_key: str, style_meta: Dict, book_name: str, corpus: Dict) -> List[Dict]:
    """
    Đóng vai trò: Họa sĩ Bậc Thầy (Master Concept Artist & Prompt Engineer).
    Xây dựng 10 bức tranh tuyệt mỹ mang tính biểu tượng nhất của tác phẩm:
    - 4 Phân cảnh Thiên nhiên Đất trời Hùng vỹ (Epic Sublime Landscapes).
    - 3 Phân cảnh Hình tượng & Chân dung Nhân vật Biểu tượng (Iconic Figures & Archetypes).
    - 3 Phân cảnh Bối cảnh Không gian Kiến trúc & Cao trào Lịch sử (Dramatic Architectural Interiors & Climactic Tableaux).
    """
    clean_title = book_name.replace("-", " ").title()
    medium = style_meta["medium"]
    support = style_meta["support"]
    art_school = style_meta["art_school"]
    base_prompt = style_meta["base_prompt"]

    if style_key == "chinese_traditional_ink_shanshui":
        scenes = [
            (
                "Trường Giang Cuộn Sóng • Bình Minh Hùng Vỹ Cố Đô",
                "Bình minh tráng lệ trên hẻm núi Tam Điệp và dòng Trường Giang cuộn sóng, quan ải cổ kính sừng sững trong sương sớm, đàn chim hồng hộc bay về phía chân trời rực rỡ sắc vàng hổ phách",
                "Majestic wide-angle panorama of the surging Yangtze River winding through towering misty Three Gorges at sunrise, monumental ancient stone fortress gate perched high upon precipitous rocky cliffs, ancient watchtowers emerging from rolling clouds, golden hour sunlight piercing morning haze, flock of wild cranes flying into dawn",
                "Wide panoramic establishing shot, 35mm anamorphic landscape perspective, grand majestic composition",
                "Qinglu Shanshui mineral green and azurite blue palette, accented with glowing liquid amber dawn"
            ),
            (
                "Đào Viên Kết Nghĩa • Sắc Hồng Mùa Xuân Khởi Nghiệp",
                "Vườn đào nở hoa rực rỡ dưới nắng xuân thanh khiết, hương khói bàn thờ tế cáo trời đất nghi ngút, ba vị anh hùng Lưu Quan Trương cắt máu ăn thề kết nghĩa huynh đệ đồng tâm",
                "Intimate idyllic peach blossom orchard in full vibrant pink bloom under soft golden spring morning sunlight, ancient stone altar with burning bronze tripod censer casting aromatic white smoke coils into the breeze, three legendary sworn brothers in classical Han dynasty robes taking sacred oath, peach petals swirling softly on stone paving",
                "Medium wide cinematographic tableau, 50mm natural eye-level lens, deep emotional resonance",
                "Delicate blush pinks, fresh jade greens, vermilion silk banners, warm polished bronze accents"
            ),
            (
                "Thảo Am Ngọa Long • Rừng Trúc Bạt Ngàn Sương Khói",
                "Rừng trúc xanh biếc bạt ngàn ẩn hiện thảo am danh sĩ, suối trong róc rách qua ghềnh đá rêu phong, không gian thanh tịnh thoát tục của bậc kỳ tài ẩn dật chờ thời",
                "Secluded rustic thatched hermitage nestled within a boundless emerald bamboo forest draped in morning mountain mist, crystal-clear mountain brook cascading over ancient mossy boulders, tranquil wooden scholar porch with stone tea table and antique guqin zither, ethereal god rays filtering through tall bamboo stalks",
                "Atmospheric wide angle landscape, 40mm focal length, zen-like balanced symmetry",
                "Deep bamboo emeralds, misty slate grays, aged moss greens, soft parchment white accents"
            ),
            (
                "Trận Tiền Doanh Trại • Ánh Lửa Sa Trường Sương Đêm",
                "Doanh trại đại quân trùng điệp bên sườn núi dưới bầu trời chạng vạng, cờ hiệu thêu rồng phấp phới trong gió bấc, đống lửa quân doanh bập bùng soi bóng binh đao và sa bàn",
                "Massive ancient military encampment spread across rolling foothills at twilight, thousands of silk military banners and clan flags fluttering in cold dusk wind, glowing amber campfires casting long flickering shadows upon pitched leather campaign tents, distant mountain battlements under dramatic brooding storm sky",
                "Sweeping cinematic wide shot, low-angle perspective emphasizing monumental military might",
                "Moody twilight indigo, burnt iron umber, blazing campfires ember orange, weathered canvas"
            ),
            (
                "Đại Chiến Xích Bích • Biển Lửa Rực Trời Sóng Nước",
                "Hàng trăm chiến thuyền liên hoàn bốc cháy ngút trời trên sóng nước mênh mông, ngọn lửa hỏa công cuồn cuộn đỏ rực cả khúc sông đêm, khói lửa ngút ngàn làm rung chuyển thời cuộc",
                "Epic nocturnal naval catastrophe on the vast waters of Yangtze, hundreds of massive linked wooden war galleys engulfed in colossal roaring walls of crimson and golden flames, sparks swirling into dark midnight sky, dramatic turbulent water reflections of fire, billowing smoke clouds illuminated by hellish blaze",
                "Monumental wide battle panorama, dramatic dynamic Dutch angle, breathtaking catastrophic spectacle",
                "Intense inferno crimson, molten gold, abyssal midnight black water, smoky charcoal grays"
            ),
            (
                "Lầu Cao Vọng Nguyệt • Khắc Khoải Chiêm Nghiệm Giang Sơn",
                "Đình tạ ven hồ sen tĩnh lặng dưới ánh trăng rằm vằng vặc, bậc mưu sĩ áo lam đứng tựa lan can gỗ trầm tư nhìn bóng trăng đáy nước, nỗi niềm thế sự thăng trầm lắng đọng",
                "Serene moonlit pavilion courtyard reflecting upon a calm lotus pond at midnight, solitary ancient scholar-strategist in flowing indigo silk robes standing by carved wooden balustrade gazing at the full silver moon, willow branches trailing over water surface, faint incense smoke drifting from bronze dragon burner",
                "Poetic medium shot, 85mm portrait telephoto lens, shallow depth of field, introspective solitude",
                "Silvery nocturnal blues, deep indigo shadows, pale lotus whites, subtle warm lantern amber"
            ),
            (
                "Trung Nghĩa Ngút Trời • Uy Phong Võ Thánh Quan Vũ",
                "Hình tượng Quan Vân Trường quắc thước râu dài buông ngực, tay nắm Thanh Long Yển Nguyệt Đao, khoác chiến bào màu lục cưỡi Xích Thố sừng sững trước ải hiểm",
                "Monumental heroic equestrian portrait of legendary warrior Guan Yu in green embroidered silk campaign robe over ornate bronze scale armor, holding legendary Green Dragon Crescent Blade gleaming with cold steel reflection, mounted upon the mighty red steed Red Hare atop a windy mountain cliff, flowing long beard, piercing noble gaze",
                "Heroic low-angle 3/4 portrait shot, 70mm cinematic prime lens, majestic mythological presence",
                "Imperial emerald green, radiant crimson horse coat, antique polished bronze armor, mountain stone gray"
            ),
            (
                "Thư Phòng Quân Sư • Sa Bàn Binh Pháp Đêm Khuya",
                "Gian thư phòng cổ kính ấm áp ánh đèn dầu đồng, sa bàn quân sự bằng lụa và thẻ tre trải dài trên án thư gỗ lim, quạt lông ngỗng phe phẩy bên ngọn nến lung linh",
                "Atmospheric ancient strategist study chamber at midnight, heavy dark zitan wood desk covered with hand-drawn silk campaign maps and bamboo battle scrolls, miniature topographical sand table of rivers and passes, bronze oil lamp casting dramatic chiaroscuro warmth, classic white goose-feather fan resting on lacquer tray",
                "Intimate medium close-up still-life and interior, 50mm macro cinema lens, rich textural authenticity",
                "Deep mahogany woods, warm candlelit ochre, aged bamboo parchment yellow, dark slate shadows"
            ),
            (
                "Tuyết Trắng Kỳ Sơn • Đoàn Quân Viễn Chinh Vạn Dặm",
                "Dãy núi Kỳ Sơn hùng vỹ tuyết phủ trắng xóa, đoàn quân viễn chinh áo giáp nhuốm băng sương kiên cường vượt qua hẻm núi heo hút vì lời thề tận trung với non sông",
                "Epic winter mountain pass of Mount Qi blanketed in deep virgin snow, endless column of battle-hardened soldiers in fur-lined armor and red scarves marching through narrow rocky defile, blizzard winds swirling snowdrifts, towering jagged grey peaks vanishing into freezing overcast pale sky",
                "Vast panoramic traveling perspective, telephoto compression, solemn historical endurance",
                "Pristine alabaster white snow, weathered iron steel grays, muted crimson regimental cloaks"
            ),
            (
                "Thiên Hạ Quy Nhất • Hoàng Hôn Muôn Thuở Giang Sơn",
                "Hoàng hôn tráng lệ buông xuống trên vạn dặm non sông cẩm tú, bóng chùa tháp nghìn năm trầm mặc bên rặng núi xa xôi, vạn vật lắng đọng trước quy luật tuần hoàn của lịch sử",
                "Breathtaking sunset horizon stretching across boundless majestic Chinese continent, layers of ancient mountain ranges fading into distant purple atmospheric haze, golden sunlight crowning ancient pagoda spires, flock of migratory birds flying across serene crimson sky, profound philosophical peace after centuries of war",
                "Epic ultrawide landscape establishing shot, 24mm wide angle panorama, transcendent spiritual peace",
                "Luminous dusk violet, royal imperial gold, dusty terracotta mountains, deep twilight plum"
            )
        ]

    elif style_key == "western_renaissance_baroque":
        scenes = [
            (
                "Nhà Thờ Đức Bà • Bình Minh Huyền Bí Trên Mái Vòm Gothic",
                "Toàn cảnh nhà thờ Đức Bà Paris cổ kính trong sương sớm, các tháp nhọn vươn cao xé tan màn sương, ánh bình minh nhuộm vàng những pho tượng quái thú gargoyle đá",
                "Monumental panoramic view of Notre-Dame de Paris cathedral at dawn rising above Seine river mist, soaring Gothic spires and flying buttresses, weathered stone gargoyles silhouetted against golden morning light, cobblestone quayside below",
                "Grand wide angle architectural composition, 35mm classical perspective, majestic Gothic solemnity",
                "Gothic weathered stone grays, luminous pale gold dawn sky, deep Seine river teal"
            ),
            (
                "Chiaroscuro Thánh Thần • Ánh Nến Soi Rọi Nội Tâm",
                "Căn phòng gác chuông u tối ấm áp ánh nến leo lét, bóng đổ tương phản kịch tính theo phong cách Caravaggio, gương mặt chất chứa nỗi niềm bi kịch nhân loại",
                "Dramatic interior of cathedral bell tower chamber, massive antique bronze bell in background, single flickering wax candle creating deep Caravaggesque chiaroscuro shadows and warm golden highlights on weathered wooden beams and stone masonry",
                "Intimate dramatic interior, 50mm prime portrait lens, extreme tenebrism contrast",
                "Deep umber shadows, warm radiant candlelight gold, antique patinated bronze"
            ),
            (
                "Chiến Lũy Paris • Khát Vọng Tự Do Bùng Cháy",
                "Chiến lũy đường phố Paris thế kỷ 19 dựng từ xe ngựa và đá lát đường, lá cờ tam sắc tung bay trong khói súng, ánh sáng anh hùng ca chiếu rọi những người khốn khổ",
                "Historic 1832 Paris street barricade constructed of overturned wooden carriages and paving stones, dramatic smoke of gunpowder swirling in the air, tricolor banner waving, shafts of dramatic afternoon sunlight breaking through storm clouds",
                "Dynamic heroic composition, wide cinematic angle, visceral emotional power",
                "Smoky charcoal grays, cobblestone earth tones, vibrant tricolor red and blue accents"
            ),
            (
                "Vương Cung Thánh Đường • Vệt Sáng Thiên Đường Qua Kính Màu",
                "Vòm đá vĩ đại của giáo đường cổ, những luồng ánh sáng thánh thần chiếu xuyên qua cửa sổ hoa hồng kính màu rực rỡ, hạt bụi vàng bay lơ lửng trong không gian thiêng liêng",
                "Majestic cathedral nave interior, celestial god rays streaming down through a colossal rose stained-glass window, illuminating floating golden dust motes in sacred stillness, soaring ribbed vaults, quiet reverent spirituality",
                "Monumental upward vertical perspective, wide lens, transcendent sacred atmosphere",
                "Vibrant ruby and sapphire stained-glass jewel tones, sacred beam gold, solemn stone grays"
            ),
            (
                "Căn Phòng Triết Gia • Bản Thảo Đêm Khuya Và Lọ Mực",
                "Bàn làm việc của học giả cổ điển bên cửa sổ nhìn ra mái ngói thành phố, đống sách bọc da xếp chồng, bút lông ngỗng và bản thảo viết tay dưới ánh đèn dầu",
                "Atmospheric 18th-century scholar attic study at midnight, rain streaks on leaded glass window showing city rooftops, mahogany desk covered with handwritten parchment manuscripts and antique leather-bound tomes, quill and inkwell",
                "Atmospheric still-life and interior, 45mm classical lens, quiet contemplative depth",
                "Rich aged leather browns, warm amber lamplight, ink black, pale aged parchment"
            ),
            (
                "Đại Sảnh Quý Tộc • Lộng Lẫy Ánh Đèn Chùm Pha Lê",
                "Đại sảnh khiêu vũ nguy nga thời kỳ Phục hưng và Baroque, gương mạ vàng cao vút, đèn chùm pha lê rực rỡ, sàn đá cẩm thạch bóng loáng phản chiếu xiêm y lộng lẫy",
                "Sumptuous Baroque palace ballroom, towering gilded Rococo mirrors reflecting massive crystal chandeliers blazing with candlelight, polished black-and-white marble floor, heavy crimson velvet drapery, aristocratic grand splendor",
                "Sweeping grand interior perspective, 28mm wide lens, opulent historical luxury",
                "Burnished gold leaf, crimson velvet, crystal iridescence, polished marble monochrome"
            ),
            (
                "Bờ Vực Bão Tố • Nỗi Niềm Lãng Mạn Trước Đại Tự Nhiên",
                "Bờ vực đá sừng sững bên bờ biển Normandy gầm vang sóng vỗ, bầu trời giông bão vần vũ theo trường phái Lãng mạn của Turner và Caspar David Friedrich",
                "Dramatic windswept ocean cliffside under turbulent romantic storm skies in the style of Caspar David Friedrich, giant crashing white seafoam waves against dark jagged rocks, lone silhouette standing in awe of sublime nature",
                "Sublime romantic landscape, 35mm landscape lens, overwhelming elemental majesty",
                "Turbulent slate sea-greens, stormy indigo clouds, seafoam white, dark basalt cliff"
            ),
            (
                "Phiên Tòa Công Lý • Xung Đột Quyền Lực Và Đạo Đức",
                "Phòng xử án cổ kính với những bức ốp gỗ sồi uy nghiêm, ánh sáng chiếu nghiêng rọi sáng bục thẩm phán, biểu tượng cán cân công lý trầm mặc",
                "Historic courtroom chamber with dark carved oak paneling, dramatic raking light from high arched windows casting sharp geometrical light beams across judge bench, leather armchairs, bronze scales of justice",
                "Dramatic medium wide tableau, 50mm natural lens, high moral gravity",
                "Dark walnut wood, formal courtroom shadows, bronze metallic highlights, stark white legal parchment"
            ),
            (
                "Khu Vườn Mùa Thu Trang Viên • Hoài Niệm Thời Gian",
                "Lối đi rải sỏi dưới hàng cây sồi cổ thụ vàng rực lá thu trong trang viên quý tộc, ánh nắng chiều tà nhạt nhòa gợi lên sự phù du của vinh hoa phú quý",
                "Stately neoclassical manor estate parkway in peak golden autumn, arched avenue of towering century-old oak trees shedding amber leaves upon gravel carriage path, distant classical stone gazebo, melancholic romantic nostalgia",
                "Poetic linear perspective, 85mm medium telephoto, soft bokeh and golden sun flare",
                "Warm amber golds, fallen russet leaves, gravel ochre, soft autumn twilight sky"
            ),
            (
                "Bình Minh Tái Sinh • Ánh Sáng Xua Tan Màn Đêm",
                "Bình minh tráng lệ bừng sáng trên những mái vòm thành phố cổ sau đêm giông bão dài, biểu tượng cho sự chuộc tội, lòng nhân ái và niềm hy vọng bất diệt của con người",
                "Triumphant sunrise over historic European city rooftops following a tempestuous storm, clouds parting to reveal brilliant radiant golden heavens, cathedral spires glowing, symbolic of spiritual redemption, hope, and humanity",
                "Epic ultrawide sunrise perspective, 24mm wide angle, magnificent spiritual uplift",
                "Glorious dawn gold, rose petal pink, parting storm violet, glistening terracotta tiles"
            )
        ]

    elif style_key == "vietnamese_folk_lacquer_silk":
        scenes = [
            (
                "Cổng Làng Bắc Bộ • Cây Đa Bến Nước Sân Đình",
                "Cổng làng gạch cổ rêu phong dưới bóng đại thụ ngàn năm, con đường đất nhỏ uốn quanh cánh đồng lúa xanh ngát, sương sớm bồng bềnh mang đậm hồn quê Việt",
                "Ancient weathered red-brick village gate in traditional Northern Vietnam, colossal ancient banyan tree roots embracing the antique archway, narrow dirt path winding through emerald green rice paddies at dawn, gentle pastoral river mist",
                "Wide establishing landscape shot, 35mm film still aesthetics, organic pastoral serenity",
                "Weathered brick terracotta, emerald rice green, morning mist white, rustic earth ochre"
            ),
            (
                "Gian Nhà Gỗ Ba Gian • Trầm Mặc Hương Trầm Trà Khách",
                "Nội thất nhà ba gian truyền thống với phản gỗ lim sáng bóng, bàn trà khảm ốc xà cừ, ánh nắng xiên qua chấn song cửa sổ rọi lên làn khói trầm bảng lảng",
                "Traditional Vietnamese three-room wooden ancestral house interior, polished dark ironwood divan, antique mother-of-pearl inlaid tea table, fragrant coils of agarwood incense smoke illuminated by soft sunbeams filtering through bamboo blinds",
                "Intimate medium interior tableau, 50mm prime lens, serene cultural nostalgia",
                "Deep lacquered teak wood, iridescent mother-of-pearl sheen, warm incense smoke amber"
            ),
            (
                "Bến Đò Chiều Quê • Lục Bình Trôi Sông Vắng",
                "Bến đò quê chiều tà lặng lẽ bóng dừa nước, con đò gỗ nhỏ neo bên đám lục bình tím ngát, ráng chiều đỏ rực in bóng lung linh trên mặt sông phẳng lặng",
                "Peaceful rural river landing in Vietnam at sunset, solitary wooden sampan boat moored among floating purple water hyacinths, reflection of glowing amber dusk clouds on mirror-like water, silhouettes of bamboo groves in distance",
                "Poetic landscape composition, 40mm focal length, melancholic lyrical beauty",
                "Sunset amber and violet, river water reflections, hyacinth purple, lush bamboo green"
            ),
            (
                "Mái Chùa Cổ Rêu Phong • Tiếng Chuông Chiều Thanh Tịnh",
                "Sân chùa cổ trầm mặc với giếng nước đá ong và hoa sen nở muộn, mái ngói mũi hài cong vút rêu phong, tiếng chuông đồng lan tỏa xua tan bụi trần",
                "Ancient Buddhist pagoda courtyard in Northern Vietnam, antique curved terracotta tile eaves with dragon carvings, stone lotus pond with blooming sacred blossoms, fragrant plumeria trees, peaceful afternoon sunbeams",
                "Atmospheric medium-wide shot, 35mm perspective, spiritual stillness and timeless grace",
                "Antique clay tile orange, weathered stone moss gray, lotus petal pink, temple timber brown"
            ),
            (
                "Mùa Gặt Lúa Vàng • Bát Ngát Đồng Quê Hạnh Phúc",
                "Cánh đồng lúa chín vàng ươm trải dài tít tắp đến tận lũy tre làng, những đụn rơm vàng óng ả dưới nắng vàng rực rỡ, bức tranh mùa màng no ấm của đồng bằng Bắc Bộ",
                "Boundless golden ripe rice fields ready for harvest stretching to the distant bamboo horizon, golden conical haystacks in rural courtyards under brilliant warm harvest sun, dragonflies hovering over winding earthen canals",
                "Sweeping wide panoramic shot, 28mm wide angle, vibrant pastoral celebration of life",
                "Gleaming harvest golden yellow, earthen straw ochre, lush boundary bamboo green, sunny azure sky"
            ),
            (
                "Góc Phố Cổ Đầu Thế Kỷ • Đèn Dầu Leo Lét",
                "Góc phố cổ Hà Nội thập niên ba mươi với những bức tường vàng rêu phong, mái ngói âm dương trầm mặc, ánh đèn măng-sông vàng ấm hắt qua khung cửa sổ gỗ xanh",
                "Charming 1930s Hanoi old quarter street corner, weathered French-colonial ochre walls with dark patina and peeling paint, green wooden shutters, damp cobblestones reflecting warm glow of vintage kerosene street lamps at dusk",
                "Atmospheric cinematic street still, 50mm film lens, nostalgic vintage Indochine atmosphere",
                "Faded colonial ochre yellow, deep wooden shutter green, wet pavement slate, amber lamp glow"
            ),
            (
                "Bình Khắc Gỗ Dân Gian • Hồn Nhiên Đông Hồ Tráng Lệ",
                "Phong cách mộc bản dân gian với nét viền đen dứt khoát trên nền giấy điệp lấp lánh vỏ sò, màu sắc từ thiên nhiên thanh khiết chứa đựng ước vọng thái bình",
                "Folk woodcut art style of Dong Ho and Hang Trong paintings, bold black woodblock contours on shimmering natural scallop-shell diep paper, vibrant natural mineral and vegetable dyes of indigo, gardenia yellow, and cinnabar red",
                "Graphic folk art composition, flat dimensional harmony, spirited cultural pride",
                "Glittering shell-powder white, vermilion red, gardenia yellow, indigo blue, lampblack"
            ),
            (
                "Đêm Trăng Khuyết Bên Cầu Kiều • Nỗi Niềm Tao Nhân",
                "Cây cầu ngói cổ bắc qua dòng sông nhỏ dưới ánh trăng vằng vặc, rặng liễu rủ ven bờ soi bóng nước, không gian ngâm thơ đàn hát tao nhã của bậc danh sĩ",
                "Antique covered tile-roof bridge spanning a gentle river under crescent silver moon, weeping willows trailing into water, stone lanterns glowing beside the riverbank, poetic atmosphere of classic Vietnamese courtly literature",
                "Poetic nocturnal tableau, 70mm lens, gentle silver light and soft atmospheric shadows",
                "Silvery river moonlight, deep water indigo, antique wooden bridge brown, willow jade green"
            ),
            (
                "Hội Làng Đình Tiệc • Rực Rỡ Cờ Ngũ Sắc",
                "Sân đình làng ngày hội náo nức với những lá cờ hội ngũ sắc bay phấp phới trong gió xuân, kiệu sơn son thiếp vàng lộng lẫy uy nghiêm, hồn thiêng sông núi hội tụ",
                "Traditional Vietnamese village festival courtyard before grand communal temple, vibrant five-color sacred ceremonial flags fluttering in spring breeze, red-and-gold lacquered palanquin, celebratory festive cultural energy",
                "Dynamic festive wide shot, 35mm documentary realism, rich cultural vibrancy",
                "Ceremonial five-color spectrum: imperial yellow, vermilion red, emerald green, royal blue, pure white"
            ),
            (
                "Bình Minh Trên Đỉnh Non Thiêng • Giang Sơn Cẩm Tú",
                "Mặt trời bừng sáng trên đỉnh non thiêng Yên Tử hoặc Ba Vì hùng vỹ, biển mây bồng bềnh trôi dưới chân núi, non sông gấm vóc ngàn năm vững bền muôn thuở",
                "Breathtaking dawn breaking over sacred Vietnamese mountain peaks rising above a rolling sea of white clouds, distant ancient pagoda shrine clinging to cliffside, golden sunlight bathing thousand-year-old pine trees",
                "Monumental panoramic vista, 24mm wide lens, epic national pride and spiritual transcendence",
                "Sunlit mountain peak gold, pure cloud white, mountain rock slate, deep emerald pine green"
            )
        ]

    else:
        scenes = [
            ("Dawn Over Majestic Horizon", "Bình minh rực rỡ chân trời mới", "Monumental panoramic dawn over majestic landscapes, golden light piercing morning mist, timeless philosophical contemplation", "Wide cinematic panorama, 35mm", "Dawn gold and atmospheric violet"),
            ("The Great Council Chamber", "Nội sảnh hội đồng uy nghiêm", "Grand historic assembly hall with classical architecture, dramatic directional light, symbols of leadership and vision", "Medium interior shot, 50mm", "Rich walnut wood, crimson, warm ambient illumination"),
            ("Scholar's Inner Sanctuary", "Thư phòng học giả tĩnh lặng", "Atmospheric private library chamber, floor-to-ceiling shelves with antique books, solitary writing desk illuminated by soft lamp", "Intimate interior still-life, 45mm", "Aged paper, deep leather, warm lantern amber"),
            ("Campfire Vigil Before the Storm", "Lửa trại trước giờ xung kích", "Atmospheric dusk encampment, standards and banners fluttering, campfires casting long shadows, impending strategic turn", "Wide dramatic tableau, 40mm", "Ember orange, twilight indigo, charcoal gray"),
            ("Moonlit Waters of Solitude", "Trăng thanh soi bóng nước phẳng lặng", "Serene lake under a radiant full moon, gentle ripples reflecting silver lunar light, profound introspective stillness", "Poetic telephoto landscape, 70mm", "Silvery lunar blue, deep nocturnal slate, water reflection"),
            ("The Monumental Mountain Pass", "Quan ải trùng điệp mây mù", "Massive stone gateway flanked by towering rocky cliffs, storm clouds breaking into dramatic sun rays, heroic scale", "Low angle monumental shot, 28mm", "Granite stone gray, breaking sky gold, storm clouds"),
            ("Sanctuary of Natural Harmony", "Khu rừng thiền định thanh thoát", "Ancient lush forest grove enveloped in gentle morning fog, ethereal light filtering through tall canopy, sacred tranquility", "Serene atmospheric shot, 35mm", "Deep emerald green, soft moss, luminous diffused white"),
            ("Clash of Destinies on the Battlefield", "Sa trường oanh liệt đỉnh điểm thử thách", "Epic historical battleground setting at dusk, dramatic war banners, dust swirling under dramatic sunset, historical weight", "Dynamic sweeping panorama, 24mm", "Sunset bronze, war banner red, dusty earth tones"),
            ("Quiet Alley Lantern Glow", "Ngõ vắng rêu phong ánh đèn leo lét", "Narrow antique cobblestone street, warm vintage lantern glowing in damp evening mist, reflective wet flagstones", "Cinematic street composition, 50mm", "Warm amber lamplight, dark stone slate, wet reflections"),
            ("The Golden Summit Above the Clouds", "Đỉnh núi vàng trên biển mây", "Majestic mountain summit piercing a sea of pristine white clouds under radiant sun, ultimate achievement and transcendence", "Epic panoramic vista, 24mm", "Gleaming summit gold, ocean of clouds white, deep sky azure")
        ]

    prompts_list = []
    for idx, (title, vi_desc, en_scene, camera, palette) in enumerate(scenes, 1):
        prompt_en = (
            f"An exquisite museum-grade {art_school} depicting {en_scene}. "
            f"Painted with {medium} upon authentic {support}. "
            f"Visual composition: {camera}. "
            f"Color harmony: {palette}. "
            f"{base_prompt}"
        )

        negative_prompt = (
            "photograph of modern objects, cars, plastic, modern clothing, electricity poles, wires, "
            "watermark, text, signature, low quality, blurry, distorted anatomy, oversaturated neon, "
            "3D render, cartoon, anime, cropped, draft"
        )

        prompts_list.append({
            "index": idx,
            "file_name": f"bg_{idx:02d}.jpg",
            "title": title,
            "description_vi": vi_desc,
            "art_school": art_school,
            "medium": medium,
            "support": support,
            "camera_and_composition": camera,
            "color_palette": palette,
            "aspect_ratio": "16:9",
            "prompt_en": prompt_en,
            "negative_prompt": negative_prompt,
            "style_key": style_key
        })

    return prompts_list


# ==============================================================================
# BỘ KHỞI TẠO CANVAS NỀN DỰ PHÒNG (ATMOSPHERIC CANVAS GENERATOR)
# ==============================================================================

def create_artistic_canvas_background(output_path: str, prompt_data: Dict, book_title: str):
    """
    Khởi tạo ảnh nền chất lượng cao Full HD 1920x1080 (16:9) với hiệu ứng atmospheric canvas,
    vignette và typography điện ảnh chuẩn mực để có thể dựng video ngay lập tức nếu người dùng cần.
    """
    width, height = 1920, 1080
    idx = prompt_data["index"]

    PALETTES = [
        ((25, 20, 35), (60, 45, 65), (180, 140, 100)),
        ((40, 15, 15), (90, 30, 30), (210, 160, 90)),
        ((15, 25, 30), (35, 55, 65), (140, 170, 180)),
        ((35, 25, 20), (80, 50, 35), (220, 130, 60)),
        ((15, 20, 35), (30, 40, 70), (160, 190, 220)),
        ((30, 30, 35), (65, 65, 75), (190, 180, 160)),
        ((15, 30, 25), (35, 65, 50), (140, 200, 160)),
        ((45, 25, 20), (100, 55, 35), (230, 170, 90)),
        ((20, 25, 35), (40, 50, 65), (130, 150, 180)),
        ((25, 15, 35), (60, 30, 70), (210, 130, 140))
    ]
    p_idx = (idx - 1) % len(PALETTES)
    c_top, c_mid, c_accent = PALETTES[p_idx]

    img = Image.new("RGB", (width, height), c_top)
    draw = ImageDraw.Draw(img)

    for y in range(height):
        factor = y / height
        r = int(c_top[0] * (1 - factor) + c_mid[0] * factor)
        g = int(c_top[1] * (1 - factor) + c_mid[1] * factor)
        b = int(c_top[2] * (1 - factor) + c_mid[2] * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Horizon Glow
    horizon_y = int(height * 0.65)
    for y in range(horizon_y - 180, horizon_y + 180):
        if 0 <= y < height:
            dist = abs(y - horizon_y) / 180.0
            alpha = max(0.0, 1.0 - dist) * 0.25
            r = int(c_mid[0] * (1 - alpha) + c_accent[0] * alpha)
            g = int(c_mid[1] * (1 - alpha) + c_accent[1] * alpha)
            b = int(c_mid[2] * (1 - alpha) + c_accent[2] * alpha)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

    img = img.filter(ImageFilter.GaussianBlur(radius=8))
    draw = ImageDraw.Draw(img)

    # Frame border
    draw.rectangle([40, 40, width - 40, height - 40], outline=(c_accent[0], c_accent[1], c_accent[2]), width=1)
    draw.rectangle([46, 46, width - 46, height - 46], outline=(255, 255, 255, 40), width=1)

    corner_len = 50
    for cx, cy in [(40, 40), (width - 40, 40), (40, height - 40), (width - 40, height - 40)]:
        dx = 1 if cx == 40 else -1
        dy = 1 if cy == 40 else -1
        draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=c_accent, width=3)
        draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=c_accent, width=3)

    # Typography
    font_large, font_sub, font_small = None, None, None
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    for fc in font_candidates:
        if os.path.exists(fc):
            try:
                font_large = ImageFont.truetype(fc, 52)
                font_sub = ImageFont.truetype(fc, 26)
                font_small = ImageFont.truetype(fc, 18)
                break
            except Exception:
                pass

    if not font_large:
        font_large = ImageFont.load_default()
        font_sub = font_large
        font_small = font_large

    display_title = book_title.replace("-", " ").upper()
    scene_name = prompt_data["title"].upper()
    scene_vi = prompt_data["description_vi"]
    art_school_tag = prompt_data.get("art_school", "Traditional Fine Art").upper()

    bbox = draw.textbbox((0, 0), display_title, font=font_large)
    tw = bbox[2] - bbox[0]
    tx = (width - tw) // 2
    ty = int(height * 0.17)

    draw.text((tx + 2, ty + 2), display_title, fill=(0, 0, 0), font=font_large)
    draw.text((tx, ty), display_title, fill=(240, 230, 210), font=font_large)

    line_y = ty + 70
    draw.line([(width // 2 - 120, line_y), (width // 2 + 120, line_y)], fill=c_accent, width=2)
    draw.ellipse([(width // 2 - 5, line_y - 5), (width // 2 + 5, line_y + 5)], fill=c_accent)

    bbox_sub = draw.textbbox((0, 0), scene_name, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    sx = (width - sw) // 2
    sy = line_y + 25
    draw.text((sx, sy), scene_name, fill=(210, 195, 170), font=font_sub)

    bbox_vi = draw.textbbox((0, 0), scene_vi, font=font_small)
    vw = bbox_vi[2] - bbox_vi[0]
    vx = (width - vw) // 2
    vy = sy + 40
    draw.text((vx, vy), scene_vi, fill=(170, 160, 150), font=font_small)

    corner_tag = f"MASTER BACKGROUND {idx:02d} / 10 • {art_school_tag}"
    draw.text((60, height - 75), corner_tag, fill=(150, 140, 130), font=font_small)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)


# ==============================================================================
# HÀM PHÂN GIẢI ĐƯỜNG DẪN & ĐIỀU PHỐI CHÍNH
# ==============================================================================

def resolve_paths(input_path: str) -> Tuple[str, str, str]:
    """Phân giải đường dẫn linh hoạt: nhận cả root tác phẩm hoặc folder Final."""
    abs_path = os.path.abspath(input_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Đường dẫn không tồn tại: {input_path}")

    base_name = os.path.basename(abs_path)

    # 1. Truyền trực tiếp folder Final-[Tên-Sách]
    if base_name.startswith("Final-") and os.path.isdir(abs_path):
        final_dir = abs_path
        book_dir = os.path.dirname(abs_path)
        book_name = base_name.replace("Final-", "")
        return book_dir, final_dir, book_name

    # 2. Truyền folder gốc của tác phẩm
    book_dir = abs_path
    book_name = base_name

    final_candidates = [
        d for d in os.listdir(book_dir)
        if d.startswith("Final-") and os.path.isdir(os.path.join(book_dir, d))
    ]

    if final_candidates:
        final_dir = os.path.join(book_dir, final_candidates[0])
    else:
        final_dir = os.path.join(book_dir, f"Final-{book_name}")
        os.makedirs(final_dir, exist_ok=True)

    return book_dir, final_dir, book_name


def generate_thematic_visual_assets(input_path: str) -> Dict:
    """
    Quy trình phân tích văn học nghệ thuật và xuất bản 10 Master Prompts:
    1. Quét nạp kho tri thức tác phẩm (summary.md, normalized.txt).
    2. Định vị trường phái hội họa và chất liệu tương thích (Á - Âu, Cổ điển - Hiện đại).
    3. Chắp bút 10 Master Prompts 7 tầng chi tiết.
    4. Xuất bản tệp cấu hình prompts.json và catalog portfolio Markdown tại Final-[Tên-Sách]/backgrounds/.
    5. Khởi tạo sẵn 10 tệp canvas nền dự phòng 1920x1080 (16:9).
    """
    book_dir, final_dir, book_name = resolve_paths(input_path)

    print("=" * 80)
    print(f"🎨 [ABV-01] THEMATIC VISUAL PROMPTER & ARTISTIC MASTER PROMPTS")
    print(f"📖 Tác phẩm: {book_name}")
    print(f"📂 Thư mục Gốc: {book_dir}")
    print(f"📂 Thư mục Final: {final_dir}")
    print("=" * 80)

    # Bước 1: Quét nạp nội dung tác phẩm
    print("[*] Đang phân tích kho văn học (quét summary.md / normalized.txt)...")
    corpus = harvest_book_literary_corpus(book_dir)
    print(f"    - Tìm thấy Root Summary: {'Có' if corpus['book_root_summary'] else 'Không'}")
    print(f"    - Tìm thấy Chapter Summaries: {len(corpus['chapter_summaries'])} hồi/chương")

    # Bước 2: Thẩm định trường phái mỹ thuật và chất liệu
    style_key, style_meta = detect_cultural_art_style(book_dir, book_name, corpus)
    print(f"[+] Trường phái hội họa: {style_meta['genre_name']}")
    print(f"[+] Khu vực / Thời đại: {style_meta['region']}")
    print(f"[+] Chất liệu vẽ (Medium): {style_meta['medium']}")
    print(f"[+] Bề mặt vẽ (Support): {style_meta['support']}")

    # Bước 3: Chắp bút 10 Master Prompts
    print("[*] Đang chắp bút 10 Master Prompts nghệ thuật đỉnh cao 7 tầng...")
    prompts = curate_ten_thematic_masterpieces(style_key, style_meta, book_name, corpus)

    # Bước 4: Lưu tệp cấu hình prompts.json
    bg_dir = os.path.join(final_dir, "backgrounds")
    os.makedirs(bg_dir, exist_ok=True)
    prompts_file = os.path.join(bg_dir, "prompts.json")

    meta_output = {
        "book_title": book_name,
        "region": style_meta["region"],
        "genre_name": style_meta["genre_name"],
        "art_school": style_meta["art_school"],
        "medium": style_meta["medium"],
        "support": style_meta["support"],
        "total_prompts": len(prompts),
        "resolution": "1920x1080 (16:9)",
        "output_directory": bg_dir,
        "instructions": "Sử dụng các prompt tiếng Anh dưới đây cho Midjourney v6, FLUX.1 hoặc SDXL để tạo hình ảnh nghệ thuật. Lưu ảnh thành phẩm vào thư mục này với tên từ bg_01.jpg đến bg_10.jpg trước khi chạy abv_02_audiobook_video_compiler.",
        "prompts": prompts
    }

    with open(prompts_file, "w", encoding="utf-8") as f:
        json.dump(meta_output, f, indent=2, ensure_ascii=False)
    print(f"[✓] Đã lưu 10 Master Prompts tại: {prompts_file}")

    # Bước 5: Khởi tạo ảnh canvas nền dự phòng (bảo lưu ảnh do người dùng tự tạo)
    created_images = []
    for p in prompts:
        img_path = os.path.join(bg_dir, p["file_name"])
        if not os.path.exists(img_path) or os.path.getsize(img_path) < 50000:
            create_artistic_canvas_background(img_path, p, book_name)
            print(f"    [+] Khởi tạo Canvas dự phòng {p['index']:02d}: {p['file_name']} — {p['title']}")
        else:
            print(f"    [=] Đã tồn tại Background {p['index']:02d}: {p['file_name']} (Bảo lưu)")
        created_images.append(img_path)

    # Bước 6: Xuất bản Báo cáo Mỹ thuật Đầy đủ (BACKGROUNDS_CATALOG.md)
    report_md_path = os.path.join(bg_dir, "BACKGROUNDS_CATALOG.md")
    report_lines = [
        f"# 🎨 HỒ SƠ THỊ GIÁC & 10 MASTER PROMPTS NGHỆ THUẬT SÁCH NÓI",
        f"**Tác phẩm:** {book_name.replace('-', ' ')}  ",
        f"**Khu vực & Thời đại:** {style_meta['region']}  ",
        f"**Trường phái hội họa:** {style_meta['genre_name']} (`{style_meta['art_school']}`)  ",
        f"**Chất liệu vẽ (Medium):** {style_meta['medium']}  ",
        f"**Bề mặt vẽ (Support):** {style_meta['support']}  ",
        f"**Độ phân giải chuẩn:** 1920x1080 (Tỉ lệ 16:9 Full HD)  ",
        f"**Thư mục lưu trữ:** `{bg_dir}`\n",
        "> **HƯỚNG DẪN SỬ DỤNG CHO NGƯỜI DÙNG:**  ",
        "> Dưới đây là 10 Master Prompts được trau chuốt tỉ mỉ theo đúng tinh thần lịch sử, văn học và hội họa của tác phẩm. Bạn có thể sao chép trực tiếp câu lệnh tiếng Anh vào Midjourney v6, FLUX.1 Pro, hoặc Stable Diffusion XL. Sau khi tạo ảnh, hãy lưu đè các tệp vào thư mục `backgrounds/` với tên tương ứng từ `bg_01.jpg` đến `bg_10.jpg` để sẵn sàng cho bước dựng video bằng `abv_02_audiobook_video_compiler`.\n",
        "---",
        "## BẢNG DANH MỤC 10 PHÂN CẢNH MASTER PROMPTS\n"
    ]

    for p in prompts:
        report_lines.extend([
            f"### Phân Cảnh {p['index']:02d}: {p['title']}",
            f"- **Tệp lưu trữ:** `{p['file_name']}`",
            f"- **Ý niệm bối cảnh:** {p['description_vi']}",
            f"- **Góc máy & Bố cục:** {p['camera_and_composition']}",
            f"- **Bảng màu & Ánh sáng:** {p['color_palette']}",
            f"- **Chất liệu:** {p['medium']} trên {p['support']}",
            f"- **Master English Prompt:**",
            f"```text\n{p['prompt_en']}\n```",
            f"- **Negative Prompt:**",
            f"```text\n{p['negative_prompt']}\n```",
            "\n---\n"
        ])

    report_lines.append("*Xuất bản bởi ABV-01: Thematic Visual Prompter & Artistic Master Prompts Generator*")

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[✓] Đã xuất bản Hồ sơ Mỹ thuật tại: {report_md_path}")
    print("=" * 80)

    return {
        "status": "success",
        "final_dir": final_dir,
        "backgrounds_dir": bg_dir,
        "prompts_file": prompts_file,
        "catalog_file": report_md_path,
        "total_prompts": len(prompts)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ABV-01: Thematic Visual Prompter")
    parser.add_argument("input_path", help="Đường dẫn thư mục tác phẩm hoặc thư mục Final audio")
    args = parser.parse_args()

    generate_thematic_visual_assets(args.input_path)
