# 🎭 BÁO CÁO PHÂN ĐỊNH GIỌNG THOẠI & RANH GIỚI KỊCH BẢN (STEP 08A - SA1)
## TÁC PHẨM: TAM QUỐC DIỄN NGHĨA — HỒI 01
**Đạo diễn Phân định Giọng thoại:** Speaker Attribution & Dialogue Boundary Director (SA1)  
**Thư mục tác phẩm:** `/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/01-Hoi-01`  
**Ngày thẩm định:** 15/09/2026  

---

### I. TỔNG QUAN KHẢO SÁT & BÓC TÁCH 3 PHÂN LUỒNG TUYỆT ĐỐI
Toàn bộ 10 tệp kịch bản (`Kich-ban-1.txt` đến `Kich-ban-10.txt`) đã được rà soát tỉ mỉ từng câu, từng liên từ và dấu câu. Cấu trúc kịch bản được phân rã thành 3 luồng dữ liệu âm thanh độc lập:
1. **Dòng Thơ ca (`type: "poem"`):** Gồm 4 thi phẩm/khúc từ với tổng cộng **22 dòng thơ độc lập** (không gộp dòng, có nhịp caesura `, ` và cấu trúc đệm thở).
2. **Dòng Người dẫn chuyện (`type: "narrator"`):** Các đoạn văn xuôi dẫn dắt lịch sử, mô tả trận thế, chuyển cảnh, lời dẫn thoại và các điểm dừng kịch tính `. ......`.
3. **Dòng Thoại nhân vật (`type: "dialogue"`):** Tổng cộng **40 lượt thoại** được bóc tách ranh giới chính xác đến từng từ, xác định rõ nhân vật phát ngôn, động từ dẫn thoại/khẩu khí, và ngữ cảnh tiếp giáp trước/sau.

---

### II. DANH MỤC NHÂN VẬT THOẠI TRONG HỒI 01 (DRAMATIS PERSONAE)
Khắc phục triệt để các lỗi nhận diện của hệ thống cũ (như gán nhầm Hứa Thiệu thành Viên Thiệu, gán nhầm Châu Tĩnh thành Lưu Tĩnh, gán nhầm Hoàng Phủ Tung thành Chu Tuấn, bỏ sót 14 nhân vật thoại phụ). Bảng phân vai chính xác gồm:

| STT | Mã Định Danh (`speaker`) | Tên Nhân Vật | Vai Trò / Thân Phận | Số Lượt Thoại | Vị Trí Chunk |
| :---: | :--- | :--- | :--- | :---: | :---: |
| 1 | `Narrator` | Người dẫn chuyện | Dẫn dắt đại cục, bình luận lịch sử, ngâm vịnh | Toàn bộ | 1 – 10 |
| 2 | `Sai_Ung` | Sái Ung | Nghị lang nhà Đông Hán dâng sớ can vua | 1 | Chunk 1 |
| 3 | `Nam_Hoa_Lao_Tien` | Nam Hoa Lão Tiên | Đạo tiên ban tặng Thái Bình Yêu Thuật | 2 | Chunk 2 |
| 4 | `Truong_Giac` | Trương Giác | Đại hiền lương sư / Thiên công tướng quân | 2 | Chunk 2, 3 |
| 5 | `Truong_Luong` | Trương Lương | Nhân công tướng quân (em Trương Giác) | 1 | Chunk 3 |
| 6 | `Chau_Tinh` | Châu Tĩnh | Hiệu úy U Châu (thuộc hạ Lưu Yên) | 1 | Chunk 3 |
| 7 | `Thay_Tuong` | Thầy tướng | Người qua đường xem tướng cây dâu | 1 | Chunk 4 |
| 8 | `Luu_Bi_Nhi_Dong` | Lưu Bị (thơ ấu) | Huyền Đức lúc nhỏ chơi dưới gốc dâu | 1 | Chunk 4 |
| 9 | `Luu_Nguyen_Khoi` | Lưu Nguyên Khởi | Chú của Lưu Bị | 1 | Chunk 4 |
| 10 | `Truong_Phi` | Trương Phi (Dực Đức) | Hào kiệt Trác quận, bán thịt mổ lợn | 4 | Chunk 4, 5, 10 |
| 11 | `Luu_Bi` | Lưu Bị (Huyền Đức) | Dòng dõi Hán thất, bán chiếu đóng dép | 8 | Chunk 4, 5, 6, 7, 9, 10 |
| 12 | `Quan_Vu` | Quan Vũ (Vân Trường) | Tráng sĩ Hà Đông, trốn nạn giang hồ | 3 | Chunk 4/5, 5, 9 |
| 13 | `Dong_Thanh_Luu_Quan` | Lưu Bị & Quan Vũ | Đồng thanh tán đồng ý kiến vườn đào | 1 | Chunk 5 |
| 14 | `Loi_The_Vuon_Dao` | Ba anh em Lưu - Quan - Trương | Lời thề minh ước Vườn Đào (Chorus) | 1 | Chunk 5 |
| 15 | `Lu_Thuc` | Lư Thực | Quan Trung lang tướng, thầy học Lưu Bị | 2 | Chunk 7, 9 |
| 16 | `Hoang_Phu_Tung` | Hoàng Phủ Tung | Quan Trung lang tướng triều Hán | 2 | Chunk 7, 9 |
| 17 | `Tao_Tung` | Tào Tung | Cha của Tào Tháo | 1 | Chunk 8 |
| 18 | `Tao_Thao` | Tào Tháo (A Man) | Quan Kỵ đô úy lúc trẻ | 2 | Chunk 8 |
| 19 | `Kieu_Huyen` | Kiều Huyền | Quan Thái úy thẩm định nhân tài | 1 | Chunk 8 |
| 20 | `Ha_Ngung` | Hà Ngung | Danh sĩ Nam Dương | 1 | Chunk 8 |
| 21 | `Hua_Thieu` | Hứa Thiệu | Danh sĩ Nhữ Nam xem tướng | 1 | Chunk 8 |
| 22 | `Dong_Trac` | Đổng Trác | Quan Trung lang tướng kiêu ngạo | 1 | Chunk 10 |

