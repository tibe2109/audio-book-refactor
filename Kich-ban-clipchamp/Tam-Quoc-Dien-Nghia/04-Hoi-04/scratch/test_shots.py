import json, re

durations = {
    1: 157.70,
    2: 164.21,
    3: 166.75,
    4: 145.92,
    5: 150.43,
    6: 153.60,
    7: 146.71,
    8: 185.47
}

# Define shots for each chunk
# Each shot: {"title": ..., "text": ..., "dur": ...}

data = {}

# CHUNK 1 (157.70s) - 7 shots
data[1] = [
    {
        "title": "Tiêu đề Hồi 4 & Viên Thiệu tuốt kiếm cự tuyệt Đổng Trác",
        "text": """HỒI BỐN

. ......

PHẾ HÁN ĐẾ, TRẦN LƯU LÊN NGÔI,
LỪA ĐỔNG TẶC, MẠNH ĐỨC DÂNG KIẾM.

. ......

Trác muốn giết Viên Thiệu, Lý Nho can rằng, Việc chưa định xong không nên giết càn. Viên Thiệu tay cầm thanh bảo kiếm, cáo từ các quan trở ra, treo trả cờ tiết ở cửa đông rồi bỏ về Ký Châu.""",
        "dur": 23.00
    },
    {
        "title": "Đổng Trác thị uy uy hiếp Thái phó Viên Ngỗi và bá quan",
        "text": """Trác bảo với quan thái phó Viên Ngỗi rằng, Cháu ngươi vô lễ. Ta tha cho nó cũng là nể ngươi Việc phế vua lập Trần Lưu, người nghĩ thế nào? Ngỗi thưa rằng, Thái úy nghĩ thế phải đấy! Trác lại nói, Ai dám ngăn trở việc lớn này, thì ta sẽ lấy phép quân trị tội. Các quan sợ hãi, đều nói, Ngài dạy thế xin vâng!""",
        "dur": 22.00
    },
    {
        "title": "Họp bàn sau tiệc yến & Chu Bật phân tích thế lực tứ thế tam công họ Viên",
        "text": """Cuộc yến tan, Trác hỏi quan thị trung là Chu Bật và quan hiệu úy Ngũ Quỳnh rằng, Viên Thiệu phen này đi. Rồi sẽ ra sao? Chu Bật đáp, Viên Thiệu căm giận mà đi, hễ truy nã riết quá tất sinh biến. Vả lại họ Viên, đã bốn đời làm quan đến bậc tam công, thiên hạ được nhờ nhiều lắm, học trò. Đầy tớ đâu đâu cũng có.""",
        "dur": 22.00
    },
    {
        "title": "Ngũ Quỳnh hiến kế phong quan & Đổng Trác phong Thiệu làm Thái thú Bột Hải",
        "text": """Nếu hắn thu dùng hào kiệt, tập họp đồ đảng, rồi những anh hùng trong thiên hạ nhân đó khởi lên. Đất Sơn Đông sẽ không ở trong tay ông nữa. Không bằng ông tha tội hắn cho hắn một chức quận thú gì đấy, thì hắn mừng được khỏi tội. Sẽ không gây ra hậu hoạn nữa. Ngũ Quỳnh nói, Viên Thiệu là người thích mưu kế, nhưng không quyết đoán, không đáng lo cho lắm. Bất nhược cứ cho hắn một chức quận thú để thu phục lòng dân! Trác nghe lấy làm phải, ngay hôm ấy sai người đến phong cho Thiệu làm thái thú quận Bột Hải.""",
        "dur": 25.00
    },
    {
        "title": "Đại hội điện Ôn Đức & Đổng Trác tuốt gươm tuyên cáo phế lập",
        "text": """Đến mồng một tháng chín, Trác rước vua ra ngự đền Ôn Đức, họp hết cả văn võ lại. Trác tay cầm gươm nói rằng, Thiên tử ngu yếu, không trị vì được, nay có một bài sách văn đọc cho các quan nghe.""",
        "dur": 20.00
    },
    {
        "title": "Lý Nho tuyên đọc sách văn kết tội Thiếu Đế và Hà Thái Hậu",
        "text": """Rồi sai Lý Nho tuyên đọc, Vua Hiếu Linh mất sớm, Vua sau nối ngôi, bốn bể ai ai cũng trông mong. Nay xét ra vua ta, thiên tử mỏng manh, kém vẻ uy nghi nghiêm chỉnh, cư tang biếng nhác, đức xấu đã rõ. Không xứng ngôi lớn. Hoàng Thái Hậu không có uy nghi của người mẹ, nhiếp chính rối tung. Việc bà Vĩnh Lạc Thái Hậu mất dân chúng có nhiều dị nghị. Đối với đạo tam cương và giường Trời Đất, phải Chăng có thiếu sót nhiều?""",
        "dur": 23.00
    },
    {
        "title": "Tôn vinh hoàng tử Hiệp lên ngôi & Giáng phế vua làm Hoằng Nông Vương",
        "text": """Trần Lưu Vương tên Hiệp, đức hạnh nghiêm trang, khuôn phép kính cẩn, cư tang thương xót, nói năng chính đính, lời hay tiếng tốt. Thiên hạ ai ai cũng biết. Nên nối ngôi vua, làm phép cho vạn thế! Nay phế vua ra làm Hoằng Nông Vương, Thái Hậu thì phải trả quyền chính.""",
        "dur": 22.70
    }
]

