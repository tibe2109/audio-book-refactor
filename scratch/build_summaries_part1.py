#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 1: Build Summaries & Mindmaps for Chapters 01 - 05
Book: Building the Courage to Speak Up and Stand Out at Work
Authors: Pete Mockaitis & Prof. Jim Detert
"""

import os

BASE_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Building-the-Courage-to-Speak-Up-and-Stand-Out-at-Work"

# ==============================================================================
# CHAPTER 01: Courage can be learned
# ==============================================================================
CHAP_01_SUMMARY = """# Tóm Tắt: CHƯƠNG 1: LÒNG DŨNG CẢM LÀ KỸ NĂNG CÓ THỂ RÈN LUYỆN ĐƯỢC

## 1. Thông điệp cốt lõi (Core Message)
> Lòng dũng cảm nơi công sở không phải là thiên phú bẩm sinh hay đặc quyền của một nhóm người mang "gene dũng cảm", mà là một năng lực hành vi có thể rèn luyện thông qua sự chuẩn bị kỹ lưỡng và theo dõi sát sao hậu sự vụ.

---

## 2. Lược Đồ Phân Bổ Cấu Trúc Tài Liệu (Content Distribution Overview)

| Phần / Đề Mục Tài Liệu Gốc | Nội Dung Trọng Tâm | Số Luận Điểm Đại Diện |
| :--- | :--- | :---: |
| **Phần I: Giải Ảo Huyền Thoại Về Phẩm Chất Bẩm Sinh** | Phá vỡ định kiến về "gene dũng cảm", khẳng định dũng cảm là sự lựa chọn và đa dạng ở mọi mẫu người. | 3 Luận điểm |
| **Phần II: Nỗ Lực Bền Bỉ & Bài Học Từ Các Điển Hình** | Phân tích quá trình tôi luyện của John Lewis và những người dũng cảm: vẻ ngoài tự nhiên là kết quả của rèn luyện. | 3 Luận điểm |
| **Phần III: Trọng Tâm Chuẩn Bị & Theo Dõi Hậu Sự Vụ** | Chuyển dịch tiêu điểm từ khoảnh khắc bùng nổ sang công tác chuẩn bị tiền kỳ và nghệ thuật chốt cam kết/hàn gắn sau đó. | 3 Luận điểm |
| **Tổng cộng** | **Bao quát 100% cấu trúc tài liệu Chương 1** | **9 Luận điểm** |

---

## 3. Luận điểm quan trọng theo cấu trúc tài liệu (Key Takeaways: 9 ý chuyên sâu)

### 📑 PHẦN I: GIẢI ẢO HUYỀN THOẠI VỀ PHẨM CHẤT BẨM SINH

1. **PHI THẦN THÁNH HÓA LÒNG DŨNG CẢM**
   - **Bản chất & Phân tích chuyên sâu:** Đa số nhân sự tin rằng dũng cảm là thuộc tính tính cách trời cho (như hướng ngoại hoặc liều lĩnh). Nghiên cứu thực nghiệm trên hàng nghìn ca ứng xử công sở chứng minh không tồn tại bất kỳ chỉ dấu di truyền hay nền tảng xuất thân đặc thù nào định đoạt hành vi dũng cảm.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Mô hình Phân tích Hành vi Thực nghiệm (Empirical Behavioral Profiling) bóc tách các nhóm nhân khẩu học đa dạng.
   - **Ví dụ thực tế đời thường:** Một kế toán viên trầm lặng, ít nói vẫn có thể là người duy nhất đứng lên chỉ ra sai phạm dòng tiền trong cuộc họp ban giám đốc, bác bỏ quan niệm chỉ người bộc trực mới dám lên tiếng.