---

### III. BÓC TÁCH CHI TIẾT THI CA (`type: "poem"`)

#### 1. Bài từ mở đầu: "Lâm Giang Tiên" (Chunk 1)
- Dẫn thoại: `Có bài từ rằng,` (Narrator)
- Đệm thở mở: `. ......` (Lead-in coda 1.5s)
- Thơ độc lập từng dòng:
  1. `Trường Giang, cuồn cuộn, chảy về đông,`
  2. `Sóng vùi dập, hết anh hùng,`
  3. `Được, thua, phải, trái, thoắt thành không,`
  4. `Non xanh, nguyên vẻ cũ,`
  5. `Mấy độ, bóng tà hồng!`
  6. `Bạn đầu bạc, ngư tiều trên bãi,`
  7. `Đã quen nhìn, thu nguyệt xuân phong,`
  8. `Một bầu rượu, vui vẻ tương phùng,`
  9. `Xưa nay, bao nhiêu việc,`
  10. `Phó mặc, nói cười suông,`
- Đệm thở kết: `. ......` (Ending coda 1.5s)

#### 2. Thơ khen ngợi Quan Vũ và Trương Phi trận núi Đại Hưng (Chunk 6)
- Dẫn thơ: `Đời sau có thơ khen hai người rằng,`
- Thơ độc lập từng dòng:
  1. `Anh hùng xuất hiện buổi sơ đầu,`
  2. `Người thử long đao kẻ thử mâu.`
  3. `Mới bước chân ra uy đã dữ,`
  4. `Tiếng tăm lừng lẫy cuộc ganh nhau.`

#### 3. Thơ khen ngợi mưu lược Lưu Bị giải vây Thanh Châu (Chunk 7)
- Dẫn thơ: `Đời sau có thơ khen Huyền Đức rằng,`
- Thơ độc lập từng dòng:
  1. `Bầy mưu đặt mẹo khéo ra công,`
  2. `Đôi hổ chung quy kém một rồng.`
  3. `Buổi mới đã nên công trạng lớn,`
  4. `Chia ba chân vạc đáng anh hùng.`

#### 4. Thơ cảm thán kết hồi về nhân tình thế thái & Trương Phi (Chunk 10)
- Dẫn thơ: `Đó chính là,`
- Đệm thở mở: `. ......`
- Thơ độc lập từng dòng:
  1. `Nhân tình thế thái, vẫn xưa nay,`
  2. `Ai biết anh hùng, lúc trắng tay,`
  3. `Nếu được người người, như Dực Đức,`
  4. `Trên đời hẳn hết, kẻ không hay!`
- Đệm thở kết: `. ......`

---

### IV. BẢNG BÓC TÁCH RANH GIỚI HỘI THOẠI CHI TIẾT (40 LƯỢT THOẠI)

