# Coachio Mây — Bộ khởi đầu (chạy local)

Đây là "linh hồn" của Mây (cấu hình + tính cách + kỹ năng). **Engine OpenClaw lấy riêng.**

> 🌸 **Cách dễ nhất (không gõ lệnh) → đọc [`BAT-DAU.md`](BAT-DAU.md):** mở Antigravity, dán 1 "câu thần chú",
> AI tự cài + đấu Mây vào + chạy. Phần dưới đây là cách thủ công (cho ai muốn tự làm từng bước).

> Cần trước: **DeepSeek key**, **Telegram bot token** (@BotFather), **ID Telegram của bạn** (@Getmyid_bot),
> **Node 22+**, **Git**. (Chi tiết chuẩn bị tài khoản xem khoá học Coachio.)

---

## Bước 1 — Cài engine OpenClaw (bản chính thức)
```bash
npm i -g openclaw
openclaw --version      # ra 2026.6.x là ok
```

## Bước 2 — Lấy bộ này về & trỏ "nhà" của Mây vào đây
```bash
cd ~
git clone <repo-cua-ban>.git coachio-may
```
Đặt `OPENCLAW_HOME` để OpenClaw coi thư mục này là nhà:
- **Mac:** `echo 'export OPENCLAW_HOME="$HOME/coachio-may"' >> ~/.zshrc && source ~/.zshrc`
- **Windows (PowerShell):** `setx OPENCLAW_HOME "$HOME\coachio-may"` → mở lại terminal.

Kiểm tra: `echo $OPENCLAW_HOME` ra đúng đường dẫn.

## Bước 3 — Điền KEY (file bí mật)
```bash
cd ~/coachio-may/.openclaw
cp .env.example .env
```
Mở `.env` (bằng Antigravity), điền tối thiểu:
```
DEEPSEEK_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=123456:ABC...
```

## Bước 4 — Khai "chủ" của Mây
Mở `~/coachio-may/.openclaw/openclaw.json`, thay **TẤT CẢ** chỗ ghi `DAN_TELEGRAM_ID_CUA_BAN_VAO_DAY`
bằng ID Telegram của bạn (có **2 chỗ**: `allowFrom` và `ownerAllowFrom`), vd `123456789`:
```json
"allowFrom": ["123456789"],
...
"ownerAllowFrom": ["telegram:123456789"]
```
→ Để Mây **chỉ trả lời bạn** (chặn người lạ), khỏi phải pair thủ công.

## Bước 5 — Chạy Mây
```bash
openclaw doctor --fix
openclaw gateway run
```
Thấy dòng `telegram … running, connected` → nhắn cho bot Telegram của bạn → **Mây trả lời!** 🌸

---

## Có gì trong này
- `.openclaw/openclaw.json` — cấu hình (model DeepSeek flash/pro, kênh Telegram, plugin gọn nhẹ).
- `.openclaw/.env` — key của bạn (bạn tự tạo, đã được Git bỏ qua).
- `.openclaw/workspace/SOUL.md · USER.md · IDENTITY.md` — **tính cách & trí nhớ** Mây (sửa cho riêng bạn).
- `.openclaw/workspace/AGENTS.md` — luật làm việc (fact-check, không từ chối ẩu, bảo mật).
- `.openclaw/workspace/skills/` — kỹ năng có sẵn:
  | Skill | Làm gì | Cần thêm key? |
  |---|---|---|
  | `viral-writer` | Viết content/caption/bài đăng | Không (chỉ DeepSeek) |
  | `tu-van` | Tư vấn + fact-check kỷ luật | Không |
  | `jina` | Đọc web/social + research | `JINA_API_KEY` |
  | `social-extract` | Đọc bài FB/IG/TikTok/X | `APIFY_TOKEN` |
  | `coachio-image` | Tạo ảnh | `COACHIO_API_KEY` |

## Mẹo
- `/model pro` (việc khó) · `/model flash` (việc nhanh) — đổi model ngay trong chat.
- Sửa skill / thêm skill mới → `openclaw gateway restart` cho Mây nhận.
- Đổi tính cách Mây → sửa `SOUL.md` / `USER.md` → restart.
- Lỗi `409 Conflict` = 1 bot chạy 2 nơi → chỉ chạy 1 chỗ.

Xem `SETUP.md` để có các câu lệnh "vibe-code" mẫu (ra lệnh cho Antigravity làm hộ).

## ☁️ Chạy 24/7 trên cloud
Cùng repo này deploy lên cloud được (chung não Mây). Xem [`HUONG-DAN-LEN-CLOUD.md`](HUONG-DAN-LEN-CLOUD.md):
đẩy repo lên GitHub → Railway bấm nút → gắn Volume `/data` → điền Variables → Mây chạy 24/7. (Có sẵn `Dockerfile` + `cloud/start.sh`.)
- **Variables copy-paste sẵn:** [`RAILWAY-VARIABLES.md`](RAILWAY-VARIABLES.md) (khỏi nhớ tên key)
- **Checklist test + khai thác Railway:** [`TEST-RAILWAY.md`](TEST-RAILWAY.md)
