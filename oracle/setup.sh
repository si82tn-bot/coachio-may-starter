#!/bin/bash
# Cài Mây lên máy Ubuntu mới (Oracle Cloud Always Free). Chạy được nhiều lần (an toàn).
#   curl -fsSL https://raw.githubusercontent.com/si82tn-bot/coachio-may-starter/main/oracle/setup.sh | bash
# Repo khác (bản fork của bạn):  ... | bash -s -- https://github.com/<ban>/<repo>.git
set -e
REPO="${1:-https://github.com/si82tn-bot/coachio-may-starter.git}"
DIR="$HOME/coachio"

echo "== 1/5 Cài git + Docker (nếu chưa có)"
if ! command -v git >/dev/null; then sudo apt-get update -y && sudo apt-get install -y git; fi
if ! command -v docker >/dev/null; then
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
fi
sudo systemctl enable --now docker >/dev/null 2>&1 || true

echo "== 2/5 Swap (máy RAM nhỏ dễ bị tràn khi build / xử lý video)"
if [ "$(swapon --show --noheadings | wc -l)" = "0" ] && [ "$(free -m | awk '/Mem:/{print $2}')" -lt 4000 ]; then
  sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile >/dev/null && sudo swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
  echo "   đã tạo swap 2GB"
else
  echo "   bỏ qua (đã có swap hoặc RAM đủ lớn)"
fi

echo "== 3/5 Lấy code"
if [ -d "$DIR/.git" ]; then git -C "$DIR" pull --ff-only; else git clone "$REPO" "$DIR"; fi

echo "== 4/5 File key (.env)"
cd "$DIR/oracle"
if [ ! -f .env ]; then
  cp .env.example .env && chmod 600 .env
  echo
  echo "   ⚠️  Đã tạo $DIR/oracle/.env — hãy điền key rồi chạy lại lệnh này:"
  echo "       nano $DIR/oracle/.env"
  exit 0
fi
for k in GEMINI_API_KEY TELEGRAM_BOT_TOKEN OWNER_TELEGRAM_ID; do
  grep -qE "^$k=.+" .env || { echo "   ❌ Thiếu $k trong $DIR/oracle/.env — điền rồi chạy lại."; exit 1; }
done

echo "== 5/5 Build + chạy (lần đầu mất vài phút)"
sudo docker compose up -d --build
echo
echo "✅ Xong. Xem log:  cd $DIR/oracle && sudo docker compose logs -f --tail 50"
echo "   (thấy dòng '[gateway] ready' là Mây đã chạy — nhắn thử bot trên Telegram)"
