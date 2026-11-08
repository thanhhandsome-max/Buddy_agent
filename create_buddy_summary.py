from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor

out=Path(__file__).parent/'output'
out.mkdir(exist_ok=True)
doc=Document()
s=doc.sections[0]
s.page_height=Cm(29.7);s.page_width=Cm(21)
s.top_margin=Cm(1.8);s.bottom_margin=Cm(1.8);s.left_margin=Cm(2);s.right_margin=Cm(2)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','List Bullet']:
 st=doc.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
 st.font.size=Pt(10.5)
 st.paragraph_format.space_after=Pt(6)
 st.paragraph_format.line_spacing=1.12
doc.styles['Title'].font.size=Pt(25)
doc.styles['Title'].paragraph_format.space_after=Pt(8)
doc.styles['Heading 1'].font.size=Pt(14)
doc.styles['Heading 1'].paragraph_format.space_before=Pt(12)
doc.styles['Heading 1'].paragraph_format.space_after=Pt(5)
doc.core_properties.title='Tóm tắt sản phẩm Buddy'
doc.core_properties.subject='Trợ lý AI đồng hành trên web và desktop'
doc.core_properties.author='Buddy'
def p(t):doc.add_paragraph(t)
def h(t):doc.add_paragraph(t,'Heading 1')
def b(label,t):
 x=doc.add_paragraph(style='List Bullet');x.add_run(label+' ').bold=True;x.add_run(t)
doc.add_paragraph('Tóm tắt sản phẩm Buddy','Title')
p('Trợ lý AI đồng hành trên web và desktop Windows')
p('Cập nhật ngày 18 tháng 10 năm 2026')
h('Tổng quan sản phẩm')
p('Buddy là ứng dụng trợ lý AI hướng đến học sinh, sinh viên và người dùng máy tính cá nhân. Sản phẩm kết hợp không gian học tập trên web với một robot nhỏ trên desktop, cho phép người dùng trò chuyện bằng tiếng Việt, quản lý việc học và yêu cầu thực hiện các thao tác được hỗ trợ trên máy tính.')
p('Buddy được phát triển theo hướng một người bạn AI dễ tiếp cận: có hình ảnh robot sinh động, nghe và trả lời bằng giọng nói, đồng hành khi học tập và làm việc. Phiên bản hiện tại đã có các luồng tương tác chính và đang tiếp tục được tối ưu về tốc độ, độ chính xác và trải nghiệm sử dụng.')
h('Các chức năng hiện có')
b('Trò chuyện bằng giọng nói', 'Nghe lời nói, chuyển thành văn bản, tạo câu trả lời và đọc bằng tiếng Việt. Trong chế độ trò chuyện, Buddy có thể nói câu hỏi làm rõ rồi tiếp tục nghe người dùng trả lời.')
b('Robot trên desktop', 'Hiển thị robot nổi với biểu cảm, chuyển động và bong bóng hội thoại. Người dùng có thể mở ứng dụng từ biểu tượng, thu gọn giao diện chính và tiếp tục tương tác với robot.')
b('Thực hiện yêu cầu trên máy', 'Mở các ứng dụng đã hỗ trợ, mở website bằng trình duyệt, tìm và mở bài nhạc trên YouTube. Có thể mở hoặc tóm tắt thư mục được cấp quyền và tạo ghi chú mới.')
b('Hỗ trợ học tập', 'Trò chuyện theo tài liệu tải lên, hỗ trợ giải thích bài học, quản lý lịch học, tài liệu, ghi nhớ và thu chi trong cùng một không gian.')
b('Quan sát khi được cho phép', 'Dùng camera để theo dõi sự hiện diện, hướng nhìn và tín hiệu nụ cười. Có thể cung cấp ảnh cho model thị giác để hỗ trợ trao đổi theo hình ảnh.')
b('Nhắc nhở và quan tâm', 'Có thiết lập nhắc nghỉ, nhắc học bằng lời nói và thông báo. Người dùng có thể điều chỉnh hoặc tạm hoãn các lời nhắc.')
h('Ví dụ tương tác')
p('“Mở bài Ex Hate Me trên YouTube bằng Chrome.”\n“Không phải, ý mình là…” để sửa tên bài đã nghe nhầm.\n“Mở lịch học” hoặc “Cùng mình đọc tài liệu này nhé.”')

