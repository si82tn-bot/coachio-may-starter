#!/bin/bash
# Entrypoint Mây trên cloud (Railway/VPS). State ở /data/.openclaw (gắn Volume vào /data).
# Seed config+persona+skills lần đầu; ghi .env từ Variables; điền owner nếu cần; chạy gateway.
set -e
H=/data/.openclaw
mkdir -p "$H"

# 1) Seed openclaw.json + workspace lần đầu (KHÔNG đè để giữ trí nhớ Mây học trên cloud)
if [ ! -f "$H/openclaw.json" ]; then
  cp /app/seed/openclaw.json "$H/openclaw.json"
  echo "[start] đã seed openclaw.json"
fi
if [ ! -d "$H/workspace" ]; then
  cp -r /app/seed/workspace "$H/workspace"
  echo "[start] đã seed workspace (persona + skills)"
fi

# 2) Điền owner nếu config còn placeholder và có Variable OWNER_TELEGRAM_ID
if [ -n "${OWNER_TELEGRAM_ID}" ] && grep -q "DAN_TELEGRAM_ID_CUA_BAN_VAO_DAY" "$H/openclaw.json"; then
  sed -i "s/DAN_TELEGRAM_ID_CUA_BAN_VAO_DAY/${OWNER_TELEGRAM_ID}/" "$H/openclaw.json"
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

echo "[start] khởi động gateway…"
exec openclaw gateway run
