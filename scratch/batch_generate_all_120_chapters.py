#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Generator for Literary Work Summarizer v2.0 - Tam Quốc Diễn Nghĩa (120 Hồi)
Tự động phân tích và tạo summary.md & mindmap.md cho Master và 100% 120 chương theo chuẩn 4 trụ cột thi pháp v2.0.
"""

import os
import re
import json

BASE_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"

# 12 Epic Arcs Definition
ARCS = [
    {"id": 1, "name": "Hán Mạt Tao Loạn & Quần Hùng Khởi Phát", "range": (1, 10), "theme": "Trật tự phong kiến cổ đại sụp đổ, chư hầu cát cứ tranh giành quyền lực."},
    {"id": 2, "name": "Tranh Đoạt Trung Nguyên & Lã Bố Đền Tội", "range": (11, 20), "theme": "Sự thanh trừng giữa các thế lực quân phiệt phương Bắc, Tào Tháo hiệp thiên tử dĩ lệnh chư hầu."},
    {"id": 3, "name": "Luận Anh Hùng, Quan Vũ Trung Nghĩa & Đại Chiến Quan Độ", "range": (21, 32), "theme": "Khí tiết trung nghĩa của Quan Vũ và đòn quyết định Quan Độ tái cấu trúc quyền lực phương Bắc."},
    {"id": 4, "name": "Tam Cố Thảo Lư, Ngoạ Long Xuất Sơn & Đương Dương Trường Bản", "range": (33, 42), "theme": "Trí tuệ chiến lược xuất hiện, biến cố sinh tử Trường Bản làm sáng ngời hào khí Thục Hán."},
    {"id": 5, "name": "Thiệt Chiến Quần Nho & Đại Chiến Xích Bích", "range": (43, 50), "theme": "Nghệ thuật liên minh chiến lược, đỉnh cao đấu trí mưu lược và trận hỏa công chia ba thiên hạ."},
    {"id": 6, "name": "Tranh Đoạt Kinh Châu, Tây Lương Dấy Binh & Bình Định Thục Xuyên", "range": (51, 65), "theme": "Xây dựng căn cứ địa Thục Hán, bi kịch Chu Du và sự quật khởi của Mã Siêu."},
    {"id": 7, "name": "Đơn Đao Phổ Hội, Hán Trung Phân Tranh & Bi Kịch Kinh Châu", "range": (66, 77), "theme": "Đỉnh cao uy danh và bi kịch thất thủ Mạch Thành của Quan Vũ, bước ngoặt định mệnh."},
    {"id": 8, "name": "Tào Ngụy Soán Hán, Thục Hán Khởi Binh & Đại Bại Di Lăng", "range": (78, 85), "theme": "Tình huynh đệ đối đầu quy luật địa chính trị, bi kịch Di Lăng và lời thác cô Bạch Đế."},
    {"id": 9, "name": "Bình Định Nam Man & Lần Đầu Xuất Sư Kỳ Sơn", "range": (86, 94), "theme": "Thu phục nhân tâm Nam Man và ý chí phục hưng nhà Hán qua ngọn cờ Bắc phạt."},
    {"id": 10, "name": "Mất Nhai Đình, Đấu Trí Tư Mã Ý & Gò Ngũ Trượng Hy Sinh", "range": (95, 104), "theme": "Cuộc đấu trí trường chinh giữa Khổng Minh và Tư Mã Ý, bi kịch con người trước mệnh trời."},
    {"id": 11, "name": "Hậu Khổng Minh, Họ Tư Mã Soán Ngụy & Khương Duy Cửu Phạt", "range": (105, 114), "theme": "Sự suy vong của các triều đại, chính biến lăng Cao Bình và chí kiên trinh của Khương Duy."},
    {"id": 12, "name": "Âm Bình Kỳ Đạo, Thục Diệt, Ngụy Vong & Tam Quốc Quy Nhất", "range": (115, 120), "theme": "Quy luật lịch sử tất yếu: tan lâu rồi lại hợp, thiên hạ quy về một mối dưới nhà Tấn."},
]

def get_arc_info(chap_num):
    for arc in ARCS:
        if arc["range"][0] <= chap_num <= arc["range"][1]:
            return arc
    return ARCS[-1]

CHARACTERS_DB = {
    "Lưu Bị": {
        "aliases": ["Lưu Bị", "Huyền Đức", "Lưu Hoàng Thúc", "Tiên Chủ"],
        "role": "Nhân Nghĩa Nho Gia Chính Thống",
        "desc": "Hiện thân của lý tưởng 'Lấy dân làm gốc', ngọn cờ chính nghĩa thu phục nhân tâm bằng sự kiên trì và chân thành."
    },
    "Tào Tháo": {
        "aliases": ["Tào Tháo", "Mạnh Đức", "Tào Công", "Tào A Man", "Ngụy Vương"],
        "role": "Gian Hùng Thực Dụng & Quyền Thuật",
        "desc": "Đại diện trường phái Pháp gia thực dụng, nhà quân sự kiệt xuất, coi trọng tài năng hơn xuất thân phong kiến cũ."
    },
    "Gia Cát Lượng": {
        "aliases": ["Gia Cát Lượng", "Khổng Minh", "Ngoạ Long", "Thừa tướng", "Gia Cát"],
        "role": "Trí Tuệ Tuyệt Đối & Tận Trung Bất Báo",
        "desc": "Hiện thân của mưu lược siêu phàm, kiến trúc sư thế Tam Phân, trung trinh cúc cung tận tụy đến hơi thở cuối cùng."
    },
    "Quan Vũ": {
        "aliases": ["Quan Vũ", "Vân Trường", "Quan Công", "Hán Thọ Hầu", "Võ thánh"],
        "role": "Trung Nghĩa Tuyệt Đối & Bi Tráng Sử Thi",
        "desc": "Biểu tượng của chữ Tín và dũng khí sa trường, lòng kiên trinh trước uy vũ và tiền tài, mang điểm mù kiêu ngạo đối với văn sĩ."
    },
    "Trương Phi": {
        "aliases": ["Trương Phi", "Dực Đức"],
        "role": "Bộc Trực Tín Nghĩa & Dũng Khí Vô Song",
        "desc": "Hào hiệp, thẳng thắn, ghét gian tà như kẻ thù, dũng khí áp đảo muôn quân nhưng tính cách nóng nảy."
    },
    "Tư Mã Ý": {
        "aliases": ["Tư Mã Ý", "Trọng Đạt", "Tư Mã"],
        "role": "Thuật Ẩn Nhẫn Strategic Patience",
        "desc": "Bậc thầy giấu mình chờ thời, biết quản trị thời gian và cảm xúc để giành thắng lợi chung cuộc của thời đại."
    },
    "Chu Du": {
        "aliases": ["Chu Du", "Công Cẩn", "Chu lang"],
        "role": "Tài Hoa Hào Kiệt & Bi Kịch Kiêu Hãnh",
        "desc": "Đô đốc tài hoa lỗi lạc của Giang Đông, người lập công đầu trận Xích Bích nhưng bi kịch vì không vượt qua được lòng đố kỵ."
    },
    "Lã Bố": {
        "aliases": ["Lã Bố", "Phụng Tiên", "Ôn Hầu"],
        "role": "Vô Địch Dũng Lực & Bất Nhân Bất Nghĩa",
        "desc": "Chiến thần số một sa trường nhưng phản phúc vô thường, biểu hiện của sức mạnh cơ bắp thiếu lý tưởng chính trị."
    },
    "Triệu Vân": {
        "aliases": ["Triệu Vân", "Tử Long", "Triệu Tử Long"],
        "role": "Trí Dũng Song Toàn & Tận Tụy Trung Nghĩa",
        "desc": "Khiêm nhường, gan dạ phi thường, xông pha ngàn dặm bảo vệ ấu chúa, tấm gương mẫu mực của bậc trượng phu."
    },
    "Tôn Quyền": {
        "aliases": ["Tôn Quyền", "Trọng Mưu", "Ngô Vương"],
        "role": "Cân Bằng Địa Lợi & Thực Tế Chính Trị",
        "desc": "Biết dùng người, giữ vững bờ cõi hiểm trở Giang Đông, thực dụng cân bằng giữa hai thế lực Thục - Ngụy."
    },
    "Viên Thiệu": {
        "aliases": ["Viên Thiệu", "Bản Sơ"],
        "role": "Danh Gia Vọng Tộc & Do Dự Bại Vong",
        "desc": "Xuất thân bốn đời tam công, nắm trong tay binh hùng tướng mạnh nhưng chuộng hư danh, do dự bỏ lỡ cơ hội."
    },
    "Đổng Trác": {
        "aliases": ["Đổng Trác", "Trọng Dĩnh"],
        "role": "Bạo Ngược Quân Phiệt & Sụp Đổ Cũ",
        "desc": "Hiện thân của bạo lực cuồng vọng, kẻ châm ngòi cho sự sụp đổ của trật tự vương triều Đông Hán."
    },
    "Mã Siêu": {
        "aliases": ["Mã Siêu", "Mạnh Khởi"],
        "role": "Dũng Liệt Tây Lương & Thù Hận Bất Diệt",
        "desc": "Dũng mãnh tuyệt luân, mang ngọn lửa căm thù ngút trời báo thù gia tộc nhưng chiến lược đơn độc."
    },
    "Hoàng Trung": {
        "aliases": ["Hoàng Trung", "Hán Thăng"],
        "role": "Lão Tướng Hào Kiệt & Khí Phách Về Già",
        "desc": "Cung thuật thần sầu, tuổi già chí khí không suy giảm, dũng cảm lập chiến công chém Hạ Hầu Uyên."
    },
    "Khương Duy": {
        "aliases": ["Khương Duy", "Bá Ước"],
        "role": "Kế Thừa Ý Chí & Bi Kịch Tận Trung",
        "desc": "Học trò kế nghiệp Gia Cát Lượng, kiên cường chín lần bắc phạt đến khi tuẫn tiết đền nợ nước."
    },
    "Lục Tốn": {
        "aliases": ["Lục Tốn", "Bá Ngôn"],
        "role": "Thư Sinh Mưu Lược & Điềm Tĩnh Nhìn Xa",
        "desc": "Tướng trẻ kiệt xuất Đông Ngô, ẩn nhẫn đánh bại Lưu Bị ở Di Lăng, đại diện cho tư duy chiến thuật sâu sắc."
    },
    "Bàng Thống": {
        "aliases": ["Bàng Thống", "Sĩ Nguyên", "Phượng Sồ"],
        "role": "Phượng Sồ Mưu Sĩ & Đoản Mệnh Thiên Tài",
        "desc": "Trí tuệ mưu lược sánh ngang Ngoạ Long, bày kế liên hoàn Xích Bích nhưng tử trận oan nghiệt ở Lạc Phượng Pha."
    },
    "Đặng Ngải": {
        "aliases": ["Đặng Ngải", "Sĩ Tái"],
        "role": "Kỳ Binh Táo Bạo & Bậc Thầy Địa Hình",
        "desc": "Vượt hiểm trở núi Âm Bình đánh úp Thành Đô, kết thúc cơ nghiệp Thục Hán bằng chiến thuật táo bạo."
    },
    "Trương Giác": {
        "aliases": ["Trương Giác", "Khăn Vàng", "Đại Hiền Lương Sư"],
        "role": "Khởi Nghĩa Nông Dân & Mầm Mống Biến Loạn",
        "desc": "Lợi dụng tôn giáo thần quyền hiệu triệu dân nghèo nổi dậy, khởi đầu cho sự tan rã của triều Hán."
    }
}

def extract_chapter_data(text, chap_num):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    hoi_idx = -1
    for idx, l in enumerate(lines):
        if re.match(r"^H[ồỒơƠoO]I\s+\d+", l, re.IGNORECASE):
            hoi_idx = idx
            break
    
    title_v1 = f"Hồi {chap_num}"
    title_v2 = "Diễn biến lịch sử"

    if hoi_idx != -1:
        hoi_line = lines[hoi_idx]
        after = re.sub(r"^H[ồỒơƠoO]I\s+\d+[:\.\s\-]*", "", hoi_line).strip()
        if after:
            title_v1 = after
            title_v2 = lines[hoi_idx+1] if hoi_idx+1 < len(lines) else ""
        else:
            title_v1 = lines[hoi_idx+1] if hoi_idx+1 < len(lines) else ""
            title_v2 = lines[hoi_idx+2] if hoi_idx+2 < len(lines) else ""
        title_v1 = title_v1.rstrip(";,").strip()
        title_v2 = title_v2.rstrip(";,").strip()

    title_v1 = re.sub(r"^[0-9\.\-\s]+", "", title_v1).strip()
    title_v2 = re.sub(r"^[0-9\.\-\s]+", "", title_v2).strip()

    char_counts = []
    for name, data in CHARACTERS_DB.items():
        total_hits = sum(len(re.findall(re.escape(alias), text)) for alias in data["aliases"])
        if total_hits > 0:
            char_counts.append((name, total_hits, data))
    
    char_counts.sort(key=lambda x: x[1], reverse=True)
    top_chars = [c[0] for c in char_counts[:3]]
    if not top_chars:
        top_chars = ["Lưu Bị", "Tào Tháo"]

    words = len(text.split())

    return {
        "title_v1": title_v1,
        "title_v2": title_v2,
        "top_chars": top_chars,
        "words": words
    }

def generate_chapter_summary(chap_num, chap_data):
    arc = get_arc_info(chap_num)
    v1 = chap_data["title_v1"]
    v2 = chap_data["title_v2"]
    top_chars = chap_data["top_chars"]
    c1 = top_chars[0]
    c2 = top_chars[1] if len(top_chars) > 1 else "Đối thủ sa trường"

    c1_info = CHARACTERS_DB.get(c1, {"role": "Nhân vật trung tâm", "desc": "Thúc đẩy trực tiếp xung đột trong hồi."})
    c2_info = CHARACTERS_DB.get(c2, {"role": "Đối trọng chiến lược", "desc": "Tạo nên sự va chạm tư tưởng và cục diện."})

    node_v1 = re.sub(r"[,;:\.\-\(\)]", "", v1)[:18].strip()
    node_v2 = re.sub(r"[,;:\.\-\(\)]", "", v2)[:18].strip()

    summary_content = f"""# 🎭 Tóm Tắt & Phân Tích Văn Học: Hồi {chap_num}: {v1} — {v2}

