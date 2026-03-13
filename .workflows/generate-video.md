---
description: Generate all LVT8 video data (theme, track titles, Suno styles, YouTube titles, description) from a single style input
---

# LVT8 Video Generation Workflow

The user provides a **style** — one of:
- **Sunset Melodic House**
- **Chill Progressive / Sunset Progressive**
- **Melodic Deep House**
- **Organic House**

From that single input, execute ALL steps below sequentially in a single run.

---

## Style-to-Pack Mapping

| Style | Pack | Genre String (for YouTube title) |
|---|---|---|
| Sunset Melodic House | A | Sunset Melodic House |
| Chill Progressive / Sunset Progressive | B | Chill Progressive / Sunset Progressive |
| Melodic Deep House | C | Melodic Deep House |
| Organic House | D | Organic House |

---

## Step 0 — Setup

1. Determine the next video number: check existing numbered folders inside `videos/`. Next = highest number + 1.
2. Create the folder `videos/{N}/`.
3. Read `theme_history.md` fully — you need it for uniqueness in Step 1.
4. Read `songs_titles.md` fully — you need it for uniqueness in Step 2.

---

## Step 1 — Generate Theme

Generate one strong, cinematic theme for this video. The theme is the creative DNA that guides all downstream steps.

### Brand Identity (always active)
LVT8: minimalist electronic music brand built around sunset, levitation, and weightless moods. Each video is a long-form playlist of original electronic tracks. Core aesthetic: minimal, clean, horizon-focused visuals (sunset orange + soft purple on black), with a feeling of floating above mountains or distant city lights.

### Uniqueness Rules (non-negotiable)
Before writing the theme, compare your Theme Title + Scenario + Theme DNA against ALL entries in `theme_history.md`. If there's overlap in concept, imagery, or emotional arc, pivot until clearly distinct.

**Too similar** means:
- Same or very close title wording
- Same core setting/imagery combo without a new angle
- Same emotional behavior with only cosmetic changes

**Actively vary:**
- Primary environment (peaks / ocean horizon / desert haze / night highway / rooftop skyline / cloud sea / canyon / aurora / tundra / archipelago)
- Light behavior (ember glow / violet wash / eclipse shade / prism flare / neon fog / silver gradient / copper sheen / teal shift)
- Motion language (hover / drift / orbit / dissolve / glide / rise / sink / sway / spiral)
- Emotional temperature (warm / meditative / yearning / nocturnal / euphoric / serene / hypnotic / tender)

### Constraints
- Non-narrative: no characters, no dialogue, no storyline
- Minimalist, cinematic, dreamy; sunset/levitation/weightless always present
- No EDM clichés ("festival", "banger", "drop", "club anthem")
- Must fit the given style bucket
- YouTube-safe

### Output Format
Save to `videos/{N}/theme.md` and **also append** to `theme_history.md`:

```
**Theme Title:** [2–5 words]

**Scenario:**
[2–3 vivid sentences. Cinematic imagery, motion, light, emotional temperature. No characters, no plot.]

==========================================
```

### Self-Check
- Clearly different from ALL entries in `theme_history.md`
- Scenario feels like a vivid cinematic frame (not generic)
- Fits LVT8's minimalist sunset-levitation identity and the given style bucket

---

## Step 2 — Generate 24 Track Titles

Generate 24 unique English track titles matching the theme from Step 1.

### Strict No-Reuse Rule (absolute)
Any title that appears in `songs_titles.md` is **completely forbidden** (case-insensitive, punctuation-insensitive, minor-variant-insensitive).

Also avoid near-duplicates within the new set:
- "Horizon Lift" vs "Horizon Lifting" → too similar, change concept significantly

### Title Design Philosophy (LVT8 DNA)
Titles should feel:
- Minimalist, cinematic, dreamy
- Abstract but emotionally readable
- Like a photograph caption, a scene marker, or a memory fragment

