# 📘 HƯỚNG DẪN ĐẦY ĐỦ — Cài đặt & Cấu hình Mây (cho người KHÔNG biết lập trình)

> Đọc từ trên xuống. Không cần biết code — bạn chỉ **bấm nút** và **ra lệnh cho AI**.
> Tài liệu gồm 2 phần lớn:
> - **PHẦN A — Antigravity:** phát triển Mây trên máy (mở folder, thêm/nhúng skill).
> - **PHẦN B — Railway:** đưa Mây lên mạng chạy 24/7 (+ Telegram + pairing).

---

# PHẦN A — DÙNG ANTIGRAVITY ĐỂ PHÁT TRIỂN MÂY

## A0. Antigravity là gì?
Antigravity là **IDE có AI** (như một "đồng đội lập trình") của Google. Bạn **nói chuyện** với AI trong đó, nó tự viết code, cài đặt, sửa lỗi. Bạn chỉ cần **ra lệnh + kiểm tra kết quả** — đó gọi là "vibe-code".

## A1. Chuẩn bị (làm 1 lần)
- Cài **Antigravity** (tải từ trang Google Antigravity).
- Cài **Node.js 22** (nodejs.org → LTS) và **Git** (git-scm.com) — cài bằng bộ cài .msi/.dmg, bấm Next tới hết. *(Windows: xem thêm mục "Lỗi Windows" cuối tài liệu.)*
- Tải 2 folder về máy, để **CẠNH NHAU** (không lồng nhau), ví dụ trong **Downloads**:
  - `openclaw` — *cái máy* (engine). Cài bằng lệnh hoặc tải bản chính thức.
  - `coachio-may-starter` — *linh hồn Mây* (cấu hình + kỹ năng + tính cách).

## A2. Mở folder trong Antigravity
1. Mở Antigravity.
2. **File → Open Folder…** → chọn folder **`openclaw`** (cái máy) → Open.
3. Mở **khung chat AI** trong Antigravity (panel bên cạnh).

> Chỉ cần mở **1 folder** (openclaw). Folder Mây chỉ cần **nằm sẵn trên máy**, AI tự tìm.

## A3. "Câu thần chú" — để AI tự cài + đấu nối + chạy
Dán đoạn này vào chat AI (nó sẽ tự làm, hỏi bạn key khi cần):

```
Mình đang ở folder OpenClaw. Mình muốn chạy trợ lý "Mây" mà cấu hình + kỹ năng nằm ở
folder "coachio-may-starter" (trong Downloads). Hãy giúp mình TỪNG BƯỚC, giải thích ngắn
gọn tiếng Việt, và TỰ CHẠY lệnh hộ mình (mình không muốn tự gõ lệnh):
1. Kiểm tra Node 22+ và pnpm; thiếu thì cài.
2. Trong folder OpenClaw: cài dependencies + build lần đầu nếu cần.
3. Đấu nối: đặt OPENCLAW_HOME trỏ tới folder coachio-may-starter.
4. Tạo file key: copy ".openclaw/.env.example" thành ".env", rồi HỎI mình dán DEEPSEEK_API_KEY
   và TELEGRAM_BOT_TOKEN. DeepSeek cần đăng ký vào auth store: chạy
   "openclaw models auth paste-api-key --provider deepseek" rồi dán key.
5. Mở "coachio-may-starter/.openclaw/openclaw.json", thay TẤT CẢ chỗ "DAN_TELEGRAM_ID_CUA_BAN_VAO_DAY"
   bằng ID Telegram của mình (lấy từ @Getmyid_bot).
6. Tạo file chạy nhanh trên Desktop (double-click là chạy Mây): đặt OPENCLAW_HOME + vào folder
   OpenClaw + chạy "pnpm openclaw gateway run".
7. Chạy thử + báo mình khi Telegram "running, connected".
```

Xong → nhắn cho bot Telegram của bạn → **Mây trả lời**. Lần sau chỉ **double-click file chạy** trên Desktop.

## A4. Hiểu "skill" là gì
- Mỗi **skill** là 1 thư mục trong `coachio-may-starter/.openclaw/workspace/skills/<tên-skill>/`.
- Trong đó có:
  - **`SKILL.md`** — mô tả skill làm gì + khi nào dùng (Mây tự đọc để biết lúc nào cần).
  - **`scripts/`** (tuỳ chọn) — mã lệnh chạy (Python…) nếu skill cần.
- Mây **tự nạp** mọi skill trong thư mục đó lúc khởi động.