2. **DŨNG CẢM LÀ MỘT SỰ LỰA CHỌN CÓ Ý THỨC**
   - **Bản chất & Phân tích chuyên sâu:** Lên tiếng hay im lặng không phản ánh bạn là "ai khi sinh ra", mà là "bạn quyết định làm gì" tại thời khắc trách nhiệm xuất hiện. Khi coi dũng cảm là định mệnh, ta trao cho mình cái cớ để thoái thác trách nhiệm đạo đức.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Khung Tự Thẩm Định Trách Nhiệm Cá Nhân (Personal Agency Matrix).
   - **Ví dụ thực tế đời thường:** Thay vì tự nhủ "mình sinh ra vốn nhút nhát nên việc phản biện là của sếp", nhân viên chủ động nhìn nhận việc góp ý cho quy trình lỗi là lựa chọn đóng góp chuyên môn.

3. **TÍNH ĐA DẠNG CỦA CHỦ THỂ HÀNH ĐỘNG DŨNG CẢM**
   - **Bản chất & Phân tích chuyên sâu:** Những người dám dấn thân tại nơi làm việc trải rộng trên mọi giới tính, độ tuổi, cấp bậc và kiểu tính cách. Sự khác biệt duy nhất giữa họ và người im lặng là mức độ cam kết với mục tiêu chung và khả năng làm chủ nỗi bất an.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Bản đồ Đa dạng Hành vi Tổ chức (Organizational Behavioral Spectrum).
   - **Ví dụ thực tế đời thường:** Một thực tập sinh tuần đầu tiên đi làm vẫn có thể dũng cảm đề xuất giải pháp bảo mật dữ liệu tốt hơn khi thấy lỗ hổng hệ thống.

---

### 📑 PHẦN II: NỖ LỰC BỀN BỈ & BÀI HỌC TỪ CÁC ĐIỂN HÌNH

4. **ẢO ẢNH CỦA SỰ THUẬN TỰ NHIÊN**
   - **Bản chất & Phân tích chuyên sâu:** Khi chứng kiến một người phát biểu sắc sảo, dứt khoát trước hội đồng quản trị, người quan sát thường nghĩ hành động đó thật dễ dàng với họ. Thực chất, sự điềm tĩnh và phong thái đĩnh đạc đó là sản phẩm của hàng trăm giờ tích lũy nội lực và thử nghiệm trước đó.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Nguyên lý Luyện tập Có chủ đích (Deliberate Practice Framework theo K. Anders Ericsson).
   - **Ví dụ thực tế đời thường:** Một diễn giả nội bộ nói năng lưu loát và tự tin đối đáp chất vấn gay gắt thực ra đã tập dượt bài thuyết trình hơn mười lần trước gương và ghi âm tự chỉnh giọng.

5. **BÀI HỌC TÔI LUYỆN TỪ DI SẢN JOHN LEWIS**
   - **Bản chất & Phân tích chuyên sâu:** Nhà hoạt động dân quyền John Lewis nổi tiếng với những hành động quả cảm làm thay đổi lịch sử. Nhưng phong thái của ông không đến từ sự bốc đồng, mà từ những năm tháng rèn luyện phản ứng bất bạo động, chịu đựng áp lực và giữ vững mục tiêu bất chấp hiểm nguy.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Nghiên cứu Tình huống Điển hình Lịch sử (Historical Case-Method Analysis).
   - **Ví dụ thực tế đời thường:** Trước khi bước vào cuộc tuần hành, các thành viên phong trào dân quyền đã phải trải qua các buổi diễn tập bị khiêu khích để không mất kiểm soát cảm xúc.

6. **LÒNG DŨNG CẢM LÀ KỸ NĂNG CƠ BẮP CẦN ĐƯỢC TẬP LUYỆN**
   - **Bản chất & Phân tích chuyên sâu:** Tương tự như cơ bắp sẽ teo đi nếu không vận động, lòng dũng cảm sẽ thui chột nếu liên tục chọn giải pháp né tránh. Ngược lại, việc rèn luyện thường xuyên ở quy mô nhỏ sẽ tạo ra trí nhớ cơ bắp tâm lý (Psychological Muscle Memory).
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Mô hình Thể lực Tâm lý (Psychological Fitness Model).
   - **Ví dụ thực tế đời thường:** Tập thói quen nói "tôi có góc nhìn khác" trong các cuộc họp nhóm nhỏ 3 người trước khi phát biểu phản biện trong đại hội toàn công ty 500 người.

