#!/usr/bin/env python3
"""jina.py — đọc web/social + search + (tùy chọn) deep research qua Jina AI.

Dùng chung kho token Jina (key trong ~/.openclaw/.env: JINA_API_KEY).

Lệnh:
  read <url> [respond=readerlm-v2] [instruction="..."]   # đọc 1 URL → markdown sạch (rẻ; social/JS ok)
  search <từ khóa...>                                     # web search trả nội dung đầy đủ (~10k token/lần)
  deepresearch <câu hỏi...> [reasoning=low|medium] [budget=<token>]  # research sâu — TỐN token, hỏi xác nhận trước

Mặc định TIẾT KIỆM: deepresearch dùng reasoning=low + budget=50000 + team_size=1.
Output bị cắt bớt để khỏi nuốt context (đọc đủ ý là được).
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

READ_CAP = 9000      # ký tự tối đa khi đọc 1 URL
SEARCH_CAP = 800     # ký tự nội dung mỗi kết quả search
DEEP_BUDGET = 50000  # trần token mặc định cho deepresearch (tiết kiệm)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def die(msg, code=1):
    log("ERROR:", msg)
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(code)


def load_env():
    path = os.path.expanduser("~/.openclaw/.env")
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def http(url, key, method="GET", body=None, extra_headers=None, timeout=120):
    # UA thật để qua Cloudflare (urllib mặc định bị chặn 1010).
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json", "User-Agent": UA}
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(body).encode() if body is not None else None
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace") if e.fp else ""
        # 402/429 = hết token/quota → báo rõ để Mây fallback
        die(f"Jina HTTP {e.code}: {detail[:300]}", code=2 if e.code in (402, 429) else 1)
    except urllib.error.URLError as e:
        die(f"không gọi được Jina: {e.reason}")


def parse_kv(args):
    pos, kv = [], {}
    for a in args:
        if "=" in a and not a.startswith("http"):
            k, v = a.split("=", 1)
            kv[k] = v
        else:
            pos.append(a)
    return pos, kv


def cmd_read(key, args):
    pos, kv = parse_kv(args)
    if not pos:
        die("read cần <url>")
    url = pos[0]
    extra = {}
    if kv.get("respond"):
        extra["X-Respond-With"] = kv["respond"]      # readerlm-v2 = chất lượng cao hơn
    if kv.get("instruction"):
        extra["X-Instruction"] = kv["instruction"]    # trích theo yêu cầu
    raw = http(f"https://r.jina.ai/{url}", key, extra_headers={"Accept": "text/plain", **extra})
    if len(raw) > READ_CAP:
        raw = raw[:READ_CAP] + f"\n…[cắt bớt, còn {len(raw) - READ_CAP} ký tự nữa]"
    print(raw)


def cmd_search(key, args):
    q = " ".join(args).strip()
    if not q:
        die("search cần <từ khóa>")
    raw = http("https://s.jina.ai/?" + urllib.parse.urlencode({"q": q}), key)
    try:
        data = json.loads(raw).get("data", [])
        out = [{"title": d.get("title"), "url": d.get("url"),
                "content": (d.get("content") or d.get("description") or "")[:SEARCH_CAP]} for d in data[:5]]
        print(json.dumps({"ok": True, "query": q, "results": out}, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(raw[:6000])


def cmd_deep(key, args):
    pos, kv = parse_kv(args)
    q = " ".join(pos).strip()
    if not q:
        die("deepresearch cần <câu hỏi>")
    body = {
        "model": "jina-deepsearch-v1",
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý research. Trả lời NGẮN GỌN, đúng trọng tâm, "
             "bằng tiếng Việt, có dẫn nguồn (URL). Không lan man, không triết lý."},
            {"role": "user", "content": q},
        ],
        "stream": False,
        "reasoning_effort": kv.get("reasoning", "low"),     # mặc định rẻ
        "budget_tokens": int(kv.get("budget", DEEP_BUDGET)),  # trần token cứng
        "team_size": 1,
    }
    log(f"→ deepresearch (reasoning={body['reasoning_effort']}, budget≤{body['budget_tokens']} token)…")
    raw = http("https://deepsearch.jina.ai/v1/chat/completions", key, method="POST", body=body, timeout=300)
    try:
        d = json.loads(raw)
        msg = d.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = d.get("usage", {})
        print(json.dumps({"ok": True, "answer": msg,
                          "tokens_used": usage.get("total_tokens")}, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(raw[:8000])


def main():
    load_env()
    key = os.environ.get("JINA_API_KEY")
    if not key:
        die("JINA_API_KEY thiếu trong ~/.openclaw/.env")
    if len(sys.argv) < 2:
        die("thiếu lệnh: read | search | deepresearch")
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "read":
        cmd_read(key, args)
    elif cmd == "search":
        cmd_search(key, args)
    elif cmd in ("deepresearch", "deep", "research"):
        cmd_deep(key, args)
    else:
        die(f"lệnh không hiểu: {cmd} (read | search | deepresearch)")


if __name__ == "__main__":
    main()
