#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder for Chapter 09: Prepare for fear and anger
"""
import os

BASE_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Building-the-Courage-to-Speak-Up-and-Stand-Out-at-Work"

C09_SUMMARY = """# Tóm Tắt: CHƯƠNG 9: CHUẨN BỊ VÀ QUẢN TRỊ CẢM XÚC SỢ HÃI LẪN GIẬN DỮ

## 1. Thông điệp cốt lõi (Core Message)
> Sợ hãi và giận dữ là hai cảm xúc có khuynh hướng sinh lý hoàn toàn trái ngược nhau: sợ hãi thôi thúc tháo chạy né tránh đòi hỏi sự rèn luyện thể lực và tập dượt phản biện từ trước; trong khi giận dữ thôi thúc tấn công tiếp cận đòi hỏi kỹ thuật kích hoạt hệ thần kinh phó giao cảm làm dịu tức thời và cơ chế trì hoãn công nghệ (như bộ đếm giờ 60 phút Outlook) để ngăn chặn hành xử vụng về gây tổn thương.

---

## 2. Lược Đồ Phân Bổ Cấu Trúc Tài Liệu (Content Distribution Overview)

| Phần / Đề Mục Tài Liệu Gốc | Nội Dung Trọng Tâm | Số Luận Điểm Đại Diện |
| :--- | :--- | :---: |
| **Phần I: Đối Lập Sinh Lý Giữa Sợ Hãi & Giận Dữ** | Phân tích cơ chế cảm xúc Né tránh (Avoidance - Sợ hãi) vs. Tiếp cận (Approach - Giận dữ) và hệ lụy của chúng nơi công sở. | 3 Luận điểm |
| **Phần II: Kỹ Thuật Làm Dịu Phản Ứng Sinh Lý Tức Thời** | Phương pháp kích hoạt hệ thần kinh phó giao cảm (đếm 1-10, thở sâu 3 nhịp) và quy tắc dời lịch hẹn khi giận dữ bốc hỏa. | 3 Luận điểm |
| **Phần III: Cơ Chế Trì Hoãn Công Nghệ & Bài Học Outlook** | Trải nghiệm cá nhân của Jim Detert: dùng công cụ hẹn giờ hoãn gửi email 60 phút trên Outlook để cứu vãn các quan hệ công việc. | 3 Luận điểm |
| **Tổng cộng** | **Bao quát 100% cấu trúc tài liệu Chương 9** | **9 Luận điểm** |

---

## 3. Luận điểm quan trọng theo cấu trúc tài liệu (Key Takeaways: 9 ý chuyên sâu)

### 📑 PHẦN I: ĐỐI LẬP SINH LÝ GIỮA SỢ HÃI & GIẬN DỮ

1. **KHUYNH HƯỚNG HÀNH ĐỘNG TRÁI NGƯỢC CỦA CẢM XÚC**
   - **Bản chất & Phân tích chuyên sâu:** Về mặt sinh học thần kinh, sợ hãi là một cảm xúc Né tránh (Avoidance Emotion) thúc đẩy bản năng tháo chạy hoặc đóng băng (Freeze); ngược lại, giận dữ là một cảm xúc Tiếp cận (Approach Emotion) thôi thúc bản năng xông thẳng về phía trước để tấn công, đối đầu.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Mô Hình Khuynh Hướng Hành Động Cảm Xúc (Emotional Action Tendency Framework).
   - **Ví dụ thực tế đời thường:** Khi bị chỉ trích trong cuộc họp, người sợ hãi sẽ cúi gằm mặt im lặng mong buổi họp chóng qua, trong khi người giận dữ sẽ lập tức bật dậy cãi tay đôi với người phê bình.