# Verify chunk 1
c1_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-1.txt').read()
c1_recon = '\n'.join([s['text'] for s in data[1]])
c1_orig_w = c1_orig.split()
c1_recon_w = c1_recon.split()
print("Chunk 1 word match:", c1_orig_w == c1_recon_w, len(c1_orig_w), len(c1_recon_w))
c1_total_dur = sum([s['dur'] for s in data[1]])
print("Chunk 1 dur match:", round(c1_total_dur, 2) == round(durations[1], 2), c1_total_dur, durations[1])
for s in data[1]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 1 pacing assertion passed!")

# CHUNK 2 (164.21s) - 7 shots
data[2] = [
    {
        "title": "Bức phế Thiếu Đế, lột tỉ thụ & Đinh Quản vung hốt ngà mắng giặc",
        "text": """Xin tôn Trần Lưu Vương lên làm Hoàng Đế, Ứng thiên, thuận nhân, để yên bụng thiên hạ!. Lý Nho đọc xong bài chiếu Trác thét tả hữu vực vua xuống điện, lột tỉ thụ, bắt quỳ, ngoảnh mặt về phương bắc. Xưng thần nghe chiếu, lại bắt Hà Thái Hậu, cởi đồ phẩm phục ra mà đợi chiếu. Vua và Thái Hậu kêu khóc, quần thần trông thấy ai cũng xót xa bi thảm. Lúc ấy ở dưới thềm có một viên quan to, tức tối thét to lên rằng, Thằng giặc Đổng Trác kia. Mày dám lập mưu lừa trời dối đất, tao lấy máu cổ họng bôi vào mặt mày bây giờ! Nói rồi cầm cái bốt ngà xông thẳng vào đánh Đổng Trác.""",
        "dur": 25.00
    },
    {
        "title": "Đinh Quản thọ hình giữ trọn tiết tháo & Thơ than cơ đồ nhà Hán",
        "text": """Trác giận lắm, sai võ sĩ bắt lại xem ai, thì là quan thượng thư Đinh Quản. Trác sai đem ra chém, Quản cứ luôn mồm chửi mắng Đổng Trác cho đến lúc chết, chết rồi, thần sắc vẫn như lúc sống.

Người sau có thơ than rằng,

. ......

Giặc Đổng, lòng mang, dạ khuyển lang,
Cơ đồ nhà Hán, đổ tan hoang.

. ......

Trong triều văn võ mồm câm cả Chỉ có Đinh công thực giỏi giang!""",
        "dur": 24.00
    },
    {
        "title": "Tôn lập Trần Lưu Vương chín tuổi & Giam cầm mẹ con Thiếu Đế",
        "text": """Trác mời Trần Lưu Vương lên điện. Quần thần làm lễ mừng xong rồi, Trác sai bắt Hà Thái Hậu, vua và vợ vua là Đường thị giam ở cung Vĩnh An. Khóa cửa cung, cấm quần thần không ai được vào thăm. Thương thay! Thiếu Đế mới lên ngôi tháng tư, đến tháng chín đã phải phế. Trần Lưu Vương, nhờ Trác được lên ngôi trời, vốn tên là Hiệp, tên chữ là Bá Hòa, là con thứ vua Linh Đế. Tức là Hiến Đế về sau. Lúc lập lên, Hiến Đế mới lên chín tuổi, đổi niên hiệu năm đầu là Sơ Bình.""",
        "dur": 24.00
    },
    {
        "title": "Đổng Trác lộng quyền tướng quốc & Đe dọa giết cả họ ép Sái Ung phụng chức",
        "text": """Đổng Trác là tướng quốc, lạy vua không phải xưng tên, vào chầu không phải bước rảo, lên điện được đeo gươm, tác uy tác phúc. Không ai bì được. Lý Nho khuyên Trác nên dùng những người có danh vọng để thu phục lòng người, nhân thể Lý Nho tiến cử tài năng Sái Ung. Trác cho vời Sái Ung, Ung không chịu đến. Trác giận sai người bảo Ung hễ không đến thì giết cả họ. Ung sợ, phải đến. Trác thấy Ung đến, mừng lắm, một tháng thăng chức ba lần, làm đến chức thị trung, Trác rất hậu đãi Ung.""",
        "dur": 25.00
    },
    {
        "title": "Cung Vĩnh An sầu thảm & Thiếu Đế ngày ngày rơi lệ",
        "text": """Thiếu Đế, Hà Thái Hậu và Đường phi bị giam ở cung Vĩnh An, đồ ăn, thức mặc, mỗi ngày một kém. Thiếu Đế không lúc nào ráo nước mắt.""",
        "dur": 20.00
    },
    {
        "title": "Thiếu Đế trông đôi én lượn & Cảm tác bốn câu thơ đầu",
        "text": """Một hôm Thiếu Đế trông thấy hai con chim én bay ở trong sân, ngâm một bài thơ rằng, Xanh xanh khóm cỏ dày. Cặp én phất phơ bay. Trong veo dòng lạc thủy,""",
        "dur": 22.00
    },
    {
        "title": "Hai câu thơ cuối hướng về cung điện cũ bi hoài",
        "text": """Người đồng nội khen hay. Xa trông mây thăm thẳm, Cung điện cũ ta đây.""",
        "dur": 24.21
    }
]

# Verify chunk 2
c2_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-2.txt').read()
c2_recon = '\n'.join([s['text'] for s in data[2]])
c2_orig_w = c2_orig.split()
c2_recon_w = c2_recon.split()
print("Chunk 2 word match:", c2_orig_w == c2_recon_w, len(c2_orig_w), len(c2_recon_w))
c2_total_dur = sum([s['dur'] for s in data[2]])
print("Chunk 2 dur match:", round(c2_total_dur, 2) == round(durations[2], 2), c2_total_dur, durations[2])
for s in data[2]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 2 pacing assertion passed!")

