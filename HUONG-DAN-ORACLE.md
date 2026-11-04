# ☁️ Chạy Mây 24/7 MIỄN PHÍ trên Oracle Cloud (Always Free)

Lựa chọn **thay thế Railway** (Railway ~5$/tháng, bấm nút là chạy). Oracle **0đ** nhưng bạn tự quản 1 máy chủ Linux — làm theo đúng từng bước dưới đây, chỉ cần copy–paste.

> Code dùng chung với Railway (cùng `Dockerfile` + `cloud/start.sh`) → Mây chạy y hệt. Các file riêng cho Oracle nằm trong thư mục [`oracle/`](oracle/).

---

## ⚠️ Đọc trước (quan trọng)

1. **Chỉ chạy Mây ở MỘT nơi.** Cùng 1 `TELEGRAM_BOT_TOKEN` mà chạy cả Railway lẫn Oracle → 2 bot giành tin nhắn, chập chờn. Chuyển sang Oracle thì **tắt service trên Railway** (hoặc ngược lại).
2. **Cần thẻ Visa/Mastercard** để Oracle xác minh danh tính (có thể giữ tạm 1 khoản nhỏ rồi hoàn). Máy Always Free **không tính tiền**.
3. **Home Region chọn 1 lần, không đổi được.** Gần Việt Nam: *Singapore*, *Tokyo*, *Seoul*. Máy ARM miễn phí hay **hết chỗ ("Out of capacity")** → thử lại vào giờ khác / chọn Availability Domain khác.
4. **Máy "nhàn rỗi" có thể bị Oracle thu hồi.** Theo chính sách Always Free, máy dùng rất ít CPU/mạng trong 7 ngày có thể bị dừng. Bot chat dùng ít CPU nên có rủi ro này. Cách chắc ăn: **nâng tài khoản lên Pay As You Go** (vẫn **0đ** nếu chỉ dùng tài nguyên trong hạn mức Always Free). *Chính sách có thể thay đổi — kiểm tra lại trên trang Oracle.*
5. **Trí nhớ không tự chuyển từ Railway.** Mây trên Oracle bắt đầu như mới (sẽ tự onboarding lại).

---

## Bước 1 — Tạo tài khoản
Vào **cloud.oracle.com** → *Sign up* → chọn Home Region (xem lưu ý 3) → xác minh thẻ.

## Bước 2 — Tạo máy ảo (miễn phí)
**☰ Menu → Compute → Instances → Create instance**

| Mục | Chọn |
|---|---|
| Name | `coachio` |
| Image | **Change image → Ubuntu → Canonical Ubuntu 24.04** |
| Shape | **Change shape → Ampere → VM.Standard.A1.Flex**, **1 OCPU + 6 GB RAM** (miễn phí tới 4 OCPU / 24 GB) |
| Networking | Để mặc định (*Assign a public IPv4 address* = Yes) |
| Add SSH keys | **Generate a key pair for me → Save private key** (lưu file `.key` cẩn thận, mất là không vào được máy) |

Bấm **Create** → chờ trạng thái **Running** → copy **Public IP address**.

> Không cần mở cổng firewall nào: Mây tự kết nối ra Telegram, không ai cần kết nối vào máy.

## Bước 3 — Đăng nhập vào máy (từ Windows)
Mở **PowerShell**, thay đường dẫn file key và IP của bạn:

```powershell
# Chỉ làm 1 lần: khoá quyền file key (SSH từ chối key "ai cũng đọc được")
icacls "C:\Users\BAN\Downloads\ssh-key.key" /inheritance:r /grant:r "$($env:USERNAME):R"

ssh -i "C:\Users\BAN\Downloads\ssh-key.key" ubuntu@IP_CUA_MAY
```
Hỏi *Are you sure you want to continue connecting* → gõ `yes`.

## Bước 4 — Cài Mây (copy nguyên dòng, dán vào cửa sổ SSH)
```bash
curl -fsSL https://raw.githubusercontent.com/si82tn-bot/coachio-may-starter/main/oracle/setup.sh | bash
```
> Repo của bạn khác? Thêm link repo vào cuối: `... | bash -s -- https://github.com/<ban>/<repo>.git`

Lần đầu script cài Docker + tải code rồi **dừng lại** để bạn điền key:

```bash
nano ~/coachio/oracle/.env
```
Điền `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `OWNER_TELEGRAM_ID` (và key tuỳ chọn nếu có — ý nghĩa xem [`RAILWAY-VARIABLES.md`](RAILWAY-VARIABLES.md)).
Lưu: **Ctrl+O → Enter → Ctrl+X**.

Chạy lại **đúng lệnh `curl ... | bash` ở trên** → lần này build + chạy Mây (lần đầu ~5–10 phút).

## Bước 5 — Kiểm tra
```bash
cd ~/coachio/oracle && sudo docker compose logs -f --tail 50
```
Thấy `[gateway] ready` là xong → **nhắn thử bot trên Telegram**. Thoát xem log: **Ctrl+C** (Mây vẫn chạy).

---

## Dùng hằng ngày

| Muốn… | Lệnh (trong cửa sổ SSH) |
|---|---|
| Cập nhật sau khi `git push` code mới | `bash ~/coachio/oracle/update.sh` |
| Xem log | `cd ~/coachio/oracle && sudo docker compose logs -f --tail 50` |
| Khởi động lại | `cd ~/coachio/oracle && sudo docker compose restart` |
| Tắt Mây | `cd ~/coachio/oracle && sudo docker compose down` (trí nhớ vẫn giữ) |
| Đổi key | `nano ~/coachio/oracle/.env` rồi `cd ~/coachio/oracle && sudo docker compose up -d` |

- Máy chủ khởi động lại → Mây **tự chạy lại** (không cần làm gì).
- Trí nhớ Mây nằm trong Docker volume `oracle_coachio-data` — **đừng** chạy `docker compose down -v` (chữ `-v` = xoá trí nhớ).

## Gặp lỗi?
| Hiện tượng | Cách xử lý |
|---|---|
| `Out of capacity` khi tạo máy | Hết máy ARM miễn phí ở vùng đó → thử lại sau vài giờ / đổi Availability Domain |
| `Permission denied (publickey)` khi SSH | Sai file key, sai user (phải là `ubuntu`), hoặc chưa chạy lệnh `icacls` |
| Log báo `Telegram ... 409 Conflict` | Bot đang chạy ở nơi khác (Railway/máy tính) → tắt nơi đó |
| Log báo `503 ... high demand` | Gemini đang quá tải (phía Google) → tự hết sau ít phút |
| `❌ Thiếu ... trong .env` | Mở `nano ~/coachio/oracle/.env` điền đủ 3 key bắt buộc |