## A5. NHÚNG (thêm) một skill mới
**Cách 1 — nhờ AI làm (khuyên dùng, không cần code):**
Dán vào chat Antigravity, ví dụ:
```
Tạo cho mình 1 skill tên "dich-thuat" trong coachio-may-starter/.openclaw/workspace/skills:
dịch đoạn văn Anh↔Việt. Viết SKILL.md mô tả rõ khi nào dùng + script nếu cần.
Không hardcode key (nếu cần key thì để trong .env). Xong hướng dẫn mình test trên Telegram
và restart gateway để Mây nhận skill mới.
```
**Cách 2 — có sẵn skill (copy vào):**
Copy nguyên thư mục skill (vd ai đó gửi) vào `.openclaw/workspace/skills/` → **restart gateway**.

> **Sau khi thêm/sửa skill → LUÔN restart** để Mây nạp lại:
> nói với AI *"restart gateway"* (hoặc `openclaw gateway restart`).

## A6. Đổi tính cách Mây
Sửa các file trong `.openclaw/workspace/`:
- **`SOUL.md`** — tính cách, giọng điệu, luật ứng xử của Mây.
- **`USER.md`** — thông tin về bạn (Mây tự học + ghi vào đây).
- **`AGENTS.md`** — luật làm việc (khi nào chạy skill, cách trả lời).
Sửa xong → **restart gateway**.

> 💡 Bản Mây này **chưa có tên** — lần đầu chat, Mây sẽ **hỏi bạn đặt tên** + vài câu để cá tính hoá, rồi tự nhớ.

---

# PHẦN B — CÀI & CHẠY TRÊN RAILWAY (24/7) + TELEGRAM + PAIRING

> Railway = dịch vụ chạy Mây trên mạng, tắt máy vẫn chạy. **Toàn bộ là bấm nút trên web.**
> Bạn KHÔNG cần tải mã nguồn OpenClaw — Railway **tự cài engine** khi build (nhờ file `Dockerfile` có sẵn).

## B0. Chuẩn bị 3 KEY (làm trước)
| Cần | Lấy ở đâu |
|---|---|
| **DeepSeek API key** | platform.deepseek.com → API Keys |
| **Telegram bot token** | Chat **@BotFather** trên Telegram → gõ `/newbot` → làm theo → nhận token dạng `123456:ABC...` |
| **ID Telegram của bạn** | Chat **@Getmyid_bot** → bấm Start → nó trả về 1 **số** (đây là ID cá nhân của bạn) |

## B1. Đưa repo Mây về GitHub của BẠN
Railway chỉ deploy từ repo trong GitHub của chính bạn:
- Vào repo mẫu trên GitHub → bấm **"Use this template" → Create a new repository** → đặt tên → chọn **Private** → Create.

## B2. Tạo project trên Railway
1. Vào **railway.app** → đăng nhập.
2. **New Project → Deploy from GitHub repo** → (lần đầu bấm *Configure GitHub App* để Railway thấy repo) → chọn repo Mây.
3. Railway thấy `Dockerfile` → **tự build**.
   > Lần build đầu có thể ĐỎ (chưa có key + Volume) → bình thường, làm B3–B4 rồi Deploy lại.

## B3. Gắn Volume (để Mây NHỚ — BẮT BUỘC)
Service → **Settings → Volumes → New Volume** → **Mount path = `/data`** → Save.
> Không có Volume = mỗi lần deploy Mây mất sạch cấu hình + trí nhớ.

## B4. Nhập KEY (Variables) — copy-paste sẵn
Service → tab **Variables → RAW Editor** → dán khối này rồi điền giá trị thật:
```
DEEPSEEK_API_KEY=
TELEGRAM_BOT_TOKEN=
OWNER_TELEGRAM_ID=
# tuỳ chọn (mở thêm skill):
COACHIO_API_KEY=
JINA_API_KEY=
APIFY_TOKEN=
GROQ_API_KEY=
```
→ bấm **Deploy**.
> `OWNER_TELEGRAM_ID` = **số ID cá nhân của bạn** (từ @Getmyid_bot), KHÔNG phải số đầu của bot token.

## B5. Xem log để biết Mây đã lên
Service → **Deployments → View Logs**. Chờ tới khi thấy:
```
[start] owner đồng bộ từ Variable: <id của bạn>
[start] cài plugin deepseek…  → Installed plugin: deepseek
[start] đã đăng ký auth deepseek vào auth store
[telegram] [default] starting provider (@tên-bot-của-bạn)
```
Thấy dòng `starting provider (@bot…)` = **Mây đã online**. 🎉

## B6. Kết nối Telegram + Test
Nhắn cho **bot của bạn** trên Telegram → Mây trả lời (từ cloud). Tắt máy vẫn chạy.

---