2. **CƠ CHẾ RÈN LUYỆN KIỂM SOÁT NỖI SỢ DÀI HẠN**
   - **Bản chất & Phân tích chuyên sâu:** Bạn không thể dẹp bỏ nỗi sợ hãi chỉ bằng vài lời tự động viên trong 5 phút. Kiểm soát nỗi sợ đòi hỏi quá trình chuẩn bị thể chất và tinh thần dài hạn: duy trì thể lực dẻo dai, thực hành thiền chánh niệm, tập yoga nhằm điều hòa lại phản ứng sinh lý nền tảng của hệ thần kinh giao cảm.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Điều Hòa Sinh Lý Nền Tảng (Baseline Physiological Regulation Protocol).
   - **Ví dụ thực tế đời thường:** Duy trì thói quen chạy bộ buổi sáng và thiền 15 phút mỗi ngày giúp nhịp tim của bạn ổn định hơn khi bước vào phòng đàm phán hợp đồng căng thẳng.

3. **SOẠN KỊCH BẢN & TẬP ĐÓNG VAI PHẢN BIỆN GAY GẮT**
   - **Bản chất & Phân tích chuyên sâu:** Đa số mọi người không thực sự tháo chạy ra khỏi phòng họp, nhưng nỗi sợ khiến họ câm lặng và nhượng bộ vô điều kiện. Liều thuốc duy nhất là soạn sẵn kịch bản từng câu từng chữ và nhờ người đóng vai phản biện gay gắt để làm quen với cảm giác áp lực trước khi bước vào thực tế.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Diễn Tập Phơi Nhiễm Áp Lực (Stress-Inoculation Roleplay).
   - **Ví dụ thực tế đời thường:** Nhờ một người bạn khó tính đóng vai sếp liên tục ngắt lời và chất vấn gay gắt để rèn luyện phản xạ giữ vững lập trường mà không bị run giọng.

---

### 📑 PHẦN II: KỸ THUẬT LÀM DỊU PHẢN ỨNG SINH LÝ TỨC THỜI

4. **LỢI THẾ VÀ CẠM BẪY CỦA CƠN GIẬN DỮ**
   - **Bản chất & Phân tích chuyên sâu:** Giận dữ mang lại nguồn năng lượng và động lực cực lớn để bạn dám đứng lên hành động chống lại sự bất công. Tuy nhiên, cạm bẫy chết người là nó làm tê liệt thùy trán (Prefrontal Cortex), khiến bạn hành xử vụng về, dùng lời lẽ xúc phạm và phá hủy hoàn toàn tính chính nghĩa của thông điệp.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Phân Tích Hai Mặt Của Cơn Giận Tổ Chức (Dual-Edged Nature of Workplace Anger).
   - **Ví dụ thực tế đời thường:** Thấy cấp dưới bị đối xử tệ bạc, trưởng phòng bừng bừng tức giận xông vào phòng giám đốc chửi bới, kết quả là bị kỷ luật vì vi phạm quy tắc ứng xử thay vì bảo vệ được nhân viên.

5. **KÍCH HOẠT HỆ THẦN KINH PHÓ GIAO CẢM (PARASYMPATHETIC ACTIVATION)**
   - **Bản chất & Phân tích chuyên sâu:** Những lời khuyên cổ xưa như "đếm từ 1 đến 10" hay "hít thở sâu 3 nhịp" thực chất có nền tảng khoa học vững chắc: chúng trực tiếp kích hoạt dây thần kinh phế vị (Vagus Nerve), làm chậm nhịp tim, hạ huyết áp và phát tín hiệu an toàn cho não bộ để lấy lại lý trí.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Kỹ Thuật Thở Hộp & Làm Dịu Thần Kinh (Box Breathing & Parasympathetic Reset).
   - **Ví dụ thực tế đời thường:** Cảm thấy máu dồn lên mặt khi bị sếp mắng oan, dừng lại 10 giây hít sâu bằng mũi và thở chậm bằng miệng trước khi cất lời giải thích.