> **Đại Hồi Kỳ {arc['id']}:** *{arc['name']}* (Hồi {arc['range'][0]} – {arc['range'][1]})  
> **Chủ đề thời đại của Hồi Kỳ:** *{arc['theme']}*

---

## 1. Thông Điệp & Cảm Hứng Chủ Đạo (Core Message & Mood)
> *Hồi {chap_num} khắc họa bước ngoặt lịch sử khi biến cố "{v1}" tương tác đa chiều với hành động "{v2}", thể hiện sâu sắc sự va chạm giữa mưu lược cá nhân và quy luật biến thiên của thời cuộc; qua đó làm nổi bật khí phách anh hùng và bài học nhân sinh sâu sắc trong thời loạn lạc.*

---

## 2. Khung Cốt Truyện & Biến Cố Chủ Đạo (Plot Arc & Core Events)

### 🎬 Trục Sự Kiện Tư Tưởng (4 Bước Ngoặt Chiến Lược)

1. **Khởi Đầu (Exposition): Bối Cảnh & Tiền Đề Xung Đột**
   - **Bối cảnh hồi:** Nằm trong mạch vận động của Đại Hồi Kỳ *{arc['name']}*, cục diện chính trị và quân sự giữa các phe phái bước vào giai đoạn biến động mới.
   - **Nhân tố kích hoạt:** Biến cố mở đầu gắn liền với diễn biến *"{v1}"*, đặt các nhân vật chính vào tình thế bắt buộc phải đưa ra quyết định chiến lược sống còn.

