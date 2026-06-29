---
name: jina
description: >-
  Đọc web/social + tìm kiếm + research sâu qua Jina AI. Dùng khi user gửi link nhờ "đọc/tóm tắt
  bài/web/post này", "trang này nói gì", "đọc giúp link", hoặc cần "tìm hiểu", "research", "nghiên
  cứu sâu" một chủ đề. read = đọc 1 URL WEB/blog/news/docs (KHÔNG đọc được Facebook/Instagram — login wall).
  search = tìm web nội dung đầy đủ. deepresearch = research nhiều bước (TỐN token — user nói rõ + xác nhận).
  Link MẠNG XÃ HỘI (Facebook/Instagram/TikTok/X) → dùng skill social-extract (Apify), KHÔNG dùng jina read.
---

# Jina — đọc web/social, search, deep research

Gọi Jina AI (key dùng chung kho ~700M token của anh, trong `.env`). 3 mức, chọn rẻ nhất đủ việc:

```bash
python3 scripts/jina.py read <url> [respond=readerlm-v2] [instruction="lấy gì"]
python3 scripts/jina.py search <từ khóa...>
python3 scripts/jina.py deepresearch "<câu hỏi>" [reasoning=low|medium] [budget=<token>]
```

## Chọn lệnh nào (QUAN TRỌNG — tiết kiệm token)
- **`read`** — user đưa 1 link **web/blog/báo/docs** cụ thể, nhờ đọc/tóm tắt. **Rẻ nhất**.
  ⚠️ **Link Facebook/Instagram/TikTok/X → KHÔNG dùng read** (FB/IG có login wall) → chuyển skill **`social-extract`**.
- **`search`** — cần tìm thông tin trên web (1 lần ~10k token). Dùng cho tư vấn/kiểm chứng khi cần nội dung đầy đủ
  (so với Tavily chỉ snippet). Nếu chỉ cần check nhanh 1 ý → dùng Tavily (skill `tu-van`) cho rẻ.
- **`deepresearch`** — CHỈ khi user nói rõ "research sâu / nghiên cứu kỹ / đào sâu". **TỐN token**
  (~50k+/câu). **Bắt buộc:** tóm tắt sẽ research gì + **báo "việc này tốn ~50k token Jina, chạy nhé?" → chờ
  user đồng ý** rồi mới chạy. Mặc định đã để mức rẻ (`reasoning=low`, trần `budget=50000`, 1 agent).
  Câu hỏi thường → đừng dùng deepresearch, dùng search/read.

## Phân vai với công cụ khác
- **Tavily** (skill tu-van): check nhanh 1-2 ý, rẻ → dùng cho fact-check khi tư vấn.
- **Jina read**: đọc trọn 1 trang/social cụ thể.
- **Jina search**: tìm + lấy nội dung đầy đủ nhiều nguồn.
- **Jina deepresearch**: tổng hợp đa nguồn nhiều bước (đắt, hiếm khi).

## Kết quả & lỗi
- `read` in markdown (cắt ~9k ký tự cho gọn context; cần đầy đủ thì nói). `search` in JSON top-5.
  `deepresearch` in `{answer, tokens_used}`.
- **Hết token/quota Jina** → script trả lỗi `HTTP 402/429`. Lúc đó **báo anh "Jina hết token"** và **chuyển
  sang Tavily/`browser`** để tra tiếp (như fallback ở skill tu-van). Đừng đoán mò.

## Env (~/.openclaw/.env)
- `JINA_API_KEY` (dạng `jina_...`).