6. **QUY TẮC "DỜI LỊCH ĐỐI THOẠI" KHI CƠN GIẬN BỐC HỎA**
   - **Bản chất & Phân tích chuyên sâu:** Trừ các trường hợp khẩn cấp đe dọa an toàn tính mạng, một nguyên tắc vàng là tuyệt đối không lên tiếng hoặc đưa ra quyết định quan trọng ngay trong thời khắc cơn thịnh nộ đang bùng phát. Hãy chủ động xin hoãn cuộc trao đổi sang buổi sau để hai bên cùng bình tâm.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Giao Thức Tạm Dừng Chiến Lược (Strategic Pause & Rescheduling Protocol).
   - **Ví dụ thực tế đời thường:** "Tôi thấy vấn đề này đang rất căng thẳng và cả hai chúng ta đều cần thêm thời gian suy ngẫm, tôi đề xuất chúng ta tạm dừng và tiếp tục cuộc họp vào 9 giờ sáng mai".

---

### 📑 PHẦN III: CƠ CHẾ TRÌ HOÃN CÔNG NGHỆ & BÀI HỌC OUTLOOK

7. **BÀI HỌC TỰ VẤN ĐẮT GIÁ CỦA CHÍNH TÁC GIẢ JIM DETERT**
   - **Bản chất & Phân tích chuyên sâu:** Giáo sư Jim Detert thẳng thắn thừa nhận: bản thân ông chưa từng gặp khó khăn trong việc chọn lòng dũng cảm, nhưng ông từng nhiều lần thất bại thảm hại trong việc thể hiện "dũng cảm có năng lực" chỉ vì để cơn thịnh nộ trước những điều bất công làm lu mờ lý trí và gửi đi những email mang tính hủy diệt.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Tự Phản Tỉnh Lỗ Hổng Lãnh Đạo (Executive Vulnerability Case Method).
   - **Ví dụ thực tế đời thường:** Sau một cuộc họp bất công, ngồi viết một email dài 5 trang vạch tội tất cả các bên liên quan và ấn nút gửi trong sự hối hận ngay vài phút sau đó.

8. **KỸ THUẬT CÀI ĐẶT BỘ ĐẾM GIỜ TRÌ HOÃN 60 PHÚT TRÊN OUTLOOK**
   - **Bản chất & Phân tích chuyên sâu:** Để tự bảo vệ mình trước những phút giây bốc đồng, Jim Detert đã cài đặt tính năng trì hoãn trong Outlook: toàn bộ email gửi đi sẽ tự động nằm lại trong Hộp thư đi (Outbox) đúng 60 phút trước khi được phát tán đi thực sự. Khoảng đệm thời gian này là phao cứu sinh cho sự nghiệp.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Rào Chắn Công Nghệ Tự Động (Technological Emotional Guardrail).
   - **Ví dụ thực tế đời thường:** Bực bội soạn một email từ chức gay gắt lúc 11 giờ trưa; đến 11 giờ 45 phút sau khi ăn trưa và hạ hỏa, ông mở Outbox ra xóa bức thư đó và viết lại một đề xuất điềm tĩnh, chuyên nghiệp.

9. **XÂY DỰNG HỆ THỐNG PHÒNG THỦ CẢM XÚC ĐA TẦNG**
   - **Bản chất & Phân tích chuyên sâu:** Người trưởng thành về mặt cảm xúc không dựa vào ý chí đơn thuần để kiềm chế cơn giận, mà họ thiết kế một hệ thống các rào chắn hành vi, công nghệ và sự hỗ trợ của đồng đội để ngăn chặn những sai lầm chết người trước khi chúng xảy ra.
   - **Phương pháp / Công cụ / Quy trình đi kèm:** Hệ Thống Phòng Thủ Cảm Xúc Đa Tầng (Multi-layered Emotional Defense Architecture).
   - **Ví dụ thực tế đời thường:** Nhờ một đồng nghiệp thân cận đọc duyệt qua mọi email quan trọng gửi lên ban giám đốc trước khi chính thức bấm gửi.

---

## 4. Kế hoạch hành động (Action Plan: 14 việc cụ thể)

