# 🌸 BẮT ĐẦU — Đấu Mây vào OpenClaw bằng Antigravity (không gõ lệnh)

> Tinh thần vibe-code: bạn **không gõ lệnh**. Bạn mở AI IDE (Antigravity), **dán 1 câu thần chú**,
> rồi AI tự cài + đấu nối + chạy Mây. Bạn chỉ trả lời khi AI hỏi (dán key) và bấm xác nhận.

## Bạn đã có sẵn (đủ rồi)
1. ✅ **Antigravity** đã cài.
2. ✅ Folder **OpenClaw** (tải từ GitHub về, đã giải nén) — đây là *cái máy*.
3. ✅ Folder **coachio-may-starter** (cái này) — đây là *linh hồn Mây*.

> Mẹo: để 2 folder ở chỗ dễ tìm, ví dụ trong **Tải về (Downloads)**.

## Bạn cần (chuẩn bị trước, để dán khi AI hỏi)
- **DeepSeek API key** (platform.deepseek.com → API Keys)
- **Telegram bot token** (chat **@BotFather** → `/newbot`)
- **ID Telegram của bạn** (chat **@Getmyid_bot** → Start)

---

## 3 bước

### Bước 1 — Mở Antigravity, mở folder OpenClaw
Antigravity → **File → Open Folder…** → chọn folder **OpenClaw** (cái máy) → Open.

### Bước 2 — Mở khung chat AI trong Antigravity
Mở panel chat của AI agent (Antigravity có sẵn). Đây là nơi bạn "ra lệnh".

### Bước 3 — Dán "CÂU THẦN CHÚ" dưới đây vào chat, gửi
AI sẽ tự làm hết: cài thư viện, đấu Mây vào, hỏi bạn key, rồi chạy Mây.

```
Mình đang ở trong folder OpenClaw (engine chạy từ source). Mình muốn chạy con trợ lý "Mây"
mà cấu hình + kỹ năng nằm ở folder riêng tên "coachio-may-starter" (trong Downloads của mình).

Hãy giúp mình TỪNG BƯỚC, giải thích ngắn gọn tiếng Việt, và TỰ CHẠY lệnh hộ mình
(mình không muốn tự gõ lệnh):

1. Kiểm tra máy có Node 22+ và pnpm chưa; thiếu thì cài giúp (bật corepack nếu cần).
2. Trong folder OpenClaw hiện tại: cài dependencies (pnpm install) và build lần đầu nếu dự án cần.
3. Tìm folder "coachio-may-starter" (hỏi mình đường dẫn nếu không thấy trong Downloads).
   Đây là "nhà" của Mây: nó có sẵn thư mục con .openclaw. Hãy ĐẤU NỐI bằng cách đặt biến
   môi trường OPENCLAW_HOME trỏ tới folder coachio-may-starter này.
4. Tạo file key cho Mây: copy "coachio-may-starter/.openclaw/.env.example" thành ".env",
   rồi HỎI mình dán: DEEPSEEK_API_KEY và TELEGRAM_BOT_TOKEN. Ghi vào .env hộ mình.
5. Mở "coachio-may-starter/.openclaw/openclaw.json", tìm dòng "ownerAllowFrom",
   HỎI mình ID Telegram của mình rồi thay vào (dạng "telegram:123456789").
6. Tạo cho mình MỘT file chạy nhanh (double-click là chạy Mây): trên Mac là "chay-may.command",
   trên Windows là "chay-may.bat" — đặt trên Desktop. File này phải: set OPENCLAW_HOME trỏ tới
   folder coachio-may-starter, vào folder OpenClaw, rồi chạy "pnpm openclaw gateway run".
   (Mac nhớ chmod +x cho file.)
7. Chạy thử ngay: "pnpm openclaw doctor --fix" rồi "pnpm openclaw gateway run".
   Theo dõi log, báo mình khi thấy Telegram "running, connected". Có lỗi thì giải thích + sửa hộ.

Sau khi xong, nói cho mình: từ lần sau chỉ cần double-click file "chay-may" trên Desktop là Mây chạy lại.
```

---

## Sau khi AI báo xong
- Mở **Telegram**, nhắn cho bot của bạn → **Mây trả lời!** 🌸
- **Lần sau:** chỉ cần **double-click `chay-may`** trên Desktop (không cần mở Antigravity nữa).
- Muốn tắt Mây: đóng cửa sổ đang chạy (hoặc bấm Ctrl+C trong đó).

## Nếu kẹt
Dán nguyên lỗi vào chat Antigravity và nói: *"Bị lỗi này, kiểm tra và sửa giúp mình."*
AI sẽ đọc log, tìm nguyên nhân, sửa. (Đây chính là kỹ năng làm chủ: AI làm — bạn kiểm chứng.)