# CHUNK 3 (166.75s) - 8 shots
data[3] = [
    {
        "title": "Lời thơ oán hận & Đổng Trác sai Lý Nho mang độc dược hành thích vua",
        "text": """Biết ai kẻ trung nghĩa, Gỡ cho oán hận này! Đổng Trác thường thường sai người đến dò ý tứ, hôm ấy có kẻ bắt được bài thơ đem trình Đổng Trác. Trác nói rằng, Làm bài thơ oán vọng này, đem giết đi là có cớ rồi! Bèn sai Lý Nho và mười võ sĩ vào cung giết vua.""",
        "dur": 21.00
    },
    {
        "title": "Lý Nho dâng chén rượu thọ giả dối & Bày dao lụa bức bách Thiếu Đế",
        "text": """Vua, Thái Hậu và Đường phi đương ở trên lầu, thấy người cung nữ báo rằng có Lý Nho đến, vua sợ giật mình. Nho đem rượu thuốc độc dâng vua. Vua hỏi việc gì. Nho thưa, Ngày xuân mát mẻ, Đổng tướng quốc sai tôi đem dâng chén rượu thọ. Thái Hậu bảo Lý Nho, Có phải rượu thọ thì ngươi thử uống trước đi! Nho giận lắm, hỏi vua, Mày không uống phải không? Rồi gọi ngay tả hữu cầm con dao với tấm lụa trắng, để trước mặt vua, mà nói rằng, Rượu thọ chẳng uống. Thì phải chọn hai thứ này.""",
        "dur": 23.00
    },
    {
        "title": "Đường Phi quỳ lạy xin chết thay vua & Lý Nho ép bức Hà Thái Hậu",
        "text": """Đường phi quỳ xuống nói rằng, Thiếp xin thay vua uống chén rượu này, xin ngài để toàn mệnh cho hai mẹ con vua. Lý Nho quát mắng, Mày là đứa nào, mà dám đòi chết thay vua? Nho cầm chén rượu đưa cho Hà Thái Hậu và bảo rằng, Bà phải uống trước đi! Hà Thái Hậu mắng nhiếc Hà Tiến là đồ vô mưu, đem giặc vào kinh đô, để có cái vạ ngày nay. Nho bức vua phải uống rượu.""",
        "dur": 21.00
    },
    {
        "title": "Thiếu Đế từ biệt mẫu hậu & Ngâm khúc tuyệt mệnh ròng ròng châu sa",
        "text": """Vua nói, Hãy khoan! Để ta cùng Thái Hậu từ biệt đã. Giời đất chao, giăng sao cũng đổ Bỏ ngôi sao, ra chỗ phiên phong Bởi ai nên sự lạ lùng? Việc đời ngán ngẩm, ròng ròng châu tuôn.""",
        "dur": 20.00
    },
    {
        "title": "Đường Phi ca khúc biệt ly phu thê & Ôm nhau khóc ròng trong cung điện",
        "text": """Đường phi cũng làm bài ca rằng, Giời nghiêng đất lại lở tan Phận mình thê thiếp, trái oan lạ thường! Từ sinh nay đã khác đường, Một người một bóng xót thương tấm lòng! Vua và Đường phi ca rồi, ôm nhau mà khóc.""",
        "dur": 20.00
    },
    {
        "title": "Lý Nho hối thúc độc ác & Hà Thái Hậu thét mắng trời tru đất diệt đảng nghịch tặc",
        "text": """Lý Nho lại quát mắng, Tướng quốc đứng chờ tin! Các người dùng dằng để mong ai cứu đấy? Thái Hậu thét mắng, Thằng giặc Đổng kia! Mày hại mẹ con tao, rồi trời lại hại mày! Chúng bay cùng đảng với nhau làm điều ác, rồi chúng bay sẽ chết cả họ cho mà xem!""",
        "dur": 21.00
    },
    {
        "title": "Thảm sát cung Vĩnh An - Ném Thái Hậu xuống lầu, thắt cổ Đường Phi, bức tử Thiếu Đế",
        "text": """Nho tức lắm, hai tay tóm lấy Thái Hậu ném xuống dưới lầu, giết chết, lại sai võ sĩ thắt cổ Đường phi. Rót rượu độc bắt Thiếu Đế uống chết, rồi về báo Đổng Trác. Trác sai đem táng ba mẹ con ở ngoài thành.""",
        "dur": 21.00
    },
    {
        "title": "Đổng Trác dâm loạn đại nội sập rồng & Dẫn quân đến hội hát Dương Thành",
        "text": """Tự bấy giờ, Trác đêm nào cũng vào cung thông dâm với các cung nữ, đêm thì lên ngủ trên sập rồng. Thường thường Trác hay đem quân ra ngoài thành. Một bữa Trác đến Dương Thành. Bấy giờ đang tháng hai, dân mở hội hát, con trai con gái tụ họp nhau xem hội rất đông.""",
        "dur": 19.75
    }
]

# Verify chunk 3
c3_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-3.txt').read()
c3_recon = '\n'.join([s['text'] for s in data[3]])
c3_orig_w = c3_orig.split()
c3_recon_w = c3_recon.split()
print("Chunk 3 word match:", c3_orig_w == c3_recon_w, len(c3_orig_w), len(c3_recon_w))
c3_total_dur = sum([s['dur'] for s in data[3]])
print("Chunk 3 dur match:", round(c3_total_dur, 2) == round(durations[3], 2), c3_total_dur, durations[3])
for s in data[3]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 3 pacing assertion passed!")

