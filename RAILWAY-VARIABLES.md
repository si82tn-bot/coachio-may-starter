# 📋 Variables cho Railway — copy & paste sẵn

Học viên KHÔNG cần nhớ tên key. Làm 2 bước:

1. **Copy nguyên khối** trong ô code bên dưới.
2. Railway → service → tab **Variables** → bấm **RAW Editor** → **dán vào** → điền giá trị sau dấu `=` → **Save / Deploy**.

```dotenv
# ===== BẮT BUỘC (3 cái — không có là Mây không chạy) =====
GEMINI_API_KEY=
TELEGRAM_BOT_TOKEN=
OWNER_TELEGRAM_ID=

# ===== TUỲ CHỌN (mở thêm skill — để TRỐNG nếu chưa dùng) =====
COACHIO_API_KEY=
JINA_API_KEY=
APIFY_TOKEN=
GROQ_API_KEY=

# ===== ĐỔI BỘ NÃO (để TRỐNG = dùng Gemini mặc định) =====
AI_MODEL=
AI_FALLBACKS=
DEEPSEEK_API_KEY=
```

> Railway RAW Editor bỏ qua dòng bắt đầu bằng `#`. Nếu phiên bản Railway báo lỗi vì dòng `#`, cứ **xoá các dòng `#`** đi, chỉ giữ các dòng `KEY=`.

---

## Mỗi key là gì + lấy ở đâu

| Variable | Bắt buộc? | Dùng cho | Lấy ở đâu |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Có | Bộ não chat của Mây (mặc định Gemini 3.8 Flash, dự phòng 3.5 Flash-Lite) | aistudio.google.com → Get API key. **Miễn phí nếu project của key CHƯA bật Billing** |
| `TELEGRAM_BOT_TOKEN` | ✅ Có | Con bot Telegram | Chat **@BotFather** → `/newbot` |
| `OWNER_TELEGRAM_ID` | ✅ Có | Để Mây **chỉ nghe bạn** (số ID cá nhân, KHÔNG phải số của bot) | Chat **@Getmyid_bot** → Start |
| `COACHIO_API_KEY` | ⬜ Tuỳ | skill **coachio-image** (tạo ảnh) | Coachio cấp |
| `JINA_API_KEY` | ⬜ Tuỳ | skill **jina** (đọc web, research) | jina.ai |
| `APIFY_TOKEN` | ⬜ Tuỳ | skill **social-extract** (đọc FB/IG/TikTok/X) | apify.com |
| `AI_MODEL` | ⬜ Tuỳ | Đổi model chính, vd `deepseek/deepseek-v4-flash`. Trống = `google/gemini-3.8-flash` | — |
| `AI_FALLBACKS` | ⬜ Tuỳ | Model dự phòng, cách nhau dấu phẩy; `none` = không dự phòng. Trống = `google/gemini-3.5-flash-lite` | — |
| `DEEPSEEK_API_KEY` | ⬜ Tuỳ | Chỉ cần khi `AI_MODEL`/`AI_FALLBACKS` dùng `deepseek/...` (tính phí theo token) | platform.deepseek.com → API Keys |
| `GROQ_API_KEY` | ⬜ Tuỳ | **transcribe video TikTok** (giọng nói → chữ, qua Groq Whisper) | console.groq.com (free tier) |

## Lưu ý
- **Gemini miễn phí có giới hạn lượt/phút & lượt/ngày** — nhắn dồn dập có thể bị báo lỗi tạm, chờ vài phút là chạy lại. Gói miễn phí: Google có thể dùng nội dung để cải thiện model.
- **Gói Gemini Pro (app Gemini) KHÔNG bao gồm API** — API tính riêng; giữ project AI Studio KHÔNG bật Billing để không mất tiền.
- **Đổi key bất cứ lúc nào:** sửa trong Variables → **Deploy** lại là cập nhật (kể cả `OWNER_TELEGRAM_ID`).
- **`OWNER_TELEGRAM_ID` sai = Mây báo "not authorized" hoặc im** → lấy lại số đúng từ @Getmyid_bot.
- Key là bí mật: chỉ đặt trong **Railway Variables**, KHÔNG commit vào GitHub.
