# ☁️ Đưa Mây từ LOCAL lên CLOUD (chạy 24/7, tắt máy vẫn chạy)

> Tin vui: **không phải làm lại từ đầu.** Mây dùng **chung 1 repo** này cho cả local lẫn cloud.
> "Não" (persona + skills + cấu hình) giữ nguyên — chỉ **đổi cách chạy** + **nhập lại key** trên cloud.

## Cái gì GIỮ — cái gì ĐỔI

| | Local (đã làm) | Cloud (Railway) |
|---|---|---|
| Engine | folder OpenClaw + Antigravity | Docker tự cài `openclaw` (file `Dockerfile` có sẵn trong repo) |
| Não Mây | `.openclaw/workspace` | **Y HỆT** — copy gì? Không, cùng repo này |
| Key | file `.openclaw/.env` | **Railway → Variables** (dán lại) |
| Owner ID | trong `openclaw.json` | có sẵn trong repo, hoặc đặt Variable `OWNER_TELEGRAM_ID` |
| Bật/tắt | double-click `chay-may` | Railway tự chạy 24/7 |

→ **Copy gì:** không cần copy gì cả (cùng repo). **Đổi gì:** key chuyển vào Railway Variables; tắt Mây ở máy.

---

## Các bước (thao tác trên web, không gõ lệnh)

### 1. Đẩy repo Mây lên GitHub (nếu chưa)
Repo này (kèm skills bạn đã tự thêm, persona đã chỉnh) đẩy lên GitHub **private**.
> Nếu lúc local bạn đã chỉnh `openclaw.json` (owner) + thêm skill → nhớ **commit + push** để cloud có bản mới nhất.
> ⚠️ File `.env` (chứa key) KHÔNG lên GitHub — đã được chặn sẵn. Key sẽ nhập ở bước 3.

### 2. Tạo service trên Railway
[railway.app](https://railway.app) → **New Project → Deploy from GitHub repo** → chọn repo Mây.
Railway tự thấy `Dockerfile` và build.

### 3. Đặt Variables (Service → Variables → RAW editor)
Dán (điền giá trị thật):
```
DEEPSEEK_API_KEY=
TELEGRAM_BOT_TOKEN=
OWNER_TELEGRAM_ID=
# tuỳ chọn (skill nào dùng thì điền):
JINA_API_KEY=
APIFY_TOKEN=
COACHIO_API_KEY=
```
> `OWNER_TELEGRAM_ID` ở đây để Mây tự điền nếu repo chưa set owner — tiện cho người fork mới.

### 4. Gắn Volume (BẮT BUỘC — để Mây nhớ)
Service → Settings → **Volumes → New Volume** → Mount path = **`/data`**.
(Không có Volume = mỗi lần deploy mất hết trí nhớ + lịch sử.)

### 5. Deploy + xem log
Railway tự deploy. Mở **Deployments → Logs**, thấy:
`đã seed openclaw.json` → `seed workspace` → `khởi động gateway…` → `telegram … running, connected`.

### 6. ⚠️ TẮT Mây ở máy (tránh xung đột Telegram 409)
**1 bot Telegram chỉ chạy 1 nơi.** Khi cloud lên → ở máy: đóng cửa sổ `chay-may` (hoặc Ctrl+C).
> Máy = backup nguội: muốn quay lại máy → tắt service Railway trước, rồi mới chạy lại ở máy.

### 7. Test
Nhắn bot Telegram → Mây trả lời (từ cloud). Tắt máy → Mây **vẫn chạy**. 🎉

---

## Giới hạn cloud GĐ1 (nói trước)
- **Không** đăng TikTok/Facebook (cần trình duyệt Chrome) + **không** tạo video (cần TTS local) trên cloud.
  → để máy làm, hoặc nâng cấp GĐ2 (VPS + Chrome/VNC).
- Skill cần dịch vụ riêng (n8n/Zalo/funnel…) thì thêm Variable tương ứng + bật skill sau.

## Cập nhật Mây sau này
- Sửa skill/persona ở máy → `git push` → Railway tự build lại (**state trên Volume giữ nguyên**).
- Đổi key → sửa Variables trên Railway → Restart (start.sh ghi lại `.env` mỗi lần chạy).

## Lưu ý kỹ thuật
- `Dockerfile` đã ghim `openclaw@2026.6.10`. Nâng version: sửa số đó → push → rebuild.
- Lần đầu seed từ image vào Volume; các lần sau **không đè** workspace (giữ trí nhớ Mây học trên cloud).
- (Bản Docker chưa build thử trực tiếp — lần deploy đầu là lần chạy thật đầu tiên; xem log nếu lỗi.)
