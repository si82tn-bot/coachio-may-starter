# Câu lệnh "vibe-code" mẫu — ra lệnh cho Antigravity làm hộ

> Triết lý khoá học: bạn **không cần thuộc lệnh**. Bạn *nói chuyện* với AI IDE (Antigravity),
> nó làm, bạn **kiểm chứng**. Dưới đây là các câu nói mẫu — copy vào Antigravity.

## Cài đặt môi trường
> "Giúp tôi kiểm tra máy [Mac/Windows] đã có Node 22+ và Git chưa. Chưa có thì hướng dẫn cài, rồi chạy `node -v`, `git --version` cho tôi xem kết quả."

> "Cài OpenClaw bản chính thức bằng `npm i -g openclaw`, rồi cho tôi xem `openclaw --version`."

## Lấy bộ Mây & cấu hình
> "Clone repo này về `~/coachio-may`, rồi đặt biến `OPENCLAW_HOME` trỏ vào đó (sửa đúng file shell của máy tôi), và xác nhận `echo $OPENCLAW_HOME` ra đúng."

> "Trong `~/coachio-may/.openclaw`, copy `.env.example` thành `.env`. Tôi sẽ tự dán key vào. Giải thích mỗi key dùng cho việc gì."

> "Mở `~/coachio-may/.openclaw/openclaw.json`, giải thích từng phần cho tôi (model, kênh Telegram, chủ, plugin), rồi chỉ đúng dòng tôi cần sửa ID Telegram của mình."

## Chạy & kiểm tra
> "Chạy `openclaw doctor --fix` rồi `openclaw gateway run`. Theo dõi log, báo tôi khi Telegram đã `running, connected`, và nếu có lỗi thì giải thích nguyên nhân."

## Hiểu cấu trúc (Module làm chủ)
> "Liệt kê các skill Mây đang có và mỗi skill làm gì (đọc trong `workspace/skills/*/SKILL.md`)."

> "Giải thích khác nhau giữa `SOUL.md`, `USER.md`, `IDENTITY.md`. Tôi muốn Mây gọi tôi là '[anh/chị/tên]' và có giọng [vui/nghiêm túc] — sửa giúp, rồi nhắc tôi restart."

## Tự thêm 1 skill (bài tập trọng tâm)
> "Tạo cho tôi 1 skill tên `dich-thuat`: nhận 1 đoạn text và dịch Anh↔Việt. Viết `SKILL.md` mô tả rõ khi nào dùng + script nếu cần. Sau đó hướng dẫn tôi test thật trên Telegram. Nhớ: không hardcode key, nếu cần key thì để trong `.env`."

> "Skill tôi vừa thêm chưa chạy. Đọc log, tìm nguyên nhân, sửa, rồi restart gateway và test lại."

## Khi gặp lỗi
> "Bot Telegram không trả lời. Kiểm tra: token trong `.env` đúng chưa, gateway có chạy không, `ownerAllowFrom` đúng ID tôi chưa. Chạy `openclaw doctor` và báo kết quả."

---

**Luôn nhớ:** AI làm xong → bạn **đọc kết quả + chạy thử** rồi mới tin. Đó chính là kỹ năng "làm chủ".