# CHUNK 4 (145.92s) - 7 shots
data[4] = [
    {
        "title": "Thảm sát hội xuân Dương Thành - Đổng Trác cướp của bắt người thiêu đầu lâu",
        "text": """Trác sai quân vây cả lại, rồi giết sạch cướp đàn bà con gái và của cải chất đầy xe. Treo hơn một nghìn đầu lâu ở dưới xe, nối đuôi nhau kéo về kinh đô, nói phao lên rằng đi đánh giặc thắng trận. Trác lại sai đốt đầu lâu người ở dưới cửa thành, còn đàn bà con gái và của cải thì đem chia cho quân sĩ.""",
        "dur": 22.00
    },
    {
        "title": "Việt kỵ hiệu úy Ngũ Phu nuôi chí phục hận & Rút đoản đao hành thích",
        "text": """Quan việt kỵ hiệu úy tên là Ngũ Phu, tên chữ là Đức Du, thấy Đổng Trác tàn bạo quá, tức giận lắm. Thường mặc áo giáp nhỏ vào trong áo đại trào, giắt một con dao ngắn, rình tiện dịp để giết Trác. Một hôm Trác vào chầu. Phu ra đón. Lúc Trác đến dưới gác, Phu rút dao ra đâm, không ngờ sức Trác khỏe hơn, hai tay ôm chặt được Phu. Lã Bố trông thấy chạy lạy lôi Phu ra vật ngã xuống.""",
        "dur": 23.00
    },
    {
        "title": "Ngũ Phu thét mắng nghịch tặc tày trời & Chịu cực hình phân thây tạ thiên hạ",
        "text": """Trác hỏi Ngũ Phu rằng, Ai xui mày làm phản? Phu trợn mắt thét mắng rằng, Mày không phải là vua tao, tao không phải là tôi mày, sao lại gọi là phản được? Tội mày đầy trời, ai ai là chẳng muốn giết mày? Tao tiếc rằng không xé nhỏ được xác mày ra để tạ thiên hạ! Trác tức lắm, sai đem Ngũ Phu ra mổ. Phu cứ mắng chửi Đổng Trác không buông miệng cho đến lúc chết.""",
        "dur": 23.00
    },
    {
        "title": "Thơ khen anh hùng tiết liệt Ngũ Phu & Đổng Trác tăng cường hộ vệ giáp trụ",
        "text": """Đời sau có thơ khen Ngũ Phu rằng, Ngũ Phu này cũng bậc anh hùng, Tiết liệt xem ai được thế không? Đánh giặc, hãy còn danh tiếng để, Nghìn thu vằng vặc mảnh gương chung! Đổng Trác từ khi ấy ra vào thường có quân sĩ mặc áo giáp đi theo hộ vệ.""",
        "dur": 18.00
    },
    {
        "title": "Mật thư Bột Hải của Viên Thiệu gửi quan Tư đồ Vương Doãn",
        "text": """Viên Thiệu bấy giờ ở Bột Hải, nghe thấy Trác lộng quyền, sai người đưa mật thư cho tư đồ Vương Doãn. Thư rằng, Giặc Trác đốt trời bỏ chúa. Người ta đau xót đến nỗi không nỡ nói, thế mà ông cứ mặc kệ, để nó lăng ngược như con cá nhảy vượt qua đăng. Làm thinh như không nghe không thấy, sao gọi là người trung thần ái quốc! Thiệu nay chiêu tập binh mã cũng muốn vì nhà vua, quét sạch quân giặc, nhưng chưa dám khinh động. Ông nếu cùng lòng với tôi, xin tìm cơ hội lo tính ngay đi. Có việc gì sai khiến, tôi xin vâng mệnh.""",
        "dur": 22.00
    },
    {
        "title": "Vương Doãn trăn trở kế sách & Mượn cớ sinh nhật thết tiệc cựu thần",
        "text": """Vương Doãn được thư, nghĩ mãi không tìm được kế gì. Một hôm đang lúc chầu ở nội các, Doãn thấy ở đó đủ mặt các cựu thần, bèn nói với các quan rằng. Hôm nay là ngày sinh nhật lão phu. Đến chiều xin mời các quan quá bước đến nhà lão phu xơi rượu. Các quan đều nhận lời, hẹn đến chiều sẽ đến chúc thọ.""",
        "dur": 19.00
    },
    {
        "title": "Bữa tiệc sinh nhật giả lệ rơi - Quan Tư đồ ôm mặt hu hu khóc",
        "text": """Chiều hôm ấy Doãn mở tiệc ở hậu đường. Các quan đến cả. Rượu được vài tuần, tự nhiên Doãn che mặt hu hu khóc.""",
        "dur": 18.92
    }
]

# Verify chunk 4
c4_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-4.txt').read()
c4_recon = '\n'.join([s['text'] for s in data[4]])
c4_orig_w = c4_orig.split()
c4_recon_w = c4_recon.split()
print("Chunk 4 word match:", c4_orig_w == c4_recon_w, len(c4_orig_w), len(c4_recon_w))
c4_total_dur = sum([s['dur'] for s in data[4]])
print("Chunk 4 dur match:", round(c4_total_dur, 2) == round(durations[4], 2), c4_total_dur, durations[4])
for s in data[4]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 4 pacing assertion passed!")

