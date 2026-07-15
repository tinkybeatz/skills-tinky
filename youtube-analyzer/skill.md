---
name: "youtube-analyzer"
description: >
  Transcribe and analyze YouTube videos into structured reports, then export
  to Notion. Use this skill whenever the user asks to: "transcribe this video",
  "summarize this YouTube video", "analyze this video", "YouTube transcription",
  "video report", "summarize this video", "transcribe this YouTube video",
  "what does this video say", or any phrasing implying transcription, summary,
  or analysis of a YouTube video. Also trigger when the user pastes a YouTube
  URL (youtube.com/watch, youtu.be/) and asks for any form of content extraction.
  Do not use for non-YouTube video files or audio files stored locally.
---

# YOUTUBE-ANALYZER

Transcribes and analyzes YouTube videos to produce structured reports that are
exported to Notion — similar to Atlas.org, but integrated into your own workflow.

Read `reference/setup.md` on first use (one-time installation).

---

## Scope

**In scope:** public YouTube videos with available subtitles (auto-generated or
manual), in French or English. Talks, tutorials, interviews, podcasts,
presentations.

**Out of scope:** private videos, videos without subtitles, local video files,
platforms other than YouTube (Vimeo, Twitch, etc.).

---

## Prerequisites

The skill needs `youtube-transcript-api` (Python). If it isn't installed, run
this once:

```bash
pip install youtube-transcript-api
```

No API key, no Google account, no configuration. The package fetches the
subtitles directly from YouTube (internal timedtext API).

---

## Step 0 — Parse and validate the URL

Extract the `video_id` from the URL provided:

| URL format | Extraction |
|---|---|
| `youtube.com/watch?v=VIDEO_ID` | `v` parameter |
| `youtu.be/VIDEO_ID` | path after `/` |
| `youtube.com/embed/VIDEO_ID` | path after `/embed/` |
| `youtube.com/watch?v=VIDEO_ID&t=123` | `v` parameter (ignore `t`) |

If the user provides just an ID (11 characters), accept it directly.

**Validation:** confirm the video_id is 11 alphanumeric characters
(plus hyphens and underscores).

---

## Step 1 — Fetch the metadata

Use WebFetch to load the YouTube page and extract:

- Video **title**
- **Channel** (creator name)
- **Publication date** (if visible)
- Approximate **duration**

This metadata is used to structure the report and the Notion page.

---

## Step 2 — Fetch the transcript

Run this via Bash, using the Python from the dedicated venv:

```bash
~/.venvs/youtube/bin/python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch('VIDEO_ID')
for s in transcript:
    minutes = int(s.start // 60)
    seconds = int(s.start % 60)
    print(f'[{minutes:02d}:{seconds:02d}] {s.text}')
"
```

### Language handling

Try in this order:
1. Manual subtitles in the video's language (fr or en)
2. Auto-generated subtitles in the video's language
3. Subtitles in the other language (fallback)

```bash
~/.venvs/youtube/bin/python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
try:
    transcript = ytt.fetch('VIDEO_ID', languages=['fr', 'en'])
except:
    transcript = ytt.fetch('VIDEO_ID')
for s in transcript:
    minutes = int(s.start // 60)
    seconds = int(s.start % 60)
    print(f'[{minutes:02d}:{seconds:02d}] {s.text}')
"
```

### Long videos

If the transcript exceeds 50,000 characters, process it in chunks to avoid
saturating the context. Summarize section by section, but keep the full
transcript for the Notion export.

---

## Step 3 — Generate the structured report

From the raw transcript, produce the following report. The report's language
follows the video's language (French or English).

### Report structure

```markdown
# [Video title]

> **Channel:** [name] | **Date:** [date] | **Duration:** [duration]
> **Language:** [fr/en] | **Source:** [YouTube URL]

---

## Summary

[3-5 sentences. The essence of the video — what it says, why it's
interesting, and the main takeaway. No fluff.]

## Key points

- [Point 1 — one sentence, with a timestamp if relevant]
- [Point 2]
- [Point 3]
- [...]
[5-10 points maximum. Each point must convey a distinct piece of information.]

## Detailed outline

### [00:00] Introduction / [Section title]
[Summary of this section in 2-4 sentences. Capture the main ideas,
don't paraphrase word for word.]

### [MM:SS] [Next section title]
[Summary...]

### [MM:SS] [Next section title]
[Summary...]

[Break the video into logical sections of 3-10 minutes.
The number of sections depends on the length and density.]

## Notable quotes

> "[Exact quote]" — [timestamp]

> "[Exact quote]" — [timestamp]

[2-5 striking quotes, verbatim from the transcript.
Only if some sentences are worth quoting word for word.]

## Full transcript

<details>
<summary>View the full transcript</summary>

[00:00] text...
[00:05] text...
[...]

</details>
```