#### CHUNK 1
- **Thoại #01:**
  - **Speaker:** `Sai_Ung` (Sái Ung)
  - **Động từ dẫn/Khẩu khí:** "dâng sớ lên, lời lẽ thống thiết, nói rằng," (Thống thiết, trung can nghĩa đảm, bi phẫn)
  - **Văn bản thoại:** "Cầu vồng sa xuống, gà mái hóa trống. Ấy là bởi quyền chính trong nước ở tay đàn bà và ở tay hoạn quan."
  - **Ngữ cảnh trước:** Vua hạ chiếu hỏi nguyên do điềm gở.
  - **Ngữ cảnh sau:** "Vua xem sớ ngậm ngùi thở dài, đứng dậy thay áo."

#### CHUNK 2
- **Thoại #02:**
  - **Speaker:** `Nam_Hoa_Lao_Tien` (Nam Hoa Lão Tiên)
  - **Động từ dẫn/Khẩu khí:** "gọi Trương Giác vào trong một cái động. Trao cho ba quyển sách và bảo rằng," (Uy nghiêm, răn dạy, siêu phàm thoát tục)
  - **Văn bản thoại:** "Đây là cuốn Thái bình yêu thuật, có được cuốn này ngươi nên thay trời dạy người. Để cứu lấy đời. Nếu sau này manh tâm tà gian ắt bị ác báo."
  - **Ngữ cảnh trước:** Trương Giác thi trượt vào núi hái thuốc gặp ông lão.
  - **Ngữ cảnh sau:** Trương Giác sụp lạy hỏi họ tên.
- **Thoại #03:**
  - **Speaker:** `Nam_Hoa_Lao_Tien` (Nam Hoa Lão Tiên)
  - **Động từ dẫn/Khẩu khí:** "cụ già nói," (Phiêu dật, ngắn gọn, thần bí)
  - **Văn bản thoại:** "Ta là Nam Hoa lão tiên,"
  - **Ngữ cảnh trước:** Trương Giác sụp xuống lạy hỏi họ tên.
  - **Ngữ cảnh sau:** "nói đoạn. Hóa ra một trận gió biến mất."
- **Thoại #04:**
  - **Speaker:** `Truong_Giac` (Trương Giác)
  - **Động từ dẫn/Khẩu khí:** "Giác nói phao lên rằng," (Kích động, mị dân, cuồng tín)
  - **Văn bản thoại:** "Trời xanh đã chết, trời vàng nên dựng, Đến năm giáp tý, thiên hạ thái bình."
  - **Ngữ cảnh trước:** Đồ đệ đông đúc chia làm 36 phương.
  - **Ngữ cảnh sau:** Sai người lấy đất thó trắng viết chữ Giáp tý giữa cửa.

#### CHUNK 3
- **Thoại #05:**
  - **Speaker:** `Truong_Giac` (Trương Giác)
  - **Động từ dẫn/Khẩu khí:** "rồi bàn với hai em rằng," (Mưu mô, dã tâm bá nghiệp)
  - **Văn bản thoại:** "Không gì khó bằng thu phục được lòng dân. Nay lòng dân đã quy thuận về ta, nếu không thừa thế chiếm lấy thiên hạ thì thật là đáng tiếc lắm."
  - **Ngữ cảnh trước:** Mật giao với hoạn quan Phong Tư làm nội ứng.
  - **Ngữ cảnh sau:** Sai may cờ vàng hẹn ngày khởi sự.
- **Thoại #06:**
  - **Speaker:** `Truong_Luong` (Trương Lương)
  - **Động từ dẫn/Khẩu khí:** "Trương Lương xưng Nhân công tướng quân nói với mọi người rằng," (Hô hào phản loạn, kích động quần chúng)
  - **Văn bản thoại:** "Nay vận nhà Hán sắp hết, đại thánh nhân ra đời. Các ngươi nên thuận mệnh trời, theo về ta để cùng vui hưởng thái bình!."
  - **Ngữ cảnh trước:** Việc khởi sự bị bại lộ do Đường Châu tố giác.
  - **Ngữ cảnh sau:** Bốn phương đội khăn vàng theo Trương Giác tới bốn năm mươi vạn người.
- **Thoại #07:**
  - **Speaker:** `Chau_Tinh` (Châu Tĩnh)
  - **Động từ dẫn/Khẩu khí:** "Tĩnh nói," (Khẩn cấp, lo âu, can gián thực tế)
  - **Văn bản thoại:** "Quân giặc nhiều, quân ta ít, ông nên tức khắc chiêu mộ thêm quân thì mới kịp ứng phó."
  - **Ngữ cảnh trước:** Giặc phạm U Châu, Lưu Yên triệu Châu Tĩnh bàn luận.
  - **Ngữ cảnh sau:** Lưu Yên cho là phải, bèn sai treo bảng mộ quân.

