# DataIntel — YouTube Analytics Platform

Ask any question about your YouTube analytics in plain English.  
Get an interactive dashboard with KPIs, charts, and AI insights in under 5 seconds.

---

## Project structure

```
dataintel/
├── app/
│   ├── api/
│   │   └── claude/
│   │       └── route.js       ← API proxy (keeps key server-side)
│   ├── layout.js
│   └── page.js
├── components/
│   └── DIDashboard.jsx        ← Entire app (3200+ lines)
├── .env.local                 ← Your API key goes here (never commit)
├── .gitignore
├── next.config.js
└── package.json
```

---

## Setup in VS Code — 4 steps

### Step 1 — Paste these files

Create a new folder called `dataintel` and paste all files exactly as shown above.

### Step 2 — Install dependencies

Open the terminal in VS Code (`Ctrl+\`` or `Cmd+\``) and run:

```bash
npm install
```

This installs: Next.js 14, React 18, Recharts.

### Step 3 — Add your API key

Open `.env.local` and replace the placeholder:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

Get your key from: https://console.anthropic.com/settings/api-keys

### Step 4 — Run it

```bash
npm run dev
```

Open http://localhost:3000 — you should see the DataIntel landing page.

---

## Deploy to Vercel (free)

### Option A — Vercel CLI (fastest)

```bash
npm install -g vercel
vercel
```

Follow the prompts. When asked about environment variables, add:
- Key: `ANTHROPIC_API_KEY`
- Value: your key from console.anthropic.com

### Option B — GitHub + Vercel dashboard

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "DataIntel v1.0"
git remote add origin https://github.com/YOUR_USERNAME/dataintel.git
git push -u origin main

# 2. Go to vercel.com → New Project → Import your repo
# 3. Add ANTHROPIC_API_KEY in the Environment Variables section
# 4. Click Deploy
```

Your app will be live at `https://dataintel.vercel.app` (or similar).

---

## How the API proxy works

The component calls `/api/claude` (a Next.js route in `app/api/claude/route.js`).  
That route adds your `ANTHROPIC_API_KEY` server-side and forwards to Anthropic.  
Your key is **never exposed to the browser**.

On localhost: uses `/api/claude`  
In the Claude artifact environment: calls Anthropic directly (no key needed there)

---

## Tech stack

| Technology | Purpose |
|---|---|
| React 18 | UI framework |
| Next.js 14 | React framework + API routes |
| Claude Sonnet | Natural language → SQL + chart config |
| Recharts 2 | Chart rendering |
| Vercel | Deployment |
| Web Speech API | Voice input |
| localStorage | Saved dashboards persistence |

---

## Dataset schema

The app is pre-configured for this YouTube analytics table:

```sql
TABLE: youtube_videos (
  timestamp       DATETIME,
  video_id        VARCHAR,
  category        VARCHAR,
  language        VARCHAR,
  region          VARCHAR,
  duration_sec    INTEGER,
  views           INTEGER,
  likes           INTEGER,
  comments        INTEGER,
  shares          INTEGER,
  sentiment_score FLOAT,
  ads_enabled     BOOLEAN
)
```

---

## Common issues

**`Module not found: recharts`**  
→ Run `npm install` again

**`ANTHROPIC_API_KEY is undefined`**  
→ Make sure `.env.local` exists and restart `npm run dev`

**`API 401 Unauthorized`**  
→ Your API key is wrong. Check console.anthropic.com

**Port 3000 already in use**  
→ Run `npm run dev -- --port 3001`

---

Made with ♥ in India · Hackathon 2025
