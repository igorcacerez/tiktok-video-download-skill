# TikTok Video Download — Codex skill

Small Python wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp).
Downloads one public TikTok video and verifies it with FFprobe. It retains
minimal source metadata and never exports browser cookies or signed media URLs.

Install Python, FFmpeg/FFprobe, then `pip install -r requirements.txt`.
Run `python scripts/download.py URL --output PATH`.
To install as a Codex skill, copy this directory into `~/.codex/skills/tiktok-video-download`.

See SKILL.md for workflow and limitations. Private videos, paywalls, CAPTCHA
and blocked requests are not bypassed. Availability depends on TikTok and yt-dlp.
This repository includes code only, not creator footage or account data.