#### CHUNK 4
- **Thoại #08:**
  - **Speaker:** `Thay_Tuong` (Thầy tướng)
  - **Động từ dẫn/Khẩu khí:** "Có người thầy tướng đi qua trông thấy khen rằng," (Kinh ngạc, tán thán điềm lành)
  - **Văn bản thoại:** "Nhà có cây dâu này tất sinh quý tử."
  - **Ngữ cảnh trước:** Miêu tả cây dâu trước nhà Huyền Đức xòe ra như tán che xe.
  - **Ngữ cảnh sau:** Lưu Bị lúc nhỏ chơi dưới gốc dâu.
- **Thoại #09:**
  - **Speaker:** `Luu_Bi_Nhi_Dong` (Lưu Bị thơ ấu)
  - **Động từ dẫn/Khẩu khí:** "thường vẫn nói rằng," (Hồn nhiên nhưng chí khí đế vương bẩm sinh)
  - **Văn bản thoại:** "Ngày sau ta làm vua. Cũng ngự cái xe có tán che như cây dâu này."
  - **Ngữ cảnh trước:** Cùng trẻ con chơi dưới gốc dâu.
  - **Ngữ cảnh sau:** Người chú Lưu Nguyên Khởi nghe thấy lấy làm lạ.
- **Thoại #10:**
  - **Speaker:** `Luu_Nguyen_Khoi` (Lưu Nguyên Khởi)
  - **Động từ dẫn/Khẩu khí:** "lấy làm lạ bảo rằng," (Ngạc nhiên, thương yêu bảo bọc)
  - **Văn bản thoại:** "Thằng bé này không phải người thường."
  - **Ngữ cảnh trước:** Nghe Lưu Bị nói chí làm vua.
  - **Ngữ cảnh sau:** Thường chu cấp tiền bạc cho gia đình Lưu Bị.
- **Thoại #11:**
  - **Speaker:** `Truong_Phi` (Trương Phi)
  - **Động từ dẫn/Khẩu khí:** "Có một người đứng phía sau nói lớn lên rằng," (Tiếng vang như sấm, hào sảng, chất vấn)
  - **Văn bản thoại:** "Đại trượng phu như ông, không ra giúp nước, đứng thở dài đó, được việc chi?"
  - **Ngữ cảnh trước:** Lưu Bị xem bảng mộ quân thở dài.
  - **Ngữ cảnh sau:** Lưu Bị ngoảnh lại nhìn thấy tướng mạo dị thường.
- **Thoại #12:**
  - **Speaker:** `Truong_Phi` (Trương Phi)
  - **Động từ dẫn/Khẩu khí:** "Người ấy nói," (Bộc trực, sảng khoái, tự tin gia thế và chí hướng)
  - **Văn bản thoại:** "Tôi họ Trương tên Phi, tự là Dực Đức, ở Trác quận đã lâu đời. Gia tư có trang trại ruộng vườn, lại có lò mổ lợn và ngôi hàng bán rượu. Tôi chỉ thích kết giao với hào kiệt trong thiên hạ. Vừa rồi thấy ông xem bảng văn rồi thở dài, nên tôi mới hỏi."
  - **Ngữ cảnh trước:** Lưu Bị hỏi họ tên.
  - **Ngữ cảnh sau:** Lưu Bị xưng danh và giãi bày tâm sự.
- **Thoại #13:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức nói," (Khiêm nhường, trầm tĩnh, nặng lòng vì dân nước)
  - **Văn bản thoại:** "Tôi đây vốn dòng dõi nhà Hán, họ Lưu tên Bị, nay thấy giặc Khăn Vàng nổi loạn. Muốn ra dẹp giặc yên dân, chỉ hiềm sức mình không làm nổi, nên mới thở dài."
  - **Ngữ cảnh trước:** Trương Phi hỏi lý do thở dài.
  - **Ngữ cảnh sau:** Trương Phi mừng rỡ đề nghị hợp tác.
- **Thoại #14:**
  - **Speaker:** `Truong_Phi` (Trương Phi)
  - **Động từ dẫn/Khẩu khí:** "Phi nói," (Hào hứng, nhiệt thành, quyết đoán)
  - **Văn bản thoại:** "Nhà tôi gia tư cũng khá. Ý tôi muốn chiêu mộ trai tráng trong làng, cùng ông mưu đồ việc lớn, ông tính sao?"
  - **Ngữ cảnh trước:** Lưu Bị than sức mình không làm nổi.
  - **Ngữ cảnh sau:** Lưu Bị mừng rỡ cùng vào quán uống rượu.