**Avoid:**
- Generic EDM clichés: "Drop", "Bass", "Banger", "Club", "Dancefloor", "Festival", "Rave"
- Overusing "Sunset" (don't put it in more than 1 title)
- Excessive sci-fi/cyberpunk unless theme explicitly asks
- Long descriptive sentences

### Title Shape Distribution (target across 24)
1. **One-word power titles** — ~3 (single evocative cinematic word)
2. **Two-word power titles** — ~6 (clean, punchy aesthetic pairings: noun+noun, adj+noun, verb+noun)
3. **Poetic cinematic phrases** — ~8 (3–5 words, filmic, atmospheric, soft motion implied)
4. **Fragment / whisper titles** — ~5 (3–5 words, caption-like, thought-like; occasional ellipsis OK but rare)
5. **Abstract / conceptual** — ~2 (may include numbers, symbols, coordinate vibes **DO NOT REPEAT SAME CONCEPT AS PREVIOUS 3 VIDEOS**)

### Style Bucket Alignment
- **Sunset Melodic House**: warm, accessible, glowing, emotional clarity
- **Chill Progressive / Sunset Progressive**: forward motion, evolving arcs, lift, horizon-drive
- **Melodic Deep House**: hypnotic, deeper, intimate, low-slung glow
- **Organic House**: natural textures, earthy air, hand-percussion feel, wide landscapes

Don't mention BPM or instruments in titles.

### Output Format
Save to `videos/{N}/track_titles.md`:

```
1. [Title]
2. [Title]
...
24. [Title]
```

**Also append** ALL 24 titles (one per line, plain text, no numbering) to `songs_titles.md`.

### Self-Check
- No title duplicates inside the new 24
- No exact or near-matches with anything in `songs_titles.md`
- Title shape distribution roughly matches targets
- Titles match the theme mood + style bucket + imagery
- English only

---

## Step 3 — Generate Suno Style Prompts

Generate 12 Suno AI style prompts. Each prompt will produce 2 versions in Suno AI, resulting in 24 total tracks that match the 24 track titles from Step 2.

Run the Python program that generates Suno AI style prompts, saving directly to the video folder:

```
// turbo
python suno_prompt_generator.py --pack {PACK_LETTER} --output {ABSOLUTE_PATH_TO_videos/{N}/suno_styles.txt}
```

Working directory: `styles-project/`

The pack letter comes from the Style-to-Pack Mapping table at the top (A/B/C/D).
The `--output` flag saves directly to the video folder — no manual copy needed.

---

## Step 4 — Generate 10 YouTube Video Title Variants

**This step is YouTube / SEO / Engagement optimized.** The titles must be designed to maximize click-through rate (CTR) on YouTube while staying true to the LVT8 brand. Think like a YouTube strategist: every variant should make a viewer want to click.

Generate 10 YouTube title variants for this video.

### Exact Format
```
[Theme Title] | [Style] Playlist for [Creative situation text]
```

- **Theme Title**: copied verbatim from Step 1's Theme Title
- **Style**: copied verbatim from the user's input style
- Only **"Creative situation text"** changes across the 10 variants

### Creative Situation Text Rules (CTR-focused)
- 2–8 words describing a **use-case moment or atmospheric situation** that a viewer can immediately picture themselves in
- Target viewer intent: people searching for focus music, driving playlists, sunset mixes, chill sessions, late-night work, travel soundtracks
- Must match the theme's imagery (ocean/coast → oceanic situations; mountains/clouds → sky/altitude; etc.)
- **Vary the use cases** across the 10 variants — don't repeat the same activity; cover different listener moments (driving, working, unwinding, traveling, meditating, rooftop evenings, etc.)
- Avoid hype words: "BEST", "ULTIMATE", "TOP"
- No keyword spam
- Max 1 emoji (default: no emoji in titles)
- Feel clickable but honest — describe a mood or moment, not a marketing claim

### Output Format
Save to `videos/{N}/youtube_titles.md`:

```
1) [Full title variant]
2) [Full title variant]
...
10) [Full title variant]
```

### Self-Check
- All 10 are unique and meaningfully different (not just punctuation changes)
- All follow the exact template format
- Situation text fits the theme's scenario
- Use cases are varied — a viewer scanning the list should see multiple relatable moments
- No hype spam, no work related, no focus or study
- Titles feel search-friendly (natural keywords a real listener would type)

---

## Step 5 — Generate YouTube Description

**This step is YouTube / SEO / Engagement optimized.** The description must help YouTube's algorithm classify the video correctly, surface it in search results, and encourage viewer interaction. Write for both the algorithm and the human reader.

Generate a YouTube-optimized description based on the **style** and **theme** from Step 1. This description does NOT reference a specific picked title — it is written around the theme's mood, imagery, and style bucket.

### Structure
Save to `videos/{N}/description.txt`:

**CRITICAL: The description must follow this EXACT structure:**

```
[Theme Title] — a [Style] playlist [atmospheric hook inspired by theme scenario, mentioning a use-case] 🌅✨

[Engagement CTA line 1: ask what track/moment hit hardest, or what they were doing while listening]
[Engagement CTA line 2: encourage like + subscribe naturally, no aggressive marketing]

🔊 Listen also on streaming:
💚 Spotify → https://open.spotify.com/artist/4H5ZVRKpTE2avqsxTFuTMC
🩷 Apple Music → https://music.apple.com/artist/lvt8/1874489965
❤️ YT Music → https://music.youtube.com/channel/UC_s8a9-udx7sZj0VsZEt2Uw

🎧 Tracklist / Timestamps:
[TO BE ADDED AFTER PRODUCTION]

Subscribe to https://www.youtube.com/@lvt8_music for more sunset / levitation playlists. 💎

[Closing line — 1 line, minimal, cinematic, weightless. Should feel like gliding forward into the afterglow.]

[3–5 hashtags, space-separated]
```

### Style Rules
- **Clarity + atmosphere** — poetry must never obscure genre, style, or use case
- Minimalist, cinematic, dreamy, clean & modern
- "DJ / producer identity" tone (not a faceless SEO farm)
- Second person ("you"), short lines, mobile-friendly
- Emojis restrained (1–2 in intro max)
- Naturally include: genre name, a mood anchor (sunset, golden hour, afterglow, night drive, floating), a use case (focus, work, driving, chill, travel)

### SEO Guidelines
- The first 1–2 lines are the most important — YouTube shows ~100–120 characters above the "Show more" fold on mobile. Front-load the genre, mood, and use case there.
- Naturally embed searchable phrases a real listener would type (e.g., "melodic house playlist", "sunset chill mix", "music for focus")
- Hashtags should be genre-relevant and lowercase (e.g., #melodichouse #sunsetmix #chillprogressive)

### Do NOT
- Write long storytelling paragraphs
- Use "best / ultimate / top" marketing language
- Add excessive keyword spam
- Mention AI generation
- Add multiple languages

### Self-Check
- Intro explains WHAT this is (electronic playlist + style)
- Vibe matches LVT8: sunset / levitation / minimalist / cinematic
- Reads well on mobile (short lines, no wall of text)
- Emojis restrained
- Hashtags 3–5 max and relevant
- First 120 characters work as a compelling preview above the fold

After saving `description.txt`, also create an **empty** `videos/{N}/title.txt` file (placeholder — the user will paste their chosen title here later).

---

## Step 6 — Validation Pass

After all generation steps are complete, perform a final integrity check:

1. **Files exist**: Confirm all 6 files were created in `videos/{N}/`:
   - `theme.md`, `track_titles.md`, `suno_styles.txt`, `youtube_titles.md`, `description.txt`, `title.txt`
2. **Title uniqueness**: Re-read `songs_titles.md` and verify the 24 new titles just appended have zero exact duplicates against the rest of the file (case-insensitive).
3. **Theme uniqueness**: Re-read `theme_history.md` and confirm the new Theme Title is not a near-duplicate of any previous entry.
4. **Count check**: `track_titles.md` has exactly 24 entries, `youtube_titles.md` has exactly 10 entries, `suno_styles.txt` has exactly 12 entries.
5. **CRITICAL - Description structure validation**: Read `description.txt` and verify it follows the EXACT template structure from Step 5:
   - Line 1: `[Theme Title] — a [Style] playlist [hook] 🌅✨` (must contain theme title, style, emojis)
   - Line 2: Empty
   - Line 3: Engagement CTA asking about track/moment
   - Line 4: Engagement CTA encouraging like/subscribe
   - Line 5: Empty
   - Line 6: `🔊 Listen also on streaming:`
   - Lines 7-9: Spotify, Apple Music, YT Music links (exact URLs from template)
   - Line 10: Empty
   - Line 11: `🎧 Tracklist / Timestamps:`
   - Line 12: `[TO BE ADDED AFTER PRODUCTION]` (NOT the actual tracklist)
   - Line 13: Empty
   - Line 14: `Subscribe to https://www.youtube.com/@lvt8_music for more sunset / levitation playlists. 💎`
   - Line 15: Empty
   - Line 16: Single-line closing (cinematic, weightless)
   - Line 17: Empty
   - Line 18: 3-5 hashtags, space-separated, lowercase (e.g., `#melodicdeephouse #sunsetmix #deephouse`)

**If description does NOT match this structure, regenerate it immediately.**

If any check fails, report the issue and fix it before finishing.

---

## Summary of Files Created/Modified Per Run

### New files in `videos/{N}/`
| File | Content |
|---|---|
| `theme.md` | Generated theme (Step 1) |
| `track_titles.md` | 24 numbered track titles (Step 2) |
| `suno_styles.txt` | 12 Suno AI style prompts (Step 3) |
| `youtube_titles.md` | 10 YouTube title variants (Step 4) |
| `description.txt` | YouTube description template (Step 5) |
| `title.txt` | Empty placeholder — user fills after picking a title (Step 5) |

### Updated files (append)
| File | What's appended |
|---|---|
| `theme_history.md` | New theme block (Step 1) |
| `songs_titles.md` | 24 new titles, one per line (Step 2) |
