---
name: coachio-image
description: Generate or EDIT images via the Coachio API (GPT Image 2). Use ONLY when the user explicitly asks for an image action — keywords like create/generate/draw/make an image, illustration, poster/banner/thumbnail, or edit/restyle/add-to "this image". Do NOT run for plain chat, greetings, or when the user merely sends an image without asking for an edit (ask what they want instead). Supports image-to-image via reference images.
homepage: https://coachio.ai
---

# Coachio Image (GPT Image 2) — text→image & image→image

Generate a new image from text, OR edit/restyle an image the user provides.

## Requirements

- `python3` (stdlib only)
- `COACHIO_API_KEY` in the environment (stored in `~/.openclaw/.env`)

## Text-to-image

```bash
python3 scripts/generate.py "PROMPT" --out /path/out.png
```

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
- `--out` — download the result PNG; otherwise just prints the URL
- `--timeout` — max seconds (default 240)

Prints the image URL on the last line (and `Saved: <path>` with `--out`).

## Notes

- Cost (credits): 1k ≈ 0.81, 2k ≈ 1.35, 4k ≈ 3.2. Don't bulk-generate unasked.
- Social presets: feed `1:1`, story/reel `9:16`.
- Write a vivid, specific English prompt even if the user asks in Vietnamese.
- Uploaded reference images are stored permanently on Coachio.