- **Thoại #15:**
  - **Speaker:** `Quan_Vu` (Quan Vũ)
  - **Động từ dẫn/Khẩu khí:** "vào hàng ngồi phịch xuống gọi nhà hàng." (Uy dũng, khẩn trương, khí phách)
  - **Văn bản thoại:** "Rượu mau lên! Để ta uống xong còn vào thành ứng mộ!" *(Vắt từ cuối Chunk 4 sang đầu Chunk 5)*
  - **Ngữ cảnh trước:** Đẩy cỗ xe vào quán rượu.
  - **Ngữ cảnh sau:** Lưu Bị ngắm nhìn tướng mạo phi phàm mời cùng ngồi.

#### CHUNK 5
- **Thoại #16:**
  - **Speaker:** `Quan_Vu` (Quan Vũ)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức bèn mời cùng ngồi và hỏi họ tên. Người ấy nói," (Đĩnh đạc, trầm hùng, trượng nghĩa diệt ác)
  - **Văn bản thoại:** "Tôi họ Quan tên Vũ, tự là Trương Sinh, sau đổi là Vân Trường, người làng Giải Lương, tỉnh Hà Đông. Nhân thấy có đứa thổ hào ỷ thế hiếp người, tôi bèn giết chết rồi đi làm kẻ giang hồ đã năm, sáu năm rồi. Nay nghe ở đây có lệnh chiêu binh phá giặc nên tôi đến ứng mộ."
  - **Ngữ cảnh trước:** Lưu Bị tiếp đãi hỏi lai lịch.
  - **Ngữ cảnh sau:** Ba người cùng về trại Trương Phi bàn việc.
- **Thoại #17:**
  - **Speaker:** `Truong_Phi` (Trương Phi)
  - **Động từ dẫn/Khẩu khí:** "Phi nói," (Hồ hởi, sáng kiến hào hiệp)
  - **Văn bản thoại:** "Sau trại tôi có một vườn đào đang nở hoa đẹp lắm, ngày mai ta nên làm lễ tế trời đất ở trong vườn. Rồi ba chúng ta kết làm anh em, cùng lòng hợp sức, sau mới có thể tính được việc lớn."
  - **Ngữ cảnh trước:** Bàn tính mưu sự tại trang trại Trương Phi.
  - **Ngữ cảnh sau:** Lưu Bị và Quan Vũ đồng tình.
- **Thoại #18:**
  - **Speaker:** `Dong_Thanh_Luu_Quan` (Lưu Bị & Quan Vũ)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức, Vân Trường đều nói," (Đồng thanh tán thưởng, phấn khởi)
  - **Văn bản thoại:** "Như thế tốt lắm!"
  - **Ngữ cảnh trước:** Trương Phi đề xuất kết nghĩa vườn đào.
  - **Ngữ cảnh sau:** Chuẩn bị trâu đen ngựa trắng tế cáo trời đất.
- **Thoại #19:**
  - **Speaker:** `Loi_The_Vuon_Dao` (Lưu Bị, Quan Vũ, Trương Phi)
  - **Động từ dẫn/Khẩu khí:** "ba người đốt hương lạy hai lạy thề rằng." (Thiêng liêng, trang trọng tột cùng, đồng thanh tuyên thệ)
  - **Văn bản thoại:** "Chúng tôi là Lưu Bị, Quan Vũ, Trương Phi, dẫu rằng khác họ, song đã kết làm anh em, thì phải cùng lòng hợp sức. Cứu khốn phù nguy, trên báo đền nợ nước, dưới yên định muôn dân. Chúng tôi không cần sinh cùng ngày, cùng tháng, cùng năm, chỉ muốn chết cùng năm, cùng ngày, cùng tháng. Hoàng thiên hậu thổ soi xét lòng này. Nếu ai bội nghĩa quên ơn thì trời người cùng giết."
  - **Ngữ cảnh trước:** Thắp hương bái tế trời đất trong vườn đào.
  - **Ngữ cảnh sau:** Tôn Lưu Bị làm anh cả, Quan Vũ thứ hai, Trương Phi em út.
- **Thoại #20:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức nói," (Vui mừng khôn xiết, cảm kích thiên duyên)
  - **Văn bản thoại:** "Thực là trời giúp chúng ta!"
  - **Ngữ cảnh trước:** Đang lo thiếu ngựa chiến thì có lái buôn đến trại.
  - **Ngữ cảnh sau:** Ra đón hai lái buôn Trương Thế Bình và Tô Song.

