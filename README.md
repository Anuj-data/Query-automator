# AI Query Automator

**Internal tool for Wizikey media intelligence teams** — generate multilingual Boolean search queries instantly, ready to deploy on Opoint.

![Wizikey] https://github.com/Anuj-data/Query-automator/blob/main/query_automator/wizkey.png

## What It Does

Enter a brand or keyword in English, select target languages, and get a ready-to-use Boolean search expression — **phonetically transliterated, not meaning-translated** — with a one-click redirect into Opoint.

- Cuts query creation time from 15–20 minutes down to under 10 seconds
- Removes the need for language specialists on routine query building
- Supports 11 Indian languages with phonetically accurate transliteration
- One-click redirect to Opoint search with the query pre-filled

## The Problem

Media monitoring across Indian regional languages had a recurring bottleneck:

- Analysts manually typed brand names in each regional language — slow and error-prone
- Phonetic variants of the same brand (e.g. "Airtel" in Hindi, Bengali, Tamil) were inconsistent across teams
- No standardized process for multilingual query construction
- Every new campaign or brand meant repeating the same manual work from scratch

Net effect: missed coverage, inconsistent monitoring quality, and analyst time lost to non-analytical work.

## How It Works

| Step | What Happens |
|---|---|
| 1. Input | Analyst enters a keyword (e.g. "Ather Energy") and selects target languages |
| 2. Transliteration | Google Input Tools API phonetically converts the keyword into each selected language |
| 3. Query Build | A Boolean query is assembled with the correct OR/AND operators and quoted terms |
| 4. Review | The generated query is shown in an output box for the analyst to verify |
| 5. Redirect | One click opens Opoint with the query pre-loaded — results appear instantly |

### Why Transliteration, Not Translation

Standard translation converts *meaning* — "energy" becomes "urja" in Hindi, which is not how the brand actually appears in news coverage. This tool uses **Google Input Tools phonetic transliteration** instead, so "Ather Energy" comes out as it's actually written by journalists — phonetically, not semantically.

### Language Support

| Language | Code |
|---|---|
| English | `en` — original / lowercase / UPPERCASE / Title Case |
| Hindi | `hi` |
| Bengali | `bn` |
| Gujarati | `gu` |
| Marathi | `mr` |
| Tamil | `ta` |
| Telugu | `te` |
| Kannada | `kn` |
| Malayalam | `ml` |
| Punjabi | `pa` |
| Urdu | `ur` |

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.x + Flask | REST API server, query generation logic |
| Transliteration | Google Input Tools API | Free, keyless, phonetically accurate |
| Frontend | HTML5 + CSS + JavaScript | No framework dependency |
| Styling | Custom CSS (CSS variables) | Dark theme, responsive, animated UI |
| Deployment | Flask dev server | Single command: `python app.py` |

## Project Structure
(https://m360.opoint.com/search/?expression={URL_ENCODED_QUERY}&filters=geo:1144)


The generated query is URL-encoded into the `expression` parameter. The `geo:1144` filter is fixed to India-specific results — the user only needs to press Enter on Opoint to fetch results.

## Limitations

| Limitation | Detail |
|---|---|
| Transliteration accuracy | Google Input Tools may not capture every brand variant — human review recommended for critical queries |
| No authentication | Currently open access — suitable for internal use only |
| In-memory cache | Cache resets on server restart, no persistence |
| Fixed geo filter | Opoint redirect is hardcoded to `geo:1144` (India) |

## Planned Improvements

- Word-level control — choose which words to transliterate vs. keep in English
- Saved query templates — persist frequently used queries
- Multi-geo support — select different Opoint geo filters
- Bulk keyword input — upload a CSV, generate queries in batch
- Query history — per-session log of previously generated queries
- Auth integration — SSO with Wizikey internal systems

## Setup

**Prerequisites:** Python 3.8+, pip, and an internet connection (for the Google Input Tools API).

```bash
# 1. Place the QUERY_AUTOMATOR folder on the server

# 2. Install dependencies
pip install flask requests

# 3. Run the server
python app.py

# 4. Open in browser
http://localhost:5000
```

**Dependencies**

| Package | Purpose |
|---|---|
| `flask` | Web framework — serves the UI and API endpoints |
| `requests` | HTTP client — calls the Google Input Tools API |

No paid APIs, no environment variables, no `.env` file required.

## Security Notes

- No user data is stored — all processing is stateless per request
- No API keys in source — the Google Input Tools API is public and keyless
- Should be deployed behind an internal network / VPN for production use
- `debug=True` should be disabled before any production deployment

## Quick Reference

**Start the tool:**
```bash
python app.py
```

**Example:**
Keyword: "Airtel" | Languages: English, Hindi, Tamil
Result: ("Airtel" OR "airtel" OR "AIRTEL" OR "<hindi>" OR "<tamil>")


---

*AI Query Automator · v1.0 · 2026 · Internal / Confidential — Wizikey*
