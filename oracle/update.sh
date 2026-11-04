#!/bin/bash
# Cập nhật Mây sau khi git push code mới (giống bấm Deploy trên Railway). Trí nhớ /data được giữ.
#   bash ~/coachio/oracle/update.sh
set -e
cd "$(dirname "$0")"
git -C .. pull --ff-only
sudo docker compose up -d --build
sudo docker image prune -f >/dev/null   # dọn image cũ cho đỡ đầy ổ
echo "✅ Đã cập nhật. Log: sudo docker compose logs -f --tail 50"