#### CHUNK 6
- **Thoại #21:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức nhảy ngựa vụt ra, tả có Vân Trường, hữu có Dực Đức, giơ roi mắng lớn." (Oai vệ, nghiêm khắc, chính khí áp đảo nghịch tặc)
  - **Văn bản thoại:** "Quân giặc phản nước kia! Sao không xuống ngựa hàng ngay đi?"
  - **Ngữ cảnh trước:** Dàn trận dưới chân núi Đại Hưng đối mặt Trình Viễn Chí.
  - **Ngữ cảnh sau:** Trình Viễn Chí tức giận sai Đặng Mậu ra đánh.
- **Thoại #22:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Lưu Yên bàn với Huyền Đức. Huyền Đức nói," (Quả quyết, khẳng khái, sẵn sàng chi viện)
  - **Văn bản thoại:** "Bị này tình nguyện đem quân đi cứu."
  - **Ngữ cảnh trước:** Cung Cảnh cầu cứu khẩn cấp tại Thanh Châu.
  - **Ngữ cảnh sau:** Lưu Yên điều Châu Tĩnh và 5.000 quân cùng ba anh em đi cứu.
- **Thoại #23:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "lui ba mươi dặm đóng trại, rồi bảo Quan, Trương rằng," (Điềm tĩnh, quyền biến, mưu lược quân sự)
  - **Văn bản thoại:** "Giặc nhiều, ta ít. Tất phải dùng kỳ binh mới có thể thắng được."
  - **Ngữ cảnh trước:** Quân giặc Thanh Châu đông thế mạnh, lui binh đóng trại.
  - **Ngữ cảnh sau:** Bố trí phục binh hai cánh núi tả hữu.

#### CHUNK 7
- **Thoại #24:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Cung Cảnh khao quân xong, Châu Tĩnh muốn về. Huyền Đức nói," (Trọng nghĩa thầy trò, tận tụy phò trợ)
  - **Văn bản thoại:** "Mới rồi nghe tin quan trung lang tướng Lư Thực cùng Trương Giác đánh nhau ở Quảng Tôn. Bị này trước kia có học Lư tướng quân, nghĩa đạo thầy trò, muốn sang giúp sức."
  - **Ngữ cảnh trước:** Đại thắng giải vây Thanh Châu, Châu Tĩnh muốn rút quân về U Châu.
  - **Ngữ cảnh sau:** Ba anh em dẫn quân bản bộ sang Quảng Tôn hội sư cùng Lư Thực.
- **Thoại #25:**
  - **Speaker:** `Lu_Thuc` (Lư Thực)
  - **Động từ dẫn/Khẩu khí:** "Một hôm Lư Thực bảo Huyền Đức rằng," (Uy nghiêm tướng soái, tin cậy giao phó ấn kiếm)
  - **Văn bản thoại:** "Trương Giác đã bị ta vây ở đây rồi. Duy hai em nó là Trương Bảo, Trương Lương đang chống nhau với Hoàng Phủ Tung và Chu Tuấn ở Dĩnh Xuyên. Ông nên đem quân ngay bản bộ và một nghìn quân ta giúp thêm, đến thẳng Dĩnh Xuyên dò xem tin tức ra sao. Rồi cùng nhau hẹn ngày tiến đánh."
  - **Ngữ cảnh trước:** Thế trận giằng co 15 vạn quân Trương Giác vs 5 vạn quân Lư Thực.
  - **Ngữ cảnh sau:** Lưu Bị lĩnh mệnh hành quân cấp tốc sang Dĩnh Xuyên.
- **Thoại #26:**
  - **Speaker:** `Hoang_Phu_Tung` (Hoàng Phủ Tung)
  - **Động từ dẫn/Khẩu khí:** "Tung bàn với Tuấn rằng," (Nhạy bén chiến thuật, quyết đoán hỏa công)
  - **Văn bản thoại:** "Quân giặc dựa vào chỗ có cỏ rậm đóng quân thì ta nên dùng mẹo hóa công."
  - **Ngữ cảnh trước:** Quân Khăn Vàng lui về dựa bụi rậm Trường Xã lập trại.
  - **Ngữ cảnh sau:** Sai quân chuẩn bị bó cỏ phục kích chờ gió nổi.

#### CHUNK 8
- **Thoại #27:**
  - **Speaker:** `Tao_Tung` (Tào Tung)
  - **Động từ dẫn/Khẩu khí:** "Tung vội lại xem, thấy Tháo không có bệnh chi cả, bèn hỏi." (Nghi ngại, ngạc nhiên, gặng hỏi)
  - **Văn bản thoại:** "Chú mày nói mày trúng phong, đã khỏi rồi à?"
  - **Ngữ cảnh trước:** Người chú mách Tào Tháo trúng phong, Tào Tung hốt hoảng chạy lại xem.
  - **Ngữ cảnh sau:** Tào Tháo phân trần lừa cha.
