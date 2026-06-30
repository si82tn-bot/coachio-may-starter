#!/usr/bin/env python3
"""Generate / edit images via the Coachio API (GPT Image 2).

Text-to-image: just pass a prompt.
Image-to-image (edit/restyle a user-provided image): pass --image one or more
times (local path or http URL). Local files are uploaded to Coachio first
(POST /upload/image), then referenced via media_inputs.images_url (up to 5).

Flow: [upload refs] -> POST /task/submit -> poll GET /task/status/{id} -> result_urls.
Reads the API key from COACHIO_API_KEY (env, e.g. ~/.openclaw/.env).
"""
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.request
import uuid

# Windows: ép UTF-8 cho stdout/stderr (mặc định Windows dùng code page → UnicodeEncodeError
# với tiếng Việt/emoji). errors="replace" để không bao giờ crash vì 1 ký tự lạ.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE = "https://api.coachio.ai/api/v1"
MAX_REFS = 5
# aspect_ratio "auto" only supports resolution "1k" (Coachio constraint).
AUTO_ONLY_1K = "auto"


def _state_dir():
    """OpenClaw state dir, cross-platform: $OPENCLAW_HOME/.openclaw or ~/.openclaw."""
    home = os.environ.get("OPENCLAW_HOME") or os.path.expanduser("~")
    return os.path.join(home, ".openclaw")


def _load_env():
    """Load keys from the state-dir .env so the script works without pre-set env
    (respects OPENCLAW_HOME → works on Windows/Mac/Linux). Existing env wins."""
    path = os.path.join(_state_dir(), ".env")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and not os.environ.get(key):
                os.environ[key] = val


def _json_req(url, method="GET", api_key="", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-API-Key", api_key)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def _upload_image(path, api_key):
    """Multipart upload a local image; returns the permanent Coachio URL."""
    with open(path, "rb") as fh:
        file_bytes = fh.read()
    filename = os.path.basename(path) or "image.png"
    content_type = mimetypes.guess_type(filename)[0] or "image/png"
    boundary = f"----openclaw{uuid.uuid4().hex}"
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            file_bytes,
            f"\r\n--{boundary}--\r\n".encode(),
        ]
    )
    req = urllib.request.Request(f"{BASE}/upload/image", data=body, method="POST")
    req.add_header("X-API-Key", api_key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.loads(resp.read().decode())
    url = out.get("url")
    if not url:
        sys.exit(f"upload failed for {path}: {json.dumps(out)}")
    return url


def main():
    ap = argparse.ArgumentParser(description="Coachio image generate/edit (GPT Image 2)")
    ap.add_argument("prompt", help="Image prompt (English works best)")
    ap.add_argument(
        "--image",
        action="append",
        default=[],
        metavar="PATH_OR_URL",
        help="Reference image for image-to-image (repeatable, up to 5). Local files are uploaded.",
    )
    ap.add_argument("--aspect-ratio", default="auto",
                    help="auto,1:1,5:4,9:16,21:9,16:9,4:3,3:2,4:5,3:4,2:3")
    ap.add_argument("--resolution", default="1k", help="1k, 2k, 4k")
    ap.add_argument("--model", default="gpt_image_2")
    ap.add_argument("--out", default=None,
                    help="Save result PNG here (default: <state>/media/coachio-<id>.png)")
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    _load_env()
    api_key = os.environ.get("COACHIO_API_KEY", "").strip()
    if not api_key:
        sys.exit("COACHIO_API_KEY chưa có. Thêm dòng COACHIO_API_KEY=... vào "
                 + os.path.join(_state_dir(), ".env"))

    # Always save a local file so the assistant can send it directly to chat.
    out_path = args.out or os.path.join(_state_dir(), "media", f"coachio-{uuid.uuid4().hex[:8]}.png")
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if args.aspect_ratio == AUTO_ONLY_1K and args.resolution != "1k":
        sys.exit('aspect_ratio "auto" only supports resolution "1k"; pick a fixed ratio for 2k/4k')

    refs = args.image[:MAX_REFS]
    if len(args.image) > MAX_REFS:
        print(f"note: only first {MAX_REFS} reference images used", file=sys.stderr)

    image_urls = []
    for ref in refs:
        if ref.startswith("http://") or ref.startswith("https://"):
            image_urls.append(ref)
        else:
            if not os.path.isfile(ref):
                sys.exit(f"reference image not found: {ref}")
            image_urls.append(_upload_image(ref, api_key))

    payload = {
        "task_type": "image",
        "prompt": args.prompt,
        "ai_model_config": {
            "model_identifier": args.model,
            "generation_mode": "default",
            "aspect_ratio": args.aspect_ratio,
            "resolution": args.resolution,
        },
    }
    if image_urls:
        payload["media_inputs"] = {"images_url": image_urls}

    submit = _json_req(f"{BASE}/task/submit", method="POST", api_key=api_key, body=payload)
    task_id = submit.get("task_id")
    if not task_id:
        sys.exit(f"submit failed: {json.dumps(submit)}")

    deadline = time.time() + args.timeout
    status = "pending"
    while time.time() < deadline:
        st = _json_req(f"{BASE}/task/status/{task_id}", api_key=api_key)
        status = st.get("status")
        if status == "completed":
            urls = st.get("result_urls") or []
            if not urls:
                sys.exit(f"completed but no result_urls: {json.dumps(st)}")
            url = urls[0]
            urllib.request.urlretrieve(url, out_path)
            # Clear, machine-readable last line: the local file to send to chat.
            print(f"URL: {url}")
            print(f"IMAGE_PATH: {out_path}")
            return
        if status in ("failed", "error"):
            sys.exit(f"task failed: {st.get('error_message') or json.dumps(st)}")
        time.sleep(3)
    sys.exit(f"timeout after {args.timeout}s (task {task_id} still {status})")


if __name__ == "__main__":
    main()