---

### 📑 PHẦN III: TRỌNG TÂM CHUẨN BỊ & THEO DÕI HẬU SỰ VỤ

7. **BẪY QUAN SÁT KHOẢNH KHẮC BÙNG NỔ**
   - **Bản chất & Phân tích chuyên sâu:** Văn hóa đại chúng và truyền thông thường tôn sùng "thời khắc đối đầu kịch tính" (bước ra đối chất, đập bàn lên tiếng). Điều này làm lệch lạc nhận thức, khiến người ta quên rằng khoảnh khắc đó chỉ chiếm 5% sự thành bại của toàn bộ tiến trình.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Mô hình Phân rã Tiến trình Hành động 3 Giai đoạn (Pre - During - Post Framework).
   - **Ví dụ thực tế đời thường:** Người ta nhớ đến câu trả lời đanh thép của giám đốc kỹ thuật trước khách hàng, nhưng quên rằng nhóm kỹ sư đã thức trắng ba đêm kiểm toán toàn bộ số liệu để bảo đảm phát ngôn đó không có kẽ hở.

8. **TẦM QUAN TRỌNG TỐI THƯỢNG CỦA CÔNG TÁC CHUẨN BỊ TIỀN KỲ**
   - **Bản chất & Phân tích chuyên sâu:** Người dũng cảm có năng lực luôn thu thập dữ liệu xác đáng, xây dựng liên minh ủng hộ và lường trước các phản ứng phản bác trước khi chính thức lên tiếng. Chuẩn bị tốt là liều thuốc giải độc hiệu quả nhất cho nỗi sợ hãi.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Kế hoạch Tiền khả thi cho Cuộc đối thoại Khó (Pre-conversation Due Diligence Checklist).
   - **Ví dụ thực tế đời thường:** Trước khi xin gặp tổng giám đốc đề xuất hủy bỏ một dự án lãng phí, trưởng phòng chuẩn bị sẵn bảng đối chiếu chi phí cơ hội và phỏng vấn ý kiến của ba trưởng bộ phận liên quan.

9. **NGHỆ THUẬT THEO DÕI & XỬ LÝ HẬU SỰ VỤ (FOLLOW-UP)**
   - **Bản chất & Phân tích chuyên sâu:** Sau khi khoảnh khắc lên tiếng kết thúc, nếu thành công, người khôn ngoan sẽ nhanh chóng chốt hạ các cam kết bằng văn bản; nếu gặp trắc trở hoặc phản ứng tiêu cực, họ chủ động mở cuộc đối thoại hàn gắn để giải tỏa bức xúc, ngăn chặn sự thù hằn ngầm.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Quy trình Đóng Cam kết & Giải tỏa Căng thẳng Hậu Thảo luận (Post-Meeting Closure & Repair Protocol).
   - **Ví dụ thực tế đời thường:** Sau một cuộc tranh luận nảy lửa, chủ động ghé bàn làm việc của đồng nghiệp và nói: "Tôi thấy cuộc họp vừa rồi khá căng thẳng và dường như bạn chưa hài lòng, chúng ta đi uống cà phê để trao đổi thêm nhé".

---

## 4. Kế hoạch hành động (Action Plan: 14 việc cụ thể)