- **Thoại #28:**
  - **Speaker:** `Tao_Thao` (Tào Tháo - niên thiếu)
  - **Động từ dẫn/Khẩu khí:** "Thưa cha," (Giả vờ oan ức, xảo quyệt, tinh ranh)
  - **Văn bản thoại:** "Thưa cha, thuở bé đến giờ con có bệnh ấy đâu! Chẳng qua chú con ghét con, cho nên, đặt điều ra thế."
  - **Ngữ cảnh trước:** Cha gặng hỏi bệnh trúng phong.
  - **Ngữ cảnh sau:** Tào Tung tin lời, từ đó không nghe người chú mách tội nữa.
- **Thoại #29:**
  - **Speaker:** `Kieu_Huyen` (Kiều Huyền)
  - **Động từ dẫn/Khẩu khí:** "Bấy giờ, có người tên là Kiều Huyền bảo Tháo rằng," (Trầm trồ, thấu thị thời thế)
  - **Văn bản thoại:** "Thiên hạ sắp loạn. Phi có tay tài giỏi hơn đời thì không sao dẹp được loạn. Làm được như thế có lẽ chỉ có bác!"
  - **Ngữ cảnh trước:** Tào Tháo phóng đãng nổi tiếng cơ biến quyền mưu.
  - **Ngữ cảnh sau:** Hà Ngung trông thấy cũng tán tụng.
- **Thoại #30:**
  - **Speaker:** `Ha_Ngung` (Hà Ngung)
  - **Động từ dẫn/Khẩu khí:** "một hôm trông thấy Tháo cũng tán tụng rằng," (Chắc nịch, dự cảm tương lai)
  - **Văn bản thoại:** "Nhà Hán sắp mất. Yên được thiên hạ chắc chỉ có người này!"
  - **Ngữ cảnh trước:** Danh tiếng Tào Tháo lan truyền trong giới danh sĩ.
  - **Ngữ cảnh sau:** Tào Tháo đến hỏi Hứa Thiệu ở Nhữ Nam.
- **Thoại #31:**
  - **Speaker:** `Tao_Thao` (Tào Tháo)
  - **Động từ dẫn/Khẩu khí:** "Tháo thân đến hỏi," (Tự tin, thăm dò, khao khát khẳng định bản thân)
  - **Văn bản thoại:** "Như tôi là người thế nào?"
  - **Ngữ cảnh trước:** Hứa Thiệu có tiếng giỏi biết người.
  - **Ngữ cảnh sau:** Thiệu ban đầu im lặng, Tháo gặng hỏi lần nữa.
- **Thoại #32:**
  - **Speaker:** `Hua_Thieu` (Hứa Thiệu)
  - **Động từ dẫn/Khẩu khí:** "Thiệu không trả lời. Tháo hỏi lại lần nữa. Thiệu nói," (Sắc sảo, đanh thép, định mệnh lịch sử)
  - **Văn bản thoại:** "Anh là năng thần của đời trị và gian hùng của đời loạn!"
  - **Ngữ cảnh trước:** Tào Tháo gặng hỏi phẩm bình nhân cách.
  - **Ngữ cảnh sau:** Tào Tháo nghe xong cả mừng, bước vào hoạn lộ.

#### CHUNK 9
- **Thoại #33:**
  - **Speaker:** `Hoang_Phu_Tung` (Hoàng Phủ Tung)
  - **Động từ dẫn/Khẩu khí:** "Tung nói," (Phân tích cục diện, khuyên nhủ định hướng)
  - **Văn bản thoại:** "Nay Trương Lương, Trương Bảo thế cùng lực kiệt tất chạy đến Quảng Tôn nương nhờ Trương Giác. Ông nên đi gấp đường về giúp ngay Lư Thực."
  - **Ngữ cảnh trước:** Lưu Bị đến Dĩnh Xuyên thì giặc đã tan, yết kiến Hoàng Phủ Tung.
  - **Ngữ cảnh sau:** Lưu Bị quay lại Quảng Tôn, giữa đường gặp xe tù Lư Thực.
