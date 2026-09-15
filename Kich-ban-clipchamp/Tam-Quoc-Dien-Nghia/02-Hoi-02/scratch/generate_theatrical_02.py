# -*- coding: utf-8 -*-
"""
Script to build theatrical_script.json and .theatrical_bible.json for 02-Hoi-02.
Strictly following arf_08a_theatrical_voice_director specification and ARF Rules v2.5.
"""

import json
import os
import re

CHAPTER_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/02-Hoi-02"
KICH_BAN_DIR = os.path.join(CHAPTER_DIR, "kich-ban")

def load_chunk(chunk_id):
    p = os.path.join(KICH_BAN_DIR, f"Kich-ban-{chunk_id}.txt")
    with open(p, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_entries():
    entries = []

    # CHUNK 1
    c1_lines = [
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": "HỒI HAI",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "0.30s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": ". ......",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "1.50s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "TRƯƠNG DỰC ĐỨC GIẬN ĐÁNH ĐỐC BƯU,\nHÀ QUỐC CỬU MƯU GIẾT QUAN HOẠN.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.18s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": ". ......",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "1.50s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Trác tên chữ là Trọng Dĩnh, quê ở huyện Lâm Thao, quận Lũng Tây, làm quan thái thú ở Hà Đông. Xưa nay vốn tính kiêu ngạo. Lúc ấy vì khinh Huyền Đức nên Trương Phi nổi nóng muốn vào giết ngay. Huyền Đức, Quan Công vội ngăn mà rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 1,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Không nên, hắn là quan triều đình, em chớ nên tự tiện giết hắn!",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-3%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Phi nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 1,
            "type": "dialogue",
            "speaker": "Truong_Phi",
            "character_name": "Trương Phi",
            "text": "Nếu không giết nó, mà lại ở đây làm đầy tớ cho nó sai khiến, thì tôi không thể chịu được! Nếu hai anh muốn ở đây thì tôi xin đi ngay nơi khác.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+6Hz",
            "rate": "+8%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 1,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Ba anh em ta kết nghĩa cùng sống chết, sao nỡ lìa nhau? Thôi cùng đi nơi khác là hơn cả.",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-3%",
            "lead_in_pause": "0.42s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Phi nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 1,
            "type": "dialogue",
            "speaker": "Truong_Phi",
            "character_name": "Trương Phi",
            "text": "Có thế thì cái tức này mới hơi hả.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Ngay đêm ấy ba người dẫn quân đến với Chu Tuấn. Tuấn khoản đãi rất hậu. Cùng nhau họp quân, tiến đánh Trương Bảo. Bấy giờ, Tào Tháo đương theo Hoàng Phủ Tung đánh Trương Lương, hai bên đánh nhau một trận to ở Khúc Dương. Bên này Chu Tuấn tiến đánh Trương Bảo, Bảo dẫn tám chín vạn quân đóng ở mé sau núi. Tuấn sai Huyền Đức dẫn đội tiên phong ra đối địch với giặc. Trương Bảo sai phó tướng Cao Thăng phi ngựa ra thách đánh, Huyền Đức sai Trương Phi cự với Cao Thăng. Phi phóng ngựa cầm mâu cùng Thăng giao chiến, chưa được vài hiệp đã đâm Thăng ngã ngựa. Huyền Đức thúc quân xông lên, Trương Bảo ngồi trên ngựa xõa tóc múa gươm, giở yêu thuật, phút chốc gió ầm ầm. Một luồng khí đen tự trên không tỏa xuống, trong luồng khí đen có vô số người ngựa xông ra. Quân Huyền Đức sợ hãi rối loạn, Huyền Đức vội vàng thu quân về, cùng Chu Tuấn bàn mưu định kế. Tuấn nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 1,
            "type": "dialogue",
            "speaker": "Chu_Tuan",
            "character_name": "Chu Tuấn",
            "text": "Nó dùng yêu thuật thì ta phá cũng dễ. Ngày mai nên sai quân chứa sẵn máu lợn máu chó, máu dê phục ở trên núi, đợi quân giặc kéo đến, đứng trên vẩy xuống. Tự khắc giải được phép yêu.",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 1,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức tuân lệnh, sai Quan Công, Trương Phi mỗi người dẫn một nghìn quân đem sẵn máu chó, máu lợn. Máu dê và đồ uế vật, phục trên đỉnh núi. Hôm sau Trương Bảo lại kéo cờ gióng trống đem quân đến thách đánh. Huyền Đức tự ra nghênh địch. Trương Bảo lại dùng phép yêu, phút chốc gió, sấm nổi lên, cát đá tung trời, trong luồng khí đen kéo ra vô số người ngựa. Huyền Đức quay ngựa chạy.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        }
    ]
    entries.extend(c1_lines)

    # CHUNK 2
    c2_lines = [
        {
            "chunk_id": 2,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Trương Bảo thúc quân đuổi theo, khi vào đến gần núi, quân mai phục của Quan, Trương nổ một tiếng trống lệnh, uế vật vung ra. Tức thì những người ngựa bằng giấy đều tự trên không rơi xuống, sấm gió yên lặng, cát đá không bay nữa. Trương Bảo thấy phép yêu đã bị phá vội vã lui quân song tả có Quan Công, hữu có Trương Phi, hai bên đổ ra. Sau lưng có Huyền Đức, Chu Tuấn kéo đến, quân giặc bị thua to. Huyền Đức trông thấy hiệu cờ Địa Công tướng quân phi ngựa đuổi theo. Trương Bảo cuống cuồng chạy trốn. Huyền Đức bắn ngay một phát tên trúng cánh tay trái, Trương Bảo đeo tên cố chết mà chạy vào Dương Thành, đóng chặt cửa. Không dám ra nữa. Chu Tuấn đem quân vây thành, một mặt sai người đi dò tin tức Hoàng Phủ Tung. Thám tử về báo, Hoàng Phủ Tung đánh trận nào thắng trận ấy. Triều đình thấy Đổng Trác thua luôn, hạ lệnh cho Tung thay Trác. Lúc Tung đến nơi thì Trương Giác đã chết rồi. Trương Lương thống xuất cả quân ấy cùng quân Tung chống cự, bị Tung đánh thắng luôn bảy trận chém được Trương Lương ở Khúc Dương. Trương Giác chết rồi cũng bị quật mả, cắt lấy thủ cấp đem về bêu ở kinh sư, còn quân giặc ra hàng hết cả. Hoàng Phủ Tung có công, triều đình gia phong làm sa kỵ tướng quân, lĩnh chức mục Ký Châu. Hoàng Phủ Tung dâng biểu tâu Lư Thực có công không tội, triều đình lại cho Lư Thực giữ nguyên chức cũ. Tào Tháo cũng có công, được thăng Tế nam tướng sửa soạn đi nhậm chức. Chu Tuấn nghe nói, hạ lệnh thúc quân hết sức đánh lấy Dương Thành. Thế giặc bây giờ rất nguy khốn. Một tên tướng giặc là Nghiêm Chánh đâm chết Trương Bảo, cắt lấy thủ cấp đầu hàng. Chu Tuấn đem quân bình luôn được mấy quận, rồi dâng biểu tâu bày việc thắng trận. Bấy giờ, còn ba tên dư đảng giặc Khăn Vàng là Triệu Hoằng, Hàn Trung và Tôn Trọng. Tụ tập được mấy vạn đi đến đâu cũng cướp của đốt nhà, nói là báo thù cho Trương Giác. Triều đình giáng chỉ cho Chu Tuấn đem quân vừa thắng trận đi đánh. Tuấn vội vàng dẫn quân tiến ngay. Lúc ấy giặc đương chiếm giữ Uyển Thành, Tuấn đem quân đến đánh. Triệu Hoằng sai Hàn Trung ra đối địch. Tuấn phái Huyền Đức, Quan, Trương đánh góc thành tây nam, Hàn Trung sợ góc tây nam thất thủ. Đem hết quân tinh nhuệ ra chống cự.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        }
    ]
    entries.extend(c2_lines)

    # CHUNK 3
    c3_lines = [
        {
            "chunk_id": 3,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Chu Tuấn đem hai nghìn quân thiết kỵ đến đánh góc đông bắc, giặc sợ thành hãm, vội bỏ góc tây nam. Huyền Đức đem quân đánh mạnh đằng sau, quân giặc thua to, phải chạy vào thành. Chu Tuấn chia quân vây kín bốn mặt, trong thành lương cạn. Hàn Trung sai người ra xin hàng. Tuấn không cho, Huyền Đức nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 3,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Xưa vua Cao Tổ lấy được thiên hạ, cũng hay chiêu kẻ đầu hàng, dung kẻ quy thuận. Nay Hàn Trung đã hàng thuận, sao ông không cho?",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-3%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 3,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tuấn nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 3,
            "type": "dialogue",
            "speaker": "Chu_Tuan",
            "character_name": "Chu Tuấn",
            "text": "Cái đó mỗi lúc mỗi khác, không thể câu nệ được. Xưa vào đời Tần, Sở, thiên hạ rối loạn, dân không biết ai là chủ, cho nên, chiêu kẻ đầu hàng. Thưởng kẻ quy phục để khuyến khích kẻ khác về với mình. Nay bốn bể đã về một mối, chỉ có giặc Khăn Vàng phản nghịch, nếu cho phép nó hàng. Thì không sao khuyên được người lương thiện. Bọn giặc lúc đắc ý thì tha hồ giết người cướp của, lúc bị thua lại ra đầu hàng. Nếu nhận cho chúng đầu hàng, tức là nuôi cái mầm phản nghịch cho chúng nó, không phải là việc hay vậy.",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 3,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 3,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Ngài dạy cũng phải, nhưng bây giờ bốn mặt thành vây kín như bờ rào sắt, giặc xin hàng không được. Tất nhiên phải cố chết mà đánh. Nghìn người một bụng còn khó đương nổi, nữa là trong thành còn những mấy vạn người liều mạng. Chi bằng bỏ trống hai mặt đông, nam, chỉ đánh hai mặt tây, bắc. Giặc thấy có đường tháo, tất bỏ thành mà chạy, không còn bụng nào ham đánh, ta có thể bắt sống được chúng.",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-3%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 3,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tuấn lấy làm phải, lập tức hạ lệnh rút quân hai mặt đông nam, dồn lại đánh vào mặt tây, mặt bắc. Quả nhiên Hàn Trung dẫn quân bỏ thành chạy. Tuấn cùng Huyền Đức, Quan, Trương thúc quân đuổi đánh, bắt chết Hàn Trung, quân giặc đều tan vỡ chạy trốn. Trong khi đang đuổi đánh xô xát, gặp ngay Triệu Hoằng. Tôn Trọng dẫn quân đến, cùng Tuấn đánh nhau. Tuấn thấy quân Hoằng thế mạnh, đem quân tạm lui Hoằng thừa kế lại cướp được Uyển Thành. Tuấn đóng trại cách thành mười dặm. Chu Tuấn đang sắp sửa đánh thành, bỗng thấy một toán ngựa từ phía đông dẫn đến, một viên tướng đi đầu mặt to, trán rộng. Mình hổ, lưng gấu. Tướng ấy họ Tôn tên Kiên, tên chữ là Văn Đài, dòng dõi Tôn Vũ ngày xưa, quê ở huyện Phú Xuân thuộc Ngô Quận.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        }
    ]
    entries.extend(c3_lines)

    # CHUNK 4
    c4_lines = [
        {
            "chunk_id": 4,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tôn Kiên năm mười bảy tuổi, một hôm ông cùng cha đi thuyền đến sông Tiền Đường. Thấy một bọn giặc bể hơn mười đứa vừa cướp được tiền của khách buôn, đang chia nhau trên bờ. Kiên nói với cha rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 4,
            "type": "dialogue",
            "speaker": "Ton_Kien",
            "character_name": "Tôn Kiên",
            "text": "Con xin lên bắt lũ giặc này.",
            "age_stage": "vo_giong",
            "temperament": "anh_hung_hao_sang",
            "emotion": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+5%",
            "lead_in_pause": "0.40s",
            "timbre_eq": "youth_bright"
        },
        {
            "chunk_id": 4,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Bèn cầm dao nhảy vọt lên bờ, vừa múa đao vừa thét, chỉ đông chỉ tây như cách ra hiệu gọi người. Giặc tưởng quan quân đến bỏ hết của cải chạy trốn. Kiên đuổi giết được một đứa, bởi thế nổi tiếng ở mấy quận huyện, được tiến cử làm chức hiệu úy. Sau quân Cối Kê có đưa yêu tặc là Hứa Xương làm phản, tự xưng là Dương Minh Hoàng đế, tụ họp đến mấy vạn quân. Kiên cùng quan tư mã ấy chiêu mộ dũng sĩ được hơn nghìn người họp với mấy quân châu quận đánh tan giặc ấy. Chém được Hứa Xương và con là Hứa Thiều. Quan thứ sử Tang Mâm dâng biểu tâu công cho Kiên, triều đình bổ Kiên làm quan thừa ở Diêm Độc. Sau lại đổi làm thừa ở Vu Thai, làm thừa ở Hạ Phi. Nay thấy giặc Khăn Vàng nổi loạn. Kiên tụ tập thiếu niên trong làng cùng bọn khách buôn và tinh binh ở Hoài Tứ cả thảy được một nghìn năm trăm người. Dẫn đến tiếp ứng. Chu Tuấn cả mừng, liền sai Kiên đánh cửa nam, Huyền Đức đánh cửa bắc, Tuấn tự đánh cửa tây, để cửa đông cho giặc chạy. Tôn Kiên đi trước nhảy lên thành, chém luôn hơn hai mươi tên giặc, quân giặc sợ hãi bỏ chạy. Triệu Hoằng cầm giáo phi ngựa ra địch với Tôn Kiên, Kiên bèn tự trên mặt thành nhảy xuống. Cướp giáo của Hoằng đâm Hoằng ngã ngựa, rồi lại nhảy lên ngựa Hoằng xông vào giết giặc. Tôn Trọng dẫn quân lẻn ra cửa bắc, gặp ngay Huyền Đức, không còn bụng nào đối địch, chỉ trực chạy thoát thân. Huyền Đức bắn một phát tên. Trọng tự trên ngựa lăn xuống. Lúc ấy đại quân Chu Tuấn tự sau dồn đến, chém được vài vạn đầu giặc. Giặc đầu hàng không biết bao nhiêu mà kể. Một dải Nam Dương hơn mười quận đều yên. Tuấn kéo quân về kinh, được phong làm sa kỵ tướng quân, lĩnh chức Hà Nam lệnh doãn. Tuấn dâng biểu tâu công Tôn Kiên và Lưu Bị. Vì Kiên chạy chọt, nên được bổ làm tư mã đi nhậm chức ngay. Còn Lưu Bị chờ đợi mãi vẫn không được bổ dụng. Ba người buồn bã không vui, một hôm đi chơi giong đường phố gặp quan lang trung Trương Quân. Huyền Đức đến chào, nhân kể luôn công mình đánh giặc cho Quân nghe.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        }
    ]
    entries.extend(c4_lines)

    # CHUNK 5
    c5_lines = [
        {
            "chunk_id": 5,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Quân lấy làm kinh ngạc, bèn vào triều bệ kiến và tâu rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 5,
            "type": "dialogue",
            "speaker": "Truong_Quan",
            "character_name": "Trương Quân",
            "text": "Trước đây giặc Khăn Vàng phản nghịch. Căn do cũng bởi bọn hoạn quan mười người bán quan buôn tước, phi người thân không dùng, phi kẻ thù không giết. Cho nên, thiên hạ rối loạn. Xin bệ hạ chém ngay mười tên này, bêu đầu ở Nam Giao, rồi sai sứ giả đi bố cáo thiên hạ. Ai có công thì trọng thưởng ngay. Như thế thì bốn bể tự khắc bình yên.",
            "age_stage": "trung_nien",
            "temperament": "khac_kho_lanh_lung",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 5,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Mười tên hoạn quan vội tâu vua rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 5,
            "type": "dialogue",
            "speaker": "Truong_Nhuong",
            "character_name": "Trương Nhượng và đồng bọn",
            "text": "Trương Quân đặt điều tâu bậy, đáng tội khi quân.",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+6%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "servile_flatterer"
        },
        {
            "chunk_id": 5,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Vua sai võ sĩ đuổi Trương Quân ra. Mười tên hoạn quan bàn với nhau rằng.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 5,
            "type": "dialogue",
            "speaker": "Truong_Nhuong",
            "character_name": "Trương Nhượng và đồng bọn",
            "text": "Chắc hẳn có kẻ nào có công đánh giặc Khăn Vàng chưa bổ dụng nên sinh ra oán hận. Ta hãy bảo nha môn ghi tên một số người, cất nhắc cho họ một chút, rồi sau sẽ liệu.",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "emotion": "de_doa_tham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+4Hz",
            "rate": "+2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "sharp_cunning"
        },
        {
            "chunk_id": 5,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Bởi vậy, Huyền Đức được bổ làm quan úy huyện An Hỷ, phủ Trung Sơn, Châu Định và phái đi nhậm chức ngay. Huyền Đức giải tán quân sĩ cho về làng, chỉ đem theo hơn hai mươi người thân tín cùng Quan, Trương đến huyện An Hỷ. Làm việc quan suốt một tháng, chẳng lấy lễ của dân một chút gì, nên ai nấy đều cảm phục. Sau khi nhậm chức, cùng Quan, Trương ăn một mâm, nằm một chiếu, khi Huyền Đức ngồi chỗ đông người, thì Quan. Trương đứng hầu hai bên, cả ngày không biết mỏi. Huyền Đức đến huyện chưa được bốn tháng, bỗng triều đình xuống chiếu, Những người nào có công đánh giặc mà làm trưởng lại. Thì đều bị thải hồi. Huyền Đức nghĩ mình có lẽ cũng ở trong số bị thải ấy, còn đang nghi hoặc, bỗng thấy báo có đốc bưu đến huyện. Huyền Đức vội đi đón tiến. Lúc gặp viên đốc bưu, Huyền Đức vái chào một cách cung kính, viên đốc bưu ngồi trên mình ngựa, chỉ vẫy đầu roi đáp lại. Quan, Trương thấy vậy, tức giận vô cùng. Khi đến nhà khách viên đốc bưu ngoảnh mặt hướng nam ngồi cao ngất ngưởng. Huyền Đức đứng hầu ở dưới thềm. Lúc lâu viên đốc bưu mới cất tiếng hỏi,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 5,
            "type": "dialogue",
            "speaker": "Doc_Buu",
            "character_name": "Viên Đốc Bưu",
            "text": "Thầy huyện Lưu xuất thân từ chân gì?",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+3Hz",
            "rate": "+4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 5,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức đáp,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 5,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Bị này dòng dõi Trung sơn Tĩnh vương, khởi thân từ Trác Quận, chém giết giặc Khăn Vàng. Lớn nhỏ hơn ba mươi trận đánh, có chút công lao, nên được bổ chức này.",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-3%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 5,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Viên đốc bưu thét mắng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 5,
            "type": "dialogue",
            "speaker": "Doc_Buu",
            "character_name": "Viên Đốc Bưu",
            "text": "Mi giả mạo hoàng thân, báo càn công trạng, hiện nay triều đình xuống chiếu. Chính để thải bớt những bọn tham quan ô lại như mi đó.",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+8%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "tyrant_arrogant"
        }
    ]
    entries.extend(c5_lines)

    # CHUNK 6
    c6_lines = [
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức vâng dạ luôn mấy tiếng, lui về huyện nha, cùng viên đề lại bàn tính. Đề lại nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "De_Lai",
            "character_name": "Đề Lại",
            "text": "Lão đốc bưu làm dữ như vậy, chẳng qua chỉ chực đòi của đút đấy thôi.",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "0%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Ta không tơ hào của dân một tý gì, lấy đâu mà cung đốn hắn?",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-3%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Ngày hôm viên đốc bưu đòi đề lại đến trước, bắt ép phải khai man là quan huyện hại dân. Huyền Đức mấy lần kéo đến để kêu van, đều bị quân canh cửa không cho vào. Lúc ấy Trương Phi vừa uống mấy chén rượu giải buồn, cưỡi ngựa đi chơi qua nhà khách, thấy năm. Sáu mươi ông già đang khóc than ở trước cửa. Phi hỏi cớ sao thì các lão đều nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Cac_Cu_Gia",
            "character_name": "Các Cụ Già",
            "text": "Viên đốc bưu cố ép đề lại khai man để hại ông Lưu. Chúng tôi biết tin, đến đây kêu giúp, nhưng không cho vào, lại sai quân gác cửa đánh đuổi chúng tôi.",
            "age_stage": "lao_hoa",
            "temperament": "bi_kich_uat_nghen",
            "emotion": "dau_don_trang_troi",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-4Hz",
            "rate": "-8%",
            "lead_in_pause": "0.50s",
            "timbre_eq": "aged_gravel"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Trương Phi cả giận, giương mắt tròn xoe, hai hàm răng nghiến ken két, nhảy ngay xuống ngựa, chạy sấn vào quân địch. Những quân canh cửa không tài nào cản lại được. Phi chạy thẳng vào hậu đường, thấy Viên đốc bưu đang ngồi chễm chệ trên sảnh, đề lại bị trói ở dưới đất. Phi thét lớn lên rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Truong_Phi",
            "character_name": "Trương Phi",
            "text": "Thằng mọt dân kia! Có biết ta là ai không?",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+6Hz",
            "rate": "+8%",
            "lead_in_pause": "0.30s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Viên đốc bưu chưa kịp nói câu gì cả, đã bị Trương Phi túm tóc lôi tuột ra ngoài nhà khách, kéo thẳng về trước huyện. Trói vào tàu ngựa, rồi bẻ cành liễu đánh vào hai đùi viên đốc bưu, đánh gãy luôn đến hơn mười cành liễu. Huyền Đức đang lúc ngồi buồn bỗng nghe ngoài cửa huyện có tiếng xôn xao liền hỏi, tả hữu nói rằng.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Ta_Huu",
            "character_name": "Tả Hữu",
            "text": "Trương tướng quân đang trói đánh một người nào ở cửa huyện.",
            "age_stage": "thanh_xuan",
            "temperament": "binh_than_tu_nhien",
            "emotion": "hoi_hop_thi_thao",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+2%",
            "lead_in_pause": "0.40s",
            "timbre_eq": "intimate_narrator"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức vội chạy ra xem, tưởng Phi trói đánh ai, té ra là quan thanh tra! Huyền Đức kinh ngạc, hỏi đầu đuôi. Phi nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Truong_Phi",
            "character_name": "Trương Phi",
            "text": "Cái thằng hại nước mọt dân này, chẳng đánh cho chết còn đợi đến bao giờ!",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+6Hz",
            "rate": "+8%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Viên đốc bưu kêu,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Doc_Buu",
            "character_name": "Viên Đốc Bưu",
            "text": "Ông Huyền Đức ơi! Cứu tôi với!",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "emotion": "ninh_bo_van_xin",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+6Hz",
            "rate": "+8%",
            "lead_in_pause": "0.30s",
            "timbre_eq": "servile_flatterer"
        },
        {
            "chunk_id": 6,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức vốn người nhân từ, trong lòng không nỡ liền bảo Trương Phi không được đánh nữa. Quan Công cũng chạy lại nói, rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 6,
            "type": "dialogue",
            "speaker": "Quan_Vu",
            "character_name": "Quan Vũ",
            "text": "Huynh trưởng làm nên biết bao công lớn, chỉ mới được bổ chức huyện úy nhỏ mọn này. Nay lại còn bị thằng đốc bưu nó sỉ nhục. Tôi nghĩ cái bụi chông gai không phải là nơi chim loan chim phượng đậu. Bất nhược ta giết quách thằng đốc bưu này đi, rồi bỏ quan về làng, mưu tính việc lớn còn hơn.",
            "age_stage": "thanh_xuan",
            "temperament": "khac_kho_lanh_lung",
            "emotion": "khac_kho_lanh_lung",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-3Hz",
            "rate": "-5%",
            "lead_in_pause": "0.48s",
            "timbre_eq": "warm_authority"
        }
    ]
    entries.extend(c6_lines)

    # CHUNK 7
    c7_lines = [
        {
            "chunk_id": 7,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức bèn đem cái ấn treo vào cổ viên đốc bưu mà mắng rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 7,
            "type": "dialogue",
            "speaker": "Luu_Bi",
            "character_name": "Lưu Bị",
            "text": "Cứ cái tội mày hại dân. Đáng nên giết chết mới phải, nhưng nay hãy tạm tha cho mày. Ấn đây, tao trả chúng mày. Từ nay chúng tao không ở đây nữa!",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 7,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Viên đốc bưu được sống sót, về nói với quan thái thú Định Châu, quan thái thú tư giấy đi các nơi. Sai người nã bắt anh em Huyền Đức. Huyền Đức cùng Quan, Trương sang Đại Châu ở với Lưu Khôi. Khôi thấy Huyền Đức là người tôn thất nhà Hán, bèn giấu ở trong nhà, không cho ai biết. Nói về mười hoạn quan, trong tay đã nắm được quyền to, bèn bàn tính với nhau hễ ai không theo, chúng đều giết đi cả. Triệu Trung, Trương Nhượng sai người đến đòi các tướng có công phá giặc Khăn Vàng ngày trước phải lễ vàng bạc mới được làm quan. Bằng không thì tâu vua bắt bãi chức. Vì lẽ ấy mà Hoàng Phủ Tung, Chu Tuấn không chịu đút lót, đều bị bãi cả. Vua lại phong Triệu Trung làm sa kỵ tướng quân, bọn Trương Nhượng mười ba người đều phong tước hầu. Triều chính mỗi ngày một suy đồi, nhân dân cũng ta oán. Bởi thế ở Trường Sa có Khu Tinh nổi loạn, ở Ngư Đương có Trương Thuần, Trương Cử là phản. Cử tự xưng là thiên tử, Thuần xưng là đại tướng quân. Những tờ biểu cáo cấp gửi về triều đình như bướm bay, bọn hoạn quan đều giấu cả, không tâu vua biết. Một hôm vua đang cùng mười viên hoạn quan uống rượu ở vườn hoa sau cung. Bỗng thấy quan gián nghị đại phu Lưu Đào đi tắt đến trước mặt vua mà khóc. Vua hỏi vì cớ gì. Đào nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 7,
            "type": "dialogue",
            "speaker": "Luu_Dao",
            "character_name": "Lưu Đào",
            "text": "Thiên hạ nguy ngập đến nơi rồi, mà bệ hạ còn cứu vui chơi say tỉnh với bọn hoạn quan như thế ru?",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "emotion": "dau_don_trang_troi",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-3Hz",
            "rate": "-6%",
            "lead_in_pause": "0.55s",
            "timbre_eq": "tragic_grief"
        },
        {
            "chunk_id": 7,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Vua nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 7,
            "type": "dialogue",
            "speaker": "Vua_Linh_De",
            "character_name": "Hán Linh Đế",
            "text": "Nhà nước đương yên ổn, có việc gì mà nguy ngập?",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 7,
            "type": "dialogue",
            "speaker": "Luu_Dao",
            "character_name": "Lưu Đào",
            "text": "Tâu bệ hạ! Hiện nay giặc cướp nổi lên tứ tung xâm chiếm khắp các châu quận, cái vạ đều bởi mười tên hoạn quan bán quan hại dân. Lừa dối quân thượng mà ra cả. Cho nên, những người chính nhân quân tử bỏ đi hết cả, cái nguy đã ở ngay trước mắt rồi còn gì?",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "emotion": "dau_don_trang_troi",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-3Hz",
            "rate": "-6%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "tragic_grief"
        },
        {
            "chunk_id": 7,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Mười viên hoạn quan đều phủ phục trước mặt vua tâu rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 7,
            "type": "dialogue",
            "speaker": "Truong_Nhuong",
            "character_name": "Trương Nhượng và đồng bọn",
            "text": "Muôn tâu thánh thượng, quan đại thần đã không có lượng bao dung. Chúng tôi biết mình chẳng thoát. Cúi xin thánh thượng cho chúng tôi được toàn tính mạng trở về quê quán, tình nguyện đem hết gia sản giúp đỡ việc quân.",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "emotion": "ninh_bo_van_xin",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+4%",
            "lead_in_pause": "0.42s",
            "timbre_eq": "servile_flatterer"
        },
        {
            "chunk_id": 7,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "elegiac",
            "text": "Nói đoạn, đều khóc nức nở.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-8%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "elegiac_narrator"
        }
    ]
    entries.extend(c7_lines)

    # CHUNK 8
    c8_lines = [
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Vua cả giận mắng Đào rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Vua_Linh_De",
            "character_name": "Hán Linh Đế",
            "text": "Nhà ngươi cũng có người hầu hạ, sao không cho trẫm có người hầu hạ?",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+4Hz",
            "rate": "+6%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tức thì sai võ sĩ lôi Lưu Đào ra chém. Lưu Đào vừa đi vừa kêu lớn rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Luu_Dao",
            "character_name": "Lưu Đào",
            "text": "Trời ơi! Đào này chết không đáng tiếc, chỉ tiếc cái cơ nghiệp nhà Hán hơn bốn trăm năm nay bỗng tiêu diệt trong khoảnh khắc.",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "emotion": "dau_don_trang_troi",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-3Hz",
            "rate": "-6%",
            "lead_in_pause": "0.40s",
            "timbre_eq": "tragic_grief"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Võ sĩ đem Lưu Đào ra, sắp hành hình thì có một quan đại thần nói to lên rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Tran_Dam",
            "character_name": "Trần Đam",
            "text": "Khoan, không được hạ thủ vội. Đợi ta vào can vua đã.",
            "age_stage": "lao_hoa",
            "temperament": "anh_hung_hao_sang",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-3Hz",
            "rate": "+2%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "aged_gravel"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Mọi người nhìn xem ai, thì là quan tư đồ Trần Đam. Đam đi tắt vào cung tâu rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Tran_Dam",
            "character_name": "Trần Đam",
            "text": "Tâu bệ hạ, chẳng hay Lưu gián nghị can tội gì mà bị giết?",
            "age_stage": "lao_hoa",
            "temperament": "khac_kho_lanh_lung",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-4Hz",
            "rate": "-6%",
            "lead_in_pause": "0.50s",
            "timbre_eq": "aged_gravel"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Vua phán,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Vua_Linh_De",
            "character_name": "Hán Linh Đế",
            "text": "Nó dám gièm pha cận thần của trẫm, lại xúc phạm cả trẫm nữa.",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Đam tâu,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Tran_Dam",
            "character_name": "Trần Đam",
            "text": "Hiện thiên hạ ai cũng muốn nuốt sống ăn tươi mười tên hoạn quan. Vậy mà bệ hạ kinh nó như cha mẹ. Chúng không có một chút công nào mà được phong đến tước hầu. Huống chi lũ Phong Tư kết liên với giặc Khăn Vàng, toan làm tay trong cho chúng nó. Nay nếu bệ hạ không tỉnh ngộ, xã tắc đến đổ mất!",
            "age_stage": "lao_hoa",
            "temperament": "khac_kho_lanh_lung",
            "emotion": "dau_don_trang_troi",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-3Hz",
            "rate": "-4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "aged_gravel"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Vua phán,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 8,
            "type": "dialogue",
            "speaker": "Vua_Linh_De",
            "character_name": "Hán Linh Đế",
            "text": "Phong Tư làm loạn, việc còn mập mờ chưa rõ, còn trong bọn hoạn quan mười người. Há không có một hai người trung nghĩa hay sao?",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 8,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Trần Đam đập đầu xuống đất, cố can. Vua nổi giận, sai lôi Đam ra, bắt bỏ ngục cùng với Lưu Đào. Ngay đêm hôm ấy bọn hoạn quan vào ngục giết cả hai người. Rồi giả làm chiếu chỉ nhà vua cử Tôn Kiên làm thái thú Trường Sa và đem quân đi đánh Khu Tinh. Chưa đầy năm mươi ngày có tin báo thắng trận, khu Giang Hạ đều bình định cả. Vua chiếu xuống phong Kiên làm Ô trình hầu, phong Lưu Ngu làm quan mục U Châu, đem quân đến Ngư Dương đánh Trương Thuần. Trương Cử. Ở Đại Châu Lưu, Khôi được tin bèn viết thư tiến dẫn Huyền Đức. Nga mừng lắm, cử Huyền Đức làm quan đô úy, đem quân đến tận hang ổ giặc đánh mấy trận lớn, giặc bị thua luôn. Trương Thuận tính vốn hung hăng, không được lòng quân bị tên thủ hạ chặt đầu đem nộp rồi dẫn quân ra hàng. Trương Cử biết thế mình không sao địch nổi, cũng tự thắt cổ chết. Thế là cả cõi Ngư Dương đều bình định. Lưu Ngu dâng biểu tâu công lớn của Lưu Bị. Triều đình tha tội đánh viên đốc bưu và bổ làm quan thừa ở Hạ Mật, sau lại nhắc lên làm quan úy ở Cao Đường. Công Tôn Toản lại dâng biểu tâu công đánh giặc trước kia của Huyền Đức và tiến cử làm quan tư mã. Lĩnh chức huyện lệnh Bình Nguyên.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        }
    ]
    entries.extend(c8_lines)

    # CHUNK 9
    c9_lines = [
        {
            "chunk_id": 9,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Huyền Đức ở Bình Nguyên nhờ có lương tiền và quân mã, nên khôi phục lại được cảnh phồn vinh ngày trước. Lưu Ngu cũng có công dẹp giặc, nên được thăng làm quan thái úy. Tháng tư, mùa hạ năm Trung bình thứ sáu, một trăm tám mươi chín, vua Linh Đế bệnh nặng. Triệu quan đại tướng quân Hà Tiến vào cung bàn tính mọi việc quan trọng về sau. Nguyên Hà Tiến vốn xuất thân con nhà hàng thịt, vì có em gái lấy vua. Sinh được hoàng tử tên là Biện được lập làm Hoàng hậu, nên Tiến nhờ đó được quyền cao chức trọng. Vua lại yêu mến một mỹ nhân nữa họ Vương, sinh được hoàng tử tên là Hiệp. Hà hậu ghen ghét, bỏ thuốc độc giết Vương mỹ nhân, nên hoàng tử Hiệp phải nuôi ở trong cung Đổng Thái Hậu. Đổng Thái Hậu là mẹ vua Linh Đế, nguyên là vợ Giải độc đình hầu Lưu Thường. Bởi khi trước vua Hoàn Đế không có con trai, phải đón con trai Giải độc đình hầu lên làm vua, tức là vua Linh Đế. Linh Đế lên ngôi, bèn đón mẹ vào phụng dưỡng ở trong cung và tôn làm Thái Hậu. Đổng Thái Hậu thường khuyên vua lập hoàng tử Hiệp làm thái tử để nối ngôi vua về sau. Vua cũng yêu Hiệp hơn, nên có ý muốn lập Hiệp. Lúc ấy bệnh vua đã nguy, trung thường thị là Kiển Thạc tâu rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 9,
            "type": "dialogue",
            "speaker": "Kien_Thac",
            "character_name": "Kiển Thạc",
            "text": "Tâu bệ hạ! Việc này quan hệ rất lớn, nếu muốn lập hoàng tử Hiệp, trước hết xin giết Hà Tiến mới khỏi lo ngại về sau.",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "emotion": "de_doa_tham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "sharp_cunning"
        },
        {
            "chunk_id": 9,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Vua lấy làm phải, giáng chỉ vời Tiến vào cung. Tiến vừa đi đến cửa cung, gặp quan tư mã Phan Ẩn bảo Tiến rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 9,
            "type": "dialogue",
            "speaker": "Phan_An",
            "character_name": "Phan Ẩn",
            "text": "Đừng vào cung, Kiển Thạc nó định mưu giết ông đấy!",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "hoi_hop_thi_thao",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "0Hz",
            "rate": "+5%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "suspense_narrator"
        },
        {
            "chunk_id": 9,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến cả sợ, vội về nhà, triệu các quan đại thần đến bàn định, muốn giết hết cả bọn hoạn quan. Một người đứng lên nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 9,
            "type": "dialogue",
            "speaker": "Tao_Thao",
            "character_name": "Tào Tháo",
            "text": "Thế lực của bọn hoạn quan, gây ra tự đời vua Xung, vua Chất. Ngày nay lan rộng khắp cả trong triều, giết hết thế nào được. Nếu cơ mưu không kín, chết đến cả họ ngay, vậy xin nghĩ cho kỹ.",
            "age_stage": "thanh_xuan",
            "temperament": "giao_hoat_nham_hiem",
            "emotion": "khac_kho_lanh_lung",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "-2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "sharp_cunning"
        },
        {
            "chunk_id": 9,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nhìn xem ai, thì là quan điển quân hiệu úy Tào Tháo. Tiến mắng Tháo rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 9,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Trẻ con biết đâu việc lớn của triều đình!",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+6%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 9,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Đang lúc Tiến còn dùng dằng chưa quyết. Phan An chạy đến báo rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 9,
            "type": "dialogue",
            "speaker": "Phan_An",
            "character_name": "Phan Ẩn",
            "text": "Hoàng đế đã băng hà rồi. Hiện Kiển Thạc đang bàn với mười tên hoạn quan định một mặt giấu kín không phát tang, một mặt giả làm chiếu chỉ. Triệu Hà Quốc Cữu vào cung giết đi, rồi lập Hoàng tử Hiệp lên ngôi.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "bang_hoang_chet_lang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "0Hz",
            "rate": "+6%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "suspense_narrator"
        }
    ]
    entries.extend(c9_lines)

    # CHUNK 10
    c10_lines = [
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Nói chưa dứt lời, có sứ giả đến triệu Tiến vào cung, Tào Tháo nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Tao_Thao",
            "character_name": "Tào Tháo",
            "text": "Việc cốt yếu bây giờ là phải lập vua trước đã. Rồi sau hãy nói đến việc trừ giặc.",
            "age_stage": "thanh_xuan",
            "temperament": "giao_hoat_nham_hiem",
            "emotion": "khac_kho_lanh_lung",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "-2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "sharp_cunning"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Có ai dám cùng ta vào cung lập vua mới và đánh giặc không?",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "+2%",
            "lead_in_pause": "0.40s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Một người đứng phắt dậy nói rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Vien_Thieu",
            "character_name": "Viên Thiệu",
            "text": "Tôi xin đem năm nghìn tinh binh, chém khóa cửa cung, vào lập vua mới. Giết hết bọn hoạn quan, quét sạch trong triều để yên thiên hạ.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+3Hz",
            "rate": "+6%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nhìn xem, thì người ấy là con quan tư đồ Viên Phùng, cháu Viên Ngỗi tên là Thiệu. Tự là Bản Sơ biện làm quan tư lệ hiệu úy. Tiến cả mừng, bèn điểm năm nghìn quân ngự lâm giao cho Viên Thiệu. Thiệu nai nịt đem quân đi trước. Hà Tiến dẫn bọn Hà Ngung, Tuân Du, Trịnh Thái, hơn ba mươi quan đại thần đi sau, cùng vào trong cung. Đến trước linh cữu vua Linh Đế, lập thái tử Biện lên làm vua. Các quan tung hô xong đâu đấy, Viên Thiệu bèn đi vào cung bắt Kiển Thạc. Thạc kinh hoảng chạy nấp vào dưới bụi cây trong vườn ngự uyển, bị trung thường thị là Quách Thắng giết chết. Quân cấm binh do Thạc quản lĩnh đều ra hàng hết cả. Viên Thiệu nói với Hà Tiến rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Vien_Thieu",
            "character_name": "Viên Thiệu",
            "text": "Bọn thái giám trước kết bè với nhau, bây giờ nên thừa thế giết cả đi.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Bọn Trương Nhượng biết tin, sợ hãi hết hồn, vội chạy vào cung van lạy Hà Hậu rằng.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Truong_Nhuong",
            "character_name": "Trương Nhượng và đồng bọn",
            "text": "Bày mưu hại quốc cữu trước đây chỉ có một mình Kiển Thạc thực quả không dính dáng gì đến chúng tôi. Nay quốc cữu nghe lời Viên Thiệu, muốn giết hết cả chúng tôi, thật là oan quá, xin mẫu hậu rủ lòng thương cứu cho.",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "emotion": "ninh_bo_van_xin",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+6Hz",
            "rate": "+6%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "servile_flatterer"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Hà Hậu nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Ha_Hoang_Hau",
            "character_name": "Hà Hoàng Hậu",
            "text": "Các ngươi đừng lo, ta sẽ bảo hộ cho.",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+4Hz",
            "rate": "0%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Bèn giáng chỉ triệu Hà Tiến vào cung, khẽ bảo rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Ha_Hoang_Hau",
            "character_name": "Hà Hoàng Hậu",
            "text": "Anh em ta hàn vi từ thuở nhỏ, nếu không có bọn Trương Nhượng. Sao có phú quý ngày nay? Nay thằng Kiển Thạc bất nhân đã bị giết rồi, sao anh còn tin lời người ta nói mà toan giết cả bọn hoạn quan?",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+4Hz",
            "rate": "-2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Hà Tiến nghe đoạn, ra bảo các quan rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Kiển Thạc bày mưu hại ta đem giết cả họ nó đi. Còn những người khác đừng nên giết hại!",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "+2%",
            "lead_in_pause": "0.40s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Viên Thiệu nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Vien_Thieu",
            "character_name": "Viên Thiệu",
            "text": "Nhổ cỏ không nhổ hết rễ, rồi mang vạ vào thân!",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+3Hz",
            "rate": "+4%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 10,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Ý ta đã quyết, người đừng nhiều lời nữa!",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+6%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 10,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Các quan đều lui về cả. Hôm sau Thái Hậu cho Hà Tiến tham xét công việc các bộ thượng thư, còn các người khá đều được thăng chức.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        }
    ]
    entries.extend(c10_lines)

    # CHUNK 11
    c11_lines = [
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Đổng Thái Hậu nghe biết chuyện, bèn cho vời bọn Trương Nhượng vào cung phán rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Dong_Thai_Hau",
            "character_name": "Đổng Thái Hậu",
            "text": "Con em thằng Hà Tiến. Trước kia vì có ta cất nhắc cho nên, mới được sung sướng. Ngày nay con nó lên ngôi Hoàng Đế, các quan trong ngoài đều là vây cánh nó cả, uy thế nó to lắm. Ta biết tính sao bây giờ?",
            "age_stage": "lao_hoa",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+3Hz",
            "rate": "-4%",
            "lead_in_pause": "0.50s",
            "timbre_eq": "aged_gravel"
        },
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Trương Nhượng nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Truong_Nhuong",
            "character_name": "Trương Nhượng",
            "text": "Tâu mẫu hậu, việc đó cũng dễ. Xin mẫu hậu cứ ra ngự triều đường, rủ mành mành coi xét việc chính, phong hoàng tử Hiệp lên tước vương. Gia phong quốc cữu Đổng Trọng lên chức lớn coi giữ binh quyền. Và trọng dụng bọn hạ thần thì việc lớn có thể mưu tính xong được.",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "emotion": "ninh_bo_van_xin",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+4%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "servile_flatterer"
        },
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Đổng Thái Hậu cả mừng, sáng hôm sau lâm triều giáng chỉ phong hoàng tử Hiệp làm Trần lưu vương. Đổng Trọng làm phiêu kỵ tướng quân. Bọn Trương Nhượng cũng đều được tham dự triều chính. Hà Thái Hậu thấy Đổng Thái Hậu chuyên quyền, bèn sửa một tiệc yến ở trong cung, mời Đổng Thái Hậu đến dự. Giữa tiệc, Hà Thái Hậu đứng dậy, nâng chén rượu vái hai vái mà thưa rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Ha_Hoang_Hau",
            "character_name": "Hà Hoàng Hậu",
            "text": "Chúng ta đều là đàn bà. Không nên tham dự triều chính. Xưa bà Lã hậu chỉ vì tham giữ trọng quyền, đến nỗi nghìn người trong họ đều bị giết. Nay chúng ta chỉ nên ở yên trong cung cấm, việc triều chính đã có các nguyên lão đại thần bàn tính với nhau. Thế mới là hạnh phúc cho nhà nước, cúi xin Thái Hậu soi xét.",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+4Hz",
            "rate": "-2%",
            "lead_in_pause": "0.55s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Đổng Thái Hậu nổi giận mắng rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Dong_Thai_Hau",
            "character_name": "Đổng Thái Hậu",
            "text": "Mày đã đem lòng ghen ghét, đánh thuốc độc giết Vương mỹ nhân. Nay mày cậy có con làm vua, cậy thế lực anh mày là thằng Hà Tiến, dám nói hỗn với tao à? Tao sai quan phiêu kỵ, trỏ vào Đổng Trọng, chặt cổ anh mày dễ như trở bàn tay cho mà xem!",
            "age_stage": "lao_hoa",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+6%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Hà hậu cũng tức giận cãi lại rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Ha_Hoang_Hau",
            "character_name": "Hà Hoàng Hậu",
            "text": "Ta đem lời khuyên can, mà người lại trở mặt giận à?",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+5Hz",
            "rate": "+4%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Đổng Thái Hậu càng tức, lại nhiếc móc Hà hậu,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Dong_Thai_Hau",
            "character_name": "Đổng Thái Hậu",
            "text": "Cái đồ bán thịt nhà mày, còn biết cái gì!",
            "age_stage": "lao_hoa",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "cuong_no",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+6Hz",
            "rate": "+8%",
            "lead_in_pause": "0.30s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 11,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Hai người cãi nhau mãi, sau có bọn Trương Nhượng khuyên can, người nào mới về cung người nấy. Đêm hôm ấy Hà hậu triệu Hà Tiến vào cung, kể lại việc đã xảy ra. Tiến về mời các quan tam công đến bàn bạc. Buổi chầu sáng hôm sau, Tiến xui các đình thần tâu rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 11,
            "type": "dialogue",
            "speaker": "Cac_Quan_Dinh_Than",
            "character_name": "Các Đình Thần",
            "text": "Đổng Thái Hậu nguyên là một vị Phiên phi. Không nên ở lâu trong cung cấm. Xin rời ngay ra an trí ở Hà Giang, hạn lập tức phải đi ngay!",
            "age_stage": "trung_nien",
            "temperament": "khac_kho_lanh_lung",
            "emotion": "khac_kho_lanh_lung",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-4%",
            "lead_in_pause": "0.50s",
            "timbre_eq": "warm_authority"
        }
    ]
    entries.extend(c11_lines)

    # CHUNK 12
    c12_lines = [
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Hà Tiến một mặt sai người đưa Đổng Thái Hậu đi. Một mặt phái quân cấm binh đến vây nhà phiêu kỵ tướng quân Đổng Trọng đòi lấy ấn thụ. Đổng Trọng biết việc chẳng lành, liền tự vẫn ở hậu đường. Lúc người nhà cất tiếng khóc, quân sĩ mới không vây nữa trở về. Bọn Trương Nhượng, Đoàn Khuê thấy phe Đổng Thái Hậu thất bại, bèn đem vàng ngọc. Châu báu đút lót em trai Hà Tiến là Hà Miêu và mẹ Tiến là Vũ Dương Quân. Nhờ vào nói khéo với Hà Thái Hậu che chở cho. Bởi vậy, mười tên hoạn quan lại được tin dùng. Tháng sáu năm ấy, Hà Tiến ngầm sai người đến Hà Giang đánh thuốc độc giết Đổng Thái Hậu, đem linh cữu về kinh. Táng ở Văn Lăng. Tiến cáo bệnh không đi đưa đám. Một hôm quan tư lệ hiệu úy Viên Thiệu vào nói với Tiến rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Vien_Thieu",
            "character_name": "Viên Thiệu",
            "text": "Bọn Trương Nhượng. Đoàn Khuê đang đi nói phao lên rằng ông đánh thuốc độc giết Đổng Thái Hậu, để mưu việc lớn. Nếu bây giờ ông không giết ngay bọn chúng nó, tất có vạ lớn về sau. Xưa Đậu Vũ muốn nhờ bọn hoạn quan trong cung, vì mưu mô không kín lại bị chúng giết. Hiện giờ anh em vây cánh ông, đều là những tay anh tuấn, vả lại quyền ở trong tay, thật là cơ hội trời cho. Không nên bỏ lỡ.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.42s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Thong thả để sau sẽ bàn tính.",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-1Hz",
            "rate": "-2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Mấy đứa tả hữu nghe lỏm được chuyện ấy, liền đi báo với Trương Nhượng. Bọn Trương Nhượng lại đem rất nhiều của báu lễ đút Hà Miêu. Miêu vào tâu Hà hậu rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Ha_Mieu",
            "character_name": "Hà Miêu",
            "text": "Đại tướng quân phò tá vua mới, không làm điều nhân từ, chỉ chăm chém giết. Nay tự nhiên vô cớ lại toan giết cả mười hoạn quan, thật tự mình gây ra mầm loạn.",
            "age_stage": "thanh_xuan",
            "temperament": "xun_xoe_don_hen",
            "emotion": "xun_xoe_don_hen",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "servile_flatterer"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Hà hậu cho là phải. Một chốc, Hà Tiến vào tâu xin giết bọn hoạn quan. Hậu nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Ha_Hoang_Hau",
            "character_name": "Hà Hoàng Hậu",
            "text": "Bọn hoạn quan coi sóc việc trong cung cấm, phép cũ nhà Hán từ xưa vẫn thế. Cớ sao tiên đế vừa mới chầu trời mà người chỉ muốn giết những bầy tôi cũ. Thế không phải là tôn trọng sự thờ cúng đối với tiên đế!",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "binh_than_tu_nhien",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+4Hz",
            "rate": "-2%",
            "lead_in_pause": "0.45s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến vốn là một người nhù nhờ không quyết đoán, nghe Hà Thái Hậu nói như vậy, vâng dạ luôn miệng rồi lui ra. Viên Thiệu đứng đón ngoài cửa, hỏi rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Vien_Thieu",
            "character_name": "Viên Thiệu",
            "text": "Việc lớn thế nào?",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "hoi_hop_thi_thao",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.38s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Thái Hậu không nghe thì làm thế nào?",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "emotion": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-2%",
            "lead_in_pause": "0.42s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Thiệu nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Vien_Thieu",
            "character_name": "Viên Thiệu",
            "text": "Nên triệu những người anh hùng các nơi đem quân về kinh giết hết bọn hoạn quan này đi. Đến lúc việc đã cấp bách thì Thái Hậu muốn chẳng nghe cũng chẳng được.",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "emotion": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.40s",
            "timbre_eq": "chest_resonance"
        },
        {
            "chunk_id": 12,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 12,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Kế ấy diệu lắm.",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "hoan_ca_dac_thang",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+2%",
            "lead_in_pause": "0.35s",
            "timbre_eq": "tyrant_arrogant"
        }
    ]
    entries.extend(c12_lines)

    # CHUNK 13
    c13_lines = [
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Bèn truyền hịch đi các trấn, triệu các tướng lĩnh đem quân về kinh đô. Quan chủ bạ Trần Lâm can rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 13,
            "type": "dialogue",
            "speaker": "Tran_Lam",
            "character_name": "Trần Lâm",
            "text": "Việc ấy không nên. Tục ngữ có câu, Bưng mắt bắt chim, ấy là mình tự dối mình. Việc nhỏ mọn cũng không thể tự dối mà làm xong, huống chi là việc lớn nước nhà? Nay tướng quân dựa uy vua, cầm quyền lớn, như rồng bay hổ nhảy, muốn làm thế nào cũng được. Việc giết bọn hoạn quan thật dễ không khác quạt lò than đốt mấy sợi tóc. Làm việc một cách quyền biến, quyết đoán ngay, phát động nhanh như sấm sét tức là thuận đạo trời và lòng người. Nay nếu triệu các quan ngoại trấn, mỗi người một bụng, biết ai thế nào? Có khác đưa chuôi dao cho người cầm mà mình cầm đằng lưỡi không? Như thế không những việc không thành mà lại sinh biến loạn nữa.",
            "age_stage": "thanh_xuan",
            "temperament": "khac_kho_lanh_lung",
            "emotion": "khac_kho_lanh_lung",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-4%",
            "lead_in_pause": "0.50s",
            "timbre_eq": "warm_authority"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Tiến cười nói,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 13,
            "type": "dialogue",
            "speaker": "Ha_Tien",
            "character_name": "Hà Tiến",
            "text": "Đó là kiến thức của hạng người hèn nhát!",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "emotion": "mia_mai_cham_biem",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+6%",
            "lead_in_pause": "0.32s",
            "timbre_eq": "tyrant_arrogant"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Một người đứng lên vỗ tay cười lớn mà rằng,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 13,
            "type": "dialogue",
            "speaker": "Tao_Thao",
            "character_name": "Tào Tháo",
            "text": "Việc ấy dễ như trở bàn tay, hà tất phải bàn cho lắm!",
            "age_stage": "thanh_xuan",
            "temperament": "giao_hoat_nham_hiem",
            "emotion": "mia_mai_cham_biem",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+2Hz",
            "rate": "+4%",
            "lead_in_pause": "0.30s",
            "timbre_eq": "sharp_cunning"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "epic",
            "text": "Mọi người nhìn xem ai, người ấy chính là Tào Tháo.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "+1Hz",
            "rate": "+0%",
            "lead_in_pause": "0.28s",
            "timbre_eq": "epic_narrator"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": "Đó chính là,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "0.85s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": ". ......",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "1.50s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 13,
            "type": "poem",
            "speaker": "Narrator",
            "text": "Muốn giết tiểu nhân, bên cạnh chúa,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-18%",
            "lead_in_pause": "0.85s",
            "timbre_eq": "poetic_recitation"
        },
        {
            "chunk_id": 13,
            "type": "poem",
            "speaker": "Narrator",
            "text": "Nên nghe mưu sĩ, ở trong triều.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-18%",
            "lead_in_pause": "0.85s",
            "timbre_eq": "poetic_recitation"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": ". ......",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "1.50s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": "Muốn biết Tào Tháo nói thế nào,",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "0.65s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": ". ......",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "1.50s",
            "timbre_eq": "contemplative_narrator"
        },
        {
            "chunk_id": 13,
            "type": "narrator",
            "speaker": "Narrator",
            "narrative_mode": "contemplative",
            "text": "xem hồi sau sẽ rõ.",
            "voice": "vi-VN-NamMinhNeural",
            "pitch": "-2Hz",
            "rate": "-12%",
            "lead_in_pause": "0.65s",
            "timbre_eq": "contemplative_narrator"
        }
    ]
    entries.extend(c13_lines)

    for idx, e in enumerate(entries):
        e["line_id"] = idx + 1

    return entries