#### Nhóm 1: Hành động ngay hôm nay (Micro-habits dưới 2 phút)
- [ ] **Hành động 1:** Viết ra giấy 1 tình huống công việc mà bạn đang ngần ngại chưa dám lên tiếng hoặc hành động.
- [ ] **Hành động 2:** Tự xóa bỏ suy nghĩ "tính mình nhút nhát" bằng câu tự nhủ: "Dũng cảm là kỹ năng rèn luyện được".
- [ ] **Hành động 3:** Ghi nhận 1 đồng nghiệp vừa có hành vi dũng cảm hoặc đóng góp ý kiến thẳng thắn trong ngày.
- [ ] **Hành động 4:** Hít thở sâu 3 nhịp và ghi lại 3 bằng chứng thực tế cho ý tưởng bạn muốn đề xuất.
- [ ] **Hành động 5:** Gửi 1 tin nhắn ngắn xin lịch hẹn 15 phút với người liên quan để trao đổi một băn khoăn nhỏ.

#### Nhóm 2: Kế hoạch rèn luyện trong tuần (Áp dụng vào công việc & đời sống)
- [ ] **Hành động 6:** Thực hành lên tiếng ít nhất 1 lần trong cuộc họp tuần này với một câu hỏi làm rõ vấn đề.
- [ ] **Hành động 7:** Lập danh sách kiểm tra chuẩn bị dữ liệu trước khi tham gia bất kỳ cuộc họp quan trọng nào.
- [ ] **Hành động 8:** Thực hành đóng vai phản biện thử với một người bạn tin cậy trước một buổi thuyết trình khó.
- [ ] **Hành động 9:** Thực hiện 1 cuộc trò chuyện tiếp nối (follow-up) sau một cuộc thảo luận chưa tìm được tiếng nói chung.
- [ ] **Hành động 10:** Tách biệt cảm xúc cá nhân khỏi vấn đề chuyên môn trong biên bản làm việc.

#### Nhóm 3: Thói quen duy trì & Chuyển hóa lâu dài (Phát triển bền vững)
- [ ] **Hành động 11:** Thiết lập nhật ký ghi chép các khoảnh khắc can đảm hàng tuần để theo dõi sự tiến bộ.
- [ ] **Hành động 12:** Định kỳ mỗi quý đánh giá lại xem mình có né tránh việc khó vì sợ mất an toàn hay không.
- [ ] **Hành động 13:** Xây dựng mạng lưới hỗ trợ gồm 2 - 3 đồng nghiệp có tư duy chính trực và dám nói thật.
- [ ] **Hành động 14:** Huấn luyện cấp dưới cách chuẩn bị số liệu và tâm thế trước khi trình bày với cấp trên.

---

## 5. Câu hỏi tự ngẫm (Reflection: 20 câu hỏi sâu sắc)

#### Nhóm 1: Tự vấn Nhận thức & Hệ tư duy (Self-Awareness & Mindset)
1. Tôi có đang vô thức tin rằng mình là người "thiếu gene dũng cảm" để bào chữa cho sự im lặng?
2. Khi nhìn thấy một người dám lên tiếng, phản ứng đầu tiên của tôi là ngưỡng mộ hay nghĩ họ "thích thể hiện"?
3. Lần gần đây nhất tôi chọn cách im lặng vì sợ rủi ro, kết quả lâu dài là tốt lên hay tồi tệ đi?
4. Tôi định nghĩa thế nào là một người dũng cảm trong môi trường công sở hiện tại?
5. Sự khác biệt giữa bộc phát cảm xúc nhất thời và hành vi dũng cảm có năng lực là gì?

#### Nhóm 2: Nhận diện Thói quen & Điểm mù (Habits & Blind Spots)
6. Tôi thường tập trung năng lượng vào lúc tranh luận hay vào khâu chuẩn bị trước đó?
7. Sau những cuộc đối đầu căng thẳng, tôi có thói quen né tránh người đối diện hay chủ động hàn gắn?
8. Điều gì ngăn cản tôi thực hiện bước theo dõi hậu sự vụ (follow-up) sau cuộc họp?
9. Tôi có thường xuyên chuẩn bị kịch bản phản biện trước khi phát biểu không?
10. Tôi có xu hướng nhượng bộ ngay khi thấy đối phương tỏ thái độ cau mày hoặc im lặng khó chịu?

