---
name: social-extract
description: Extract the real content/data from a social or web link — X/Twitter, Instagram, Facebook, TikTok (spoken transcript), or any public URL — so it can be summarized, rewritten, or repurposed. Use ONLY when the user pastes/sends a link AND asks to extract, get the content, transcribe, rewrite, summarize, or repurpose it. Do NOT run on plain chat or on a bare link with no instruction (ask what they want first).
homepage: https://apify.com
---

# Social Extract — lấy dữ liệu từ link để viết lại

Nhận 1 link (X / Instagram / Facebook / TikTok / web bất kỳ), trả về **nội dung sạch**
(caption, text bài, transcript video, metric, ảnh) để bước sau viết lại content.

Skill này **chỉ lấy dữ liệu**. Việc viết lại content do agent làm sau khi có data
(hoặc skill viral riêng nếu đã cài).

## Khi nào dùng

- User dán link **và** nói: "viết lại", "tóm tắt", "lấy nội dung", "repurpose",
  "transcript cái này", "làm content từ link này"…
- Bare link không kèm yêu cầu → **đừng tự chạy**, hỏi user muốn làm gì.

## Cách chạy

```bash
python3 scripts/extract.py "<URL>"
```

Script tự nhận diện nền tảng từ URL và chọn cách lấy:

| Nền tảng | Cách lấy | Cần |
|---|---|---|
| X / Twitter | Jina Reader (free) trước → fallback Apify `apidojo/tweet-scraper` | `APIFY_TOKEN` (cho fallback) |
| Instagram | Apify `apify/instagram-scraper` | `APIFY_TOKEN` |
| Facebook | Apify `apify/facebook-posts-scraper` (kèm transcript video) | `APIFY_TOKEN` |
| TikTok | Apify `clockworks/tiktok-scraper` (caption+mp4) → ffmpeg → Groq Whisper | `APIFY_TOKEN` + `GROQ_API_KEY` |
| Web khác | Jina Reader (free) | — |

(TikTok dùng Apify chứ không phải yt-dlp: yt-dlp hay vỡ vì TikTok đổi chống-bot liên tục.)

Output: in **JSON sạch ra stdout** (dòng cuối). Agent đọc JSON đó rồi viết lại.
Log tiến trình in ra stderr (không lẫn vào kết quả).

## Tùy chọn

- `--json` — (mặc định) in JSON.
- `--raw` — in cả item gốc từ Apify (debug).
- `--no-transcribe` — TikTok chỉ lấy caption/metadata (không tải video + không transcribe; rẻ hơn).
- `--whisper-model <name>` — model Groq (mặc định `whisper-large-v3-turbo`).
- `--timeout <s>` — timeout mỗi call mạng (mặc định 240).

## Output (các field chính)

```json
{
  "platform": "instagram|facebook|x|tiktok|web",
  "url": "...",
  "author": "...",
  "text": "caption/nội dung bài",
  "transcript": "lời nói trong video (TikTok/FB video)",
  "metrics": {"likes": 0, "comments": 0, "shares": 0, "views": 0},
  "timestamp": "...",
  "images": ["url", "..."],
  "source": "jina|apify|yt-dlp+groq"
}
```

## Trả ảnh về Telegram

Sau khi extract, nếu có field `images`, **gửi ảnh kèm về** (đừng chỉ trả text):
dùng công cụ `message` (action=send) với `mediaUrls` = mảng URL ảnh. URL remote IG/FB
gửi thẳng được, nhiều ảnh truyền cả mảng (Telegram gửi từng ảnh kiểu album, tối đa ~10).
Bài viết dài gửi text riêng vì caption Telegram giới hạn ~1024 ký tự.

## Báo tiến độ

Extract mất ~10-60s (Apify chậm hơn, TikTok transcribe lâu hơn). TRƯỚC khi chạy,
nhắn 1 câu cho user biết đang lấy dữ liệu, chờ chút (theo AGENTS.md).

## Error thường gặp

- `APIFY_TOKEN missing` → chưa có key Apify trong `~/.openclaw/.env`.
- `GROQ_API_KEY missing` (chỉ TikTok transcribe) → thêm key vào `.env`.
- Instagram/Facebook trả rỗng → post private, bị chặn, hoặc hết credit Apify.
- TikTok audio > giới hạn Groq → dùng `--no-transcribe`, hoặc cắt bớt.

## Lưu ý

- Apify tính phí mỗi lần chạy (pay-per-event). Đừng chạy lại link đã lấy trừ khi cần.
- Lấy dữ liệu mạng xã hội là vùng xám ToS; ưu tiên nội dung public / của chính user.
- Viết lại content: giữ ý chính, KHÔNG bịa số liệu không có trong nguồn.
