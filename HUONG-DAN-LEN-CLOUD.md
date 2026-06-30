# ☁️ Đưa Mây lên Railway (chạy 24/7) — hướng dẫn từng bước cho người mới

> Mây dùng **chung 1 repo** này cho cả local lẫn cloud. Lên cloud = đổi "thân" (Railway chạy thay máy),
> **không phải làm lại** persona/skill. Toàn bộ thao tác là **bấm nút trên web**, không gõ lệnh.

## Cần chuẩn bị (5 phút)
- ✅ Tài khoản **Railway** (railway.app) — đã có (gói $5).
- ✅ Tài khoản **GitHub** + bản repo Mây này **trên GitHub của bạn** (xem Bước 0).
- ✅ 3 thứ bắt buộc: **DeepSeek key**, **Telegram bot token** (@BotFather), **ID Telegram của bạn** (@Getmyid_bot).

---

## Bước 0 — Đưa repo Mây về GitHub của BẠN
Railway chỉ deploy từ repo nằm trong GitHub của chính bạn. Chọn 1 cách:
- **Cách A (dễ nhất):** mở repo mẫu trên GitHub → bấm **"Use this template" → Create a new repository** → đặt tên (vd `may-cua-toi`), chọn **Private** → Create. Xong, bạn có bản riêng.
- **Cách B:** **Fork** repo về tài khoản mình.

> File `.env` (chứa key) KHÔNG nằm trong repo — đã chặn sẵn. Key sẽ nhập ở Bước 3 (trên Railway).

---

## Bước 1 — Tạo project trên Railway
1. Vào **railway.app** → đăng nhập.
2. Bấm **New Project**.
3. Chọn **Deploy from GitHub repo** → (lần đầu) bấm **Configure GitHub App** để cho Railway thấy repo của bạn → chọn repo Mây.
4. Railway tự thấy file **`Dockerfile`** và **bắt đầu build**.

> 💡 Lần build đầu có thể **đỏ/lỗi** vì chưa có key + chưa có Volume — **bình thường**, làm tiếp Bước 2-3 rồi deploy lại là xanh.

---

## Bước 2 — Gắn Volume (để Mây NHỚ — BẮT BUỘC)
Không có Volume = mỗi lần deploy Mây **mất sạch** cấu hình + trí nhớ + lịch sử.
1. Bấm vào **service** (ô vuông tên repo) → tab **Settings** (hoặc chuột phải service → **Attach Volume**).
2. Mục **Volumes → + New Volume** (hoặc Add Volume).
3. **Mount path** điền đúng: **`/data`** → Save.

---

## Bước 3 — Nhập KEY (Variables)
1. Vào service → tab **Variables** → bấm **RAW Editor** (hoặc + New Variable từng cái).
2. Dán theo mẫu này, **điền giá trị thật**:
```
DEEPSEEK_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=123456:ABC...
OWNER_TELEGRAM_ID=123456789
```
3. (Tuỳ chọn) Skill nào dùng thì thêm: `JINA_API_KEY`, `APIFY_TOKEN`, `COACHIO_API_KEY`.
4. Bấm **Deploy** (Railway tự deploy lại với key mới).

> `OWNER_TELEGRAM_ID` = **ID Telegram cá nhân của bạn** (số từ @Getmyid_bot), KHÔNG phải số đầu của bot token.

---

## Bước 4 — Xem log để biết Mây đã lên
Vào service → tab **Deployments → View Logs**. Đợi tới khi thấy lần lượt:
```
[start] đã seed openclaw.json + sinh gateway token
[start] cài plugin deepseek…   → Installed plugin: deepseek
[start] đã đăng ký auth deepseek vào auth store
[start] khởi động gateway…
[telegram] [default] starting provider (@<tên bot của bạn>)
```
Thấy dòng `starting provider (@bot...)` = **Mây đã online trên cloud** 🎉

---

## Bước 5 — ⚠️ TẮT Mây ở máy (tránh xung đột Telegram 409)
**1 bot Telegram chỉ chạy được 1 nơi.** Khi cloud đã lên:
- Nếu dùng **cùng 1 bot** với máy → **tắt Mây trên máy** (đóng cửa sổ chạy / tắt dịch vụ nền). Không tắt → cả 2 đánh nhau, Mây chập chờn.
- Hoặc khi **test**: dùng **1 bot Telegram khác** cho cloud để máy vẫn chạy bot cũ song song.

---

## Bước 6 — Test
Nhắn cho bot Telegram → Mây trả lời (từ cloud). **Tắt máy tính → Mây vẫn chạy.** Thử: "tạo ảnh con mèo", "đọc link web".

---

## 💰 Lưu ý gói $5 Railway
- Mây GĐ1 (chat + skill nhẹ) ngốn ~**0.5GB RAM**, chạy 24/7. Railway tính tiền theo dùng → khoảng **$5-8/tháng**. Gói $5 đủ để **test gần hết 1 tháng**.
- Theo dõi ở tab **Usage** trên Railway. Gần hết thì nạp thêm hoặc tắt bớt.
- **KHÔNG bật phần nặng (đăng TikTok/FB + video)** trên Railway $5 — cái đó cần RAM/CPU lớn hơn nhiều (để VPS riêng).

## 🔄 Cập nhật Mây sau này
- Sửa skill/persona ở máy → `git push` → Railway **tự build lại** (state trên Volume giữ nguyên).
- Đổi key → sửa **Variables** trên Railway → Redeploy.
- Nâng version engine: sửa số `openclaw@...` trong `Dockerfile` → push.

## Giới hạn GĐ1 (nói trước)
Không đăng TikTok/FB + không tạo video trên cloud (cần Chrome/TTS). Cái đó để máy làm, hoặc VPS riêng (GĐ2).