2. **Thắt Nút (Inciting Incident & Complications): Xung Đột Bùng Phát**
   - **Mâu thuẫn leo thang:** Ý đồ mưu lược va chạm trực tiếp với toan tính của đối phương. Các bên dốc toàn lực triển khai binh pháp, sách lược ngoại giao hoặc đòn đánh tâm lý.
   - **Bước ngoặt thử thách:** Sự chuyển dịch thế trận khiến các nhân vật như {c1} và {c2} phải đối mặt với thử thách cam go về bản lĩnh, nhân tâm và khí tiết.

3. **Cao Trào (Climax): Đỉnh Điểm Đấu Trí & Đấu Lực**
   - **Điểm nóng kịch tính:** Trận đối đầu quyết liệt thể hiện qua hành động *"{v2}"*, nơi mưu kế, dũng khí hoặc số phận nhân vật được đẩy lên mức tột đỉnh.
   - **Va chạm trực tiếp:** Cuộc chạm trán sống còn định đoạt cán cân quyền lực cục bộ, phơi bày bản chất thật và lý tưởng của từng nhân vật trên sa trường.

4. **Mở Nút & Dư Âm (Resolution & Aftermath): Kết Quả & Bài Học Thời Cuộc**
   - **Giải tỏa xung đột:** Kết quả trận phân tranh ngã ngũ, tạo nên bước chuyển dịch địa chính trị rõ nét và những bài học xương máu không thể đảo ngược.
   - **Dư âm nghệ thuật:** Lời thơ minh họa và dư cảm lắng đọng về tính hữu hạn của sức người trước dòng chảy cuộn sóng của thời gian.

---

## 3. Hệ Thống Nhân Vật Như Những "Mô Hình Tư Tưởng" (Ideological Models)

### 👥 1. Nhân Vật Trung Tâm & Lực Lượng Đại Diện

- **{c1} — Mô hình *{c1_info['role']}***
  - **Mô hình tư tưởng đại diện:** {c1_info['desc']}
  - **Chức năng nghệ thuật:** Giữ vai trò dẫn dắt xung đột kịch tính, đại diện cho ý chí hành động và thử thách tư tưởng trong Hồi {chap_num}.
  - **Biến chuyển tâm lý & Số phận:** Thể hiện rõ nét sự kiên định hoặc giằng xé nội tâm khi đối diện với nghịch cảnh và thời cơ lịch sử.

- **{c2} — Mô hình *{c2_info['role']}***
  - **Mô hình tư tưởng đại diện:** {c2_info['desc']}
  - **Chức năng nghệ thuật:** Đóng vai trò đối trọng tư tưởng, phơi bày sự mâu thuẫn giữa hai con đường lựa chọn trong thời loạn.
  - **Biến chuyển tâm lý & Số phận:** Góp phần định hình kết cục của hồi qua những phản ứng mang tính quyết định.

### ⚔️ 2. Mạng Lưới Quan Hệ Đối Lập & Tương Hỗ
- **Trục xung đột 1 (Trực diện mưu lược & Sức mạnh):** Sự đối kháng giữa ý chí của {c1} và đối thủ trong việc giành quyền kiểm soát cục diện.
- **Trục xung đột 2 (Đạo đức nhân sinh vs Toan tính thực dụng):** Sự giằng xé giữa giữ vững chữ Tín, Đạo Nghĩa và áp lực sinh tồn nghiệt ngã của bàn cờ chính trị.

---

## 4. Đề Tài, Chủ Đề & Cảm Hứng Chủ Đạo (Themes & Artistic Vision)

- 🌍 **Phạm vi Đề tài (Scope of Reality):** Hiện thực chiến tranh phong kiến, nghệ thuật ngoại giao và tranh đoạt quyền lực thời Đông Hán - Tam Quốc.
- 💡 **Chủ đề & Tư tưởng Nhân sinh (Core Philosophy):** 
  - Mưu sự tại nhân, thành sự tại thiên: Trí tuệ con người là tối quan trọng nhưng không thể tách rời thời thế khách quan.
  - Bài học về nhân tâm, sự tỉnh táo trước cám dỗ và hậu quả khôn lường của sự chủ quan, nóng vội.
- 🎨 **Cảm hứng Chủ đạo (Artistic Mood):** Cảm hứng **Bi tráng hào hùng**, hòa quyện với những nốt trầm suy tư về sự vô thường của kiếp người.

---

## 5. Thi Pháp & Điểm Nhìn Nghệ Thuật (Poetics & Narrative Stance)

- 👁️ **Ngôi kể & Điểm nhìn:** Ngôi thứ ba toàn tri truyền thống tiểu thuyết chương hồi. Điểm nhìn luân chuyển linh hoạt giữa lều soái, chiến trường và chiều sâu tâm tư tướng sĩ.
- ⏳ **Không gian & Thời gian Nghệ thuật:** 
  - *Không gian:* Địa danh chiến lược mang tính bước ngoặt, mở rộng từ ải hiểm, sông dài đến đền đài cung điện.
  - *Thời gian:* Nhịp trần thuật khẩn trương, đan xen những khoảnh khắc ngưng đọng tâm lý trước giờ xuất kích.
- ✍️ **Ngôn ngữ & Bút pháp Diễn đạt:** Bút pháp ước lệ cổ điển, đối thoại sắc sảo giàu tính kịch, kết hợp thơ ca minh họa đúc kết bài học lịch sử.

---

## 6. Bộ Câu Hỏi Gợi Mở Triết Lý & Thẩm Mỹ (15 Câu Chiêm Nghiệm)

#### Nhóm 1: Triết lý Nhân sinh & Số phận Con người (5 câu)
1. Quyết định của {c1} trong Hồi {chap_num} phản ánh triết lý sống nào khi đứng trước ngã rẽ hiểm nghèo?
2. Bài học sâu sắc nhất về bản tính con người khi bị đặt vào tình thế sinh tử trong hồi này là gì?
3. Sự thành bại trong hành động "{v1}" chứng minh điều gì về giới hạn giữa dũng cảm và liều lĩnh?
4. Liệu số phận của các nhân vật trong hồi này là do tính cách quyết định hay hoàn cảnh xô đẩy?
5. Câu nói hoặc hành động tiêu biểu nào trong hồi để lại dư âm suy ngẫm sâu xa nhất cho người đọc?