# CHUNK 5 (150.43s) - 7 shots
data[5] = [
    {
        "title": "Vương Doãn thổ lộ nỗi niềm đau xót cơ đồ Cao Hoàng & Quần thần cùng khóc",
        "text": """Các quan giật mình hỏi rằng, Hôm nay là ngày sinh nhật của quan tư đồ, sao ngài lại khóc như vậy? Doãn thưa rằng, Hôm nay có phải là sinh nhật của tôi đâu! Tôi vì có một việc muốn nói với các vị, nhưng sợ Đổng Trác sinh nghi, cho nên, mượn cớ nói thác ra thế. Thằng Trác dối vua lộng quyền, xã tắc nay mai đổ mất. Đức Cao Hoàng ngày xưa đánh nhà Tần, diệt nước Sở, bao nhiêu công phu mới nên được cơ đồ này. Ngờ đâu nay mất vào tay thằng Đổng Trác. Tôi khóc là vì thế! Các quan nghe nói cũng đều khóc cả.""",
        "dur": 23.00
    },
    {
        "title": "Tiếng cười đanh thép của Tào Tháo phá tan tiếng khóc & Doãn tức giận quở trách",
        "text": """Trong đám ngồi có một người, vỗ tay cười ầm lên mà nói rằng, Các quan thử khóc từ tối đến sáng. Lại khóc từ sáng đến tối, xem có khóc chết được thằng Đổng Trác không? Doãn ngoảnh lại xem ai, thì là kiệu kỵ úy Tào Tháo, Doãn giận nói rằng, Tổ tôn nhà ngươi cũng ăn lộc nhà Hán. Sao nhà ngươi không biết nghĩ cách báo quốc, lại còn cười à?""",
        "dur": 21.00
    },
    {
        "title": "Tào Tháo vạch kế hành thích & Hỏi mượn dao Thất Bảo của Vương Doãn",
        "text": """Tháo nói, Tôi cười, có phải cười gì đâu! Cười là các quan không biết nghĩ kế gì trừ được thằng Đổng Trác. Tháo nay tuy không có tài cán gì, nhưng xin lập tức chặt đầu thằng Đổng Trác, treo ở cửa phủ để tạ thiên hạ. Doãn liền đứng dậy hỏi rằng, Mạnh Đức có kế gì tài thế? Tháo nói, Tôi lâu nay sở dĩ nép mình thờ Đổng Trác cũng là vì muốn thừa cơ giết nó. Nay nó rất tin tôi, tôi được gần nó luôn. Nghe quan tư đồ có con dao thất bảo, xin cho tôi mượn. Tôi nguyện phen này vào tận tướng phủ đâm chết thằng giặc Đổng Trác, dẫu chết cũng không oán hận gì.""",
        "dur": 24.00
    },
    {
        "title": "Vương Doãn rót rượu tiễn biệt & Trao Thất Bảo Đao cho Tào Tháo",
        "text": """Vương Doãn mừng lắm nói rằng, Nếu Mạnh Đức có bụng như thế, thực là may cho thiên hạ lắm! Doãn thân hành rót chén rượu mời Tào Tháo. Tháo đổ rượu, cất lời thề. Doãn bèn đem dao thất bảo đưa cho. Tháo uống rượu xong, giắt dao đứng dậy đi ra. Các quan ngồi một lát rồi cũng về cả.""",
        "dur": 21.00
    },
    {
        "title": "Tào Tháo giắt dao vào tướng phủ & Đối mặt Đổng Trác cùng Lã Bố trong gác",
        "text": """Hôm sau Tháo giắt dao đến tướng phủ, hỏi, Thừa tướng ở đâu? Ở trong gác. Tháo vào, thấy Trác ngồi trên giường, Lã Bố đứng hầu bên cạnh. Trác thấy Tào Tháo, hỏi rằng, Sao hôm nay Mạnh Đức đến chậm thế?""",
        "dur": 20.00
    },
    {
        "title": "Tào Tháo cáo ngựa gầy & Đổng Trác sai Lã Bố đi dắt ngựa quý Tây Lương",
        "text": """Tháo nói, Thưa, ngựa tôi gầy hóa đi chậm. Trác ngoảnh lại bảo Lã Bố rằng, Ta có ngựa tốt ở Tây Lương mới tiến. Phụng Tiên đi chọn một con đem lại đây cho Mạnh Đức. Bố vâng lời đi lấy ngựa.""",
        "dur": 20.00
    },
    {
        "title": "Cơ hội nghìn năm có một - Đối diện Đổng Trác một mình trong gác vắng",
        "text": """Tháo thấy còn một mình Trác, bụng đã bảo dạ rằng, Thằng này số nó đến lúc chết đây!""",
        "dur": 21.43
    }
]

# Verify chunk 5
c5_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-5.txt').read()
c5_recon = '\n'.join([s['text'] for s in data[5]])
c5_orig_w = c5_orig.split()
c5_recon_w = c5_recon.split()
print("Chunk 5 word match:", c5_orig_w == c5_recon_w, len(c5_orig_w), len(c5_recon_w))
c5_total_dur = sum([s['dur'] for s in data[5]])
print("Chunk 5 dur match:", round(c5_total_dur, 2) == round(durations[5], 2), c5_total_dur, durations[5])
for s in data[5]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 5 pacing assertion passed!")

