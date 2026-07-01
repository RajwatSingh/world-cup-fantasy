# Learning Roadmap: Build the World-Fantasy Frontend Yourself

## Context
You are **new to React** and want to build a React + Vite + Recharts dashboard on
top of the existing FastAPI backend — **as a learning exercise**. This plan is a
study guide, not an implementation. You write all the code; Claude explains
concepts, reviews what you write, and hints when asked. Because React is new, we
start from React fundamentals and only reach charts once the basics click.
Delivery style: **concepts first, then build, with self-verified checkpoints.**
Pace is deliberately slow — do not skip ahead; each concept builds on the last.

Backend endpoints you'll consume:
- `GET /api/players?position=FWD` → object keyed by player name
- `GET /api/teams?min_strength=0` → `{ team: strengthNumber }`
- `GET /api/ranks?players=a,b&round=4` → object keyed by manager:
  `{ "ramborajwat": { rounds:[...], ranks:[...], points:[...] } }`

---

## Part 1 — React fundamentals FIRST (new to React)
Learn these before touching the dashboard. Practice each in a throwaway component
(e.g. edit the default `App.jsx` Vite gives you). Each has a checkpoint you verify.

1. **What React even is.** Components = functions that return UI. JSX = HTML-like
   syntax inside JS (`className` not `class`, `{}` to embed JS values). The virtual
   DOM idea in one sentence: you describe *what* the UI should look like for the
   current data, React figures out the DOM changes. ✅ *Checkpoint: write a component
   that returns `<h1>` with a value from a JS variable via `{}`.*

2. **Components + props.** How to split UI into small functions and pass data down
   with props (read-only inputs). ✅ *Checkpoint: make a `<TeamRow name= strength=>`
   child and render it from a parent.*

3. **State + re-rendering (`useState`).** State = data that changes over time; setting
   it re-renders the component. Why you never mutate state directly. ✅ *Checkpoint:
   a button that increments a counter shown on screen.*

4. **Rendering lists.** `array.map()` → array of JSX, and why each item needs a `key`.
   ✅ *Checkpoint: render a hardcoded array of teams as a list.*

5. **Side effects + fetching (`useEffect`).** Effects run after render; use one to
   fetch data on mount (empty dependency array). The three states every request has:
   loading / error / data — and why you must handle all three. ✅ *Checkpoint: sketch
   the state variables a data-loading component needs and when each is shown.*

## Part 1b — Dashboard-specific concepts (once Part 1 clicks)

6. **Vite dev server + proxy.** Why a build tool, what `npm run dev` does, and why we
   proxy `/api` → `http://127.0.0.1:8000` instead of hardcoding the host / fighting
   CORS. ✅ *Checkpoint: explain what breaks if you fetch `http://localhost:8000/...`
   directly from the browser.*

7. **The pivot transform (the crux of the chart).** Your API is keyed by manager;
   Recharts wants an array with one row per x-axis point (round). Target shape:
   `[{ round:1, ramborajwat:29, CHEKCHY:41 }, ...]`. ✅ *Checkpoint: on paper, convert
   a 2-manager/3-round sample by hand before coding it.*

8. **Recharts mental model.** Declarative components: `ResponsiveContainer` →
   `LineChart data` → `XAxis`/`YAxis`/`Tooltip`/`Legend` → one `<Line dataKey=...>`
   per series. Two specifics for you: `<YAxis reversed>` for rank (1 = best on top),
   and `<Line>` animates on mount by default (your "progress animation"). ✅
   *Checkpoint: explain what `dataKey` points at and why each manager needs its own Line.*

---

## Part 2 — Build order (you code each step; verify before moving on)
Do these in order. Each step ends with something you can see working.

1. **Scaffold.** `npm create vite@latest frontend -- --template react`, install
   `recharts`. Add the `/api` proxy to `vite.config.js`. ✅ *Verify: `npm run dev`
   serves the default page.*

2. **API layer.** A small `src/api.js` with one helper per endpoint (returns parsed
   JSON, throws on non-OK). Keeps fetch details out of components. ✅ *Verify: log the
   result of the players call in the console.*

3. **One data-driven view first: Teams.** Simplest shape (`{team: number}`). Fetch,
   handle loading/error, render a sorted list or a Recharts `<BarChart>`. This is
   where you learn the fetch-render loop with the least friction. ✅ *Verify: teams
   render sorted by strength.*

4. **Players table.** Convert the name-keyed object to an array, sort by `score`,
   add a position filter (drives the `?position=` query). ✅ *Verify: filtering FWD
   changes the rows.*

5. **Progression chart (the goal).** Fetch `/api/ranks`, apply your pivot transform,
   render two `LineChart`s: ranks (reversed Y) and points. Add inputs for the
   `players` and `round` params. ✅ *Verify: lines animate in and match the numbers;
   a slow first load confirms it's hitting the live FIFA API.*

6. **Shell + navigation.** Tabs/routes tying the three views together. ✅ *Verify:
   switching tabs preserves each view.*

---

## Things to watch (real constraints, not bugs to fix now)
- `/api/ranks` is **slow** (multiple live FIFA calls per request) — this is exactly
  why step 5 must show a loading state. Good motivation for backend caching later.
- The FIFA `Cookie` in `league_ranking.py:9` expires; if progression goes empty,
  that's why — not your frontend.

## How we'll work
When you hit a checkpoint or get stuck: paste your code or the error, and Claude
reviews/hints rather than rewriting it. Ask for the "why" anytime.