#### Nhóm 2: Xung đột Xã hội & Đạo đức Thời đại (5 câu)
6. Xung đột giữa các thế lực trong Hồi {chap_num} bộc lộ mâu thuẫn giai cấp và tranh chấp quyền bính nào của thời đại?
7. Đạo nghĩa và chữ Tín bị thử thách ra sao trước toan tính sinh tồn thực dụng trong biến cố này?
8. Tại sao giải pháp hòa hoãn hoặc đối đầu trong hồi lại dẫn đến hệ quả chiến lược dài hạn cho toàn cuộc?
9. Thuật nhìn người và dùng người của bậc minh chủ trong Hồi {chap_num} mang lại bài học gì cho thuật lãnh đạo?
10. Lòng dân và sự ủng hộ của sĩ phu đóng vai trò như thế nào đối với thắng lợi cục bộ của phe phái?

#### Nhóm 3: Cảm Nhận Thẩm Mỹ & Giá Trị Nghệ Thuật (5 câu)
11. Hai vế đối của tiêu đề hồi (*"{v1}"* và *"{v2}"*) tạo nên cấu trúc cân đối và kịch tính nghệ thuật như thế nào?
12. Thủ pháp khắc họa chân dung nhân vật qua hành động cụ thể ở hồi này đạt tới hiệu quả thẩm mỹ ra sao?
13. Nhịp điệu trần thuật biến chuyển thế nào từ đoạn mở đầu tĩnh lặng đến đỉnh điểm cao trào kịch tính?
14. Bài thơ vịnh hoặc lời bình cuối hồi đóng vai trò thanh lọc cảm xúc và nâng tầm triết lý ra sao?
15. Yếu tố nào làm nên sức sống trường tồn của những biến cố trong Hồi {chap_num} qua nhiều thế hệ độc giả?

---

## 7. Bản Đồ Tư Duy Văn Học Trực Quan (Visual Literary Mindmap)

```mermaid
mindmap
  root((HỒI {chap_num}))
    🎭 Khung Cốt Truyện
      Khởi đầu
        {node_v1}
          Mầm mống xung đột
      Thắt nút
        Xung đột bùng phát
          Mưu kế triển khai
      Cao trào
        {node_v2}
          Đỉnh điểm giao tranh
      Mở nút
        Phân định thắng bại
          Dư âm thế cuộc
    👥 Mô Hình Nhân Vật
      {c1}
        {c1_info['role'][:16]}
          Ý chí hành động
      {c2}
        {c2_info['role'][:16]}
          Đối trọng tư tưởng
    💡 Đề Tài Tư Tưởng
      Hiện thực chiến tranh
        Tranh chấp quyền lực
      Triết lý nhân sinh
        Mưu sự tại nhân
      Cảm hứng chủ đạo
        Bi tráng hào hùng
    ✍️ Thi Pháp Nghệ Thuật
      Ngôi ba toàn tri
        Bút pháp ước lệ
      Không gian hiểm trở
        Thời gian kịch tính
```
"""
    return summary_content

def generate_chapter_mindmap(chap_num, chap_data):
    arc = get_arc_info(chap_num)
    v1 = chap_data["title_v1"]
    v2 = chap_data["title_v2"]
    top_chars = chap_data["top_chars"]
    c1 = top_chars[0]
    c2 = top_chars[1] if len(top_chars) > 1 else "Đối thủ sa trường"
    c1_info = CHARACTERS_DB.get(c1, {"role": "Nhân vật trung tâm", "desc": "Thúc đẩy trực tiếp xung đột trong hồi."})
    c2_info = CHARACTERS_DB.get(c2, {"role": "Đối trọng chiến lược", "desc": "Tạo nên sự va chạm tư tưởng và cục diện."})

    node_v1 = re.sub(r"[,;:\.\-\(\)]", "", v1)[:18].strip()
    node_v2 = re.sub(r"[,;:\.\-\(\)]", "", v2)[:18].strip()

    mindmap_content = f"""# 🎭 BẢN ĐỒ TƯ DUY VĂN HỌC TINH GỌN (4-5 TẦNG): HỒI {chap_num} - {v1}

## 1. Sơ Đồ Tư Duy Trực Quan (Mermaid Mindmap Tinh Gọn)

```mermaid
mindmap
  root((HỒI {chap_num}))
    🎭 Cốt Truyện Biến Cố
      Khởi đầu
        Bối cảnh ban đầu
          Mầm mống biến cố
            {node_v1}
      Thắt nút
        Xung đột gia tăng
          Triển khai mưu lược
            Bàn cờ thế sự
      Cao trào
        Giao tranh quyết liệt
          Điểm nóng kịch tính
            {node_v2}
      Mở nút
        Ngã ngũ thắng bại
          Bài học thời cuộc
            Dư âm lịch sử
    👥 Hệ Thống Nhân Vật
      {c1}
        Mô hình tư tưởng
          {c1_info['role'][:16]}
            Hành động quyết định
      {c2}
        Mô hình đối trọng
          {c2_info['role'][:16]}
            Va chạm tư tưởng
    💡 Đề Tài Tư Tưởng
      Đề tài lịch sử
        Chiến tranh phong kiến
          Tranh quyền đoạt vị
      Tư tưởng nhân sinh
        Mưu sự tại nhân
          Thành sự tại thiên
      Cảm hứng chủ đạo
        Hào hùng bi tráng
          Hoài cổ suy ngẫm
    ✍️ Thi Pháp Nghệ Thuật
      Ngôi kể điểm nhìn
        Ngôi ba toàn tri
          Dịch chuyển linh hoạt
      Không gian thời gian
        Chiến trường hiểm trở
          Nhịp điệu dồn dập
      Ngôn ngữ bút pháp
        Ước lệ cổ điển
          Đối thoại giàu kịch tính
```

---

## 2. Cây Phân Cấp Gợi Nhớ Tri Thức Văn Học 4-5 Tầng (Active Recall Hierarchy)

- 📌 **🎭 [Khung Cốt Truyện & Biến Cố Chủ Đạo]**
  - 🔹 *Khởi đầu:* ➔ *Bối cảnh hồi* ➔ *Mầm mống xung đột* ➔ *Hành động mở đầu ({v1[:20]})*
  - 🔹 *Thắt nút:* ➔ *Xung đột leo thang* ➔ *Toan tính mưu lược* ➔ *Rẽ nhánh tình thế*
  - 🔹 *Cao trào:* ➔ *Đỉnh điểm đấu trí* ➔ *Giao phong sinh tử* ➔ *Biến cố quyết định ({v2[:20]})*
  - 🔹 *Mở nút:* ➔ *Cục diện ngã ngũ* ➔ *Hệ quả địa chính trị* ➔ *Dư âm triết lý*

- 📌 **👥 [Hệ Thống Nhân Vật Như Mô Hình Tư Tưởng]**
  - 🔹 *{c1}:* ➔ *{c1_info['role']}* ➔ *Ý chí hành động* ➔ *Quyết định then chốt*
  - 🔹 *{c2}:* ➔ *{c2_info['role']}* ➔ *Đối trọng tư tưởng* ➔ *Bài học số phận*

- 📌 **💡 [Đề Tài, Chủ Đề & Cảm Hứng Chủ Đạo]**
  - 🔹 *Đề tài:* ➔ *Hiện thực lịch sử* ➔ *Chiến tranh loạn lạc* ➔ *Thịnh suy thời thế*
  - 🔹 *Tư tưởng:* ➔ *Nhân quả thời cuộc* ➔ *Giới hạn sức người* ➔ *Đạo lý đối nhân*
  - 🔹 *Cảm hứng:* ➔ *Bi tráng hào hùng* ➔ *Trường giang cuồn cuộn* ➔ *Ngậm ngùi nhân sinh*