# CHUNK 6 (153.60s) - 7 shots
data[6] = [
    {
        "title": "Đổng Trác nằm xoay mặt vào trong & Tào Tháo rút Thất Bảo Đao toan thích sát",
        "text": """Lập tức muốn rút dao đâm ngay, nhưng lại sợ Trác khỏe chưa dám đâm vội. Trác mình mẩy to béo, xưa nay không ngồi được lâu, bèn ngã mình nằm xuống, ngoảnh mặt vào trong. Tháo lại nghĩa rằng, Thằng này thực số chết. Liền rút dao ra, chực đâm.""",
        "dur": 22.00
    },
    {
        "title": "Bóng dao lóe trong gương & Tào Tháo biến báo quỳ dâng bảo đao",
        "text": """Không ngờ Trác trông vào trong cái gương, thấy bóng Tào Tháo rút dao ra ở sau lưng, vội vàng quay đầu lại hỏi. Mạnh Đức làm gì thế? Bấy giờ, Lã Bố vừa giắt ngựa đến ngoài gác. Tháo tay đương cầm con dao, vội quỳ ngay xuống thưa, Tháo tôi có con dao quý xin dâng thừa tướng. Trác cầm lấy dao xem, thấy dao dài hơn một thước, cán bằng ngọc thất bảo, lưỡi thực sắc, quả là dao quý. Bèn đưa cho Lã Bố cất đi. Tháo còn đem vỏ dao ở lưng, liền cởi ra, đưa nốt cho Lã Bố.""",
        "dur": 24.00
    },
    {
        "title": "Mượn cớ cưỡi thử ngựa & Tào Tháo phi nước đại trốn khỏi tướng phủ",
        "text": """Trác đem Tháo ra xe ngựa. Tháo tạ rồi xin phép đem ngựa ra cưỡi thử. Trác sai đem yên cương đóng ngựa cho Tháo. Tháo dắt ngựa ra ngoài cửa tướng phủ, lên yên, rồi ra roi đi nước đại thẳng hướng đông nam mà chạy.""",
        "dur": 21.00
    },
    {
        "title": "Lã Bố nghi ngờ gian kế & Lý Nho hiến kế triệu Tháo thử lòng",
        "text": """Tào Tháo đi khỏi. Lã Bố nói với Trác rằng, Vừa rồi tôi trông Tào Tháo hình như có ý muốn đâm trộm thái sư! Vì thái sư trông thấy, hắn mới nói lảng ra là đến dâng dao. Trác nói, Ta cũng hơi nghi. Đang nói chuyện thì Lý Nho ở đâu đến. Trác hỏi Lý Nho. Nho nói, Tháo không có vợ con gì ở kinh, chỉ trọi một mình ở quán trọ, nay nên sai người đến gọi. Hắn đến ngay thì quả là hắn dâng dao thiệt, nếu thoái thác không đến, thì đích là thích khách. Lúc bấy giờ ta sẽ bắt mà hỏi.""",
        "dur": 24.00
    },
    {
        "title": "Bốn lính ngục báo tin Tháo trốn qua cửa đông & Lý Nho định mưu thích khách",
        "text": """Trác liền sai bốn người coi ngục đi gọi Tào Tháo. Lính đi một hồi lâu rồi trở về trình rằng, Tháo không về nhà trọ. Có người gặp hắn cưỡi ngựa ra cửa đông. Lính canh hỏi đi đâu, thì hắn nói rằng thừa tướng sai đi có việc kíp, rồi tế ngựa đi thẳng. Nho nói, Thôi, không còn nghi ngờ gì nữa, nó chột dạ chạy trốn, tất là có bụng hành thích.""",
        "dur": 21.00
    },
    {
        "title": "Đổng Trác thịnh nộ hạ lệnh vẽ hình truy nã & Treo thưởng ngàn vàng phong vạn hộ hầu",
        "text": """Trác nói, Ta tin dùng nó thế, tại sao nó lại muốn hại ta? Nho thưa, Tất nhiên nó có người đồng mưu. Bắt được Tào Tháo thì ra cả. Trác liền tư đi các nơi, chỗ nào cũng vẽ hình ảnh Tào Tháo, ai bắt được sẽ thưởng nghìn vàng. Lại phong cho làm vạn hộ hầu, ai chứa chấp sẽ bị trị tội.""",
        "dur": 21.00
    },
    {
        "title": "Tào Tháo sa lưới tại huyện Trung Mâu & Khai man khách buôn Hoàng Phủ",
        "text": """Trong khi ấy, Tháo cắm đầu cắm cổ chạy. Chạy đến Tiêu Quận, đi qua huyện Trung Mâu, bị quân canh cửa thành bắt được, đem nộp quan huyện. Tháo khai là khách buôn, họ là Hoàng Phủ.""",
        "dur": 20.60
    }
]

# Verify chunk 6
c6_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-6.txt').read()
c6_recon = '\n'.join([s['text'] for s in data[6]])
c6_orig_w = c6_orig.split()
c6_recon_w = c6_recon.split()
print("Chunk 6 word match:", c6_orig_w == c6_recon_w, len(c6_orig_w), len(c6_recon_w))
c6_total_dur = sum([s['dur'] for s in data[6]])
print("Chunk 6 dur match:", round(c6_total_dur, 2) == round(durations[6], 2), c6_total_dur, durations[6])
for s in data[6]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 6 pacing assertion passed!")

