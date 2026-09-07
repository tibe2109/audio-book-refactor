---
name: arf_07_audiobook_qc_auditor
description: Bước 7 - Kiểm tra QC đa tầng (Regex, số sót, ký tự cấm, Word Count delta, Red Flag) và xuất báo cáo QC_Report.md.
---

# Audiobook QC Auditor (Kiểm Soát Chất Lượng Kịch Bản Sách Nói)

Skill **07_audiobook_qc_auditor** đóng vai trò là Trưởng Bộ Phận Thẩm Định & Kiểm Soát Chất Lượng (Quality Control & Quality Assurance) trong pipeline sản xuất Audiobook tự động. Skill này đảm bảo 100% kịch bản đạt tiêu chuẩn nghiêm ngặt về kỹ thuật TTS, không sót chữ số, không chứa ký tự cấm, đúng nhịp nghỉ, và không bị AI bớt xén/tóm tắt sai lệch so với bản gốc.

---

## 1. Mục Tiêu & Tiêu Chuẩn Thẩm Định

### A. Tiêu chuẩn Kỹ thuật (Technical Format)
1. **Quy chuẩn tên thư mục chương:**
   - Chỉ sử dụng chữ cái tiếng Anh không dấu, số, và dấu gạch nối `-` (Regex: `^[a-zA-Z0-9\-]+$`).
   - Ví dụ hợp lệ: `01-Loi-mo-dau`, `Chuong-01-Thau-hieu-tam-ly`.
2. **Dung lượng file kịch bản:**
   - Mỗi file `.txt` không được vượt quá **3000 ký tự** (ngưỡng tối ưu: 2200 - 2800 ký tự để API TTS xử lý ổn định, không bị ngắt timeout).
   - Không được để file rỗng (0 bytes).
3. **Ký tự cấm trong kịch bản:**
   - Tuyệt đối không chứa: Ngoặc kép `""` `“”`, ngoặc đơn `()`, ngoặc vuông `[]`, dấu hai chấm `:`, gạch ngang dài `—` `–`.
   - Phải thay thế bằng lời dẫn tự nhiên hoặc ngắt câu phù hợp cho giọng đọc.
4. **Quy tắc phiên âm số (Zero-digit Policy):**
   - Không được sót lại bất kỳ chữ số tự nhiên nào (`0-9`).
   - Mọi con số, năm, phần trăm, số tiền, ngày tháng phải được viết hoàn toàn thành chữ tiếng Việt (Ví dụ: `1986` $\to$ `một nghìn chín trăm tám mươi sáu`, `20%` $\to$ `hai mươi phần trăm`).
5. **Cú pháp nhịp nghỉ & Dấu ba chấm:**
   - Không dùng `...` tùy tiện gây ngắc ngứ.
   - Nhịp nghỉ dài giữa các đoạn/tiêu đề phải tuân thủ định dạng chuẩn: `. ......` (chấm, khoảng trắng, 6 chấm).

### B. Kiểm Tra Chênh Lệch Số Từ (Word Count Delta)
- Đối chiếu tổng số từ của toàn bộ file kịch bản trong chương với file nguồn `raw_original.txt`.
- **Cảnh báo RED FLAG:** Nếu độ lệch số từ $|N_{\text{kịch bản}} - N_{\text{gốc}}| / N_{\text{gốc}} > 30\%$, hệ thống sẽ bật cảnh báo đỏ có nguy cơ bớt xén nội dung (Summarization/Hallucination).

---

## 2. Quy Trình AI Semantic Audit (Thẩm Định Viên AI Đọc Đối Chứng Ngữ Nghĩa)

Khi thẩm định chất lượng hoặc khi script phát hiện cờ **RED FLAG**:

1. **Đọc so sánh song song đa chiều (Parallel Cross-Check):**
   - Mở đồng thời `raw_original.txt` và các file kịch bản `Kich-ban-N.txt` của chương cần thẩm định.
   - Đối chiếu từng phân đoạn ý niệm: Mở đầu $\to$ Luận điểm chính $\to$ Câu chuyện minh họa lịch sử/thực tế $\to$ Đúc kết bài học.
2. **Đánh giá tổn thất ngữ nghĩa (Semantic Loss Assessment):**
   - Kiểm tra xem các câu chuyện, ví dụ minh họa, danh ngôn hay nhân vật lịch sử có bị cắt xén hay không.
   - **Đạt chuẩn (PASS):** Độ lệch số từ do mở rộng từ ngữ phiên âm số (`300km` $\to$ `ba trăm ki-lô-mét`), diễn giải thuật ngữ tự nhiên, hoặc bổ sung liên từ/dấu phẩy lấy hơi cho văn phong nói mà vẫn giữ trọn vẹn 100% ý $\to$ AI cấp chứng nhận **Verified 100%**.
   - **Không đạt (FAIL):** Phát hiện bị lược bỏ đoạn văn, tóm tắt ý chính hoặc thay đổi góc nhìn tác giả $\to$ AI tự động kích hoạt `arf_06_llm_script_refiner` để tái tạo lại phân đoạn đó với chỉ thị cấm tóm tắt nghiêm ngặt.
3. **Đánh giá Độ tự nhiên của Ngữ điệu (Prosody Quality):**
   - AI đọc lướt bằng giọng đọc tưởng tượng để đánh giá xem câu từ có bị vấp, từ ngữ có tự nhiên và êm tai khi phát qua loa hay không.

---

## 3. Hướng Dẫn Kích Hoạt Sub-Agent Thẩm Định Ngữ Nghĩa Từng Chương (Semantic Auditor Subagent)

Khi có cảnh báo RED FLAG hoặc cần kiểm chứng độ sâu ngữ nghĩa của từng chương:

```python
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Semantic Ground-Truth Auditor [01-quy-luat-01]",
            "Prompt": (
                "Bạn là Trưởng ban Thẩm định Ngữ nghĩa & Kiểm soát Chất lượng cho chương '01-quy-luat-01'.\n"
                "Nhiệm vụ: Mở song song '01-quy-luat-01/raw_original.txt' và toàn bộ các file 'Kich-ban-N.txt' của chương này.\n"
                "Tiến hành: Đọc đối soát đối chứng từng đoạn để xác nhận không có bất kỳ luận điểm hay câu chuyện nào bị tóm tắt hoặc bớt xén.\n"
                "Báo cáo: Cung cấp nhận xét thẩm định và xác nhận cấp quyền đóng dấu '- [x]' vào QC_Report.md."
            )
        }
    ]
)
```

---

## 4. Quy Trình Thực Hiện (Action Steps)

### Bước 1: Khởi Chạy Pipeline QC
```powershell
python .agy/skills/arf_07_audiobook_qc_auditor/scripts/qc_pipeline_v2.py --input_dir "<DUONG_DAN_THU_MUC_SACH>"
```

### Bước 2: Phân Tích Kết Quả & Báo Cáo
Đọc file `QC_Report.md` được tạo tại thư mục gốc của sách:
- **Nếu toàn bộ PASS:** Báo cáo xác nhận danh sách `- [x] <Tên-chương>` đạt chuẩn 100% (Verified 100%).
- **Nếu PHÁT HIỆN LỖI:** Hệ thống kích hoạt lại Sub-agent tương ứng để xử lý đúng chương bị lỗi.
