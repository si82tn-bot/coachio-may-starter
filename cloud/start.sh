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
# Refresh "code" (skills + persona tĩnh) MỖI lần deploy để git push tới được bot;
# GIỮ NGUYÊN USER.md (trí nhớ Mây học về người dùng) + memory.
mkdir -p "$H/workspace"
rm -rf "$H/workspace/skills"
cp -r /app/seed/workspace/skills "$H/workspace/skills"
for f in SOUL.md AGENTS.md IDENTITY.md; do
  [ -f "/app/seed/workspace/$f" ] && cp "/app/seed/workspace/$f" "$H/workspace/$f"
done
# USER.md: chỉ tạo nếu chưa có (đừng đè trí nhớ đã học)
[ -f "$H/workspace/USER.md" ] || cp /app/seed/workspace/USER.md "$H/workspace/USER.md"
echo "[start] refresh skills + persona (giữ USER.md)"

# 2) Owner: LUÔN đồng bộ từ OWNER_TELEGRAM_ID mỗi lần chạy.
#    (Quan trọng: openclaw.json nằm trên Volume nên KHÔNG seed lại; phải GHI ĐÈ owner ở đây,
#     nếu không thì đổi Variable + redeploy sẽ không có tác dụng — owner kẹt giá trị cũ.)
if [ -n "${OWNER_TELEGRAM_ID}" ]; then
  node -e 'const fs=require("fs"),f=process.argv[1],id=process.argv[2];const c=JSON.parse(fs.readFileSync(f,"utf8"));c.channels=c.channels||{};c.channels.telegram=c.channels.telegram||{};c.channels.telegram.dmPolicy="allowlist";c.channels.telegram.allowFrom=[String(id)];c.commands=c.commands||{};c.commands.ownerAllowFrom=["telegram:"+id];fs.writeFileSync(f,JSON.stringify(c,null,2))' "$H/openclaw.json" "${OWNER_TELEGRAM_ID}"
  echo "[start] owner đồng bộ từ Variable: ${OWNER_TELEGRAM_ID}"
fi