#### Nhóm 3: Ứng dụng Thực tế & Giải quyết Vấn đề (Practical Application & Problem Solving)
11. Trong tuần này, vấn đề gai góc nào đang đòi hỏi tôi phải chuẩn bị số liệu để lên tiếng?
12. Ai là người phản biện gay gắt nhất đối với ý tưởng của tôi, và tôi đã tham vấn họ trước chưa?
13. Làm thế nào để biến việc theo dõi hậu sự vụ thành quy trình chuẩn sau mỗi cuộc họp tranh luận?
14. Nếu sếp không đồng thuận ngay lập tức, bước đi tiếp theo của tôi sẽ là gì?
15. Những dữ liệu khách quan nào sẽ giúp bảo vệ luận điểm của tôi tốt nhất?

#### Nhóm 4: Bứt phá Giới hạn & Chuyển hóa Tương lai (Breakthrough & Transformation)
16. Nếu tôi xem lòng dũng cảm là một cơ bắp, bài tập tạ nhỏ nhất tôi có thể thực hiện ngày mai là gì?
17. Hình mẫu lý tưởng về sự dũng cảm mà tôi muốn trở thành trong 2 năm tới trông như thế nào?
18. Di sản nghề nghiệp của tôi sẽ bị ảnh hưởng ra sao nếu tôi tiếp tục chọn giải pháp an toàn trong 5 năm tới?
19. Làm sao để tôi tạo dựng một môi trường an toàn tâm lý cho đội ngũ của mình cùng rèn luyện sự dũng cảm?
20. Bài học lớn nhất từ tấm gương John Lewis áp dụng vào sự nghiệp của tôi là gì?

---

## 6. Bản Đồ Tư Duy Trực Quan (Visual Mindmap Overview - Tinh Gọn 4-5 Tầng)

```mermaid
mindmap
  root((LÒNG DŨNG CẢM LÀ KỸ NĂNG))
    🧬 Giải Ảo Bẩm Sinh
      Phi thần thánh
        Không gene riêng
          Đa dạng chủ thể
            Kế toán trầm lặng
      Sự lựa chọn
        Quyền tự quyết
          Cam kết mục tiêu
            Trách nhiệm cá nhân
    🏋️ Nỗ Lực Rèn Luyện
      Ảo ảnh tự nhiên
        Tập dượt bền bỉ
          Trí nhớ cơ bắp
            Diễn tập trước gương
      Gương John Lewis
        Kháng cự bạo lực
          Kỷ luật sắt đá
            Phong trào dân quyền
    🎯 Tiến Trình 3 Pha
      Khâu chuẩn bị
        Thu thập dữ liệu
          Xây dựng đồng minh
            Kiểm toán số liệu
      Theo dõi hậu sự
        Chốt cam kết
          Chủ động hàn gắn
            Cuộc hẹn cà phê
```
"""

CHAP_01_MINDMAP = """# 🧠 BẢN ĐỒ TƯ DUY TINH GỌN (4-5 TẦNG): CHƯƠNG 1 - LÒNG DŨNG CẢM LÀ KỸ NĂNG CÓ THỂ RÈN LUYỆN ĐƯỢC

## 1. Sơ Đồ Tư Duy Trực Quan (Mermaid Mindmap Tinh Gọn)

```mermaid
mindmap
  root((DŨNG CẢM CÔNG SỞ))
    🧬 Giải Ảo Bẩm Sinh
      Phi thần thánh
        Không gene riêng
          Mọi kiểu người
            Kế toán lên tiếng
      Lựa chọn hành vi
        Quyền tự quyết
          Ý thức trách nhiệm
            Hành động có chủ đích
    🏋️ Tôi Luyện Cơ Bắp
      Ảo ảnh năng khiếu
        Tập dượt bền bỉ
          K. Anders Ericsson
            Deliberate Practice
      Gương John Lewis
        Kháng cự áp lực
          Kỷ luật kiên cường
            Không bộc phát mù quáng
    🎯 Chuẩn Bị & Hậu Sự
      Công tác tiền kỳ
        Thu thập chứng cứ
          Lường trước phản bác
            Checklist kiểm toán
      Theo dõi tiếp nối
        Chốt lại cam kết
          Hàn gắn cảm xúc
            Cà phê đối thoại
```

