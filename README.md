# Christ Is God — The Divinity of Christ

A scriptural, historical, and grammatical case for the deity of Jesus Christ,
presented as a polished long-form reading website.

## Structure

- **`web/`** — the website. Next.js 16 (App Router, SSG) + React 19 +
  TypeScript + Tailwind v4 + MDX. Classical/reverent design with an animated
  hero, light/dark themes, sticky table of contents, and auto-linkified
  scripture references with KJV hover-cards. Deployed on Vercel.
- **`convert_to_mdx.py`** — content pipeline: reads `_content_raw.json`
  (extracted from the Word manuscript) and regenerates the per-chapter MDX in
  `web/src/content/`, plus the chapter registry and book metadata.
- **`*.docx`** — the source manuscript and earlier drafts.

## Develop

```bash
cd web
npm install
npm run dev        # http://localhost:3000
```

## Update content

1. Edit the manuscript and re-extract `_content_raw.json`.
2. Run the converter (uses a venv with `python-docx`):
   ```bash
   python3 convert_to_mdx.py
   ```
3. The MDX, chapter registry, and metadata under `web/src/` regenerate.

## Deploy

The site deploys to Vercel from the `web/` directory (set as the project root).

---

Scripture quotations are from the King James Version (public domain).
