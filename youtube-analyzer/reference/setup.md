# YOUTUBE-ANALYZER — Setup (one-time)

## Installation

Only one Python dependency to install:

```bash
pip install youtube-transcript-api
```

Check that it works:

```bash
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print('OK')"
```

## What the package does

`youtube-transcript-api` fetches YouTube subtitles (manual or auto-generated)
without an API key, without a Google account, and without Selenium. It uses
YouTube's internal `timedtext` API.

- **No API key** — direct access, no quota
- **Lightweight** — 2 dependencies (`requests`, `defusedxml`)
- **Reliable** — actively maintained package (MIT license)

## Known limitations

- **Cloud IPs blocked** — YouTube blocks the IPs of cloud providers
  (AWS, GCP, Azure). Works without issue locally.
- **Videos without subtitles** — if the video has neither manual nor
  auto-generated subtitles, the package can't fetch anything.
- **Auto-generated subtitles** — quality varies by language, accent, and
  background noise. English videos generally have better auto subtitles
  than French.

## Notion

The skill uses the Notion MCP already configured in Claude Code.
No additional configuration is needed.

The "YouTube Transcriptions" database will be created automatically on first
use if it doesn't exist.