## B7. TELEGRAM PAIRING — 2 cách để Mây "chỉ nghe đúng người"

Mây có 2 chế độ quản lý ai được nhắn (đặt ở `channels.telegram.dmPolicy`):

### ✅ Cách 1 — ALLOWLIST (MẶC ĐỊNH của bộ này — đơn giản nhất, KHÔNG cần pairing)
- Bộ cài đã đặt `dmPolicy: "allowlist"` + tự lấy `OWNER_TELEGRAM_ID` bạn nhập ở B4.
- → Chỉ **bạn** (đúng ID đó) nhắn được; người lạ bị chặn. **Không cần làm gì thêm.**
- Đổi/ sửa người chủ: đổi `OWNER_TELEGRAM_ID` trong Variables → **Deploy** lại là xong.
- Bot báo **"You are not authorized to use this command"** hoặc im = `OWNER_TELEGRAM_ID` chưa đúng → lấy lại số từ @Getmyid_bot, sửa Variable, Deploy.

### 🔐 Cách 2 — PAIRING (nâng cao — duyệt từng người bằng mã)
Dùng khi muốn **cho phép thêm nhiều người** nhắn Mây (không chỉ mình bạn), có kiểm soát.

**Cơ chế (đã kiểm trong OpenClaw):**
- Đặt `channels.telegram.dmPolicy` = **`"pairing"`** (sửa trong `openclaw.json` → push → Deploy).
- Người lạ nhắn bot → nhận **1 mã ngắn**, tin của họ **CHƯA được xử lý** cho tới khi bạn duyệt.
- Mã **hết hạn sau 1 giờ**; tối đa **3 yêu cầu chờ** cùng lúc.

**Cách DUYỆT (chạy lệnh trong container Railway):**
```
openclaw pairing list telegram              # xem danh sách mã đang chờ
openclaw pairing approve telegram <MÃ>      # duyệt 1 người
```
- Chạy lệnh này trong **Shell của Railway** (Service → mở shell/terminal của Railway) — hoặc bằng **Railway CLI** trên máy (`railway ssh` / `railway run`).
- **Điểm hay:** nếu **chưa có owner nào**, lệnh `approve` đầu tiên sẽ **tự đặt luôn người đó làm chủ** (`commands.ownerAllowFrom`). Những lần duyệt sau chỉ cấp quyền nhắn, không thêm chủ.

**Nên dùng cách nào?**
- Học viên / dùng cá nhân → **Allowlist** (mặc định, khỏi phải chạy lệnh). Khuyên dùng.
- Có nhiều người dùng chung 1 bot, cần duyệt từng người → **Pairing**.

---

## 💰 Lưu ý gói Railway $5
- Mây (chat + skill nhẹ) ~0.5GB RAM chạy 24/7 ≈ **$5–8/tháng**. Xem tab **Usage**.
- **KHÔNG** đăng TikTok/Facebook + tạo video trên Railway $5 (cần máy mạnh/VPS riêng).

## 🔄 Cập nhật Mây sau này
- Sửa skill/persona ở máy (Antigravity) → **git push** → Railway **tự build lại** (trí nhớ trên Volume giữ nguyên).
- Đổi key/owner → sửa **Variables** → Deploy.

## 🪟 Lỗi Windows thường gặp
- **"thiếu npm"** = chưa cài Node.js → cài Node .msi (nodejs.org) → khởi động lại.
- **Antigravity timeout khi cài** → chạy lệnh nặng (`npm i -g openclaw`) trong **PowerShell** thường, không qua AI.
- Lỗi chữ tiếng Việt (encoding) → bản skill mới đã tự xử UTF-8; nhớ `git pull` bản mới nhất.

---

## Bảng tra nhanh khi Mây không trả lời
| Triệu chứng | Nguyên nhân | Cách xử |
|---|---|---|
| "not authorized" / im | `OWNER_TELEGRAM_ID` sai | Lấy ID từ @Getmyid_bot → sửa Variable → Deploy |
| Log không có `starting provider` | Sai `TELEGRAM_BOT_TOKEN` | Kiểm token từ @BotFather |
| `409 Conflict` | 1 bot chạy 2 nơi | Chỉ chạy 1 chỗ (tắt bản kia) |
| Deploy mất trí nhớ | Chưa gắn Volume `/data` | Gắn Volume rồi Deploy |
| Skill mới không nhận | Chưa restart / chưa push | Restart gateway / git push + Deploy |

> Tài liệu liên quan trong repo: `BAT-DAU.md` (local), `HUONG-DAN-LEN-CLOUD.md` (Railway), `RAILWAY-VARIABLES.md` (mẫu key), `TEST-RAILWAY.md` (checklist test).