doc.add_page_break()
h('Cách hệ thống hoạt động')
p('Khi người dùng bắt đầu trò chuyện, ứng dụng ghi nhận giọng nói và gửi âm thanh đến dịch vụ nhận dạng tiếng nói. Nội dung được chuyển đến luồng hội thoại hoặc bộ xử lý thao tác. Kết quả được hiển thị và đọc thành tiếng; robot thể hiện trạng thái nghe, suy nghĩ hoặc nói.')
b('Model AI', 'Qwen3 VL 4B được sử dụng qua Ollama và AI gateway trên máy server, hỗ trợ xử lý ngôn ngữ và hình ảnh trong các luồng đã tích hợp.')
b('Giọng nói', 'PhoWhisper đảm nhiệm chuyển giọng nói thành văn bản; Piper cung cấp giọng đọc tiếng Việt cục bộ. Ứng dụng duy trì lượt nghe và nói để giảm thao tác bấm của người dùng.')
b('Ứng dụng', 'Giao diện web phục vụ học tập và quản lý dữ liệu; ứng dụng Electron trên Windows cung cấp robot nổi và các khả năng tích hợp desktop.')
b('Thao tác máy tính', 'Yêu cầu được ánh xạ thành công cụ có cấu trúc và được kiểm tra trước khi thực hiện. Các lệnh đơn giản đã nhận diện có thể đi trực tiếp đến công cụ để giảm thời gian chờ model.')
h('Quyền truy cập và quyền kiểm soát')
p('Quyền camera, microphone và điều khiển máy được gắn với người dùng trên thiết bị. Người dùng chủ động cấp quyền, có thể ghi nhớ lựa chọn và thu hồi quyền. Thư mục cần được cho phép trước khi Buddy truy cập. Người dùng có nút dừng microphone, xử lý AI và giọng đọc; chế độ tự thực hiện thao tác có thể được bật hoặc tắt.')
p('Dữ liệu cần suy luận có thể được gửi đến máy AI đã cấu hình. Tín hiệu khuôn mặt cơ bản được xử lý tại máy; việc gửi ảnh vào hội thoại cần thao tác của người dùng. Triển khai trên thiết bị mới cần thiết lập quyền và kết nối phù hợp.')
h('Phạm vi và giới hạn hiện tại')
p('Buddy thực hiện các thao tác trong danh sách công cụ đã tích hợp; chưa thể tự thao tác mọi phần mềm, click và gõ tùy ý trên toàn bộ desktop. Chất lượng nhận dạng tên bài hát hoặc từ tiếng Anh còn phụ thuộc dịch vụ nhận giọng nói. Việc tự phát nhạc cũng phụ thuộc chính sách của trình duyệt.')
p('Biểu cảm robot và phản hồi quan tâm là hành vi được mô phỏng. Tín hiệu camera như nụ cười không đủ để kết luận chắc chắn người dùng đang vui, buồn hoặc có trạng thái tâm lý cụ thể. Buddy chưa có cảm xúc hay ý thức như con người.')
p('Độ trễ phụ thuộc mạng, server AI, tài nguyên máy và thời gian nạp giọng đọc. Các luồng chính đã có kiểm thử tự động và một số kiểm tra dịch vụ thật; vẫn cần thử nghiệm sử dụng thực tế trên nhiều thiết bị trước khi phát hành rộng rãi.')
h('Hướng phát triển tiếp theo')
p('Ưu tiên cải thiện tốc độ phản hồi, nhận dạng tên riêng và hội thoại nhiều lượt; mở rộng các công cụ điều khiển máy có kiểm soát; hoàn thiện bộ cài, cập nhật ứng dụng và hướng dẫn cấp quyền. Tiếp tục thử nghiệm lời nhắc, biểu cảm và tương tác camera để Buddy đồng hành tự nhiên hơn trong sinh hoạt hằng ngày.')
doc.save(out/'Buddy_Tom_tat_san_pham.docx')
print(out/'Buddy_Tom_tat_san_pham.docx')