- **Thoại #34:**
  - **Speaker:** `Lu_Thuc` (Lư Thực)
  - **Động từ dẫn/Khẩu khí:** "vội xuống ngựa chạy đến hỏi thăm. Thực nói," (Bi phẫn, uất ức trung thần sa cơ)
  - **Văn bản thoại:** "Ta vây đánh Trương Giác, sắp sửa pháp tan, chỉ vì Giác dùng yêu thuật, nên còn nhùng nhằng chưa phá hẳn được. Triều đình sai viên hoạn quan tên là Tả Phong đến dò xét quân tình. Phong đòi ăn của đút mà không được, vì lương quân ta còn thiếu, tiền đâu mà cung đốn họ, bởi thế Tả Phong căm giận. Về triều tâu man cho ta ru rú ở trong lũy cao không chịu đánh giặc, làm cho lòng quân chán nản. Triều đình nổi giận, sai quan trung lang tướng Đổng Trác đến cầm quân thay ta, và bắt ta về kinh hỏi tội."
  - **Ngữ cảnh trước:** Lưu Bị kinh hãi thấy Lư Thực bị nhốt trong cũi xe tù.
  - **Ngữ cảnh sau:** Trương Phi nổi trận lôi đình toan cướp ngục.
- **Thoại #35:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức vội ngăn lại bảo rằng," (Khẩn cấp can ngăn, giữ trọn phép tắc triều cương)
  - **Văn bản thoại:** "Không nên, triều đình đã có công luận, chú không được xử sự một cách nóng nảy như thế."
  - **Ngữ cảnh trước:** Trương Phi tuốt gươm toan chém chết áp giải cứu thầy.
  - **Ngữ cảnh sau:** Quân áp giải đưa Lư Thực đi, Quan Vũ đề xuất phương án.
- **Thoại #36:**
  - **Speaker:** `Quan_Vu` (Quan Vũ)
  - **Động từ dẫn/Khẩu khí:** "Quan Công nói," (Trầm tĩnh, sáng suốt, thấu đáo)
  - **Văn bản thoại:** "Nay Lư trung lang đã bị bắt, người khác thay quyền, chúng ta đến đấy cũng vô ích. Chi bằng hãy về Trác quận."
  - **Ngữ cảnh trước:** Lư Thực bị giải đi, không còn người bảo trợ tại tiền tuyến.
  - **Ngữ cảnh sau:** Lưu Bị tán thành rút quân về hướng Bắc.

#### CHUNK 10
- **Thoại #37:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức nói," (Dứt khoát, xung trận kịp thời cứu nguy)
  - **Văn bản thoại:** "Trương Giác đây rồi, đánh ngay đi!"
  - **Ngữ cảnh trước:** Thấy cờ Thiên công tướng quân đuổi riết Đổng Trác.
  - **Ngữ cảnh sau:** Ba anh em tung ngựa xông vào trận chém tan quân Khăn Vàng.
- **Thoại #38:**
  - **Speaker:** `Dong_Trac` (Đổng Trác)
  - **Động từ dẫn/Khẩu khí:** "Ba người cứu được Đổng Trác về trại. Trác hỏi ba người" (Hách dịch, trịch thượng, khinh khỉnh)
  - **Văn bản thoại:** "hiện làm quan gì?" *(Hoặc "Hiện làm quan gì?")*
  - **Ngữ cảnh trước:** Được cứu thoát chết đưa về trại.
  - **Ngữ cảnh sau:** Lưu Bị thành thực đáp "Chân trắng".
- **Thoại #39:**
  - **Speaker:** `Luu_Bi` (Lưu Bị)
  - **Động từ dẫn/Khẩu khí:** "Huyền Đức nói," (Thành thực, không màng hư danh, điềm nhiên)
  - **Văn bản thoại:** "Chân trắng"
  - **Ngữ cảnh trước:** Đổng Trác hỏi quan chức.
  - **Ngữ cảnh sau:** Đổng Trác khinh khỉnh không thèm tạ ơn, Lưu Bị quay lưng bỏ đi.
- **Thoại #40:**
  - **Speaker:** `Truong_Phi` (Trương Phi)
  - **Động từ dẫn/Khẩu khí:** "Trương Phi cả giận nói rằng," (Cuồng nộ xung thiên, nghĩa khí bất bình, muốn trừ bạo ngược)
  - **Văn bản thoại:** "Thằng cha này láo quá! Chúng ta lăn lộn vào đất chết để cứu nó ra, nó không ơn thì chớ, lại còn làm phách khinh người đến thế. Nếu không giết nó, sao hả được giận này?"
  - **Ngữ cảnh trước:** Lưu Bị bỏ ra ngoài, Đổng Trác vô lễ bội nghĩa.
  - **Ngữ cảnh sau:** Rút dao xông vào trướng định giết Đổng Trác (dẫn vào Hồi 2).