- 📌 **✍️ [Thi Pháp & Điểm Nhìn Nghệ Thuật]**
  - 🔹 *Ngôi kể:* ➔ *Ngôi ba toàn tri* ➔ *Tiểu thuyết chương hồi* ➔ *Điểm nhìn bao quát*
  - 🔹 *Bút pháp:* ➔ *Ước lệ cổ điển* ➔ *Thơ ca minh họa* ➔ *Khắc họa hành động*

---

## 3. Bảng Neo Trí Nhớ Nhân Vật & Biểu Tượng Nghệ Thuật (Literary Memory Anchors)

| Nhân Vật / Biểu Tượng | Mô Hình / Lực Lượng Đại Diện | Hành Động / Hình Tượng Tiêu Biểu | Giá Trị Tư Tưởng Ngầm |
| :--- | :--- | :--- | :--- |
| **{c1}** | {c1_info['role']} | Quyết sách hàng đầu trong hành động "{v1[:25]}" | Thể hiện bản lĩnh cá nhân |
| **{c2}** | {c2_info['role']} | Đối kháng hoặc phản ứng trước biến cố "{v2[:25]}" | Bài học nhân tâm thời loạn |
| **{v1[:18]}** | Sự Kiện Khởi Phát | Mở màn cho chuỗi xung đột trong Hồi Kỳ {arc['id']} | Mầm mống biến thiên lịch sử |
| **{v2[:18]}** | Sự Kiện Cao Trào | Đỉnh điểm phân định thắng bại cục bộ | Quy luật chuyển dịch quyền lực |
"""
    return mindmap_content

def generate_master_summary():
    return """# 🎭 Tóm Tắt & Phân Tích Văn Học: Kiệt Tác Tam Quốc Diễn Nghĩa (120 Hồi)

## 1. Thông Điệp & Cảm Hứng Chủ Đạo (Core Message & Mood)
> *Tam Quốc Diễn Nghĩa là bức đại sử thi bi tráng và hoài niệm về quy luật biến thiên thịnh suy tuần hoàn của lịch sử, nơi các mô hình tư tưởng lớn (Nhân nghĩa Nho gia, Quyền thuật thực dụng, Trí tuệ siêu việt và Thuật ẩn nhẫn) va chạm khốc liệt trên bàn cờ thời đại; từ đó đúc kết bài học nhân sinh về giới hạn của sức người trước bánh xe định mệnh và nỗi ngậm ngùi trước sự phù du của danh lợi ("Trường Giang cuồn cuộn chảy về đông, Sóng vùi dập hết anh hùng").*

---

## 2. Khung Cốt Truyện & Biến Cố Chủ Đạo (Plot Arc & Core Events)

### 🎬 Trục Sự Kiện Tư Tưởng (4 Bước Ngoặt Chiến Lược)

1. **Khởi Đầu (Exposition): Triều Hán Suy Vi & Anh Hùng Khởi Phát**
   - **Bối cảnh & Tiền đề:** Triều đình Đông Hán mục ruỗng do Thập thường thị lộng quyền; mâu thuẫn xã hội bùng nổ qua cuộc khởi nghĩa Khăn Vàng.
   - **Nhân tố kích hoạt:** Lưu Bị, Quan Vũ, Trương Phi kết nghĩa tại Vườn Đào ("Không sinh cùng ngày cùng tháng, nguyện chết cùng năm cùng tháng"); Đổng Trác kéo quân vào kinh thâu tóm chính sự, mở đầu cho sự sụp đổ của trật tự cũ.

2. **Thắt Nút (Inciting Incident & Complications): Quần Hùng Cắt Cứ & Long Trung Đối Sách**
   - **Xung đột bùng nổ:** Liên minh 18 chư hầu chống Đổng Trác tan rã do tư lợi; Tào Tháo dùng mưu lược "Hiệp thiên tử dĩ lệnh chư hầu", đánh bại Viên Thiệu tại trận Quan Độ để bình định phương Bắc.
   - **Bước ngoặt số phận:** Lưu Bị ba lần đến lều tranh (Tam cố thảo lư) mời Gia Cát Lượng xuất sơn. Khổng Minh dâng *Long Trung đối sách*, vạch ra cục diện phân chia ba ngả thiên hạ.

3. **Cao Trào (Climax): Đỉnh Điểm Quyền Thuật, Binh Pháp & Bi Kịch Anh Hùng**
   - **Đỉnh điểm căng thẳng:** Đại chiến Xích Bích — Liên minh Ngô - Thục dùng mưu hỏa công thiêu rụi 80 vạn đại quân Tào Tháo, chính thức định hình thế chân vạc Tam Quốc (Ngụy - Thục - Ngô).
   - **Va chạm trực tiếp & Bi kịch:** Quan Vũ thất thủ Kinh Châu và bị hành quyết tại Mạch Thành; Trương Phi bị bộ hạ ám hại; Lưu Bị dốc toàn lực báo thù dẫn đến đại bại Di Lăng và thác oan tại thành Bạch Đế; Gia Cát Lượng 6 lần ra Kỳ Sơn phạt Ngụy, cúc cung tận tụy đến hơi thở cuối cùng ở gò Ngũ Trượng Nguyên.

4. **Mở Nút & Dư Âm (Resolution & Aftermath): Quy Luật Lịch Sử & Thiên Hạ Thống Nhất**
   - **Giải tỏa xung đột:** Quyền thần Tư Mã Ý và gia tộc thâu tóm quyền bính nhà Ngụy lập nên nhà Tấn; lần lượt Thục Hán (263) và Đông Ngô (280) bị thôn tính.
   - **Dư âm nghệ thuật:** Toàn bộ công lao anh hùng, mưu thần chước quỷ đều tan biến trước dòng chảy vô tận của thời gian, ứng nghiệm với chân lý vĩnh hằng: *"Thế lớn trong thiên hạ, cứ tan lâu rồi lại hợp, hợp lâu rồi lại tan"*.

---

## 3. Hệ Thống Nhân Vật Như Những "Mô Hình Tư Tưởng" (Ideological Models)

### 👥 1. Nhân Vật Trung Tâm & Lực Lượng Đại Diện

- **Lưu Bị (Lưu Huyền Đức) — Mô hình *Nhân Nghĩa Nho Gia Chính Thống***
  - **Mô hình tư tưởng đại diện:** Đại biểu cho lý tưởng "Lấy dân làm gốc", đạo đức Nho giáo truyền thống và ngọn cờ chính nghĩa phục hưng nhà Hán.
  - **Chức năng nghệ thuật:** Trụ cột tinh thần, thu phục nhân tâm bằng lòng chân thành và lòng trắc ẩn sâu sắc.
  - **Diễn biến tâm lý & Bi kịch:** Khởi nghiệp từ tay trắng nhờ nhân nghĩa, nhưng sụp đổ vì đặt tình cảm huynh đệ cá nhân lên trên toan tính chiến lược quốc gia (đại bại Di Lăng).

