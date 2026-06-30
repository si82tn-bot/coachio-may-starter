---
name: coachio-image
description: Generate or EDIT images via the Coachio API (GPT Image 2). Use ONLY when the user explicitly asks for an image action — keywords like create/generate/draw/make an image, illustration, poster/banner/thumbnail, or edit/restyle/add-to "this image". Do NOT run for plain chat, greetings, or when the user merely sends an image without asking for an edit (ask what they want instead). Supports image-to-image via reference images.
homepage: https://coachio.ai
---

# Coachio Image (GPT Image 2) — text→image & image→image

Generate a new image from text, OR edit/restyle an image the user provides.

## Requirements

- `python3` (Windows: dùng `python` nếu `python3` không có). Stdlib only.
- `COACHIO_API_KEY` trong `.env` — **script tự đọc** (`$OPENCLAW_HOME/.openclaw/.env` hoặc `~/.openclaw/.env`). KHÔNG cần set biến môi trường thủ công, KHÔNG cần `&&`.

## Text-to-image

```bash
python3 scripts/generate.py "PROMPT"
```

- Script **tự tạo thư mục** + **tự lưu** ảnh, in dòng cuối `IMAGE_PATH: <đường dẫn>`.
- Muốn lưu chỗ khác thì thêm `--out /path/out.png` (cũng tự tạo thư mục).

## SAU KHI TẠO — gửi ảnh thẳng vào chat (QUAN TRỌNG)

Lấy đường dẫn ở dòng `IMAGE_PATH:` rồi **gửi file đó vào ĐÚNG cuộc trò chuyện hiện tại**
(thread/chat mặc định) dưới dạng ảnh — KHÔNG đặt target theo tên người (vd "Sonny"),
KHÔNG chỉ dán URL. Người dùng phải **thấy ảnh hiện ngay trong Telegram**.

## Chạy GỌN (đừng làm phiền người dùng)

Chạy script **im lặng**: KHÔNG tường thuật từng bước ("đang chạy script", "thiếu thư mục",
"set env"…). Chỉ cần **1 tin kết quả + ảnh**. Script đã tự lo key + thư mục nên gọi 1 phát là xong.

## Image-to-image (IMPORTANT — use the user's attached image)

When the user **sends/attaches an image** (e.g. on Telegram) and asks to edit,
restyle, "make it like this", recreate, or transform it, you MUST pass that
image as a reference with `--image`. Do NOT ignore it and generate from text
only — that produces an unrelated picture.

```bash
python3 scripts/generate.py "EDIT INSTRUCTION" --image /path/to/user_image.png --out /path/out.png
```

- `--image` accepts a **local file path** (uploaded automatically via
  `/upload/image`) or an **http(s) URL** (used directly).
- Repeat `--image` for multiple references (max 5).
- Find the attached image's local path from the incoming message attachment, and
  pass it here.

## Options

- `--aspect-ratio` — `auto` (default), `1:1`, `9:16`, `16:9`, `4:5`, `3:4`, `5:4`, `21:9`, `4:3`, `3:2`, `2:3`
- `--resolution` — `1k` (default), `2k`, `4k`
  - Constraint: `aspect-ratio auto` only supports `1k`. For `2k`/`4k` pick a fixed ratio (e.g. `1:1`, but `1:1` does not support `4k`).
- `--out` — đường dẫn lưu (mặc định tự lưu vào `<state>/media/coachio-<id>.png`)
- `--timeout` — max seconds (default 240)

In 2 dòng cuối: `URL: <link>` và `IMAGE_PATH: <file local>`. Dùng `IMAGE_PATH` để gửi ảnh vào chat.

## Notes

- Cost (credits): 1k ≈ 0.81, 2k ≈ 1.35, 4k ≈ 3.2. Don't bulk-generate unasked.
- Social presets: feed `1:1`, story/reel `9:16`.
- Write a vivid, specific English prompt even if the user asks in Vietnamese.
- Uploaded reference images are stored permanently on Coachio.