---

## 2. Cây Phân Cấp Tri Thức Gợi Nhớ Nhanh 4-5 Tầng (Active Recall Hierarchy)

- 📌 **Giải Ảo Bẩm Sinh (The Myth of Born Courage)**
  - 🔹 *Phi thần thánh hóa:* ➔ *Không có gene dũng cảm* ➔ *Đa dạng tính cách* ➔ *Kế toán viên dám nói thật*
  - 🔹 *Sự lựa chọn hành vi:* ➔ *Quyền tự quyết cá nhân* ➔ *Cam kết đạo đức* ➔ *Hành động có chủ đích*
- 📌 **Tôi Luyện Bền Bỉ (Deliberate Practice)**
  - 🔹 *Ảo ảnh năng khiếu:* ➔ *Luyện tập có chủ đích* ➔ *Trí nhớ cơ bắp* ➔ *Tập dượt trước gương*
  - 🔹 *Tấm gương John Lewis:* ➔ *Rèn luyện phản ứng bất bạo động* ➔ *Giữ vững nguyên tắc* ➔ *Đĩnh đạc trước hiểm nguy*
- 📌 **Tiến Trình 3 Giai Đoạn (Pre - During - Post)**
  - 🔹 *Chuẩn bị tiền kỳ:* ➔ *Thu thập chứng cứ số liệu* ➔ *Thiết lập đồng minh* ➔ *Bảo vệ phát ngôn*
  - 🔹 *Theo dõi hậu sự vụ:* ➔ *Chốt văn bản cam kết* ➔ *Hàn gắn quan hệ* ➔ *Cuộc hẹn giải tỏa căng thẳng*

---

## 3. Bảng Neo Trí Nhớ Từ Khóa Vàng (Memory Anchor Cheat Sheet)

| Từ Khóa Cốt Lõi | Phần Trong Tài Liệu | Bản Chất / Vai Trò (3-5 từ) | Tín Hiệu Gợi Nhớ (Memory Trigger) |
| :--- | :--- | :--- | :--- |
| **Gene Dũng Cảm** | Phần I | Ngộ nhận bẩm sinh sai lầm | Chiếc khiên thoái thác trách nhiệm |
| **Sự Lựa Chọn** | Phần I | Quyền tự quyết của cá nhân | Ngã ba đường hành động |
| **John Lewis** | Phần II | Điển hình rèn luyện dũng khí | Cuộc tuần hành bền bỉ kiên gan |
| **Cơ Bắp Tâm Lý** | Phần II | Càng tập càng vững vàng | Phòng tập thể hình nội tâm |
| **Tiền Kỳ Chuẩn Bị** | Phần III | Chiếm 95% thành bại | Bộ hồ sơ chứng cứ sắc bén |
| **Hậu Sự Vụ (Follow-up)** | Phần III | Chốt cam kết và hàn gắn | Tách cà phê gỡ bỏ hiềm khích |
"""

# Write Chapter 1 files
c1_dir = os.path.join(BASE_DIR, "01-Courage-can-be-learned")
with open(os.path.join(c1_dir, "summary.md"), "w", encoding="utf-8") as f:
    f.write(CHAP_01_SUMMARY.strip() + "\n")
with open(os.path.join(c1_dir, "mindmap.md"), "w", encoding="utf-8") as f:
    f.write(CHAP_01_MINDMAP.strip() + "\n")
print("[✓] Chapter 01 files written successfully.")