# 2b) Model: LUÔN đồng bộ mỗi lần chạy (cùng lý do với owner — config trên Volume không seed lại).
#     Mặc định Gemini (free tier nếu project Google AI Studio CHƯA bật Billing).
#     Đổi qua Variables: AI_MODEL (vd deepseek/deepseek-v4-flash), AI_FALLBACKS (cách nhau dấu phẩy, "none" = không dự phòng).
#     (gemini-2.5-* đã bị Google đóng với người dùng mới → 404; dùng dòng 3.x.)
#     Model google/* được KHAI BÁO TƯỜNG MINH vào models.providers.google để dùng được cả model
#     mới hơn catalog của engine 2026.7.1 (vd gemini-3.8-flash) — thiếu api/baseUrl engine sẽ gọi nhầm OpenAI.
AI_MODEL="${AI_MODEL:-google/gemini-3.8-flash}"
AI_FALLBACKS="${AI_FALLBACKS:-google/gemini-3.5-flash}"
[ "$AI_FALLBACKS" = "none" ] && AI_FALLBACKS=""
node -e 'const fs=require("fs"),f=process.argv[1],p=process.argv[2],fb=process.argv[3].split(",").map(s=>s.trim()).filter(Boolean);const c=JSON.parse(fs.readFileSync(f,"utf8"));const d=((c.agents=c.agents||{}).defaults=c.agents.defaults||{});d.model={primary:p,fallbacks:fb};d.models=d.models||{};for(const m of [p,...fb])d.models[m]=d.models[m]||{};const ds=[p,...fb].some(m=>m.startsWith("deepseek/"));const pe=((c.plugins=c.plugins||{}).entries=c.plugins.entries||{});const pv=((c.models=c.models||{}).providers=c.models.providers||{});if(ds){pe.deepseek={enabled:true};pv.deepseek=JSON.parse(fs.readFileSync(process.argv[4],"utf8")).models.providers.deepseek}else{delete pe.deepseek;delete pv.deepseek;for(const k of Object.keys(d.models))if(k.startsWith("deepseek/"))delete d.models[k]}const g=[p,...fb].filter(m=>m.startsWith("google/")).map(m=>m.slice(7));if(g.length)pv.google={baseUrl:"https://generativelanguage.googleapis.com/v1beta",api:"google-generative-ai",models:g.map(id=>({id,name:id,reasoning:true,input:["text","image"],contextWindow:1048576,maxTokens:65536}))};else delete pv.google;fs.writeFileSync(f,JSON.stringify(c,null,2))' "$H/openclaw.json" "$AI_MODEL" "$AI_FALLBACKS" /app/seed/openclaw.json
echo "[start] model: $AI_MODEL (dự phòng: ${AI_FALLBACKS:-không})"
# Không dùng DeepSeek → giấu DEEPSEEK_API_KEY khỏi engine (có biến này là engine tự cài plugin deepseek)
case ",$AI_MODEL,$AI_FALLBACKS," in *deepseek/*) USE_DS=1 ;; *) USE_DS=0; unset DEEPSEEK_API_KEY ;; esac

# 3) .env (state-dir, trusted) — ghi mỗi lần chạy → đổi Variables trên Railway là cập nhật
{
  [ "$USE_DS" = 1 ] && echo "DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}"
  echo "TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}"
  echo "JINA_API_KEY=${JINA_API_KEY}"
  echo "APIFY_TOKEN=${APIFY_TOKEN}"
  echo "COACHIO_API_KEY=${COACHIO_API_KEY}"
  echo "GROQ_API_KEY=${GROQ_API_KEY}"
  echo "GEMINI_API_KEY=${GEMINI_API_KEY}"
} > "$H/.env"

# 3b) Gemini (plugin google có sẵn trong engine) — đăng ký key vào auth store mỗi boot
if [ -n "${GEMINI_API_KEY}" ]; then
  printf '%s\n' "${GEMINI_API_KEY}" | openclaw models auth paste-api-key --provider google 2>&1 | tail -1 || true
  echo "[start] đã đăng ký auth google (Gemini) vào auth store"
fi

# 4) Provision: plugin deepseek + đăng ký key vào AUTH STORE — LUÔN chạy mỗi lần boot
#    (KHÔNG gate bằng file marker: nếu gate, lần đầu lỡ fail (vd engine version chưa tương thích)
#    thì marker vẫn được tạo → auth store kẹt ở trạng thái hỏng vĩnh viễn dù sau này fix version/key).
#    DeepSeek V4 là reasoning model → cần plugin @openclaw/deepseek-provider để xử lý
#    đúng định dạng thinking; và key phải nằm trong auth store (paste-api-key), chỉ .env KHÔNG đủ.
#    Cả 2 lệnh đều idempotent (an toàn chạy lại) nên chạy mỗi boot cũng đảm bảo đổi
#    DEEPSEEK_API_KEY trên Variables + Deploy lại luôn có tác dụng ngay.
#    Ghim plugin CÙNG version với engine (Dockerfile: openclaw@2026.7.1) cho rõ ràng & tái lập được
#    (installer hiện tự chọn bản tương thích, nhưng ghim để không phụ thuộc hành vi đó).
#    Khi nâng engine trong Dockerfile thì nâng DS_VER theo.
#    Plugin nằm trên Volume: lần boot sau `install` sẽ báo "already exists" và KHÔNG nâng bản →
#    so version đang cài, lệch thì cài lại với --force (khớp thì bỏ qua, khỏi tải lại mỗi boot).
#    CHỈ chạy khi model chính/dự phòng có dùng deepseek/ (mặc định Gemini → bỏ qua, không gọi DeepSeek).
if [ "$USE_DS" = 1 ]; then
DS_VER=2026.7.1
DS_CUR="$(cat "$H"/npm/projects/openclaw-deepseek-provider-*/node_modules/@openclaw/deepseek-provider/package.json 2>/dev/null \
  | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{console.log(JSON.parse(s).version)}catch(e){}})')"
if [ "$DS_CUR" = "$DS_VER" ]; then
  echo "[start] plugin deepseek đã đúng bản $DS_VER"
else
  echo "[start] cài plugin deepseek $DS_VER (đang có: ${DS_CUR:-chưa cài})…"
  openclaw plugins install "@openclaw/deepseek-provider@$DS_VER" --force 2>&1 | tail -2 || true
fi
if [ -n "${DEEPSEEK_API_KEY}" ]; then
  printf '%s\n' "${DEEPSEEK_API_KEY}" | openclaw models auth paste-api-key --provider deepseek 2>&1 | tail -1 || true
  echo "[start] đã đăng ký auth deepseek vào auth store"
fi
fi

echo "[start] khởi động gateway…"
exec openclaw gateway run
