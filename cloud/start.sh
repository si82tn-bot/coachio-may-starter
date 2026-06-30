#!/bin/bash
# Entrypoint Mây trên cloud (Railway/VPS). State ở /data/.openclaw (gắn Volume vào /data).
# Seed config+persona+skills lần đầu; ghi .env từ Variables; điền owner nếu cần; chạy gateway.
set -e
H=/data/.openclaw
mkdir -p "$H"

# 1) Seed openclaw.json + workspace lần đầu (KHÔNG đè để giữ trí nhớ Mây học trên cloud)
if [ ! -f "$H/openclaw.json" ]; then
  cp /app/seed/openclaw.json "$H/openclaw.json"
  # Sinh gateway token (chỉ lần đầu) — bảo vệ control plane; không commit vào repo
  GTOK="$(node -e 'console.log(require("crypto").randomBytes(24).toString("hex"))')"
  node -e 'const f=process.argv[1],t=process.argv[2];const c=require(f);c.gateway=c.gateway||{mode:"local"};c.gateway.auth={mode:"token",token:t};require("fs").writeFileSync(f,JSON.stringify(c,null,2))' "$H/openclaw.json" "$GTOK"
  echo "[start] đã seed openclaw.json + sinh gateway token"
fi
if [ ! -d "$H/workspace" ]; then
  cp -r /app/seed/workspace "$H/workspace"
  echo "[start] đã seed workspace (persona + skills)"
fi

# 2) Điền owner (cả ownerAllowFrom + allowFrom) nếu còn placeholder và có OWNER_TELEGRAM_ID
if [ -n "${OWNER_TELEGRAM_ID}" ] && grep -q "DAN_TELEGRAM_ID_CUA_BAN_VAO_DAY" "$H/openclaw.json"; then
  sed -i "s/DAN_TELEGRAM_ID_CUA_BAN_VAO_DAY/${OWNER_TELEGRAM_ID}/g" "$H/openclaw.json"
  echo "[start] đã điền owner từ OWNER_TELEGRAM_ID"
fi

# 3) .env (state-dir, trusted) — ghi mỗi lần chạy → đổi Variables trên Railway là cập nhật
{
  echo "DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}"
  echo "TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}"
  echo "JINA_API_KEY=${JINA_API_KEY}"
  echo "APIFY_TOKEN=${APIFY_TOKEN}"
  echo "COACHIO_API_KEY=${COACHIO_API_KEY}"
} > "$H/.env"

# 4) Provision lần đầu: plugin deepseek + đăng ký key vào AUTH STORE.
#    DeepSeek V4 là reasoning model → cần plugin @openclaw/deepseek-provider để xử lý
#    đúng định dạng thinking; và key phải nằm trong auth store (paste-api-key), chỉ .env KHÔNG đủ.
if [ ! -f "$H/.coachio-provisioned" ]; then
  echo "[start] cài plugin deepseek…"
  openclaw plugins install @openclaw/deepseek-provider 2>&1 | tail -2 || true
  if [ -n "${DEEPSEEK_API_KEY}" ]; then
    printf '%s\n' "${DEEPSEEK_API_KEY}" | openclaw models auth paste-api-key --provider deepseek 2>&1 | tail -1 || true
    echo "[start] đã đăng ký auth deepseek vào auth store"
  fi
  touch "$H/.coachio-provisioned"
fi

echo "[start] khởi động gateway…"
exec openclaw gateway run
