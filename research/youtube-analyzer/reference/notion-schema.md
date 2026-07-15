# YOUTUBE-ANALYZER — Notion schema

## Database: "YouTube Transcriptions"

### Properties

| Property | Notion type | Description |
|---|---|---|
| **Title** | Title | YouTube video title |
| **Channel** | Rich text | Channel / creator name |
| **URL** | URL | Full YouTube link |
| **Date** | Date | Video publication date |
| **Language** | Select | Options: `fr`, `en` |
| **Duration** | Rich text | Format `MM:SS` or `HH:MM:SS` |
| **Tags** | Multi-select | Identified themes (2-4 per video) |
| **Status** | Select | Options: `Transcribed`, `In progress`, `Error` |

### Suggested tags (to reuse)

Prefer short, reusable tags:

- **Tech:** AI, Dev, Frontend, Backend, DevOps, Data, Cloud, Security
- **Business:** Marketing, Finance, Management, Freelance, SaaS, Startup
- **Creative:** Design, UX, Branding, Motion
- **Other:** Productivity, Research, Tutorial, Talk, Interview, Podcast

### Page content structure

```
[Callout block — metadata: channel, date, duration, language, URL]

## Summary
[paragraph]

## Key points
[bulleted list]

## Detailed outline
### [timestamp] Section 1
[paragraph]
### [timestamp] Section 2
[paragraph]
...

## Notable quotes
[quote blocks]

## Full transcript
[toggle block containing the timestamped transcript]
```

### Creating the database

If the database doesn't exist, create it in your main Notion workspace with the
properties above. Use a "Table" view by default, sorted by date descending.

Also offer a "Gallery" view with the title and tags visible, grouped by channel.