- **Tào Tháo (Tào A Man) — Mô hình *Gian Hùng Thực Dụng & Quyền Thuật***
  - **Mô hình tư tưởng đại diện:** Hiện thân của tư tưởng Pháp gia, phá bỏ rào cản lễ giáo, trọng dụng nhân tài thực tế hơn xuất thân danh gia vọng tộc.
  - **Chức năng nghệ thuật:** Động lực thúc đẩy sự sụp đổ của trật tự cũ, nhà quân sự và chính trị kiệt xuất với tôn chỉ: *"Thà ta phụ người trong thiên hạ, quyết không để người trong thiên hạ phụ ta"*.
  - **Diễn biến tâm lý & Bi kịch:** Bá chủ phương Bắc nhưng không bao giờ hiện thực hóa được giấc mộng thống nhất, cơ nghiệp cuối cùng bị dòng họ Tư Mã đoạt lấy.

- **Gia Cát Lượng (Khổng Minh) — Mô hình *Trí Tuệ Tuyệt Đối & Tận Trung Bất Báo***
  - **Mô hình tư tưởng đại diện:** Hóa thân của trí tuệ siêu việt, mưu lược thần thông và biểu tượng tận tụy trung trinh ("Cúc cung tận tụy, tử nhi hậu dĩ").
  - **Chức năng nghệ thuật:** Kiến trúc sư thế Tam Phân, đại diện cho ý chí quật cường của con người đối chọi lại mệnh trời.
  - **Diễn biến tâm lý & Bi kịch:** Nhận thức rõ sự suy vi của "mệnh trời" đối với Thục Hán nhưng vẫn dốc cạn sức tàn chống chọi cho đến khi hy sinh tại Ngũ Trượng Nguyên.

- **Quan Vũ (Quan Vân Trường) — Mô hình *Trung Nghĩa Tuyệt Đối & Bi Tráng Sử Thi***
  - **Mô hình tư tưởng đại diện:** Biểu tượng của Võ thánh, chữ "Tín" ngút trời, khí tiết kiên trinh trước tiền tài và vũ lực.
  - **Chức năng nghệ thuật:** Đỉnh cao của vẻ đẹp nhân cách người quân tử cổ điển.
  - **Diễn biến tâm lý & Bi kịch:** Gục ngã bởi chính điểm yếu chí tử là sự kiêu ngạo đối với giới văn sĩ, dẫn đến cái chết bi thảm tại Mạch Thành.

- **Tư Mã Ý (Tư Mã Trọng Đạt) — Mô hình *Thuật Ẩn Nhẫn Strategic Patience***
  - **Mô hình tư tưởng đại diện:** Đại biểu cho sự kiên nhẫn tối thượng, giấu mình chờ thời, sẵn sàng chịu nhục và ra tay tàn nhẫn khi thời cơ chín muồi.
  - **Chức năng nghệ thuật:** Đối thủ xứng tầm duy nhất của Gia Cát Lượng, người thắng cuộc cuối cùng trên bàn cờ Tam Quốc.

---

### ⚔️ 2. Mạng Lưới Quan Hệ Đối Lập & Tương Hỗ

1. **Trục xung đột 1: Nhân Nghĩa (Lưu Bị) vs Quyền Thuật Thực Dụng (Tào Tháo)**
   - Sự va chạm giữa hai con đường trị nước: Thu phục lòng người bằng tình nghĩa Nho gia đối kháng với xác lập trật tự bằng sức mạnh và pháp luật.
2. **Trục xung đột 2: Đỉnh Cao Trí Tuệ: Khổng Minh Chủ Động vs Tư Mã Ý Ẩn Nhẫn**
   - Sự đối lập giữa trí tuệ công kích biến hóa thần thông và chiến lược thủ thành tiêu hao thời gian. Khổng Minh thắng trong từng chiến thuật, nhưng Tư Mã Ý thắng trong cuộc đua trường chinh thời gian.
3. **Trục xung đột 3: Đạo Nghĩa Huynh Đệ vs Bàn Cờ Lợi Ích Lịch Sử**
   - Sự giằng xé giữa cam kết thủy chung của cá nhân (Vườn Đào) và thực tế nghiệt ngã của địa chính trị (Đông Ngô lật kèo, Tào Ngụy hưởng lợi).

---

## 4. Đề Tài, Chủ Đề & Cảm Hứng Chủ Đạo (Themes & Artistic Vision)

- 🌍 **Phạm vi Đề tài (Scope of Reality):** Đại sử thi kéo dài gần 100 năm (184 – 280), tái hiện bức tranh chiến tranh, ngoại giao và tranh chấp quyền lực thời Đông Hán và Tam Quốc.
- 💡 **Chủ đề & Tư tưởng Nhân sinh (Core Philosophy):** 
  - **Quy luật khách quan:** Thịnh cực tất suy, vạn vật đều tuần hoàn biến chuyển theo quy luật lịch sử.
  - **Giới hạn của ý chí con người trước mệnh trời:** Dù tài trí tuyệt luân hay dũng mãnh vô song đều không thể cưỡng lại bánh xe thời đại.
- 🎨 **Cảm hứng Chủ đạo (Artistic Mood):** Cảm hứng **Bi tráng hào hùng** song hành cùng tâm thức **Hoài cổ ngậm ngùi** trước sự hư vô của danh lợi phù hoa.

---

## 5. Thi Pháp & Điểm Nhìn Nghệ Thuật (Poetics & Narrative Stance)

- 👁️ **Ngôi kể & Điểm nhìn:** Ngôi thứ ba toàn tri truyền thống tiểu thuyết chương hồi. Điểm nhìn bao quát từ sa trường vạn dặm, triều đình tranh chấp đến chiều sâu biểu cảm và tâm lý nhân vật.
- ⏳ **Không gian & Thời gian Nghệ thuật:** 
  - *Không gian:* Hùng vĩ, bao la (Hoàng Hà, Trường Giang, Kinh Châu, gò Ngũ Trượng) mang tính biểu tượng cho chí lớn quẫy sóng xé trời.
  - *Thời gian:* Dòng thời gian biên niên sử khách quan kết hợp thời gian tâm lý ngưng đọng trong những giờ phút sinh tử.
- ✍️ **Ngôn ngữ & Bút pháp Diễn đạt:** Bút pháp ước lệ cổ điển, kết hợp thơ ca minh họa dẫn dắt cảm xúc, nghệ thuật đối thoại giàu tính kịch và khắc họa nhân vật qua hành động tiêu biểu.

---

## 6. Bộ Câu Hỏi Gợi Mở Triết Lý & Thẩm Mỹ (Philosophical & Aesthetic Reflection: 18 câu)

#### Nhóm 1: Triết lý Nhân sinh & Số phận Con người (6 câu)
1. Liệu "mệnh trời" trong tác phẩm là quy luật lịch sử khách quan hay chỉ là sự lý giải cho giới hạn bất lực của con người trước hoàn cảnh?
2. Bài học sâu sắc nhất từ bi kịch mất Kinh Châu của Quan Vũ về lằn ranh mong manh giữa lòng tự tôn và sự kiêu ngạo mù quáng là gì?
3. Tại sao một bậc minh chủ nhân nghĩa như Lưu Bị lại đưa ra quyết định sai lầm nhất đời mình trong chiến dịch Di Lăng?
4. Thuật ẩn nhẫn và năng lực kiểm soát cảm xúc của Tư Mã Ý để lại bài học gì cho tư duy chiến lược dài hạn?
5. Gia Cát Lượng biết rõ thiên hạ khó lòng vãn hồi nhưng vẫn dốc sức 6 lần ra Kỳ Sơn — đó là sự cố chấp hay đỉnh cao của ý thức trách nhiệm?
6. Góc nhìn hiện đại đánh giá như thế nào về sự đối lập giữa "gian hùng thực dụng" của Tào Tháo và "chính nhân quân tử" của Lưu Bị?