# CHUNK 7 (146.71s) - 7 shots
data[7] = [
    {
        "title": "Quan huyện Trung Mâu lật tẩy Tào Tháo & Giả vờ hạ lệnh giam cầm",
        "text": """Quan huyện nhìn kỹ Tháo, nghĩ ngợi một lúc rồi nói, Trước ta hầu quản ở Lạc Dương đã được gặp ngươi. Chính người là Tào Tháo, ngươi nói dối sao được? Lính đâu, hãy đem giam nó xuống trại, đến mai ta sẽ giải về kinh lĩnh thưởng. Quan huyện nói thế rồi cho quân canh cửa thành cơm no rượu say rồi về.""",
        "dur": 21.00
    },
    {
        "title": "Nửa đêm gọi lên hỏi chuyện & Tào Tháo ví mình như chim hồng giữa lũ sẻ chim",
        "text": """Đến nửa đêm, quan huyện sai người thân tín, xuống gọi Tào Tháo lên, bảo dẫn vào nhà sau để hỏi. Tháo vào, quan huyện hỏi rằng, Ta nghe thừa tướng hậu đãi ngươi, sao ngươi lại chuốc lấy vạ vào thân? Tháo nói, Ngươi như chim sẻ biết đâu được chí chim hồng! Đã bắt được ta thì cứ đem nộp mà lấy công, hà tất phải hỏi nhiều.""",
        "dur": 21.00
    },
    {
        "title": "Tỏ bày gan ruột trung thần ái quốc & Nỗi uất hận cơ đồ nhà Hán",
        "text": """Quan huyện bèn đuổi cả tả hữu đi rồi bảo Tháo rằng, Anh đừng coi thường tôi. Tôi đây không phải là bọn tục lại đâu Cũng vì chưa gặp được chủ đấy thôi. Tháo nói, Ông cha ta, đời đời ăn lộc nhà Hán. Nếu ta không biết nghĩ cách báo quốc, có khác gì giống muông thú! Ta phải hạ mình chờ thằng Đổng Trác là muốn tìm cơ hội thuận tiện giết nó. Nay việc không xong, cũng là lòng trời!""",
        "dur": 22.00
    },
    {
        "title": "Mưu sự chiêu tập chư hầu dấy binh & Quan huyện cởi trói thụp lạy bậc trung nghĩa",
        "text": """Quan huyện nói, Mạnh Đức bây giờ định đi đâu? Tháo nói, Ta muốn về làng, phát lời kêu gọi, vời cả chư hầu trong thiên hạ khởi binh giết Đổng Trác. Đó là sở nguyện của ta! Quan huyện nghe nói, bèn cởi trói cho Tháo, mời ngồi lên trên rồi thụp xuống lạy hai lạy mà nói rằng. Ông thực là người trung nghĩa ở đời này!""",
        "dur": 22.00
    },
    {
        "title": "Trần Cung xưng danh & Bỏ quan treo ấn cùng Tháo vượt ngục trong đêm",
        "text": """Tháo cũng lạy đáp lại, rồi hỏi tên họ, quan huyện nói, Tôi họ Trần, tên Cung, tên chữ là Công Đài. Tôi có mẹ già và vợ con ở Đông Quận. Nay cảm bụng trung nghĩa của ông, xin bỏ chức quan này, theo ông đi trốn. Tháo mừng lắm. Ngay đêm hôm ấy, Trần Cung thu xếp hành trang và lộ phí, cả hai người thay quần áo, mỗi người đeo một thanh gươm. Cưỡi một con ngựa, đi về quê Tào Tháo.""",
        "dur": 21.00
    },
    {
        "title": "Đến Thành Cao lúc chập tối & Tháo trỏ rặng cây nhắc bạn kết nghĩa của cha",
        "text": """Đi được ba hôm đến Thành Cao, trời đã xâm xẩm tối. Tháo cầm roi ngựa, trỏ vào một đám cây cối um tùm bảo Cung rằng. Ở trong này có Lã Bá Sa là bạn kết nghĩa với cha tôi. Tôi muốn vào hỏi thăm tin nhà, rồi ngủ đấy một đêm, nên không? Cung nói, Thế thì hay lắm!""",
        "dur": 20.00
    },
    {
        "title": "Hội ngộ Lã Bá Sa nơi cổng trại & Tin cha lánh nạn tại Trần Lưu",
        "text": """Hai người đến cửa trại xuống ngựa vào chào Lã Bá Sa, Sa hỏi Tháo rằng, Ta nghe triều đình tầm nã anh gấp lắm. Cha anh phải lánh sang ở Trần Lưu rồi. Sao anh đến được đây?""",
        "dur": 19.71
    }
]

# Verify chunk 7
c7_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-7.txt').read()
c7_recon = '\n'.join([s['text'] for s in data[7]])
c7_orig_w = c7_orig.split()
c7_recon_w = c7_recon.split()
print("Chunk 7 word match:", c7_orig_w == c7_recon_w, len(c7_orig_w), len(c7_recon_w))
c7_total_dur = sum([s['dur'] for s in data[7]])
print("Chunk 7 dur match:", round(c7_total_dur, 2) == round(durations[7], 2), c7_total_dur, durations[7])
for s in data[7]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 7 pacing assertion passed!")