def verify_fidelity(entries):
    for c_id in range(1, 14):
        raw_text = load_chunk(c_id)
        raw_norm = re.sub(r'\s+', ' ', raw_text).strip()
        
        c_entries = [e for e in entries if e["chunk_id"] == c_id]
        rec_text = " ".join(e["text"] for e in c_entries)
        rec_norm = re.sub(r'\s+', ' ', rec_text).strip()
        
        if raw_norm != rec_norm:
            print(f"FAILED FIDELITY on Chunk {c_id}:")
            for i in range(min(len(raw_norm), len(rec_norm))):
                if raw_norm[i] != rec_norm[i]:
                    print(f"Diff at char {i}:")
                    print("RAW:", raw_norm[max(0, i-30):i+50])
                    print("REC:", rec_norm[max(0, i-30):i+50])
                    break
            return False
    print("VERIFICATION SUCCESS: 100% Text Fidelity across all 13 chunks!")
    return True

def generate_bible(entries):
    bible = {
        "chapter_folder": "02-Hoi-02",
        "chapter_index": 2,
        "chapter_title": "Hồi 2: Trương Dực Đức giận đánh đốc bưu; Hà Quốc Cửu mưu giết quan hoạn",
        "work_title": "Tam Quốc Diễn Nghĩa",
        "genre": "classical_epic_literature",
        "total_theatrical_lines": len(entries),
        "narrator_lines": len([e for e in entries if e["type"] == "narrator"]),
        "poem_lines": len([e for e in entries if e["type"] == "poem"]),
        "dialogue_lines": len([e for e in entries if e["type"] == "dialogue"]),
        "acoustic_specification": {
            "pitch_scale": {
                "min_pitch": "-8Hz",
                "max_pitch": "+12Hz",
                "contrast_range_hz": 20
            },
            "rate_scale": {
                "min_rate": "-20%",
                "max_rate": "+15%"
            },
            "handoff_matrix": {
                "instant_interruption": "0.30s - 0.35s",
                "urgent_lead_in": "0.35s - 0.40s",
                "natural_dialogue_turn": "0.42s - 0.50s",
                "dialogue_resonance": "0.50s - 0.60s",
                "pensive_lead_in": "0.60s - 0.75s",
                "regal_ceremony": "0.70s - 0.85s",
                "dramatic_silence": "0.85s - 1.20s",
                "poetic_cushion": "0.85s - 1.80s"
            },
            "dsp_presets": {
                "chest_resonance": "Trương Phi, Viên Thiệu, dũng tướng kiêu hùng (Boost 160Hz +5dB, Boost 300Hz +2.5dB, Dip 3.5kHz -3dB)",
                "warm_authority": "Lưu Bị, Quan Vũ, Chu Tuấn, Hà Hoàng Hậu (Boost 280Hz +3.5dB, Boost 2.2kHz +2dB, Dip 4.5kHz -2.5dB)",
                "sharp_cunning": "Tào Tháo, Kiển Thạc (High-pass 220Hz, Boost 2.8kHz +4.5dB, Boost 5.5kHz +3dB)",
                "aged_gravel": "Trần Đam, Đổng Thái Hậu, Lão dân làng (Boost 420Hz +4.5dB, Low-pass 4.2kHz, Dip 1.2kHz -3dB)",
                "tyrant_arrogant": "Hán Linh Đế, Hà Tiến, Viên Đốc Bưu hách dịch (Boost 190Hz +4.5dB, Boost 1.8kHz +4dB, Boost 4kHz +2dB)",
                "servile_flatterer": "Trương Nhượng, Hà Miêu, Đốc Bưu van lạy (High-pass 320Hz, Boost 2.6kHz +4dB, Boost 4.8kHz +3.5dB)",
                "tragic_grief": "Lưu Đào can gián khóc than (Boost 320Hz +4dB, Dip 1.6kHz -3.5dB, Low-pass 4.8kHz)",
                "youth_bright": "Tôn Kiên thiếu niên 17 tuổi (High-pass 280Hz, Boost 3.8kHz +4.5dB, Boost 6.5kHz +2.5dB)",
                "poetic_recitation": "Ngâm vịnh thi ca kết hồi (Boost 220Hz +3dB, Boost 3.2kHz +2dB, High-shelf 8kHz -3dB)"
            }
        },
        "characters": {}
    }

    narrator_entries = [e for e in entries if e["type"] == "narrator"]
    modes = sorted(list(set(e.get("narrative_mode", "epic") for e in narrator_entries)))
    bible["characters"]["Narrator"] = {
        "name": "Người dẫn chuyện",
        "gender": "male",
        "voice": "vi-VN-NamMinhNeural",
        "base_pitch": "+0Hz",
        "base_rate": "-5%",
        "narrative_modes": modes,
        "timbre_eq": "epic_narrator",
        "dialogue_count": len(narrator_entries)
    }

    dia_entries = [e for e in entries if e["type"] == "dialogue"]
    spk_groups = {}
    for d in dia_entries:
        spk = d["speaker"]
        if spk not in spk_groups:
            spk_groups[spk] = []
        spk_groups[spk].append(d)

    bible["characters_cast_count"] = len(spk_groups)

    for spk, items in spk_groups.items():
        sample = items[0]
        emotions = sorted(list(set(x["emotion"] for x in items if "emotion" in x)))
        bible["characters"][spk] = {
            "name": sample.get("character_name", spk),
            "gender": "female" if spk in ["Ha_Hoang_Hau", "Dong_Thai_Hau"] else "male",
            "age_stage": sample.get("age_stage", "thanh_xuan"),
            "temperament": sample.get("temperament", "anh_hung_hao_sang"),
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": sample.get("pitch", "0Hz"),
            "base_rate": sample.get("rate", "0%"),
            "timbre_eq": sample.get("timbre_eq", "warm_authority"),
            "sample_emotions": emotions,
            "dialogue_count": len(items)
        }

    return bible

def main():
    entries = build_entries()
    if not verify_fidelity(entries):
        raise SystemExit(1)
    
    bible = generate_bible(entries)

    script_path = os.path.join(CHAPTER_DIR, "theatrical_script.json")
    bible_path = os.path.join(CHAPTER_DIR, ".theatrical_bible.json")

    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(entries)} theatrical lines to {script_path}")

    with open(bible_path, "w", encoding="utf-8") as f:
        json.dump(bible, f, ensure_ascii=False, indent=2)
    print(f"Saved theatrical bible to {bible_path}")

    print("\nSummary Statistics:")
    print(f"- Total lines: {len(entries)}")
    print(f"- Narrator lines: {bible['narrator_lines']}")
    print(f"- Poem lines: {bible['poem_lines']}")
    print(f"- Dialogue lines: {bible['dialogue_lines']}")
    print(f"- Cast count: {bible['characters_cast_count']} characters")
    for spk, data in bible["characters"].items():
        if spk == "Narrator":
            continue
        print(f"  * {data['name']} ({spk}): {data['dialogue_count']} câu, EQ: {data['timbre_eq']}, Tuổi: {data['age_stage']}, Khí chất: {data['temperament']}")

if __name__ == "__main__":
    main()