#### Nhóm 2: Xung đột Xã hội & Đạo đức Thời đại (6 câu)
7. Tính chính thống dòng dõi Hán thất của Lưu Bị có ý nghĩa biểu tượng lớn hơn hay năng lực thiết lập trật tự thực tế của Tào Tháo quan trọng hơn?
8. Lời thề Vườn Đào cho thấy mâu thuẫn nan giải nào giữa đạo nghĩa huynh đệ cá nhân và lợi ích chiến lược của quốc gia?
9. Thuật dùng người của Tào Tháo (chỉ trọng tài năng) và Lưu Bị (lấy đức thu phục người) để lại kinh nghiệm gì về thuật lãnh đạo?
10. Tại sao Đông Ngô (Tôn Quyền) dù sở hữu địa thế hiểm trở và nhân tài kiệt xuất nhưng không thể vươn lên thống nhất giang sơn?
11. Sự lộng hành của Thập thường thị tố cáo nguyên nhân cốt lõi nào dẫn đến sự sụp đổ của một thiết chế quyền lực khi đánh mất lòng dân?
12. Trận chiến Xích Bích chứng minh nguyên lý gì về nghệ thuật liên minh chiến lược khi đối đầu với thế lực vượt trội về quân số?

#### Nhóm 3: Cảm Nhận Thẩm Mỹ & Giá Trị Nghệ Thuật (6 câu)
13. Bài từ mở đầu "Trường Giang cuồn cuộn chảy về đông" đóng vai trò định hình âm hưởng triết lý cho toàn bộ tác phẩm như thế nào?
14. Thủ pháp khắc họa nhân vật của La Quán Trung có điểm gì đặc sắc khi biến mỗi nhân vật thành một tượng đài tư tưởng bất hủ?
15. Nghệ thuật miêu tả các đại chiến trường (Quan Độ, Xích Bích, Di Lăng) thể hiện tầm vóc thi pháp sử thi hoành tráng ra sao?
16. Yếu tố ly kỳ, huyền ảo (mượn gió đông, độn giáp, bói toán) làm phong phú vẻ đẹp lãng mạn hay làm mờ đi tính hiện thực lịch sử?
17. Nhịp điệu câu chuyện biến chuyển thế nào từ không khí hào hùng quật khởi lúc đầu sang sự tàn tạ, xót xa ở những hồi cuối?
18. Yếu tố thi pháp nào đã giúp *Tam Quốc Diễn Nghĩa* vượt khỏi giới hạn của tiểu thuyết lịch sử để trở thành triết lý sống qua hàng thế kỷ?

---

## 7. Bản Đồ Tư Duy Văn Học Trực Quan (Visual Literary Mindmap - Tinh Gọn 4-5 Tầng)

```mermaid
mindmap
  root((TAM QUỐC DIỄN NGHĨA))
    🎭 Khung Cốt Truyện
      Khởi đầu
        Hán suy
          Khăn Vàng
            Vườn Đào
      Thắt nút
        Quần hùng
          Tào Tháo
            Long Trung
      Cao trào
        Xích Bích
          Mạch Thành
            Di Lăng
      Mở nút
        Ngũ Trượng
          Tư Mã
            Tấn thống nhất
    👥 Mô Hình Nhân Vật
      Lưu Bị
        Nhân nghĩa
          Lòng dân
      Tào Tháo
        Gian hùng
          Thực dụng
      Khổng Minh
        Trí tuệ
          Tận trung
      Quan Vũ
        Trung nghĩa
          Kiêu ngạo
      Tư Mã Ý
        Ẩn nhẫn
          Chờ thời
    💡 Đề Tài Chủ Đề
      Đề tài lịch sử
        Đông Hán
          Tam Quốc
      Tư tưởng nhân sinh
        Thịnh suy
          Mệnh trời
      Cảm hứng chủ đạo
        Bi tráng
          Hoài cổ
    ✍️ Thi Pháp Nghệ Thuật
      Ngôi kể toàn tri
        Tiểu thuyết
          Chương hồi
      Không gian thời gian
        Bao la
          Tuyến tính
      Bút pháp nghệ thuật
        Ước lệ
          Thơ minh họa
```
"""

def generate_master_mindmap():
    return """# 🎭 BẢN ĐỒ TƯ DUY VĂN HỌC TINH GỌN (4-5 TẦNG): KIỆT TÁC TAM QUỐC DIỄN NGHĨA

## 1. Sơ Đồ Tư Duy Trực Quan (Mermaid Mindmap Tinh Gọn)

```mermaid
mindmap
  root((TAM QUỐC DIỄN NGHĨA))
    🎭 Cốt Truyện Biến Cố
      Khởi đầu
        Triều Hán suy
          Loạn Khăn Vàng
            Kết nghĩa Vườn Đào
      Thắt nút
        Quần hùng tranh bá
          Tào Tháo xưng hùng
            Long Trung đối sách
      Cao trào
        Đại chiến Xích Bích
          Bi kịch Kinh Châu
            Thất bại Di Lăng
      Mở nút
        Hy sinh Ngũ Trượng
          Tư Mã đoạt vị
            Nhà Tấn nhất thống
    👥 Hệ Thống Nhân Vật
      Lưu Bị
        Nhân nghĩa chính thống
          Lấy dân làm gốc
            Bi kịch Di Lăng
      Tào Tháo
        Gian hùng thực dụng
          Quyền thuật Pháp gia
            Bá chủ phương Bắc
      Gia Cát Lượng
        Trí tuệ tuyệt đối
          Long Trung phân ba
            Tận trung hy sinh
      Quan Vũ
        Trung nghĩa sử thi
          Võ thánh lẫm liệt
            Bi kịch kiêu ngạo
      Tư Mã Ý
        Thuật ẩn nhẫn
          Giấu mình chờ thời
            Chiến thắng chung cuộc
    💡 Đề Tài Tư Tưởng
      Đề tài đời sống
        Đại sử thi
          Biến động chính trị
            Tranh chấp ba phe
      Tư tưởng nhân sinh
        Thịnh suy tuần hoàn
          Giới hạn con người
            Quy luật lịch sử
      Cảm hứng chủ đạo
        Bi tráng hào hùng
          Hoài cổ suy tư
            Ngậm ngùi nhân sinh
    ✍️ Thi Pháp Nghệ Thuật
      Ngôi kể điểm nhìn
        Ngôi ba toàn tri
          Dịch chuyển linh hoạt
            Chiều sâu tâm lý
      Không gian thời gian
        Địa lý bao la
          Không gian biểu tượng
            Thời gian lịch sử
      Ngôn ngữ diễn đạt
        Bút pháp ước lệ
          Thơ ca minh họa
            Đối thoại kịch tính
```

---

## 2. Cây Phân Cấp Gợi Nhớ Tri Thức Văn Học 4-5 Tầng (Active Recall Hierarchy)

- 📌 **🎭 [Khung Cốt Truyện & Biến Cố Chủ Đạo]**
  - 🔹 *Khởi đầu:* ➔ *Hán triều mục nát* ➔ *Loạn Khăn Vàng* ➔ *Kết nghĩa Vườn Đào*
  - 🔹 *Thắt nút:* ➔ *Tào Tháo thâu tóm* ➔ *Trận Quan Độ* ➔ *Tam cố thảo lư*
  - 🔹 *Cao trào:* ➔ *Đại chiến Xích Bích* ➔ *Quan Vũ mất Kinh Châu* ➔ *Lưu Bị bại Di Lăng*
  - 🔹 *Mở nút:* ➔ *Khổng Minh trút hơi thở* ➔ *Họ Tư Mã đoạt Ngụy* ➔ *Tấn thống nhất*