#### Nhóm 1: Hành động ngay hôm nay (Micro-habits dưới 2 phút)
- [ ] **Hành động 1:** Cài đặt ngay quy tắc trì hoãn gửi thư (Delay delivery rule) từ 5 đến 15 phút trong ứng dụng email của bạn.
- [ ] **Hành động 2:** Thực hành kỹ thuật thở hộp (Hít 4 giây - Giữ 4 giây - Thở 4 giây - Giữ 4 giây) ngay tại bàn làm việc.
- [ ] **Hành động 3:** Viết ra giấy câu thần chú: "Không bao giờ lên tiếng hay gửi email khi đang bừng bừng tức giận".
- [ ] **Hành động 4:** Đếm chậm từ 1 đến 10 khi gặp một tin nhắn gây bực bội trước khi gõ phím trả lời.
- [ ] **Hành động 5:** Rời khỏi màn hình máy tính đi uống 1 cốc nước mát khi cảm thấy nhịp tim đập nhanh do căng thẳng.

#### Nhóm 2: Kế hoạch rèn luyện trong tuần (Áp dụng vào công việc & đời sống)
- [ ] **Hành động 6:** Tập dượt đóng vai phản biện gay gắt với một người bạn trước khi tham gia buổi thuyết trình quan trọng.
- [ ] **Hành động 7:** Thực hành nói câu: "Tôi đề xuất dời cuộc họp sang ngày mai để hai bên cùng bình tâm suy xét".
- [ ] **Hành động 8:** Thiết lập thói quen tập thể dục hoặc thiền định 20 phút mỗi ngày để điều hòa sinh lý nền tảng.
- [ ] **Hành động 9:** Nhờ 1 đồng nghiệp đáng tin cậy làm người "đọc duyệt cảm xúc" cho các văn bản quan trọng.
- [ ] **Hành động 10:** Ghi chép nhật ký nhận diện các tác nhân kích hoạt (triggers) khiến bạn dễ nổi giận nơi công sở.

#### Nhóm 3: Thói quen duy trì & Chuyển hóa lâu dài (Phát triển bền vững)
- [ ] **Hành động 11:** Làm chủ hoàn toàn nghệ thuật chuyển hóa năng lượng của sự giận dữ thành hành động xây dựng có ích.
- [ ] **Hành động 12:** Duy trì lối sống lành mạnh, ngủ đủ giấc để tăng cường năng lực kiểm soát cảm xúc của vỏ não thùy trán.
- [ ] **Hành động 13:** Xây dựng hệ thống rào chắn công nghệ và quy trình làm việc ngăn ngừa tối đa các quyết định bốc đồng.
- [ ] **Hành động 14:** Hướng dẫn cấp dưới các phương pháp quản trị căng thẳng và làm dịu phản ứng sinh lý khi gặp khủng hoảng.

---

## 5. Câu hỏi tự ngẫm (Reflection: 20 câu hỏi sâu sắc)

#### Nhóm 1: Tự vấn Nhận thức & Hệ tư duy (Self-Awareness & Mindset)
1. Khi đối mặt với hiểm họa nơi công sở, phản xạ sinh lý tự nhiên của tôi là muốn tháo chạy hay muốn tấn công?
2. Tôi có đang lầm tưởng rằng thể hiện sự giận dữ đanh thép là biểu hiện của quyền lực và lòng dũng cảm?
3. Nỗi sợ hãi đã từng khiến tôi câm lặng và nhượng bộ trong những tình huống then chốt nào?
4. Cơn thịnh nộ bộc phát đã từng phá hủy mối quan hệ hay sự nghiệp của tôi ra sao trong quá khứ?
5. Sự khác biệt giữa việc kìm nén cảm xúc độc hại và việc làm chủ cảm xúc khôn ngoan là gì?

#### Nhóm 2: Nhận diện Thói quen & Điểm mù (Habits & Blind Spots)
6. Tôi có thói quen gửi email phản pháo ngay lập tức khi vừa đọc xong một thông điệp gây ức chế?
7. Những tác nhân (triggers) cụ thể nào khiến tôi dễ mất kiểm soát lý trí và nổi giận nhất?
8. Tôi có thường xuyên bỏ bê việc chăm sóc thể lực và giấc ngủ, khiến ngưỡng chịu đựng cảm xúc bị suy giảm?
9. Lần gần nhất tôi nói ra một lời cay độc trong lúc giận dữ và phải ân hận sâu sắc là khi nào?
10. Tại sao tôi lại ngại nhờ người khác đóng vai phản biện gay gắt để diễn tập trước?

