# Mây (OpenClaw) trên cloud (Railway/VPS) — chạy 24/7. State trên Volume /data.
# Dùng chung persona + skills với bản local (cùng thư mục .openclaw/workspace của repo này).
FROM node:22-slim

# ca-certificates+python3: skill scripts; ffmpeg+yt-dlp: tách & tải audio cho transcribe
# TikTok/video (kết hợp GROQ_API_KEY = Whisper trên cloud Groq, không ngốn CPU server).
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates python3 ffmpeg curl \
    && curl -fsSL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp \
    && chmod +x /usr/local/bin/yt-dlp \
    && rm -rf /var/lib/apt/lists/*

# Engine OpenClaw từ npm (core không sửa → dùng package; ghim version cho ổn định)
# 2026.7.2 = tối thiểu để @openclaw/deepseek-provider hoạt động (plugin yêu cầu pluginApi >=2026.7.2)
RUN npm install -g openclaw@2026.7.2

ENV OPENCLAW_HOME=/data
ENV OPENCLAW_GATEWAY_PORT=18789

WORKDIR /app
# Seed = đúng não Mây của repo (config + persona + skills generic)
COPY .openclaw/openclaw.json /app/seed/openclaw.json
COPY .openclaw/workspace /app/seed/workspace
COPY cloud/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 18789
CMD ["/app/start.sh"]