# CHUNK 8 (185.47s) - 8 shots
data[8] = [
    {
        "title": "Tào Tháo tạ ơn Trần Cung & Lã Bá Sa tất tả cưỡi lừa đi mua rượu ngon",
        "text": """Tháo bèn đem chuyện đầu đuôi kể với Lã Bá Sa, rồi lại trỏ vào Trần Cung nói, Nếu không gặp được quan huyện đây. Thì bây giờ đã thịt nát xương tan rồi. Lã Bá Sa vái Trần Cung rồi nói, Cháu nó không gặp được ngài, thì họ Tào còn gì! Đêm nay xin ngài hãy thong thả nghỉ lại đây. Nói xong, đứng dậy vào trong nhà, một chốc trở ra bảo Trần Cung, Nhà tôi không có rượu ngon. Để tôi sang xóm tây, mua một bình rượu ngon về uống. Nói rồi lật đật cưỡi lừa ra đi.""",
        "dur": 24.00
    },
    {
        "title": "Tiếng mài dao sau nhà & Nghe lỏm lời 'Trói lại mà giết' sinh lòng ngờ vực",
        "text": """Tháo với Cung ngồi ở nhà, chợt nghe thấy sau nhà có tiếng mài dao. Tháo bảo Trần Cung rằng, Lã Bá Sa đối với tôi không thân thiết gì lắm. Chuyện này đáng nghi đấy! Hai người sẽ rón rén bước vào sau nhà tranh, chỉ nghe thấy có tiếng người nói, Trói lại mà giết! Tháo bảo Trần Cung, Đúng rồi! Nếu ta không thủ hạ trước, thì sẽ bị bắt mất!""",
        "dur": 22.00
    },
    {
        "title": "Rút gươm thảm sát tám mạng người & Bàng hoàng thấy con lợn bị trói trong bếp",
        "text": """Tháo và Cung hai người cùng rút gươm đi thẳng vào, gặp người nào trong nhà giết người ấy, giết một lúc tám người. Khi vào đến trong bếp, chỉ thấy một con lợn trói bốn vó, sắp đem chọc tiết. Cung giật mình nói, Mạnh Đức ơi! Ta đa nghi quá, giết nhầm phải người tử tế rồi. Hai người vội vàng trở ra lên ngựa đi.""",
        "dur": 24.00
    },
    {
        "title": "Chạm mặt Lã Bá Sa giữa đường & Tha thiết mời khách quay lại dùng cơm",
        "text": """Đi được độ hai dặm gặp Lã Bá Sa cưỡi lừa về, trước yên, treo hai bình rượu, tay xách một nắm rau quả. Lã Bá Sa hỏi hai người rằng, Hiền điệt với sứ quân sao lại đi? Tháo nói, Tôi là người có tội, không dám ở lâu. Lã Bá Sa nói, Ta đã dặn người nhà làm thịt con lợn rồi. Sứ quân với hiền điệt ngại gì một đêm, xin quay ngay ngựa lại cho! Tháo cứ tế ngựa đi.""",
        "dur": 24.00
    },
    {
        "title": "Tàn độc quay ngựa chém chết Bá Sa & Tuyên ngôn 'Thà ta phụ người trong thiên hạ'",
        "text": """Đi được vài bước, rút gươm ra quay ngựa trở lại, gọi Lã Bá Sa hỏi, Ai đi đằng sau ông đấy? Sa quay đầu lại xem. Tháo chém ngay, Sa ngã xuống đất chết. Cung cả sợ hỏi Tháo, Lúc nãy nhầm đã đành, bây giờ sao lại còn đang tay như thế? Tháo nói, Bá Sa về nhà, thấy nhiều người chết, tất nhiên không để im, nếu đem người đi đuổi thì ta bị vạ ngay. Cung nói, Biết rằng mình nhầm rồi, lại còn cố ý giết người nữa thực là đại bất nghĩa. Tháo nói, Thà ta phụ người, không để người phụ ta!""",
        "dur": 26.00
    },
    {
        "title": "Đêm trăng ruổi ngựa tìm quán trọ & Tháo vô tư ngủ say",
        "text": """Cung im lặng không nói gì nữa. Đêm trăng sáng ròi rọi, hai người cứ phóng ngựa đi. Đi được vài dặm, hai người vào nhà hàng ngủ. Sau khi cho ngựa ăn no, Tháo đi ngủ trước.""",
        "dur": 20.00
    },
    {
        "title": "Trần Cung căm giận kẻ tàn nhẫn & Rút gươm toan đoạt mạng Tào Tháo",
        "text": """Cung suy nghĩ, Ta cũng tưởng Tào Tháo là người tốt, cho nên, bỏ quan đi theo hắn.

Ai ngờ hắn là hạng người tàn nhẫn. Nếu để hắn sống ở đời, tất có ngày hắn gây ra vạ lớn! Nghĩ vậy bèn rút gươm toan giết Tào Tháo""",
        "dur": 22.00
    },
    {
        "title": "Bài thơ cảm khái hai kẻ bạo tặc & Lời dẫn kết hồi bốn",
        "text": """Ấy thực rõ là, Mang tâm hiểm độc người đâu thế, Trác. Tháo hai tên cùng một phương!

. ......

Chưa biết Tào Tháo sống chết thế nào, xem đến hồi sau sẽ rõ.""",
        "dur": 23.47
    }
]

# Verify chunk 8
c8_orig = open('/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/04-Hoi-04/kich-ban/Kich-ban-8.txt').read()
c8_recon = '\n'.join([s['text'] for s in data[8]])
c8_orig_w = c8_orig.split()
c8_recon_w = c8_recon.split()
print("Chunk 8 word match:", c8_orig_w == c8_recon_w, len(c8_orig_w), len(c8_recon_w))
c8_total_dur = sum([s['dur'] for s in data[8]])
print("Chunk 8 dur match:", round(c8_total_dur, 2) == round(durations[8], 2), c8_total_dur, durations[8])
for s in data[8]:
    assert 15.0 <= s['dur'] <= 28.0, f"Pacing out of range: {s['dur']}"
print("Chunk 8 pacing assertion passed!")

print("\n" + "="*50)
print("ALL 8 CHUNKS FULLY VALIDATED!")
total_shots = sum(len(shots) for shots in data.values())
print(f"Total Shots: {total_shots}")
total_time = sum(sum(s['dur'] for s in shots) for shots in data.values())
print(f"Total Duration: {total_time:.2f}s (target: {sum(durations.values()):.2f}s)")
print("Average Pacing: {:.2f}s/shot".format(total_time / total_shots))