#### Nhóm 3: Ứng dụng Thực tế & Giải quyết Vấn đề (Practical Application & Problem Solving)
11. Tôi có thể thiết lập rào chắn công nghệ nào trên điện thoại và máy tính để ngăn các phát ngôn bốc đồng?
12. Câu nói nào tôi sẽ chuẩn bị sẵn để chủ động xin hoãn cuộc họp khi nhận thấy mình sắp mất bình tĩnh?
13. Ai là người đồng nghiệp điềm đạm nhất mà tôi có thể tin tưởng gửi gắm nhờ đọc duyệt email trước khi gửi?
14. Làm thế nào để giải phóng bớt năng lượng dư thừa của cơn giận mà không gây tổn hại cho người xung quanh?
15. Các bài tập thể lực và nhịp thở nào mang lại hiệu quả hạ nhiệt nhanh nhất cho cơ thể tôi?

#### Nhóm 4: Bứt phá Giới hạn & Chuyển hóa Tương lai (Breakthrough & Transformation)
16. Nếu tôi làm chủ hoàn hảo cả nỗi sợ hãi lẫn cơn giận dữ, phong thái lãnh đạo của tôi sẽ uy nghiêm đến mức nào?
17. Làm sao để biến năng lượng của sự bất bình trước cái sai thành ngọn lửa bền bỉ thúc đẩy cải cách tổ chức?
18. Di sản về sự điềm đạm, bản lĩnh và tự chủ mà tôi muốn các thế hệ sau học tập là gì?
19. Làm thế nào để xây dựng một môi trường văn hóa công sở nơi mọi người cùng nâng đỡ cảm xúc cho nhau?
20. Bài học tâm đắc nhất từ trải nghiệm cài đặt Outlook 60 phút của giáo sư Jim Detert đối với tôi là gì?

---

## 6. Bản Đồ Tư Duy Trực Quan (Visual Mindmap Overview - Tinh Gọn 4-5 Tầng)

```mermaid
mindmap
  root((QUẢN TRỊ CẢM XÚC))
    ⚡ Đối Lập Sinh Lý
      Sợ hãi né tránh
        Tháo chạy đóng băng
          Điều hòa sinh lý
            Chạy bộ yoga
      Giận dữ tiếp cận
        Xông thẳng đối đầu
          Mất kiểm soát lý trí
            Hành xử vụng về
    🧘 Làm Dịu Tức Thời
      Thần kinh phó giao cảm
        Đếm từ một đến mười
          Hít thở sâu ba lần
            Làm chậm nhịp tim
      Dời lịch đối thoại
        Tránh bốc hỏa
          Hẹn sang sáng mai
            Lấy lại cân bằng
    💻 Trì Hoãn Công Nghệ
      Bài học Jim Detert
        Email lúc bực bội
          Sai lầm kinh điển
            Hối hận muộn màng
      Bộ đếm giờ Outlook
        Cài đặt sáu mươi phút
          Giữ thư hộp thư đi
            Đọc lại sửa đổi
```
"""

C09_MINDMAP = """# 🧠 BẢN ĐỒ TƯ DUY TINH GỌN (4-5 TẦNG): CHƯƠNG 9 - CHUẨN BỊ VÀ QUẢN TRỊ CẢM XÚC SỢ HÃI LẪN GIẬN DỮ

## 1. Sơ Đồ Tư Duy Trực Quan (Mermaid Mindmap Tinh Gọn)

```mermaid
mindmap
  root((QUẢN TRỊ CẢM XÚC))
    ⚡ Bản Chất Sinh Học
      Sợ hãi né tránh
        Avoidance Emotion
          Kịch bản diễn tập
            Giữ vững vị thế
      Giận dữ tiếp cận
        Approach Emotion
          Làm mờ lý trí
            Tổn thương người khác
    🧘 Làm Dịu Cấp Tốc
      Phó giao cảm
        Vagus Nerve Reset
          Thở hộp sâu
            Đếm từ một đến mười
      Tạm dừng chiến lược
        Reschedule Meeting
          Hạ hỏa tâm lý
            Đối thoại điềm tĩnh
    💻 Rào Chắn Công Nghệ
      Kinh nghiệm Detert
        Executive Vulnerability
          Hộp thư đi Outbox
            Bộ đếm giờ Outlook
      Đệm sáu mươi phút
        Khoảng lặng cứu rỗi
          Bình tâm sửa đổi
            Ngăn chặn sai lầm
```

