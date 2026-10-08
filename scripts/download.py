"""Download one public TikTok video via yt-dlp, retaining minimal provenance."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def validate_url(url):
    parts = urlparse(url)
    if parts.scheme != 'https' or parts.hostname not in {'www.tiktok.com', 'tiktok.com'}:
        raise ValueError('Use an HTTPS TikTok video URL.')
    if parts.query or parts.fragment or not re.fullmatch(r'/@[A-Za-z0-9._-]+/video/[0-9]+/?', parts.path):
        raise ValueError('Use a canonical /@user/video/id URL without query parameters.')
    return url


def download(url, output):
    from yt_dlp import YoutubeDL
    url = validate_url(url)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    options = {'outtmpl': str(output / '%(id)s.%(ext)s'), 'format': 'best[ext=mp4]/best',
               'noplaylist': True, 'quiet': True, 'retries': 1, 'extractor_retries': 1,
               'socket_timeout': 25, 'overwrites': False, 'cachedir': False,
               'ignoreconfig': True, 'writethumbnail': False}
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        media = Path(ydl.prepare_filename(info))
    if not media.is_file() or media.stat().st_size == 0:
        raise RuntimeError('No verified downloaded file.')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', str(media)], check=True, capture_output=True, text=True)
    streams = json.loads(probe.stdout)
    if not any(s.get('codec_type') == 'video' for s in streams.get('streams', [])):
        raise RuntimeError('Downloaded file has no video stream.')
    # Do not persist cookies, signed media URLs, headers or full extractor info.
    metadata = {k: info.get(k) for k in ('id', 'title', 'description', 'uploader', 'upload_date', 'duration', 'view_count', 'like_count', 'comment_count')}
    metadata.update({'source': url, 'file': media.name, 'probe': streams})
    (output / f"{info['id']}.metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    return media


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        print(download(args.url, args.output))
    except Exception as exc:
        print(f'Download failed: {type(exc).__name__}. No bypass or cookie extraction attempted.')
        raise SystemExit(2)