### Report writing rules

1. **The summary stands on its own.** Someone who reads only the summary should
   grasp the essentials without having watched the video.

2. **The key points are MECE.** No redundancy between points.
   Each point = one new piece of information.

3. **The detailed outline follows the chronology.** Break it down by
   theme/section, not by sentence. Identify the natural transitions in the talk.

4. **Timestamps are approximate.** Round to the nearest minute for sections.
   Keep the precision for quotes.

5. **Don't make things up.** All the report's content comes from the transcript.
   If a passage is inaudible or unintelligible, flag it.

6. **Adapt the depth to the length:**

| Video length | Summary | Key points | Sections | Quotes |
|---|---|---|---|---|
| < 10 min | 2-3 sentences | 3-5 | 2-3 | 1-2 |
| 10-30 min | 3-5 sentences | 5-8 | 4-6 | 2-4 |
| 30-60 min | 5-7 sentences | 7-10 | 6-10 | 3-5 |
| > 60 min | 7-10 sentences | 10-15 | 8-15 | 4-6 |

---

## Step 4 — Export to Notion

Use the Notion MCP to create a page in the dedicated database.

### Target database

The **"YouTube Transcriptions"** database lives in your Notion workspace:

- **Database URL:** `<YOUR_DATABASE_URL>`
- **Data source ID:** `<YOUR_DATA_SOURCE_ID>`

Use this `data_source_id` as the parent when creating pages.
If the database isn't found (deleted or moved), recreate it in your
workspace with these properties:

| Property | Type | Content |
|---|---|---|
| **Title** | Title | Video title |
| **Channel** | Text | YouTube channel name |
| **URL** | URL | YouTube link |
| **Date** | Date | Video publication date |
| **Language** | Select | fr / en |
| **Duration** | Text | Formatted duration (e.g. "24:35") |
| **Tags** | Multi-select | Identified themes (2-4 tags) |
| **Status** | Select | Transcribed |

### Notion page content

The page contains **two mandatory parts**: the structured report AND the raw
transcript. Both must always be present.

#### Part 1 — Structured report

Use the appropriate Notion blocks:

- **Callout** `blue_bg` with a `📺` icon for the metadata at the top of the page
- **Heading 2** for the main sections (Summary, Key points, etc.)
- **Heading 3** for the sub-sections of the detailed outline
- **Bulleted list** for the key points
- **Quote** for the notable quotes
- **Toggle** (`<details>`) for the formatted transcript with timestamps

#### Part 2 — Raw transcript

After the formatted-transcript toggle, add a separate section:

```
## Raw transcript

```
[00:00] raw text line by line...
[00:05] raw text...
[...]
```
```

This section contains the timestamped raw text in a **code block**
(no language specified) — copyable in one click, with no formatting.
It's the source text exactly as fetched by `youtube-transcript-api`,
untouched.

**Both parts are mandatory.** Never omit the raw transcript — it's the source
data that makes the content reusable (articles, client briefs, follow-up
research).

### Automatic tags

Identify 2-4 thematic tags from the content:
- Analyze the summary and the key points
- Choose short, reusable tags (e.g. "AI", "Dev", "Business",
  "Design", "Productivity", "Marketing", "Finance", "Management")
- Reuse existing tags in the database when possible

---

## Step 5 — Confirm and suggest actions

After the export, display a summary in the conversation:

```
Video analyzed: [Title]
Channel: [name] | Duration: [duration] | Language: [language]
Notion export: [link to the created page]

Summary: [2-3 sentences]
```

Then suggest:

> "Would you like me to do something with this content?
> For example: a blog article, a client brief, or follow-up research
> on one of the topics covered?"

---

## Failure modes

| Failure | Corrective action |
|---|---|
| `youtube-transcript-api` not installed | Suggest `pip install youtube-transcript-api` and wait for confirmation |
| Video without subtitles | Inform the user. Suggest alternatives: wait for YouTube to generate auto subtitles, or use an external audio transcription service |
| Subtitles in an unsupported language | Try with the available language, flag it to the user |
| Transcript too long (> 50K chars) | Split into chunks, process section by section, assemble the report |
| Invalid URL or private video | Report the error, ask for a correct URL |
| Very poor auto-subtitle quality | Note in the report that the transcript is auto-generated and may contain errors. Add a warning at the top of the report |
| Notion database not found | Create it with the defined schema, ask the user for confirmation |
| Notion MCP unavailable | Save the report as a local `.md` file and offer the Notion export later |
| Video > 3h | Warn that the report will be long. Offer to limit it to the key points without the full transcript |

---

## Additional resources

| File | When to read it |
|---|---|
| `reference/setup.md` | First use — installation and configuration |
| `reference/notion-schema.md` | If the Notion database needs to be created or modified |
