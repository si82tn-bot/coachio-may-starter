# ✅ Checklist: Test Mây + khai thác Railway đầy đủ

> Mây đã chạy trên Railway. Đây là loạt việc để **test khả năng** + **làm chủ vận hành** trên cloud.
> Đánh dấu ✅ khi xong. Phần nào cần key thì thêm ở **Railway → Variables** rồi Deploy lại.

---

## A. Kiểm tra cơ bản (nền tảng)
- [ ] Nhắn bot → Mây trả lời (chat DeepSeek)
- [ ] Hỏi "em là ai" → đúng persona Mây (xưng em, dễ thương)
- [ ] Đổi model trong chat: gõ **`/model pro`** (việc khó) và **`/model flash`** (việc nhanh) → Mây xác nhận đổi
- [ ] Mây **thả tim/like** khi được khen (reaction)

## B. Test trí nhớ + Volume (QUAN TRỌNG nhất của cloud)
- [ ] Nói "tên anh là …, anh thích …" → hỏi lại sau vài tin → Mây nhớ (ghi vào USER.md)
- [ ] **Test bền vững:** Railway → **Redeploy** → nhắn lại → Mây **vẫn nhớ** tên + lịch sử
  → chứng minh Volume `/data` lưu trạng thái (nếu quên = Volume chưa gắn đúng)

## C. Test các kỹ năng (skill) — thêm key để mở
- [ ] **viral-writer** (không cần key) → "viết 1 bài Facebook về [chủ đề]"
- [ ] **tu-van** (không cần key) → "tư vấn giúp anh: [câu hỏi], kiểm chứng giúp"
- [ ] **coachio-image** (cần `COACHIO_API_KEY`) → "tạo ảnh con mèo" → Mây **gửi ảnh ra Telegram**
- [ ] **jina** đọc web/research (cần `JINA_API_KEY`) → "đọc giúp anh link này [URL web]"
- [ ] **social-extract** (cần `APIFY_TOKEN`) → "đọc bài này [link FB/IG/TikTok/X]"

> Thêm key: Railway → Variables → thêm dòng → **Deploy**. Skill tự nhận, không cần làm gì thêm.

## D. Test tính năng VẬN HÀNH của Railway
- [ ] **Logs:** Deployments → **View Logs** → đọc được dòng `gateway ready`, `Inbound message…`
- [ ] **Đổi Variable nóng:** đổi 1 key → Deploy → log báo cập nhật (vd `owner đồng bộ…`)
- [ ] **Usage / chi phí:** mở tab **Usage** → xem RAM/CPU + tiền đã dùng (canh gói $5)
- [ ] **Tự phục hồi:** Railway → service → **Restart** → Mây tự lên lại sau ~30s (không cần anh)
- [ ] **Auto-deploy khi push code:** sửa 1 skill ở máy → `git push` → Railway **tự build lại** → state giữ nguyên
- [ ] **Metrics:** xem biểu đồ RAM/CPU theo thời gian (biết Mây ngốn bao nhiêu)

## E. Thiết lập nâng cao (tuỳ chọn)
- [ ] **Cron báo cáo:** nhờ Mây "mỗi 8h sáng nhắn anh tóm tắt/nhắc việc" (OpenClaw cron built-in)
- [ ] **Backup trí nhớ:** định kỳ tải file `/data/.openclaw/*.sqlite` về (Railway volume backup hàng tuần, muốn dày hơn thì tự cron)
- [ ] **Nhiều skill hơn:** bật/thêm skill từ ClawHub hoặc tự viết (vibe-code) → push
- [ ] **Đổi tính cách Mây:** sửa `SOUL.md`/`USER.md` ở máy → push → Mây "đổi chất"

## F. Giới hạn cần biết (đừng test trên Railway $5)
- ❌ **Đăng TikTok/Facebook** (cần Chrome + màn hình ảo) — để máy/VPS riêng
- ❌ **Tạo video** (cần TTS nặng) — để máy/VPS riêng
- ❌ **Meta Ads MCP** (cần đăng nhập OAuth qua trình duyệt) — thêm sau
- ⚠️ Gói $5 ≈ đủ ~1 tháng chạy 24/7 GĐ1. Quá thì nạp thêm hoặc tắt bớt.

---

## Thứ tự gợi ý để học viên làm
1. A (cơ bản) → 2. B (trí nhớ + redeploy) → 3. C (mở từng skill) → 4. D (vận hành Railway) → 5. E (nâng cao).
→ Làm xong A-D là **đã làm chủ** vận hành Mây trên cloud.
