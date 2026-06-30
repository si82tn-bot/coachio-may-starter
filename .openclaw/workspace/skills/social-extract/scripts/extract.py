#!/usr/bin/env python3
"""Extract clean content from a social/web link for rewriting.

Platforms: X/Twitter, Instagram, Facebook, TikTok (spoken transcript), generic web.
stdlib only; shells out to `yt-dlp` and `curl` for TikTok audio + Groq upload.
Prints clean JSON to stdout (last line). Progress/logs go to stderr.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request


def _load_env():
    """Load .env theo OPENCLAW_HOME (Windows/Mac/Linux) rồi tới ~/.openclaw. Env có sẵn thắng."""
    home = os.environ.get("OPENCLAW_HOME") or os.path.expanduser("~")
    for path in (os.path.join(home, ".openclaw", ".env"),
                 os.path.join(os.path.expanduser("~"), ".openclaw", ".env")):
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
        return


_load_env()
APIFY_TOKEN = os.environ.get("APIFY_TOKEN") or os.environ.get("APIFY_API_KEY")
GROQ_KEY = os.environ.get("GROQ_API_KEY")


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def http_json(url, payload=None, headers=None, timeout=240):
    data = json.dumps(payload).encode() if payload is not None else None
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def http_text(url, timeout=60, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def apify_run(actor, payload, timeout=240):
    if not APIFY_TOKEN:
        raise RuntimeError("APIFY_TOKEN missing in env (~/.openclaw/.env)")
    url = f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?token={APIFY_TOKEN}"
    return http_json(url, payload, timeout=timeout)


def apify_last_run_cost(actor, timeout=30):
    """Best-effort USD cost of the actor's most recent successful run (this one)."""
    if not APIFY_TOKEN:
        return None
    try:
        d = http_json(
            f"https://api.apify.com/v2/acts/{actor}/runs/last?token={APIFY_TOKEN}&status=SUCCEEDED",
            timeout=timeout,
        )
        return (d.get("data") or {}).get("usageTotalUsd")
    except Exception:
        return None


def detect(url):
    u = url.lower()
    if "tiktok.com" in u:
        return "tiktok"
    if "instagram.com" in u:
        return "instagram"
    if "facebook.com" in u or "fb.watch" in u or "fb.com" in u:
        return "facebook"
    if "x.com" in u or "twitter.com" in u:
        return "x"
    return "web"


def jina(url, timeout=60):
    """Free clean-markdown reader. Returns markdown text or raises."""
    txt = http_text(
        "https://r.jina.ai/" + url,
        timeout=timeout,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "text/markdown"},
    )
    if not txt or len(txt.strip()) < 40:
        raise RuntimeError("jina returned empty")
    return txt.strip()


# ---------- per-platform ----------

def extract_web(url, timeout):
    log("[web] Jina Reader…")
    md = jina(url, timeout=timeout)
    return {"platform": "web", "url": url, "text": md, "source": "jina", "cost_usd": 0.0}


def extract_x(url, timeout):
    # Jina free first, per user preference.
    try:
        log("[x] thử Jina free…")
        md = jina(url, timeout=min(timeout, 60))
        if len(md) > 120:
            return {"platform": "x", "url": url, "text": md, "source": "jina", "cost_usd": 0.0}
        log("[x] Jina mỏng, fallback Apify…")
    except Exception as e:
        log(f"[x] Jina fail ({e}); fallback Apify…")
    items = apify_run("apidojo~tweet-scraper", {"startUrls": [url], "maxItems": 1}, timeout=timeout)
    if not items:
        raise RuntimeError("X: no data from Apify (private/blocked/credit)")
    it = items[0]
    author = it.get("author") or {}
    return {
        "platform": "x",
        "url": it.get("url") or url,
        "author": author.get("userName") or author.get("name"),
        "text": it.get("text") or it.get("fullText"),
        "metrics": {
            "likes": it.get("likeCount"),
            "comments": it.get("replyCount"),
            "shares": it.get("retweetCount"),
            "views": it.get("viewCount"),
        },
        "timestamp": it.get("createdAt"),
        "images": [m.get("media_url_https") or m.get("url") for m in (it.get("media") or []) if isinstance(m, dict)],
        "source": "apify",
        "cost_usd": apify_last_run_cost("apidojo~tweet-scraper"),
    }