---

## 2. Cây Phân Cấp Tri Thức Gợi Nhớ Nhanh 4-5 Tầng (Active Recall Hierarchy)

- 📌 **Bản Chất Sinh Học Đối Lập (Biological Action Tendencies)**
  - 🔹 *Sợ hãi (Né tránh):* ➔ *Avoidance Emotion* ➔ *Tháo chạy & Câm lặng* ➔ *Diễn tập kịch bản chịu áp lực*
  - 🔹 *Giận dữ (Tiếp cận):* ➔ *Approach Emotion* ➔ *Tê liệt vỏ não thùy trán* ➔ *Hành xử vụng về gây tổn hại*
- 📌 **Kỹ Thuật Làm Dịu Cấp Tốc (In-the-Moment Physiological Soothing)**
  - 🔹 *Kích hoạt phó giao cảm:* ➔ *Kích thích dây thần kinh phế vị* ➔ *Thở sâu & Đếm 1-10* ➔ *Hạ nhịp tim tức thời*
  - 🔹 *Tạm dừng chiến lược:* ➔ *Không lên tiếng lúc bốc hỏa* ➔ *Dời lịch hẹn sang buổi sau* ➔ *Lấy lại cân bằng*
- 📌 **Rào Chắn Công Nghệ Trì Hoãn (Technological Guardrails)**
  - 🔹 *Bài học tự vấn Jim Detert:* ➔ *Dũng cảm nhưng thiếu năng lực* ➔ *Gửi email lúc bực tức* ➔ *Hủy hoại quan hệ*
  - 🔹 *Quy tắc Outlook 60 phút:* ➔ *Hẹn giờ giữ thư trong Outbox* ➔ *Khoảng đệm hạ nhiệt 1 giờ* ➔ *Đọc lại và sửa sai*

---

## 3. Bảng Neo Trí Nhớ Từ Khóa Vàng (Memory Anchor Cheat Sheet)

| Từ Khóa Cốt Lõi | Phần Trong Tài Liệu | Bản Chất / Vai Trò (3-5 từ) | Tín Hiệu Gợi Nhớ (Memory Trigger) |
| :--- | :--- | :--- | :--- |
| **Khuynh Hướng Cảm Xúc** | Phần I | Sợ né tránh vs Giận tiếp cận | Con linh dương chạy vs Con hổ vồ |
| **Diễn Tập Áp Lực** | Phần I | Đóng vai phản biện tôi luyện | Đấu sĩ tập dượt trong võ đài |
| **Phó Giao Cảm** | Phần II | Phanh hãm nhịp tim cơ thể | Bàn đạp phanh xe khẩn cấp |
| **Dời Lịch Hẹn** | Phần II | Khoảng lặng chiến lược tránh hỏa | Tấm biển "Tạm nghỉ phục vụ" |
| **Bài Học Jim Detert** | Phần III | Thừa nhận sai lầm để sửa mình | Vị giáo sư đứng nhìn màn hình |
| **Outlook 60 Phút** | Phần III | Phao cứu sinh công nghệ đắt giá | Đồng hồ cát đếm ngược trên thư |
"""

c9_dir = os.path.join(BASE_DIR, "09-Prepare-for-fear-and-anger")
with open(os.path.join(c9_dir, "summary.md"), "w", encoding="utf-8") as f:
    f.write(C09_SUMMARY.strip() + "\n")
with open(os.path.join(c9_dir, "mindmap.md"), "w", encoding="utf-8") as f:
    f.write(C09_MINDMAP.strip() + "\n")
print("[✓] Chapter 09 files written successfully.")
