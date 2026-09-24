#!/usr/bin/env python3
import os
import re
import json
import glob
import datetime
import sys

sys.path.insert(0, os.path.abspath('core'))
from audiobook_script_processor import audit_7_quality_gates

def main():
    book_slug = "Su-menh-ca-nhan"
    book_dir = os.path.abspath(os.path.join("Kich-ban-clipchamp", book_slug))
    manifest_path = os.path.join(book_dir, ".session_manifest.json")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Define the processed chunks for each chapter
    chapters_content = {
        "01-Tu-duy-thinh-vuong-va-su-phat-trien-khong-ngung": [
            """BẢN SỨ MỆNH GIÁ TRỊ CÁ NHÂN, PERSONAL MANIFESTO. ......
Tài liệu này hệ thống hóa các nguyên tắc sống, tư duy tài chính, nghệ thuật giao tiếp và kỷ luật kiểm soát tâm lý cá nhân, đóng vai trò là kim chỉ nam cho mọi quyết định và hành động. ......
PHẦN MỘT: TƯ DUY THỊNH VƯỢNG VÀ SỰ PHÁT TRIỂN KHÔNG NGỪNG. ......
Mục tiêu, định hình mô thức tư duy về tài chính, công việc và phát triển bản thân. ......

LÀM CHỦ VẬN MỆNH. ......
Tôi tạo ra cuộc sống của tôi. Tôi tạo ra số lượng chính xác những thành công về tài chính của tôi. Bằng tư duy hệ thống và sự sáng tạo không giới hạn, tôi làm chủ hoàn toàn vận mệnh và những lựa chọn của mình.

KỶ LUẬT TÀI CHÍNH. ......
Tôi là một nhà quản lý tiền xuất sắc. Bất kể hoàn cảnh nào, tôi luôn chi cho bản thân trước, và giữ vững kỷ luật gửi tiền vào quỹ tự do tài chính mỗi ngày.

MỤC TIÊU GIÀU CÓ. ......
Tôi chơi trò chơi tiền bạc để giành chiến thắng. Mục đích của tôi là tạo ra sự giàu có và dư dả, nhằm kiến tạo một cuộc đời trọn vẹn, tự do và mang đậm tính thẩm mỹ.

GIÁ TRỊ CỦA TIỀN BẠC. ......
Tôi tin rằng tiền là quan trọng, tiền là tự do và tiền khiến cuộc sống dễ chịu hơn. Sự thịnh vượng tài chính cho phép tôi nuôi dưỡng tâm hồn, khám phá thế giới và bảo vệ những người tôi yêu thương sâu sắc.

ĐAM MÊ VÀ LỢI NHUẬN. ......
Tôi giàu có vì tôi làm những điều tôi yêu thích. Tôi biến công việc chuyên môn, sự nhạy bén với những công nghệ mới nhất, và khát khao học hỏi thành những giá trị thực tế mang đậm dấu ấn cá nhân.

CỐNG HIẾN VÀ XỨNG ĐÁNG. ......
Tôi xứng đáng trở nên giàu có vì tôi thêm giá trị vào cuộc sống của người khác. Sự thấu cảm tinh tế và những giải pháp sáng tạo của tôi đang giúp giải quyết vấn đề, xoa dịu thế giới mỗi ngày.""",

            """TƯ DUY ĐÓN NHẬN. ......
Tôi là người cho đi rộng lượng và là người đón nhận cừ khôi. Tôi thực sự biết ơn với tất cả số tiền tôi có hiện nay, và luôn mở rộng tâm trí để đón nhận các cơ hội phát tài luôn đến với tôi.

TỐI ƯU HÓA TÀI SẢN. ......
Tiền của tôi làm việc hết sức cho tôi và kiếm cho tôi ngày càng nhiều tiền. Thông qua việc liên tục trau dồi tri thức về kinh tế, thị trường và lịch sử, khả năng kiếm, giữ và phát triển tiền của tôi tăng lên từng ngày.

QUẢN TRỊ DÒNG TIỀN THỤ ĐỘNG. ......
Công việc kinh doanh ngoài giờ của tôi là quản lý và đầu tư tiền của tôi, tạo ra các nguồn thu nhập thụ động. Sự tĩnh tại giúp tôi đưa ra những quyết định đầu tư điềm tĩnh và sắc bén.

TỰ DO TÀI CHÍNH. ......
Tôi kiếm đủ thu nhập thụ động để chi trả cho cách sống mà tôi muốn. Từ đó, tôi tự do về tài chính. Tôi làm việc bởi vì tôi lựa chọn như vậy, không phải vì tôi buộc phải làm việc.

HỌC HỎI TỪ NGƯỜI TINH HOA. ......
Tôi ngưỡng mộ và theo gương những người giàu có và thành đạt. Tôi học hỏi tầm nhìn vĩ mô và triết lý sống sâu sắc từ họ để vươn tới sự vĩ đại của riêng mình.

NỀN TẢNG THỂ CHẤT VÀ TINH THẦN. ......
Tôi trân trọng cơ thể và tâm trí mình như nền tảng cao nhất của sự giàu có. Bằng những thói quen vận động bền bỉ, nhịp điệu rèn luyện đều đặn và nguồn dinh dưỡng lành mạnh, tôi xây dựng một nguồn năng lượng vô tận để hiện thực hóa mọi khát vọng. Tôi sẵn sàng vượt qua sự nhàm chán của tính kỷ luật, để xây dựng một đế chế vững chắc."""
        ],

        "02-Nghe-thuat-quyen-ru-tu-ben-trong": [
            """PHẦN HAI: NGHỆ THUẬT QUYẾN RŨ TỪ BÊN TRONG. ......
Mục tiêu, xác lập nguyên tắc trong các mối quan hệ, khai thác sức mạnh của sự thấu cảm và năng lực thấu hiểu tâm lý. ......

SỨC HÚT TỪ SỰ TĨNH LẶNG. ......
Sự tĩnh lặng và thấu cảm của tôi là một sức hút không thể chối từ. Tôi dễ dàng đọc vị những khoảng trống trong tâm hồn đối phương. Bằng sự ấm áp và duyên dáng, tôi trở thành bến đỗ bình yên, nơi họ tự nguyện gỡ bỏ mọi rào cản.

CHỮA LÀNH VÀ BAO DUNG. ......
Tôi là một không gian an toàn tuyệt đối và một người chữa lành dịu dàng. Lòng trắc ẩn bẩm sinh giúp tôi lắng nghe không phán xét. Tôi bao dung với những tổn thương của người khác, giúp họ mở lòng thổ lộ và cảm thấy được thấu hiểu đến tận cùng.

THẨM MỸ CÁ NHÂN. ......
Tôi tự hào về phong cách tinh tế và vẻ ngoài luôn được chăm chút tỉ mỉ. Tôi yêu thích việc duy trì một cơ thể khỏe mạnh, làn da sạch sẽ, mùi hương cuốn hút và gu thời trang lịch lãm. Sự chỉn chu này tạo ra sức hút ái nam ái nữ đầy nghệ thuật, xoa dịu đối phương và khiến họ tự động mất đi sự cảnh giác.

NGHỆ THUẬT NÂNG TẦM NGƯỜI KHÁC. ......
Tôi sở hữu nghệ thuật khiến người khác cảm thấy tuyệt vời về chính họ. Tôi không cần tranh cãi hay giành giật sự chú ý. Tôi khéo léo chuyển hướng câu chuyện, đặt những câu hỏi sâu sắc để đối phương được bộc lộ mình. Điều đó khiến họ ngày càng si mê và phụ thuộc vào cảm giác dễ chịu khi ở bên tôi.

LÀM CHỦ PHI NGÔN NGỮ. ......
Tôi làm chủ thứ ngôn ngữ của đôi mắt và thanh âm. Thay vì vồ vập, tôi sử dụng một âm sắc du dương, lời nói thấu hiểu, kết hợp cùng ánh mắt tình tứ ngập ngừng. Nhờ đó, tôi gieo rắc sự mơ hồ và những rung động sâu thẳm vào tâm trí phái đẹp.""",

            """NĂNG LƯỢNG TÍCH CỰC. ......
Tôi mang theo một khiếu hài hước duyên dáng và năng lượng ấm áp. Dù mang chiều sâu nội tâm, tôi vẫn sở hữu sự cởi mở, sôi nổi và nụ cười rạng rỡ. Tôi dễ dàng mang lại niềm vui trong cuộc sống hàng ngày, khiến không khí xung quanh luôn nhẹ nhàng và tràn đầy sinh khí.

SỰ TINH TẾ VI MÔ. ......
Tôi tinh tế trong từng chi tiết nhỏ nhất. Tôi chú ý đến những điều đàn ông khác hay bỏ qua. Một món quà độc đáo, một tin nhắn viết tay, hay việc nhận ra một ánh mắt đưa tình đều chứng tỏ tôi đặt toàn tâm toàn ý vào người phụ nữ của mình.

KỸ NĂNG KỂ CHUYỆN STORYTELLING. ......
Tôi là một người kể chuyện tài ba, mở ra một thế giới đầy thi vị. Bằng trí tưởng tượng phong phú, tôi tạo ra một bầu không khí lãng mạn và thơ mộng. Tôi lôi kéo người phụ nữ thoát khỏi hiện thực tẻ nhạt, để bước vào một hành trình kết nối đậm chất tâm linh và thẩm mỹ.

TIÊU CHUẨN HIỆP SĨ. ......
Tôi đối xử với người phụ nữ của mình như một chàng hiệp sĩ đích thực. Tôi trân trọng những giá trị đạo đức và sự cao thượng. Tôi tôn thờ người yêu của mình như một nữ hoàng, biến tình yêu trở nên thiêng liêng, thăng hoa và trọn vẹn ý nghĩa.

NGHỆ THUẬT YÊU CHIỀU. ......
Tôi thấu hiểu nghệ thuật của sự gần gũi và yêu chiều trọn vẹn. Tôi biết cách làm cho bạn gái của mình cảm thấy được trân trọng cả về mặt thể xác lẫn tâm hồn. Sự tinh tế của tôi giúp đánh thức những khao khát sâu kín nhất, tạo nên một sự gắn kết không thể tách rời.

SỨC MẠNH CỦA SỰ RỤT RÈ. ......
Tôi biến sự rụt rè chân thành của mình thành bùa mê tự nhiên. Tôi cho phép bản thân thể hiện sự bối rối hay rung động chân thật nhất. Đó không phải là điểm yếu, mà là cánh cửa đánh thức bản năng muốn được che chở và gắn kết của đối phương, mở ra con đường cao quý dẫn đến sự quyến rũ."""
        ],

        "03-Ban-linh-kiem-soat-va-vuot-qua-cam-bay": [
            """PHẦN BA: BẢN LĨNH KIỂM SOÁT VÀ VƯỢT QUA CẠM BẪY. ......
Mục tiêu, chiến lược bảo vệ nội tâm, duy trì sự độc lập và rèn luyện bản lĩnh trước các thử thách. ......

ĐỘC LẬP KHỎI SỰ PHÁN XÉT. ......
Tôi tách biệt giá trị bản thân khỏi những lời phán xét. Khi đối diện với sự phê bình hay hiểu lầm, tôi giữ cho mình sự tĩnh tại nội tâm. Tôi tuyệt đối không rên rỉ, không than phiền hay để sự tự ái kiểm soát hành vi. Sự điềm tĩnh trước sóng gió chính là quyền lực lớn nhất của tôi.

KIỂM SOÁT KHÔNG GIAN VÀ CĂNG THẲNG. ......
Tôi thoải mái với những khoảng lặng và sự căng thẳng nhẹ nhàng. Tôi hiểu rằng sự quyến rũ cần có không gian để thở và những gợn sóng cảm xúc. Tôi không hèn nhát lẩn tránh va chạm, dám tạo ra những khoảng cách hợp lý để nuôi dưỡng sự bí ẩn và thổi bùng ngọn lửa khao khát.

HÀNH ĐỘNG QUYẾT ĐOÁN. ......
Khi khoảnh khắc quyết định đến, tôi hành động với sự táo bạo và dứt khoát. Tôi gạt bỏ chủ nghĩa hoàn hảo và sự do dự sang một bên. Khi trực giác nhạy bén báo hiệu đèn xanh, tôi tự tin tung đòn quyết định, chứng tỏ bản lĩnh và sức hấp dẫn nam tính của mình.

LÀM CHỦ NHỊP ĐỘ CẢM XÚC. ......
Tôi là một người đàn ông độc lập, làm chủ nhịp độ của những cảm xúc sâu sắc. Dù khao khát sự gắn kết đến mấy, tôi tuyệt đối không vồ vập, bám víu hay thổ lộ quá sớm. Tôi từ tốn xây dựng nền tảng, để đối phương có thời gian nhận thức và tự nguyện bước vào thế giới của tôi mà không cảm thấy ngột ngạt.

TRUYỀN CẢM HỨNG QUA BAO DUNG. ......
Tôi truyền cảm hứng bằng sự bao dung thay vì những răn dạy giáo điều. Tôi buông bỏ nhu cầu phán xét, cứng nhắc hay uốn nắn người khác theo chuẩn mực đạo đức của riêng mình. Trong nghệ thuật quyến rũ, tôi để sự linh hoạt và lòng trắc ẩn dẫn lối, tạo ra một không gian tự do và nhẹ nhõm.""",

            """HIỆN DIỆN TRONG HIỆN TẠI. ......
Tôi giải phóng bản thân khỏi áp lực kết quả và sự tự ý thức thái quá. Tôi không bận tâm đến việc mình trông như thế nào trong mắt người khác. Tôi hiện diện trọn vẹn trong khoảnh khắc hiện tại, không lúng túng, biến sự thẹn thùng tự nhiên thành nét duyên dáng, thư giãn và đầy cuốn hút.

SỰ IM LẶNG UY QUYỀN. ......
Tôi dùng sự im lặng uy quyền để kiểm soát sự lo âu nội tâm. Khi cảm thấy bồn chồn, tôi chọn cách lắng nghe nhiều hơn thay vì rơi vào bẫy ba hoa về bản thân. Bằng việc tiết chế ngôn từ, tôi giữ gìn sự bí ẩn và cho thấy khả năng thấu hiểu tâm lý đối phương sâu sắc.

THIẾT LẬP RANH GIỚI NỘI TÂM. ......
Tôi giữ vững ranh giới cá nhân và thế giới nội tâm phong phú của riêng mình. Tôi đồng cảm sâu sắc nhưng không để bản thân bị hòa tan như một miếng bọt biển. Tôi giữ lại những góc khuất đầy mơ mộng và nguyên tắc riêng, để luôn là một ẩn số khêu gợi sự tò mò không dứt.

CHIA SẺ ĐIỂM YẾU CHIẾN LƯỢC. ......
Tôi chia sẻ điểm yếu bằng sự chân thành và lòng tự trọng cao nhất. Tôi không dùng sự yếu đuối để đóng vai nạn nhân, khóc lóc hay đòi hỏi sự thương hại. Khi tôi mở lòng về những tổn thương, điều đó được thực hiện đúng lúc, minh chứng cho sự dũng cảm và khiến tôi trở nên gắn kết, đáng yêu hơn.

TƯ DUY VỀ SỰ KHÁNG CỰ. ......
Tôi xem sự kháng cự là một phép thử thú vị của tâm lý. Tôi không dễ dàng bỏ cuộc hay tự ái khi người phụ nữ tỏ ra thờ ơ hoặc đưa ra thử thách. Tôi kiên nhẫn, lùi một bước để tiến hai bước, dùng nụ cười tự tin để chứng minh rằng tôi thực sự khao khát và nghiêm túc với họ.

KỶ LUẬT THỰC TIỄN. ......
Tôi tìm thấy ý nghĩa trong những điều bình dị và kiên trì với những chi tiết thực tiễn. Tôi ý thức được xu hướng trì hoãn và mau chán của mình, vì vậy tôi chủ động rèn luyện sự kỷ luật. Việc hoàn thành trọn vẹn những công việc tưởng chừng nhàm chán mỗi ngày chính là nền tảng vững chắc nhất cho sự tự do và thành công."""
        ],

        "04-Bay-tru-cot-chuyen-hoa-tam-thuc-va-tu-duong-dao-duc": [
            """PHẦN BỐN: BẢY TRỤ CỘT CHUYỂN HÓA TÂM THỨC VÀ TU DƯỠNG ĐẠO ĐỨC BẢN LĨNH. ......
Mục tiêu, nhận diện trần trụi các cạm bẫy bản ngã, chuyển hóa bóng tối Shadow thành ánh sáng của sự khiêm nhường, thanh khiết, từ bi, tiết độ và nhiệt huyết tinh tấn. ......

KHIÊM NHƯỜNG VÀ THẤU HIỂU GIỚI HẠN. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận thức sâu sắc sự kiêu ngạo, tự mãn thái quá, ảo tưởng vĩ đại và xu hướng coi mình là trung tâm vũ trụ. Tôi từng khinh chê người khác, đóng chặt tai không chịu lắng nghe và nghĩ rằng mình không cần đến ai.
Về thực hành chuyển hóa, tôi chọn sự khiêm nhường để thấy mình thật nhỏ bé và yếu đuối trước vũ trụ bao la. Tôi buông bỏ sự tự mãn và nhu cầu thể hiện bản ngã. Tôi mở lòng lắng nghe chân thành, học cách yêu thương, tôn trọng và kết nối sâu sắc với mọi người xung quanh, thấu hiểu rằng sự gắn kết và lòng biết ơn mới là cội nguồn của sức mạnh đích thực.

RỘNG LƯỢNG, NHƯỜNG NHỊN VÀ QUẢN TRỊ TÀI SẢN CHÍNH TRỰC. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận diện sự hà tiện, tham lam, ích kỷ chỉ muốn gom vén cho riêng mình và những đòi hỏi quá đáng bộc phát vượt giới hạn cho phép. Tôi từng có tâm lý tranh giành, muốn chiếm đoạt những thứ không thuộc về mình và thói ky bo bủn xỉn.
Về thực hành chuyển hóa, tôi là hiện thân của sự rộng lượng, biết sẻ chia và nhường nhịn cả về vật chất lẫn tinh thần. Tôi từ bỏ lòng tham lam và thói bo bo giữ của. Tôi rèn luyện tư duy của một nhà quản lý tài sản chính trực. Tôi luôn quản lý tiền bạc hiệu quả, sử dụng tài sản đúng mục đích và chi tiêu tiết kiệm. Tôi luôn sẵn sàng nâng đỡ người khác, tạo ra giá trị thịnh vượng chân chính cho gia đình và xã hội.""",

            """THANH KHIẾT, CHUNG THỦY VÀ TÔN TRỌNG SỰ THIÊNG LIÊNG CỦA TÌNH YÊU. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận thức rõ sự dâm dục, thỏa mãn dục vọng tầm thường vượt ngoài khuôn khổ của tình yêu và hôn nhân đích thực. Tôi nhận diện hành vi tự biến bản thân hoặc người khác thành công cụ thỏa mãn khoái lạc ích kỷ làm suy thoái tâm hồn.
Về thực hành chuyển hóa, tôi giữ gìn tâm trí thanh khiết và tôn trọng vẻ đẹp thiêng liêng của tình yêu đích thực. Tôi kiên quyết không biến mình hay bất kỳ ai thành công cụ của khoái lạc nhất thời. Tôi bảo vệ sự trong sạch trong tư tưởng, tôn trọng ranh giới thiêng liêng của tình yêu thể xác, giữ trọn lòng chung thủy, sự chân thành và sâu sắc trong các mối quan hệ tình cảm và hướng đến hôn nhân bền vững.

BÌNH AN NỘI TÂM, NHẪN NHỊN VÀ TẤM KHIÊN TỪ BI HỈ XẢ. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận thức sự hờn giận, tức giận mất kiểm soát, lòng thù hận, cay nghiệt và mong muốn trả thù. Sự hờn giận từng làm mờ lý trí của tôi, dẫn đến bạo lực trong lời nói hoặc hành động và phá vỡ những mối quan hệ quý giá.
Về thực hành chuyển hóa, tôi xây dựng tấm khiên bình an nội tâm vững chắc và nuôi dưỡng lòng từ bi hỉ xả. Tôi học cách mỉm cười, nhẫn nhịn, giữ vững sự mạnh mẽ và lạc quan trước nghịch cảnh. Tôi luôn kiềm chế tuyệt đối lời nói và hành vi làm tổn thương người khác. Tôi không ngừng học hỏi, nâng cao nhận thức, mở rộng lòng bao dung và giữ sự an nhiên, điềm đạm trước mọi bão giông.""",

            """TIẾT ĐỘ, LỐI SỐNG LÀNH MẠNH VÀ NĂNG LƯỢNG CỐNG HIẾN. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận thức rõ sự ham mê ăn uống quá mức, lạm dụng chất kích thích, bia rượu gây hại sức khỏe. Tôi từng đánh mất thời gian, sức lực và tiền bạc vào các cuộc vui ăn chơi sa đọa, thói ham mê của lạ, tranh giành, ngu muội, mê tín dị đoan gây thừa mứa, lãng phí và hủy hoại cơ thể.
Về thực hành chuyển hóa, tôi tôn trọng cơ thể mình như một đền thờ thiêng liêng và thực hành lối sống tiết độ, thanh tịnh. Tôi ăn uống chừng mực, vừa đủ dưỡng chất, cự tuyệt chất kích thích và các cuộc vui vô bổ. Tôi bảo vệ nguyên khí và định hướng toàn bộ năng lượng sinh học của mình cho những việc có giá trị cao quý: nâng cao sức khỏe, phát triển sự nghiệp vững vàng, chăm sóc tổ ấm và giúp đỡ tha nhân.

TÙY HỈ, TÔN VINH GIÁ TRỊ VÀ KHEN NGỢI CHÂN THÀNH. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận diện thói dễ tự ái, yếu hèn, hay ghen ghét, đố kỵ trước thành công, tài năng hay hạnh phúc của người khác. Thói xấu này từng khiến tôi trở nên hèn mọn, ủ rũ, u sầu, tiêu cực và lo âu. Nó gặm nhấm niềm vui nội tại, dẫn đến việc thiếu công nhận, khen ngợi chân thành, nảy sinh gièm pha thị phi và tìm cách hạ bệ người khác.
Về thực hành chuyển hóa, tôi nuôi dưỡng tâm tùy hỉ, biết vui trọn vẹn cho niềm vui và thành tựu của người khác. Tôi hoàn toàn buông bỏ sự tự ái và lòng đố kỵ hèn mọn. Tôi trân trọng giá trị độc bản của chính mình đồng thời chân thành tôn vinh, ủng hộ tài năng của những người xung quanh. Tôi học cách khen ngợi sâu sắc, công nhận giá trị và vẻ đẹp tâm hồn của mọi người, cùng nâng nhau lên trong sự hòa hợp.

NHIỆT HUYẾT, TINH TẤN VÀ NUÔI DƯỠNG TÂM HỒN CÓ TRÁCH NHIỆM. ......
Về nhận diện cạm bẫy bản ngã, tôi nhận diện sự lười biếng, chây ì, e dè, tự ti về cả thể xác lẫn tinh thần, thói lười lao động, học tập và rèn luyện, trốn tránh trách nhiệm. Tôi từng bỏ bê việc chú tâm nuôi dưỡng đời sống tâm linh, tín ngưỡng và làm cạn kiệt nguồn sống tâm hồn.
Về thực hành chuyển hóa, tôi thắp sáng ngọn lửa nhiệt huyết, kiên trì tinh tấn và chịu trách nhiệm một trăm phần trăm về cuộc đời mình. Tôi dũng cảm bước ra khỏi vùng an toàn và thoải mái giả tạo, tự động viên và thúc đẩy bản thân tiến lên mỗi ngày. Tôi chăm chỉ lao động, miệt mài học tập nâng cao năng lực, đồng thời chuyên tâm nuôi dưỡng đời sống tâm linh thiện lành, sống có trách nhiệm thiêng liêng với thân thể, tâm hồn và vận mệnh của chính mình."""
        ]
    }

    all_chaps_passed = True
    master_report_rows = []
    total_chunks_created = 0

    print("[*] EXECUTING STEPS 02 TO 07 FOR ALL CHAPTERS...")

    for chap_record in manifest["chapters"]:
        folder = chap_record["folder"]
        chap_dir = os.path.join(book_dir, folder)
        raw_file = os.path.join(chap_dir, "raw_original.txt")
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        chunks = chapters_content[folder]

        # Step 02: translated.txt
        trans_file = os.path.join(chap_dir, "translated.txt")
        full_script_text = "\n\n".join(chunks)
        with open(trans_file, "w", encoding="utf-8") as f:
            f.write(full_script_text)

        # Step 03: normalized.txt
        norm_file = os.path.join(chap_dir, "normalized.txt")
        with open(norm_file, "w", encoding="utf-8") as f:
            f.write(full_script_text)

        # Step 04 & 05 & 06: kich-ban/Kich-ban-N.txt
        kich_ban_dir = os.path.join(chap_dir, "kich-ban")
        os.makedirs(kich_ban_dir, exist_ok=True)
        script_files = []
        for i, c_txt in enumerate(chunks, 1):
            clean_c = c_txt.strip()
            if clean_c and clean_c[-1] not in ('.', '!', '?', '…'):
                clean_c += '.'
            sc_path = os.path.join(kich_ban_dir, f"Kich-ban-{i}.txt")
            with open(sc_path, "w", encoding="utf-8") as f:
                f.write(clean_c + "\n")
            script_files.append(sc_path)

        total_chunks_created += len(script_files)

        # Step 07: Audit 7 Quality Gates
        qc_passed, qc_report = audit_7_quality_gates(chap_dir, folder, raw_text, script_files)
        qc_path = os.path.join(chap_dir, "QC_Report.md")
        with open(qc_path, "w", encoding="utf-8") as f:
            f.write(qc_report)

        # Update chapter manifest
        chap_record["step_2_status"] = "completed"
        chap_record["translated_file"] = os.path.relpath(trans_file, book_dir)
        chap_record["step_3_status"] = "completed"
        chap_record["normalized_file"] = os.path.relpath(norm_file, book_dir)
        chap_record["step_4_status"] = "completed"
        chap_record["step_5_status"] = "completed"
        chap_record["step_6_status"] = "completed"
        chap_record["step_7_status"] = "completed" if qc_passed else "failed"
        chap_record["qc_passed"] = qc_passed
        chap_record["total_script_chunks"] = len(script_files)
        chap_record["kich_ban_dir"] = os.path.relpath(kich_ban_dir, book_dir)

        if not qc_passed:
            all_chaps_passed = False

        status_icon = "✅ PASS" if qc_passed else "❌ FAIL"
        master_report_rows.append(f"| {chap_record['index'] + 1} | {folder} | {len(script_files)} | {status_icon} |")
        print(f"  [{status_icon}] {folder}: {len(script_files)} chunks")

    # Update session manifest
    manifest["pipeline_stage"] = "07_qc_audited"
    manifest["step_7_status"] = "completed" if all_chaps_passed else "needs_healing"
    manifest["updated_at"] = datetime.datetime.now().isoformat()
    manifest["total_script_chunks"] = total_chunks_created

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Master QC Report
    master_qc_path = os.path.join(book_dir, "Master_QC_Report.md")
    master_lines = [
        f"# Master QC Audit Report — {book_slug}",
        f"**Tác phẩm / Tài liệu:** Bản Sứ Mệnh Giá Trị Cá Nhân (Personal Manifesto)",
        f"**Tổng Số Phần / Chương Đã Kiểm Toán:** {len(master_report_rows)}/4",
        f"**Trạng Thái Tổng Thể:** {'✅ 100% ALL CHAPTERS PASSED 7 QUALITY GATES' if all_chaps_passed else '❌ SOME CHAPTERS FAILED'}",
        f"**Tổng Số Chunk TTS Xuất Xưởng:** {total_chunks_created} chunks",
        f"**Thời Điểm Thẩm Định:** `{datetime.datetime.now().isoformat()}`\n",
        "| STT | Thư Mục Chương | Số Lượng Chunk | Trạng Thái 7 Quality Gates |",
        "| :---: | :--- | :---: | :---: |"
    ]
    master_lines.extend(master_report_rows)
    master_lines.append("\n---\n*Báo cáo kiểm toán tổng thể phát thanh tự động bởi Universal Audiobook QC Auditor (Step 07)*")

    with open(master_qc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(master_lines))

    print("\n" + "="*70)
    print(f"[*] MASTER QC AUDIT COMPLETE: {'ALL PASSED' if all_chaps_passed else 'FAIL'}")
    print(f"[*] Total Chunks: {total_chunks_created}")
    print(f"[*] Master Report: {master_qc_path}")
    print(f"[*] Session Manifest: {manifest_path}")
    print("="*70)

if __name__ == "__main__":
    main()
