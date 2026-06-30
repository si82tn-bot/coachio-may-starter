# 📋 Variables cho Railway — copy & paste sẵn

Học viên KHÔNG cần nhớ tên key. Làm 2 bước:

1. **Copy nguyên khối** trong ô code bên dưới.
2. Railway → service → tab **Variables** → bấm **RAW Editor** → **dán vào** → điền giá trị sau dấu `=` → **Save / Deploy**.

```dotenv
# ===== BẮT BUỘC (3 cái — không có là Mây không chạy) =====
DEEPSEEK_API_KEY=
TELEGRAM_BOT_TOKEN=
OWNER_TELEGRAM_ID=

# ===== TUỲ CHỌN (mở thêm skill — để TRỐNG nếu chưa dùng) =====
COACHIO_API_KEY=
JINA_API_KEY=
APIFY_TOKEN=
```

> Railway RAW Editor bỏ qua dòng bắt đầu bằng `#`. Nếu phiên bản Railway báo lỗi vì dòng `#`, cứ **xoá các dòng `#`** đi, chỉ giữ các dòng `KEY=`.

---

## Mỗi key là gì + lấy ở đâu

| Variable | Bắt buộc? | Dùng cho | Lấy ở đâu |
|---|---|---|---|
| `DEEPSEEK_API_KEY` | ✅ Có | Bộ não chat của Mây | platform.deepseek.com → API Keys |
| `TELEGRAM_BOT_TOKEN` | ✅ Có | Con bot Telegram | Chat **@BotFather** → `/newbot` |
| `OWNER_TELEGRAM_ID` | ✅ Có | Để Mây **chỉ nghe bạn** (số ID cá nhân, KHÔNG phải số của bot) | Chat **@Getmyid_bot** → Start |
| `COACHIO_API_KEY` | ⬜ Tuỳ | skill **coachio-image** (tạo ảnh) | Coachio cấp |
| `JINA_API_KEY` | ⬜ Tuỳ | skill **jina** (đọc web, research) | jina.ai |
| `APIFY_TOKEN` | ⬜ Tuỳ | skill **social-extract** (đọc FB/IG/TikTok/X) | apify.com |

## Lưu ý
- **Đổi key bất cứ lúc nào:** sửa trong Variables → **Deploy** lại là cập nhật (kể cả `OWNER_TELEGRAM_ID`).
- **`OWNER_TELEGRAM_ID` sai = Mây báo "not authorized" hoặc im** → lấy lại số đúng từ @Getmyid_bot.
- Key là bí mật: chỉ đặt trong **Railway Variables**, KHÔNG commit vào GitHub.