def extract_instagram(url, timeout):
    log("[ig] Apify instagram-scraper…")
    items = apify_run(
        "apify~instagram-scraper",
        {"directUrls": [url], "resultsType": "posts", "resultsLimit": 1, "addParentData": False},
        timeout=timeout,
    )
    if not items:
        raise RuntimeError("Instagram: no data (private/blocked/credit)")
    it = items[0]
    imgs = []
    if it.get("displayUrl"):
        imgs.append(it["displayUrl"])
    for c in it.get("childPosts") or []:
        if c.get("displayUrl"):
            imgs.append(c["displayUrl"])
    for extra in it.get("images") or []:
        if extra and extra not in imgs:
            imgs.append(extra)
    return {
        "platform": "instagram",
        "url": it.get("url") or url,
        "author": it.get("ownerUsername") or it.get("ownerFullName"),
        "text": it.get("caption"),
        "metrics": {
            "likes": it.get("likesCount"),
            "comments": it.get("commentsCount"),
            "views": it.get("videoViewCount") or it.get("videoPlayCount"),
        },
        "timestamp": it.get("timestamp"),
        "images": imgs,
        "hashtags": it.get("hashtags"),
        "videoUrl": it.get("videoUrl"),
        "source": "apify",
        "cost_usd": apify_last_run_cost("apify~instagram-scraper"),
    }


def extract_facebook(url, timeout):
    log("[fb] Apify facebook-posts-scraper…")
    items = apify_run(
        "apify~facebook-posts-scraper",
        {"startUrls": [{"url": url}], "resultsLimit": 1, "captionText": True},
        timeout=timeout,
    )
    if not items:
        raise RuntimeError("Facebook: no data (private/blocked/credit)")
    it = items[0]
    user = it.get("user") or {}
    imgs = []
    for att in it.get("attachments") or []:
        if isinstance(att, dict) and att.get("url") and att.get("type", "").lower().startswith("photo"):
            imgs.append(att["url"])
    return {
        "platform": "facebook",
        "url": it.get("url") or url,
        "author": it.get("pageName") or user.get("name"),
        "text": it.get("text") or it.get("message"),
        "transcript": it.get("captions") or it.get("transcript"),
        "metrics": {
            "likes": it.get("likes"),
            "comments": it.get("comments"),
            "shares": it.get("shares"),
        },
        "timestamp": it.get("time") or it.get("timestamp"),
        "images": imgs,
        "source": "apify",
        "cost_usd": apify_last_run_cost("apify~facebook-posts-scraper"),
    }


def _groq_transcribe(audio_path, model, timeout):
    if not GROQ_KEY:
        raise RuntimeError("GROQ_API_KEY missing in env (~/.openclaw/.env) — needed for TikTok transcript")
    log("[tiktok] Groq Whisper transcribe…")
    out = subprocess.run(
        [
            "curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions",
            "-H", f"Authorization: Bearer {GROQ_KEY}",
            "-F", f"file=@{audio_path}",
            "-F", f"model={model}",
            "-F", "response_format=json",
        ],
        capture_output=True, text=True, timeout=timeout,
    )
    if out.returncode != 0:
        raise RuntimeError(f"groq curl failed: {out.stderr.strip()[:300]}")
    try:
        data = json.loads(out.stdout)
    except Exception:
        raise RuntimeError(f"groq bad response: {out.stdout[:300]}")
    if "error" in data:
        raise RuntimeError(f"groq error: {data['error']}")
    return data.get("text", "").strip()