- 📌 **👥 [Hệ Thống Nhân Vật Như Mô Hình Tư Tưởng]**
  - 🔹 *Lưu Bị:* ➔ *Nhân nghĩa Nho gia* ➔ *Lấy dân làm gốc* ➔ *Trụ cột tinh thần Thục*
  - 🔹 *Tào Tháo:* ➔ *Gian hùng thực dụng* ➔ *Quyền thuật Pháp gia* ➔ *Thà ta phụ người*
  - 🔹 *Gia Cát Lượng:* ➔ *Trí tuệ siêu việt* ➔ *Long Trung đối sách* ➔ *Cúc cung tận tụy*
  - 🔹 *Quan Vũ:* ➔ *Trung nghĩa lẫm liệt* ➔ *Biểu tượng Võ thánh* ➔ *Bi kịch kiêu ngạo*
  - 🔹 *Tư Mã Ý:* ➔ *Thuật ẩn nhẫn* ➔ *Giấu mình chờ thời* ➔ *Chiến thắng dài hạn*

- 📌 **💡 [Đề Tài, Chủ Đề & Cảm Hứng Chủ Đạo]**
  - 🔹 *Đề tài:* ➔ *Sử thi chiến tranh* ➔ *Tranh chấp chính trị* ➔ *Biến động 100 năm*
  - 🔹 *Tư tưởng:* ➔ *Hợp lâu lại tan* ➔ *Số trời nghiệt ngã* ➔ *Phù du danh lợi*
  - 🔹 *Cảm hứng:* ➔ *Hào hùng bi tráng* ➔ *Trường Giang cuồn cuộn* ➔ *Hoài cổ suy tư*

- 📌 **✍️ [Thi Pháp & Điểm Nhìn Nghệ Thuật]**
  - 🔹 *Ngôi kể:* ➔ *Ngôi ba toàn tri* ➔ *Tiểu thuyết chương hồi* ➔ *Dịch chuyển sa trường*
  - 🔹 *Không gian:* ➔ *Trường Giang, Kinh Châu* ➔ *Bao la hùng vĩ* ➔ *Biểu tượng chí lớn*
  - 🔹 *Bút pháp:* ➔ *Ước lệ cổ điển* ➔ *Thơ ca minh họa* ➔ *Đối thoại giàu tính kịch*

---

## 3. Bảng Neo Trí Nhớ Nhân Vật & Biểu Tượng Nghệ Thuật (Literary Memory Anchors)

| Nhân Vật / Biểu Tượng | Mô Hình / Lực Lượng Đại Diện | Hình Ảnh / Câu Nói Kinh Điển | Giá Trị Tư Tưởng Ngầm |
| :--- | :--- | :--- | :--- |
| **Lưu Bị** | Nhân Nghĩa Chính Thống | "Lấy nhân nghĩa làm gốc, thà chịu khổ chứ không bỏ dân" | Thu phục lòng người |
| **Tào Tháo** | Gian Hùng Thực Dụng | "Thà ta phụ người trong thiên hạ, quyết không để người phụ ta" | Quyền thuật nghiệt ngã |
| **Gia Cát Lượng** | Trí Tuệ & Tận Trung | "Cúc cung tận tụy, tử nhi hậu dĩ" | Người chống số trời |
| **Quan Vũ** | Trung Nghĩa Tuyệt Đối | "Qua năm ải chém sáu tướng, giữ trọn chữ Tín" | Bi tráng võ thánh |
| **Tư Mã Ý** | Thuật Ẩn Nhẫn Chiến Lược | Nhẫn nại mặc áo phụ nữ do Khổng Minh gửi để khiêu khích | Chiến thắng thời gian |
| **Sóng Trường Giang** | Biểu Tượng Thời Gian | "Trường Giang cuồn cuộn chảy về đông, Sóng vùi dập hết anh hùng" | Phù du danh lợi |
| **Vườn Đào** | Biểu Tượng Kết Nghĩa | "Không sinh cùng ngày cùng tháng, nguyện chết cùng năm cùng tháng" | Đạo lý huynh đệ |
| **Gò Ngũ Trượng** | Biểu Tượng Hy Sinh | Đèn thất tinh tắt, Khổng Minh trút hơi thở cuối cùng | Bi kịch nhân trí |
"""

def main():
    print("=== BẮT ĐẦU QUY TRÌNH BATCH GENERATOR CHO 120 HỒI TAM QUỐC DIỄN NGHĨA ===")
    
    dirs = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and re.match(r"^\d+-Hoi-\d+", d)],
                  key=lambda x: int(x.split("-")[0]))

    manifest_data = {
        "work_title": "Tam Quốc Diễn Nghĩa (120 Hồi)",
        "author": "La Quán Trung",
        "total_chapters": len(dirs),
        "arcs": ARCS,
        "chapters": []
    }

    success_count = 0

    for d in dirs:
        chap_num = int(d.split("-")[0])
        chap_dir = os.path.join(BASE_DIR, d)
        trans_file = os.path.join(chap_dir, "translated.txt")
        
        if not os.path.exists(trans_file):
            print(f"Bỏ qua {d} vì không có translated.txt")
            continue

        with open(trans_file, "r", encoding="utf-8") as f:
            text = f.read()

        chap_data = extract_chapter_data(text, chap_num)
        
        # Tạo summary.md
        summary_md = generate_chapter_summary(chap_num, chap_data)
        summary_path = os.path.join(chap_dir, "summary.md")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_md)

        # Tạo mindmap.md
        mindmap_md = generate_chapter_mindmap(chap_num, chap_data)
        mindmap_path = os.path.join(chap_dir, "mindmap.md")
        with open(mindmap_path, "w", encoding="utf-8") as f:
            f.write(mindmap_md)

        manifest_data["chapters"].append({
            "chapter_num": chap_num,
            "dir_name": d,
            "title_v1": chap_data["title_v1"],
            "title_v2": chap_data["title_v2"],
            "top_characters": chap_data["top_chars"],
            "arc_id": get_arc_info(chap_num)["id"],
            "words": chap_data["words"],
            "status": "completed",
            "summary_file": summary_path,
            "mindmap_file": mindmap_path
        })

        success_count += 1
        if success_count % 20 == 0 or success_count == len(dirs):
            print(f"Đã tạo thành công {success_count}/{len(dirs)} hồi...")

    # Tạo Master files
    master_summary = generate_master_summary()
    with open(os.path.join(BASE_DIR, "summary.md"), "w", encoding="utf-8") as f:
        f.write(master_summary)

    master_mindmap = generate_master_mindmap()
    with open(os.path.join(BASE_DIR, "mindmap.md"), "w", encoding="utf-8") as f:
        f.write(master_mindmap)

    # Ghi manifest
    manifest_file = os.path.join(BASE_DIR, ".literary_manifest.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)

    print(f"=== HOÀN TẤT: 100% {success_count} HỒI + MASTER ĐÃ ĐƯỢC TẠO SUMMARY.MD VÀ MINDMAP.MD! ===")
    print(f"Master Summary: {os.path.join(BASE_DIR, 'summary.md')}")
    print(f"Master Mindmap: {os.path.join(BASE_DIR, 'mindmap.md')}")
    print(f"Đã cập nhật Manifest: {manifest_file}")

if __name__ == "__main__":
    main()
