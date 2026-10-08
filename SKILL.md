---
name: tiktok-video-download
description: Download a specified public TikTok video for authorized reference or editing, with Python and yt-dlp, then verify the local media file.
---

Use a canonical HTTPS `https://www.tiktok.com/@user/video/id` URL. This skill
downloads one specified video; it does not discover trends or rank engagement.

Requirements: Python 3.10+, yt-dlp, and FFprobe on PATH. Install the dependency
from the Python package registry when installation is authorized.

```powershell
python -m pip install -r requirements.txt
python scripts/download.py https://www.tiktok.com/@user/video/123 --output C:\Media\reference
```

The helper prints the verified local filename and stores minimal public metadata.
Do not save full extractor dictionaries: they may contain signed URLs or headers.
Downloaded media and local metadata belong outside the public code repository.
The helper has bounded retries, no cookies and no proxies. If access is denied,
login or a verification is required, report the failure instead of evading it.
An ordinary download control in the user's browser is an alternative when available.

Download success does not grant a license to republish another creator's work.
For original recreation, analyze structure and use newly produced visuals/audio.
Validate playback before declaring delivery. Keep source attribution in the
local analysis and distinguish original footage from generated replacements.