def extract_tiktok(url, timeout, transcribe, whisper_model):
    # yt-dlp is unreliable for TikTok (frequent anti-bot breakage), so use the
    # Apify clockworks actor: it returns caption/metrics and, with
    # shouldDownloadVideos, an Apify-hosted mp4 we can fetch and transcribe.
    log("[tiktok] Apify clockworks…")
    items = apify_run(
        "clockworks~tiktok-scraper",
        {"postURLs": [url], "resultsPerPage": 1,
         "shouldDownloadVideos": transcribe, "shouldDownloadCovers": False,
         "shouldDownloadSubtitles": False},
        timeout=timeout,
    )
    if not items:
        raise RuntimeError("TikTok: no data (private/blocked/credit)")
    it = items[0]
    author = it.get("authorMeta") or {}
    vm = it.get("videoMeta") or {}
    result = {
        "platform": "tiktok",
        "url": it.get("webVideoUrl") or url,
        "author": author.get("name") or author.get("nickName"),
        "text": it.get("text"),
        "metrics": {
            "likes": it.get("diggCount"),
            "comments": it.get("commentCount"),
            "shares": it.get("shareCount"),
            "views": it.get("playCount"),
        },
        "timestamp": it.get("createTimeISO"),
        "images": [vm["coverUrl"]] if vm.get("coverUrl") else [],
        "duration": vm.get("duration"),
        "hashtags": [h.get("name") for h in (it.get("hashtags") or []) if isinstance(h, dict)],
        "source": "apify",
        "cost_usd": apify_last_run_cost("clockworks~tiktok-scraper"),
    }
    if not transcribe:
        return result
    media = it.get("mediaUrls") or []
    mp4 = media[0] if media else vm.get("downloadAddr")
    if not mp4:
        raise RuntimeError("TikTok: no downloadable media (cannot transcribe; try --no-transcribe)")
    # Apify KV-store records need the token appended to download.
    if mp4.startswith("https://api.apify.com") and "token=" not in mp4:
        mp4 += ("&" if "?" in mp4 else "?") + "token=" + APIFY_TOKEN
    with tempfile.TemporaryDirectory() as td:
        vid = os.path.join(td, "v.mp4")
        aud = os.path.join(td, "a.mp3")
        log("[tiktok] tải video…")
        r = subprocess.run(["curl", "-sL", "-o", vid, mp4], capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0 or not os.path.exists(vid) or os.path.getsize(vid) < 1024:
            raise RuntimeError("TikTok: mp4 download failed")
        log("[tiktok] ffmpeg tách audio…")
        f = subprocess.run(
            ["ffmpeg", "-y", "-i", vid, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", aud],
            capture_output=True, text=True, timeout=timeout,
        )
        if f.returncode != 0 or not os.path.exists(aud):
            raise RuntimeError(f"ffmpeg failed: {f.stderr.strip()[-200:]}")
        result["transcript"] = _groq_transcribe(aud, whisper_model, timeout=timeout)
        result["source"] = "apify+groq"
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--raw", action="store_true")
    ap.add_argument("--no-transcribe", dest="transcribe", action="store_false")
    ap.add_argument("--whisper-model", default="whisper-large-v3-turbo")
    ap.add_argument("--timeout", type=int, default=240)
    a = ap.parse_args()

    plat = detect(a.url)
    log(f"[detect] platform = {plat}")
    try:
        if plat == "instagram":
            res = extract_instagram(a.url, a.timeout)
        elif plat == "facebook":
            res = extract_facebook(a.url, a.timeout)
        elif plat == "x":
            res = extract_x(a.url, a.timeout)
        elif plat == "tiktok":
            res = extract_tiktok(a.url, a.timeout, a.transcribe, a.whisper_model)
        else:
            res = extract_web(a.url, a.timeout)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        log(f"[error] HTTP {e.code}: {body}")
        sys.exit(2)
    except Exception as e:
        log(f"[error] {e}")
        sys.exit(2)

    if not a.raw:
        res = {k: v for k, v in res.items() if v not in (None, [], {}, "")}
    log("[done]")
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
