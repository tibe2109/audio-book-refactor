# -*- coding: utf-8 -*-
import os
import json

base_dir = "Kich-ban-clipchamp/Building-the-Courage-to-Speak-Up-and-Stand-Out-at-Work"

translations = {
    "01-Courage-can-be-learned": """# CHƯƠNG 1: LÒNG DŨNG CẢM LÀ KỸ NĂNG CÓ THỂ RÈN LUYỆN

Chào mừng bạn đến với khóa học âm thanh này. Cảm ơn bạn đã lắng nghe. Trong suốt sự nghiệp nghiên cứu về lòng dũng cảm nơi công sở, những phát hiện nào là bất ngờ hoặc đi ngược lại những định kiến thông thường nhất mà tôi đã đúc kết được? Tôi nghĩ có một vài nhận thức sâu sắc đã xuất hiện, thoạt nhìn có vẻ phản trực giác, hoặc ít nhất là trái ngược hẳn với những câu chuyện mà chúng ta thường được nghe kể.

Chẳng hạn, chúng ta thường mang một lầm tưởng thâm căn cố đế. Trên thực tế, tôi biết chắc chắn đó là một ngộ nhận: mọi người tin rằng lòng dũng cảm là một phẩm chất bẩm sinh, một thiên phú trời ban mà chỉ một số ít người may mắn sở hữu, còn đại đa số thì không. Thế nhưng, sau khi đã trực tiếp nghiên cứu hàng nghìn con người và hàng nghìn hành vi dũng cảm trong thực tế, tôi có thể khẳng định với bạn rằng: hoàn toàn không hề có bất kỳ một loại gene dũng cảm kỳ diệu nào cả. Cũng chẳng hề có một nét tính cách đặc biệt hay nền tảng kinh nghiệm ma thuật nào định sẵn điều đó.

Những con người dám dấn thân và hành động đúng đắn tại nơi làm việc khi họ có thể và cần phải làm, thực ra vô cùng đa dạng trên mọi phương diện mà bạn và tôi có thể gọi tên. Vì vậy, một bài học mang tính khai sáng và phá vỡ lầm tưởng lớn nhất đối với tôi chính là: lòng dũng cảm không thuộc về mẫu người bạn sinh ra, mà đó là một sự lựa chọn của chính bạn.

Gắn liền với nhận thức đó, mọi người thường nói về những hành động dũng cảm như thể những cá nhân ấy sinh ra đã sẵn sàng, hoặc hành động đó đối với họ thật dễ dàng. Nhưng trên thực tế, khi bạn nghiên cứu sâu về các cá nhân này, dù đó là nhà hoạt động John Lewis trên chính trường hay vô số con người mà tôi từng nghiên cứu tại các môi trường công sở bình thường, điều bạn nhận ra là: cái vẻ ngoài giống như năng lực thiên bẩm ấy thực chất đến từ quá trình nỗ lực bền bỉ. Đó là nhiều năm luyện tập, nhiều năm thử nghiệm và đúc rút kinh nghiệm để ngày càng trở nên hiệu quả hơn.

Đó chính là bài học cốt lõi thứ hai: lòng dũng cảm cũng giống như bất kỳ một kỹ năng nào khác. Nó được bồi đắp và phát triển thông qua sự rèn luyện và tinh thần cam kết. Một nhận thức sâu sắc khác về chính tiến trình này là chúng ta thường nghĩ quá nhiều về khoảnh khắc bùng nổ, đúng không?

Khi một ai đó dám lên tiếng hoặc bước ra đương đầu, đó là khoảnh khắc chúng ta ghi nhớ và thường lưu truyền qua các câu chuyện kể. Nhưng hóa ra, điều tạo nên sự khác biệt thực sự trong phần lớn trường hợp cho kết quả của khoảnh khắc ấy lại chính là công tác chuẩn bị và những việc mọi người đã làm trước khi hành động, và có lẽ bất ngờ nhất là những gì họ làm sau đó. Những người hành động khôn ngoan không chỉ làm chủ tốt thời khắc then chốt, mà họ còn đặc biệt xuất sắc trong việc theo dõi hậu sự vụ. Khi mọi chuyện diễn ra suôn sẻ, họ biết cách tiếp nối để chốt lại các cam kết, đảm bảo các nguồn lực hỗ trợ; còn khi mọi sự không như ý, họ có đủ dũng khí để thực hiện một cuộc trò chuyện khó khăn khác và thẳng thắn nói rằng: tôi nhận thấy dường như bạn đang buồn bực, tức giận, hoặc ngôn ngữ cơ thể cho thấy bạn chưa thực sự đồng thuận. Chúng ta có thể ngồi lại trò chuyện về điều đó không?

Và tôi nghĩ rằng hành động tiếp nối theo dõi ấy chính là điều mà chúng ta hầu như không mấy khi để tâm, bởi vì chúng ta đã quá tập trung vào khoảnh khắc bùng nổ ban đầu.""",

    "02-Choose-courage": """# CHƯƠNG 2: CHỦ ĐỘNG LỰA CHỌN LÒNG DŨNG CẢM

Có lẽ chúng ta hãy mở rộng góc nhìn một chút. Về cuốn sách Chọn Lòng Dũng Cảm của tôi, luận điểm trung tâm ở đây là gì? Luận điểm cốt lõi, quay trở lại xuất phát điểm ban đầu của chúng ta, thực chất chính là: lòng dũng cảm là một sự lựa chọn mang tính cá nhân, và đó đồng thời là một trách nhiệm.

Sẽ rất hữu ích nếu chúng ta không nhìn nhận lòng dũng cảm như một dạng tài sản hữu hình. Tôi thường nói rằng nếu bạn tiến hành giải phẫu một con người, bạn sẽ không thể tìm thấy bất kỳ một kho chứa lòng dũng cảm nào nằm trong cơ thể họ. Hoàn toàn không có thứ vật chất như vậy. Vì thế, điều cần làm là tư duy dưới góc độ hành động dũng cảm.

Và một khi bạn hiểu rằng vấn đề nằm ở chỗ bạn có dám hành động trong những thời khắc quyết định hay không, bạn sẽ có thể chủ động gánh vác trách nhiệm cá nhân. Theo một nghĩa nào đó, luận điểm ở đây là chúng ta không bao giờ tự cho phép mình coi bất kỳ đức hạnh nào khác chỉ là trách nhiệm của một số ít người, hoặc chỉ cần thực hiện chúng một vài lần ngẫu hứng. Nếu bạn nghĩ về sự công bằng, lòng chừng mực, hay lòng nhân từ, rất nhiều nguyên tắc nền tảng khác đều là những đức hạnh cốt yếu. Những điều đó đâu thể chỉ là trách nhiệm của một trong mười đồng nghiệp quanh ta, hay bản thân ta chỉ cần thực hiện trong một trên mười cơ hội, phải không?

Chúng ta sẽ không bao giờ chấp nhận ai đó nói rằng: Jim này, anh biết đấy, tôi thực sự không phải là một người trung thực. Tôi nhường việc trung thực cho người khác. Sếp của tôi là người trung thực rồi, thế là quá đủ cho cả nhóm chúng tôi.

Tại sao chúng ta lại chấp nhận điều đó? Rõ ràng chúng ta không bao giờ nói như vậy về bất kỳ đức hạnh hay phẩm chất tốt đẹp nào khác.

Vậy thì tại sao chúng ta lại cho phép mình dễ dãi như thế trong địa hạt của lòng dũng cảm? Thành thật mà nói, tôi nghĩ chúng ta thường tự tha thứ và giải thoát cho chính mình quá dễ dàng. Một phần nguyên nhân là vì chúng ta sợ hãi, và vì vậy cuốn sách dành rất nhiều dung lượng để chỉ ra cách đối diện và giải quyết các nỗi sợ. Một phần khác là do chúng ta chưa được trang bị đầy đủ kỹ năng, và khi chứng kiến quá nhiều sự đổ vỡ hay sai lầm ngớ ngẩn ở bản thân cũng như người khác khi cố gắng tỏ ra dũng cảm, chúng ta vội vàng đi đến kết luận rằng việc đó quá nguy hiểm.

Do đó, cuốn sách về căn bản muốn gửi gắm rằng: bạn cần biết chọn đúng thời điểm, nhưng sau đó, bạn phải sẵn sàng chấp nhận một mức độ rủi ro nhất định và phải sẵn lòng nỗ lực để nâng cao năng lực dũng cảm thành thục của chính mình.""",

    "03-Courage-fulfills-us": """# CHƯƠNG 3: LÒNG DŨNG CẢM MANG LẠI SỰ TRỌN VẸN VÀ Ý NGHĨA

Liệu việc lựa chọn lòng dũng cảm có thực sự mang lại lợi ích tốt nhất cho những người làm việc chuyên nghiệp hay không? Liệu điều đó có giúp họ trở nên xuất sắc hơn và thăng tiến trong sự nghiệp, hay tốt hơn hết là nên chọn giải pháp thủ thế an toàn? Bạn nghĩ sao về vấn đề này? Tôi cho rằng về cơ bản có hai câu trả lời cho câu hỏi đó.

Trước hết, điều này phụ thuộc vào mục tiêu của bạn. Nếu mục tiêu của bạn chỉ đơn thuần là thăng tiến nhanh nhất có thể bằng mọi giá, thì thành thực mà nói, bạn và tôi đều biết có rất nhiều tổ chức mà ở đó, định nghĩa của việc làm tốt công việc là cúi đầu im lặng, bảo gì làm nấy và chỉ việc hoàn thành đúng phận sự. Xét theo khía cạnh đó, việc lựa chọn lòng dũng cảm trong ngắn hạn có thể không phải là một ý hay. Nhưng mặt khác, nếu bạn mong muốn sống một cuộc đời nơi bạn cảm thấy mình có quyền tự quyết, nơi bạn được sống chân thực với chính mình và sống đúng với những giá trị mà mình theo đuổi, thì dũng cảm lại là sự lựa chọn hoàn toàn đúng đắn.

Một cách tư duy khác là xem xét trên một tầm nhìn thời gian dài hạn. Nếu bạn băn khoăn liệu việc chọn lòng dũng cảm có nhất thiết giúp mình lập tức đứng đầu danh sách thăng chức tiếp theo hay không, câu trả lời có thể có, mà cũng có thể không. Nhưng khi bạn bắt đầu nhìn vào một tầm nhìn dài hạn hơn, tự hỏi: liệu tôi có tự hào về di sản mà mình đang kiến tạo hay không? Liệu người khác có thực sự nhớ đến tôi và muốn kề vai sát cánh cùng tôi hay không?

Liệu tôi có phải mang những nỗi ân hận dài lâu hay không? Đó chính là lúc sự lựa chọn này trở nên vô cùng then chốt. Chẳng hạn, nếu bạn xem xét các nghiên cứu tâm lý học về sự hối tiếc, một kết luận đã được xác lập rất rõ ràng là: con người có xu hướng ân hận sâu sắc vì những điều họ đã không làm, những điều họ nghĩ mình nên làm nhưng đã bỏ qua, hơn rất nhiều so với những hành động họ đã dấn thân thực hiện dẫu kết quả không như ý.

Điều này đúng ngay cả với những người phải gánh chịu những hậu quả rất nặng nề. Lấy ví dụ như những người dũng cảm đứng ra tố giác sai phạm nơi công sở, hầu như không một ai trong số họ nói rằng mình hối hận vì đã làm điều đó. Vì vậy, điều tôi muốn chia sẻ với thính giả là điều đó tùy thuộc vào bạn. Nếu bạn chỉ quan tâm đến việc làm sao để được lòng mọi người nhất hay tiến thân ngay ngày mai, thì việc vươn cổ chịu đòn không phải lúc nào cũng là cách tiếp cận tốt nhất.

Nhưng nếu bạn đang nói về việc sống một cuộc đời mà bạn, tôi, triết gia Aristotle hay bất kỳ ai khác gọi là một cuộc đời tốt đẹp, thì tôi tin rằng đôi khi bạn bắt buộc phải lựa chọn lòng dũng cảm. Và tôi hình dung điều này đi kèm với việc chấp nhận rủi ro một cách thận trọng, dám đứng lên nói rằng: tôi sẽ đảm nhận dự án lớn này, gánh vác trách nhiệm hay nắm bắt cơ hội này dẫu kết quả còn chưa chắc chắn. Tôi tin rằng mức độ dấn thân đó là thiết yếu để sự nghiệp của bạn có thể bứt phá, bằng không bạn sẽ chẳng có gì nổi bật.

Khi ấy, bạn chỉ giống như bao người khác: bạn làm tròn công việc trong phạm vi trách nhiệm thông thường, không tạo ra bất kỳ cải tiến đáng chú ý hay giá trị đột phá nào. Thành thật mà nói, có một vài con đường để cuối cùng giúp một người trở nên nổi bật.

Một con đường tất nhiên là trở thành một tay chơi chính trị lão luyện nơi công sở. Bạn gắn mình với những nhân vật quyền lực nhất, chơi theo luật chơi của họ, và ở một mức độ nào đó, bạn sẽ tiến thân. Nhưng đối với những ai trong chúng ta cảm thấy cách tiếp cận đó thật khó chấp nhận trên nhiều phương diện, thì bạn hoàn toàn đúng:

Cuối cùng bạn vẫn phải nổi bật một cách nhất quán theo những cách thức khác. Và đó chính là điểm tạo nên sự khác biệt to lớn giữa việc chỉ dũng cảm đơn thuần và dũng cảm một cách có năng lực. Cuốn sách của tôi mang tựa đề Chọn Lòng Dũng Cảm. Trên nhiều phương diện, lẽ ra nó nên mang tựa đề Chọn Lòng Dũng Cảm Có Năng Lực, bởi vì quả thực, con đường dẫn tới thành công không chỉ là việc cứ bộc phát lên tiếng hay phản kháng mù quáng mọi thứ bằng ngôn từ gây xúc phạm hoặc bạo lực cảm xúc tồi tệ. Vấn đề là thực hiện những điều đó theo cách giúp bạn nổi bật một cách tích cực. Bạn không chỉ chỉ ra một vấn đề, mà còn vạch ra một lối đi, một cách mở rộng thị trường, một sáng kiến giá trị, và bạn làm điều đó theo cách mà những người cấp trên có thể lắng nghe mà không cảm thấy bị xúc phạm hay đe dọa.

Bởi vì sau cùng, bạn có thể nổi bật theo cách tích cực hoặc tiêu cực. Và điều chúng ta đang hướng tới là làm sao để tỏa sáng theo hướng tích cực, và điều đó hoàn toàn nằm ở kỹ năng hành xử dũng cảm của bạn.""",

    "04-Four-fears-hold-courage-back": """# CHƯƠNG 4: BỐN NỖI SỢ CẢN TRỞ LÒNG DŨNG CẢM

Bạn có thể minh họa cụ thể hơn cho chúng tôi bằng một vài ví dụ về những tình huống thực tế nơi công sở, nơi các hành vi dũng cảm tạo nên sự khác biệt to lớn, hoặc nơi mọi người thường né tránh không? Chúng ta đang nói về những khoảnh khắc cụ thể nào ở đây?

Có một vài dạng hành vi điển hình mà nếu bạn khảo sát hàng nghìn người như tôi đã làm, khoảng bảy mươi lăm phần trăm hoặc hơn sẽ đồng tình rằng: những hành vi này đòi hỏi lòng dũng cảm từ mức độ trung bình trở lên. Nhóm hành vi rõ ràng nhất là điều mà tôi gọi là nói thật với người có quyền lực.

Đó là việc bạn dám phản biện lại sếp trực tiếp hoặc sếp cấp cao hơn. Đó có thể là về các chính sách, quy trình vận hành; có thể là về những hành vi ứng xử xúc phạm hoặc gây tổn thương giữa người với người; thậm chí có thể là những việc làm phi pháp hoặc phi đạo đức. Đó cũng có thể là việc bạn đứng lên bảo vệ cấp dưới của mình trước áp lực từ ban lãnh đạo cấp trên. Có rất nhiều hành vi nói thật với quyền lực như vậy.

Điều có phần bất ngờ là khi tôi đề nghị mọi người kể về một hành vi dũng cảm tại nơi làm việc, tôi từng kỳ vọng mọi người sẽ chỉ kể về việc phản biện cấp trên. Nhưng điều tôi hoàn toàn không lường trước được là tần suất rất cao mọi người chia sẻ về sự khó khăn khi phải có một cuộc trò chuyện thẳng thắn với đồng nghiệp ngang hàng, hay thậm chí là đưa ra những phản hồi khó khăn cho chính cấp dưới của mình.

Lý do ban đầu khiến tôi ngạc nhiên là bởi tôi chỉ nghĩ về rủi ro theo khía cạnh kinh tế hoặc hậu quả nghề nghiệp: nếu mọi chuyện không êm đẹp, cơ hội thăng tiến, mức lương hay tương lai của tôi ở công ty sẽ bị đe dọa.

Nhưng hóa ra con người có một vài nỗi sợ hãi căn bản, và rủi ro kinh tế chỉ là một trong số đó. Mọi người cũng vô cùng sợ hãi những hậu quả xã hội. Nếu bạn ngẫm nghĩ kỹ, điều này hoàn toàn hợp lý. Tổ tiên chúng ta tiến hóa trong các thị tộc, bộ lạc nhỏ, nơi nhiệm vụ sinh tồn hàng ngày là tối thượng. Và nếu bạn bị cô lập hay khai trừ khỏi nhóm, bạn cầm chắc cái chết trong một thời gian ngắn. Do đó, về mặt tiến hóa, chúng ta vẫn được lập trình sẵn nỗi sợ hãi tột cùng trước việc bị chối bỏ hay gánh chịu những hậu quả xã hội tẩy chay.

Chúng ta cũng cực kỳ ghét những rủi ro về mặt tâm lý. Nếu bạn hỏi tại sao mọi người không dám đứng lên thử nhận một nhiệm vụ mới, nhận một công việc mới hay sáng tạo đổi mới hơn? Câu trả lời thường là họ không muốn cảm thấy mình ngốc nghếch, không muốn bị xấu hổ, và không muốn nhìn thấy sự nghi ngờ bản thân len lỏi vào tâm trí.

Vì vậy, thực sự có một dải rất rộng các hành vi dũng cảm không chỉ giới hạn ở việc phản biện quyền lực: đó là việc xử lý các mối quan hệ liên cá nhân đầy gai góc với đồng nghiệp, cấp dưới, đối tác bên ngoài, và đó là việc dám đổi mới sáng tạo. Tôi đã xây dựng một danh mục gồm ba mươi lăm hành vi phổ biến nhất được đúc kết từ hàng nghìn người. Nhìn vào nhiều hành vi trong số đó, bạn có thể thốt lên: đối với một người làm chuyên môn hay một nhà quản lý, đó chẳng phải là công việc bình thường của họ sao? Và tôi sẽ trả lời: đúng vậy, nhưng những điều tưởng như bình thường ấy lại diễn ra với tần suất ít ỏi đến đáng kinh ngạc.

Như vậy, chúng ta có các nhóm nỗi sợ: rủi ro kinh tế là sợ mất việc, mất tiền, mất cơ hội thăng tiến; rủi ro xã hội là sợ người khác không thích mình, xa lánh, cô lập mình; và rủi ro tâm lý là sợ cảm thấy mình kém cỏi, bẽ bàng. Liệu còn nhóm rủi ro nào nữa không?

Nhóm thứ tư, vốn rất chân thực trong nhiều bối cảnh mà tôi chưa nhắc tới, chính là rủi ro về thể chất. Nếu bạn quay ngược thời gian hai nghìn năm trước, lịch sử viết về lòng dũng cảm chủ yếu gắn liền với bối cảnh quân sự, chiến trận. Và ngày nay, trong quân đội, cứu hỏa, lực lượng cảnh sát, rủi ro thể chất vẫn luôn hiện hữu. Thậm chí tôi từng rất bất ngờ trước tỷ lệ những người làm trong ngành dịch vụ như nhân viên pha chế, phục vụ bàn, chăm sóc khách hàng chia sẻ về việc họ bị tấn công thân thể, bị đe dọa bằng vũ lực hay vũ khí. Do đó, rủi ro thể chất cũng là một thực tế mà một số người phải đối mặt.""",

    "05-Build-credibility-before-challenging": """# CHƯƠNG 5: XÂY DỰNG UY TÍN TRƯỚC KHI ĐƯA RA THÁCH THỨC

Bây giờ, nếu chúng ta nhận thấy mình muốn, cần hoặc nên làm một điều gì đó nhưng lại cảm thấy sợ hãi, xin hãy dẫn dắt chúng tôi: làm thế nào để chúng ta có thể lựa chọn lòng dũng cảm có năng lực và đầy tự tin?

Hãy cùng trao đổi ngắn gọn về những việc bạn nên làm trước khi thực hiện hành động cụ thể đó, tiếp theo là trong chính thời khắc hành động, và cuối cùng là những việc bạn làm sau đó.

Trước tiên, một số người nói rằng: tôi chưa sẵn sàng để thực hiện hành vi dũng cảm cụ thể này. Và tôi trả lời: điều đó hoàn toàn bình thường, nhưng bạn vẫn có thể bắt tay vào xây dựng nền tảng cho mình. Một điều bạn có thể làm mỗi ngày là tạo dựng một tài khoản uy tín và lòng tin vững chắc.

Bởi vì khi bạn quyết định lên tiếng hay thách thức hiện trạng, những người lắng nghe bạn sẽ vô thức đặt ra hai câu hỏi lớn: tôi có thích và tin tưởng người này không? Ý đồ của họ là gì? Họ có thực sự đứng về phía tổ chức này hay họ chỉ đang tư lợi cá nhân? Và câu hỏi thứ hai là: họ có thực sự am hiểu những gì họ đang nói không? Liệu họ có đủ năng lực để làm việc đó và sử dụng tốt các nguồn lực hay không?

Vì vậy, mỗi ngày trôi qua, chúng ta đều đang tạo dựng trong mắt người khác nhận thức về việc liệu chúng ta có phải là một người ấm áp, chân thành và có năng lực hay không. Thể hiện cho mọi người thấy sự công bằng, trí tuệ cảm xúc của bạn một cách nhất quán hàng ngày chính là cách bạn chuẩn bị bệ phóng vững chắc nhất.

Một điều quan trọng khác là tự vấn: liệu đây có thực sự là vấn đề đúng đắn, có phải là trận đánh xứng đáng và đúng thời điểm hay không? Ở bất kỳ tổ chức nào tôi từng nghiên cứu, ngày nào bạn cũng có thể tìm ra một điều gì đó để lên tiếng phàn nàn, nhưng phần lớn trong số đó không thực sự quan trọng và không tạo ra sự khác biệt lớn lao. Do đó, sở hữu kỹ năng phân định rõ đâu là vấn đề mang tính sống còn đối với các giá trị cốt lõi và mục tiêu then chốt của bạn, và đâu chỉ là những vấn đề thứ yếu, là điều tối quan trọng.

Một đồng nghiệp từng làm việc với tôi là cô Tawanna Burnette tại Facebook, một nữ lãnh đạo da màu kiệt xuất và là một trong hai mươi nữ lãnh đạo da màu đầu tiên tại Facebook. Cô từng chia sẻ rằng: nếu tôi lên tiếng mỗi khi có ai đó phát ngôn điều gì đó thiếu tế nhị hay không phù hợp về chủng tộc hoặc giới tính, tôi sẽ phải lên tiếng mỗi ngày. Nhưng khi ấy, tôi cũng sẽ nhanh chóng đánh mất hiệu quả vì mọi người sẽ ngừng lắng nghe tôi.

Vì thế, cô ấy xác lập mục tiêu cốt lõi của mình là: chúng ta phải đưa thêm nhiều phụ nữ da màu vào các vị trí lãnh đạo cấp cao, bởi chỉ khi đó mọi thứ mới thực sự thay đổi. Nguyên tắc của cô là: mỗi khi cảm thấy bị xúc phạm, cô tự hỏi bản thân: điều này có liên quan trực tiếp đến việc tuyển dụng, đánh giá hay thăng chức cho phụ nữ da màu hay không? Nếu có, cô sẽ kiên quyết lên tiếng vì nếu cô không làm, mục tiêu chung sẽ không thể đạt được. Nhưng nếu đó chỉ là những chuyện vụn vặt khác, cô chủ động bỏ qua. Đó chính là nghệ thuật lựa chọn trận đánh một cách khôn ngoan.""",

    "06-Show-you-re-on-the-same-side": """# CHƯƠNG 6: THỂ HIỆN RẰNG BẠN ĐỨNG CÙNG MỘT CHIẾN TUYẾN

Khi thời khắc hành động và lên tiếng đã điểm, chúng ta cần làm gì trong chính khoảnh khắc đó? Điều này liên quan mật thiết đến những gì bạn nói, địa điểm bạn nói, cách thức bạn truyền đạt và tông giọng cảm xúc mà bạn thể hiện. Tôi xin đưa ra một lời khuyên mang tính bao quát và cốt lõi nhất ở đây:

Khi chuẩn bị dấn thân vào một vấn đề gai góc, bản năng đầu tiên của tất cả chúng ta là trình bày sự việc và đưa ra những lập luận thuyết phục theo lăng kính mà chính chúng ta cảm thấy thỏa đáng nhất. Xét cho cùng, chính bộ não của chúng ta là nơi nhào nặn nên câu chuyện, luận điểm và bài thuyết trình đó, nên xu hướng tự nhiên là đóng khung vấn đề theo cách có ý nghĩa với bản thân ta.

Nhưng trớ trêu thay, điều đó thường hoàn toàn sai lầm. Bởi vì nếu bạn đã nắm trong tay quyền kiểm soát hành vi hay nguồn lực của đối phương, bạn đâu cần phải nhọc công thuyết phục họ làm gì.

Hãy thử hình dung: tôi làm việc cùng bạn, và bạn là người đặc biệt quan tâm đến những yếu tố tác động trực tiếp đến hiệu quả kinh tế, lợi nhuận sau cùng, đồng thời bạn rất nhạy cảm trước những rủi ro hay mối đe dọa đối với sự an toàn của tổ chức. Bạn quan tâm đến tiền bạc và các mối đe dọa. Nhưng tôi lại bước vào, hào hứng trình bày một ý tưởng mới toanh và chỉ thao thao bất tuyệt về việc ý tưởng này phù hợp thế nào với giá trị văn hóa, với bản sắc của chúng ta và mở ra một cơ hội tuyệt vời ra sao. Lối đóng khung dựa trên cơ hội và văn hóa đó hoàn toàn không thể chạm tới bạn, bởi vì tôi đã thất bại trong việc đề cập đến thực tế kinh tế hay những mối đe dọa tiềm tàng nếu chúng ta không hành động.

Do đó, bạn phải luôn khắc cốt ghi tâm rằng: chính khả năng lắng nghe và tiếp nhận tích cực của đối tượng mục tiêu mới là yếu tố quyết định thành bại. Cuốn sách của tôi chia sẻ rất nhiều chiến lược cụ thể để đạt được điều này, nhưng nguyên lý tối cao là: bạn phải nói ngôn ngữ của đối tượng mà bạn muốn thuyết phục.

Và như chúng ta đã mở đầu, hành động theo dõi sau đó cũng tối quan trọng: dù mọi chuyện diễn ra tốt đẹp để bạn củng cố thêm nguồn lực và thời hạn, hay diễn ra chưa như ý để bạn kịp thời hàn gắn các mối quan hệ rạn nứt.

Về các khung lập luận, có những mô thức nào rộng hơn? Chẳng hạn như đóng khung giữa Tôi với Chúng ta, hay giữa Đôi bên cùng thắng với Kẻ thắng người thua. Điều chúng ta thường quên trong khoảnh khắc đó là: khi bạn đề nghị ai đó làm khác đi hoặc trình bày ý tưởng mới của mình, điều mà người nghe thường tiếp nhận trong tiềm thức là: bạn đang chê tôi kém cỏi, bạn cho rằng cách làm hiện tại của tôi là tệ hại, hoặc bạn muốn làm việc này để bạn tỏa sáng còn tôi thì trông như một kẻ ngốc.

Vì thế, một lối đóng khung tích cực sẽ giúp người đối diện thấu hiểu rằng: tôi không muốn thay thế hay giành chiến thắng trên sự thiệt hại của bạn; tôi muốn cùng bạn đưa những gì bạn đã gầy dựng lên một tầm cao mới. Tôi muốn đóng vai trò là người trinh sát đi trước mở đường để đưa tất cả chúng ta cùng tiến bước. Tôi muốn làm cho chiếc bánh lợi ích chung lớn hơn cho tất cả mọi người. Giúp người khác lắng nghe được thông điệp của bạn vì họ thực sự tin rằng bạn đang đứng cùng chiến tuyến với họ, rằng bạn đang cùng họ hướng tới sự xuất sắc chứ không phải đang vùi dập ai đó, đó chính là yếu tố then chốt của nghệ thuật đóng khung tích cực.""",

    "07-Avoid-trap-words-and-phrases": """# CHƯƠNG 7: TRÁNH NHỮNG TỪ NGỮ VÀ CỤM TỪ CẠM BẪY

Có rất nhiều điều nhỏ nhặt mà chúng ta vô tình thốt ra trong giao tiếp. Chúng ta có thể đã chuẩn bị một bộ dữ liệu tuyệt đẹp, trình bày đầy đủ chứng cứ và giải pháp xác đáng, nhưng chỉ bằng một vài từ ngữ sơ suất, chúng ta có thể phá hỏng toàn bộ nỗ lực đó.

Chúng ta thường rơi vào cái bẫy của chủ nghĩa hiện thực ngây thơ, naive realism, một ý niệm cho rằng chỉ có duy nhất một hiện thực khách quan tồn tại ngoài kia, và trùng hợp thay, đó chính là hiện thực mà tôi đang nhìn thấy. Và nếu bạn không nhìn thấy nó theo cách của tôi, thì bạn là kẻ ngốc. Khi vô thức hành xử theo lối đó, chúng ta sẽ buông ra những câu như: bởi vì sự việc này đã quá hiển nhiên rồi, hoặc vì điều này vô cùng rõ ràng, không ai có thể nghi ngờ được nữa.

Tác động của những từ ngữ như hiển nhiên, quá rõ ràng, hay không thể bàn cãi thực chất là đang ngầm truyền đi thông điệp: nếu bạn còn bất kỳ câu hỏi, nghi ngờ nào hay nhìn nhận khác đi, thì bạn là một kẻ đần độn hoặc bạn đang có động cơ vụ lợi cá nhân. Vì vậy, việc học cách nói với thái độ bớt tuyệt đối hóa và tránh những cụm từ áp đặt là vô cùng cần thiết.

Một nhóm bẫy ngôn từ khác mà tôi gọi là những từ chỉ tần suất tuyệt đối. Vợ chồng tôi sau hai mươi lăm năm chung sống vẫn thường nói đùa về việc chúng tôi từng bị phân tâm khỏi nội dung cốt lõi của cuộc trò chuyện chỉ vì người kia sử dụng từ không bao giờ hoặc luôn luôn. Chẳng hạn, nếu vợ tôi muốn tôi phụ giúp dọn dẹp bát đĩa, câu nói hoàn toàn chính xác lẽ ra phải là: anh không phụ dọn dẹp thường xuyên như anh có thể và nên làm.

Nhưng nếu cô ấy nói: anh chẳng bao giờ giúp em rửa bát cả, thì chữ chẳng bao giờ ấy ngay lập tức kích hoạt phản xạ tự vệ trong tôi. Tôi sẽ sa vào một cuộc tranh cãi về tần suất: điều đó không đúng! Tôi thậm chí còn nhớ lại: không, vào thứ Ba ngày ba mươi tháng Bảy, chính anh đã dọn đĩa bánh pizza vào bồn rửa đấy thôi. Và thế là cả hai chúng tôi bị cuốn phăng vào cuộc tranh cãi vô bổ về việc có bao giờ hay không, và rời xa hoàn toàn vấn đề thực chất ban đầu mà lẽ ra cô ấy đang hoàn toàn có lý.

Một ví dụ khác là cụm từ: đừng để bụng chuyện cá nhân. Tôi muốn khẳng định với thính giả rằng: thực chất chúng ta chẳng bao giờ dùng đến câu nói đó, ngoại trừ trong những tình huống mà ở một mức độ nào đó, chúng ta thừa biết sự việc mang tính chất cá nhân sâu sắc. Chẳng có lý do gì bạn phải thanh minh như vậy nếu sự việc thực sự khách quan.

Vì vậy, tôi nghĩ việc chủ động tránh những cụm từ như chuyện này không có ý cá nhân đâu là cực kỳ quan trọng. Các bạn thính giả nếu quan tâm có thể dễ dàng tìm đọc bài viết ngắn của tôi trên trang web H-B-R chấm O-R-G về những từ ngữ và cụm từ cạm bẫy cần tránh trong giao tiếp, nơi tôi phân tích sâu hơn về tất cả những ví dụ này.""",

    "08-Inquire-and-advocate": """# CHƯƠNG 8: HỎI THĂM DÒ VÀ TRÌNH BÀY QUAN ĐIỂM

Có những ngôn từ nào hữu hiệu mà bạn tâm đắc không? Nếu quay trở lại với bậc thầy vĩ đại Chris Argyris, ông từng giảng giải về mô hình Thang suy luận cùng nghệ thuật cân bằng giữa Hỏi thăm dò và Trình bày quan điểm.

Đối với những thính giả chưa từng nghe về điều này, ý tưởng căn bản là phần lớn thời gian chúng ta giao tiếp với nhau ở vị trí mà Chris gọi là đỉnh của chiếc thang, tức là kết luận cuối cùng của chúng ta. Tôi nói: này Pete, chúng ta nên triển khai dự án này và phải làm ngay ngày mai.

Đó là một kết luận. Và Pete đáp lại: anh điên rồi, chúng ta nên giữ nguyên những gì đang có. Đó cũng lại là một kết luận.

Điều chúng ta đã hoàn toàn thất bại là không chịu bước xuống dưới các bậc thang suy luận đó để soi chiếu những gì thực sự đang diễn ra trong tâm trí mỗi người. Khi tôi nói chúng ta nên hành động ngay ngày mai, thực chất tôi đang dựa trên những dữ liệu cụ thể: dữ liệu về động thái của đối thủ cạnh tranh, dữ liệu nội bộ về sự sụt giảm doanh số gần đây, và dữ liệu về việc chúng ta đang đánh mất một vài nhân tài hàng đầu chỉ vì họ cảm thấy nhàm chán. Từ những dữ liệu đó, tôi lập luận rằng chúng ta cần làm điều gì đó mới mẻ để thu hút sự chú ý của thị trường, và do đó tôi đi đến kết luận đã nói với bạn.

Tương tự như vậy, khi bạn bảo nên giữ nguyên hiện trạng, thực ra bạn đang nhìn vào những dữ liệu khác. Bạn có thể thấy rằng chưa có vị lãnh đạo cấp trên nào nói rằng chúng ta đang gặp vấn đề, và phần lớn các doanh nghiệp trong ngành vẫn đang làm giống hệt chúng ta. Từ đó bạn suy luận rằng mọi thứ vẫn ổn thỏa, Jim chỉ đang lo lắng thái quá, và vì vậy kết luận của bạn là hãy giữ nguyên hiện trạng.

Công cụ cụ thể ở đây chính là sự kết hợp nhuần nhuyễn giữa Trình bày quan điểm và Hỏi thăm dò. Trình bày quan điểm không có nghĩa là bạn gào thét kết luận của mình to hơn, mà là giúp người khác nhìn thấy rõ lý do vì sao bạn đi đến kết luận đó. Bạn có thể dùng những câu như: tôi có thể chia sẻ những dữ liệu mà tôi đang có với bạn không? hay tôi có thể giải thích cách lập luận của mình để bạn dễ hình dung không? Đó là những ngôn từ giúp mở rộng các bậc thang suy luận của bạn cho người khác thấy.

Và điều quyền năng nhất chính là những câu hỏi thăm dò khéo léo: này Pete, tôi nghe bạn nói rằng bạn nghĩ chúng ta nên giữ nguyên hiện trạng. Bạn có thể giúp tôi hiểu rõ lý do vì sao không? Bạn có thể chia sẻ góc nhìn và các dữ liệu mà bạn đang cân nhắc với tôi được không?

Đặt câu hỏi thăm dò một cách thành thạo có lẽ là phương thức đơn lẻ xuất sắc nhất để xây dựng những nhịp cầu giao tiếp mà tôi từng biết. Bạn chỉ cần nhìn ra thế giới chúng ta đang sống ngày nay, với đầy rẫy sự chia rẽ và phân cực, bạn sẽ nhận ra tất cả chúng ta đều đang không ngừng gào thét vào mặt nhau từ trên đỉnh thang suy luận của chính mình, mà không hề biết cách giúp người khác hiểu được gốc rễ suy nghĩ của ta, cũng như không biết cách đặt mình vào vị trí của họ bằng việc hỏi xem họ xuất phát từ đâu.""",

    "09-Prepare-for-fear-and-anger": """# CHƯƠNG 9: CHUẨN BỊ VÀ QUẢN TRỊ CẢM XÚC SỢ HÃI LẪN GIẬN DỮ

Nhắc đến cảm xúc, những lời khuyên hàng đầu của bạn để quản trị cảm xúc là gì? Chẳng hạn khi bạn cảm thấy vô cùng sợ hãi, hoặc khi bạn đang bừng bừng tức giận trong lúc chuẩn bị lên tiếng hành động dũng cảm?

Sợ hãi và giận dữ, như tất cả chúng ta đều cảm nhận được một cách trực giác, có những khuynh hướng hành động hoàn toàn trái ngược nhau. Sợ hãi có xu hướng khiến bạn muốn tháo chạy hoặc đóng băng, đó là cảm xúc né tránh; trong khi giận dữ lại là cảm xúc tiếp cận, thôi thúc bạn muốn xông thẳng về phía đối phương.

Do đó, phương pháp tiếp cận phải rất khác nhau. Đối với nỗi sợ hãi, thành thật mà nói, bạn thường phải chuẩn bị từ trước trong một khoảng thời gian dài: duy trì thể lực tốt, thực hành thiền chánh niệm hoặc yoga, bất kỳ điều gì giúp bạn điều hòa lại phản ứng sinh lý nền tảng của cơ thể. Những người có mức độ sợ hãi cao thường thấy rằng họ cần phải soạn sẵn kịch bản chi tiết cho những gì mình sắp nói, luyện tập nhiều lần và nhờ người khác đóng vai phản biện gay gắt để rèn luyện khả năng giữ vững vị thế trong thời khắc đó thay vì tháo chạy. Phần lớn mọi người không thực sự chạy ra khỏi phòng họp, nhưng bạn sẽ thấy họ lập tức câm lặng và nhượng bộ. Vì thế, bạn phải thực sự rèn luyện để kiềm chế nỗi sợ.

Ngược lại, sự giận dữ ở một khía cạnh nào đó lại khá hữu ích, bởi nếu bạn đủ tức giận trước một điều gì đó, bạn sẽ có nhiều động lực hơn để đứng lên hành động hoặc lên tiếng. Vấn đề của sự giận dữ là bạn rất dễ hành xử vụng về và gây tổn thương cho người khác.

Ở đây tôi xin kể một câu chuyện về chính bản thân mình. Hầu hết những người quen biết tôi đều nói rằng Jim chẳng gặp chút khó khăn nào trong việc chọn lựa lòng dũng cảm. Nhưng đôi khi Jim lại gặp vấn đề nghiêm trọng trong việc thể hiện lòng dũng cảm có năng lực. Và trong phần lớn các trường hợp, nguyên nhân là vì tôi đã để cho sự giận dữ trước những bất công hay sai sót cản trở lý trí của mình.

Một phần của việc xử lý cơn giận là những gì bạn làm ngay trong thời khắc đó. Những lời khuyên cổ xưa như đếm từ một đến mười hay hít thở sâu ba lần hóa ra lại cực kỳ hữu ích, bởi chúng thực sự kích hoạt hệ thần kinh phó giao cảm giúp cơ thể bạn dịu lại. Một chiến thuật rất hữu hiệu là rèn luyện cho mình thói quen: trừ những trường hợp khẩn cấp, tuyệt đối không lên tiếng trong chính khoảnh khắc cơn giận đang bốc hỏa. Hãy đề xuất một cuộc hẹn tiếp theo, để thời khắc đó trôi qua và chỉ thảo luận lại sau khi bạn đã lấy lại sự bình tĩnh và cân bằng cảm xúc.

Thêm vào đó, điều quan trọng là thấu hiểu bản thân và tận dụng các chiến lược, thậm chí cả công nghệ làm trợ thủ đắc lực. Trong trường hợp của tôi, cách đây nhiều năm, sau khi từng phạm phải sai lầm kinh điển là vội vã gửi đi những email gay gắt lúc đang bực bội, tôi phát hiện ra bạn hoàn toàn có thể cài đặt bộ đếm giờ trong phần mềm Outlook để tự động giữ lại toàn bộ thư gửi đi trong hộp thư đi trong một khoảng thời gian chỉ định.

Suốt một thời gian dài, tôi đã cài đặt Outlook giữ thư lại trong sáu mươi phút, bởi tôi biết rằng nếu email không bị gửi đi ngay trong vòng một giờ, gần như chắc chắn tôi sẽ bình tâm trở lại, đọc lại bức thư và có cơ hội sửa đổi nó trước khi quá muộn. Học hỏi các chiến lược để vừa làm dịu cơn giận, vừa biết cách lèo lái vượt qua nó là điều vô cùng thiết yếu.""",

    "10-Build-your-courage-ladder": """# CHƯƠNG 10: XÂY DỰNG NẤC THANG LÒNG DŨNG CẢM CỦA RIÊNG BẠN

Còn điều gì quan trọng khác mà bạn muốn nhắn nhủ đến mọi người không? Tôi nghĩ điều cốt lõi cần ghi nhớ là: nếu bạn chấp nhận tiền đề mà chúng ta đã cùng trao đổi hôm nay, rằng lòng dũng cảm là một sự lựa chọn mà mỗi người đều phải đưa ra và nó hoàn toàn dựa trên kỹ năng, thì một việc vô cùng quan trọng cần làm là thiết lập những mục tiêu cụ thể.

Lý do khiến mọi người thường e ngại không dám dấn thân hành động dũng cảm nơi làm việc là vì họ thường nghĩ ngay tới điều đáng sợ nhất xuất hiện trong tâm trí, rồi từ đó họ đi đến một trong hai kết luận: hoặc là tôi sẽ không bao giờ làm điều đó vì nó quá khó khăn và kết cục sẽ vô cùng tồi tệ; hoặc là tôi đã thử làm một lần, nhưng vì nó quá đỗi khó khăn và tôi chưa sẵn sàng, tôi đã làm hỏng bét mọi chuyện, và điều đó càng khẳng định chắc nịch rằng lựa chọn lòng dũng cảm thật là ngớ ngẩn.

Tôi cho rằng điều này tương tự như việc một người chưa từng chạy bộ bao giờ nhưng đùng một cái quyết định sẽ chạy cự ly mười ki-lô-mét. Điều ngớ ngẩn nhất bạn có thể làm là xỏ giày ra đường và cố chạy mười cây số ngay trong ngày đầu tiên. Bạn sẽ gặp vô số chấn thương đau đớn và có lẽ sẽ không bao giờ dám chạy bộ trở lại nữa.

Vì vậy, điều tôi luôn khuyến khích mọi người là hãy tự xây dựng một nấc thang lòng dũng cảm cho riêng mình. Đúng vậy, bạn hoàn toàn có thể đặt mục tiêu đáng sợ nhất đó lên nấc thang cao nhất trên cùng. Nhưng hãy đặt những việc có độ khó vừa phải ở các nấc thang ở giữa, và đặt những việc mà bạn chỉ hơi e ngại đôi chút nhưng hoàn toàn có thể hình dung mình làm được vào những nấc thang thấp nhất ở dưới cùng, rồi bắt đầu hành động từ chính những nấc thang thấp đó.

Bởi vì cũng như bất kỳ kỹ năng nào khác, cách duy nhất để bạn thực sự bồi đắp năng lực theo thời gian là bắt đầu từ những việc nhỏ, gặt hái một chút thành công ban đầu, bạn cảm thấy tự tin hơn vào bản thân, và điều đó sẽ gia tăng động lực thúc đẩy bạn tiến bước. Điều mà chúng ta chưa nhấn mạnh đủ chính là tầm quan trọng của việc bắt đầu từ những việc nhỏ bé. Đó chính là cách mọi kỹ năng vĩ đại được hình thành và phát triển."""
}

manifest_path = os.path.join(base_dir, ".session_manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"Translating {len(translations)} chapters...")
for chap in manifest["chapters"]:
    folder = chap["folder"]
    if folder in translations:
        c_dir = os.path.join(base_dir, folder)
        trans_file = os.path.join(c_dir, "translated.txt")
        text = translations[folder].strip()
        with open(trans_file, "w", encoding="utf-8") as tf:
            tf.write(text)
        
        raw_words = chap["word_count"]
        trans_words = len(text.split())
        ratio = round(trans_words / raw_words, 4)
        print(f"[*] {folder}: Raw {raw_words} words -> Trans {trans_words} words | Ratio: {ratio*100:.1f}%")
        
        chap["step_2_status"] = "completed"
        chap["status"] = "translated"
        chap["translated_file"] = f"{folder}/translated.txt"
        chap["translated_char_count"] = len(text)
        chap["translated_word_count"] = trans_words
        chap["word_expansion_ratio"] = ratio

manifest["pipeline_stage"] = "02_translated"
manifest["step_2_status"] = "completed"

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("\n[✓] STEP 02 TRANSLATION COMPLETED FOR ALL 10 CHAPTERS!")
