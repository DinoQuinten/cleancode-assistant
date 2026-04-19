# UI Master Guide

A unified reference distilled from 8 books + the WCAG 2.2 accessibility standard. Use this as the north-star checklist for any UI decision. Each rule cites its source so you can dig deeper.

**Sources**
- `[RUI]` Refactoring UI — Wathan & Schoger
- `[DMMT]` Don't Make Me Think (3rd ed.) — Krug
- `[DI]` Designing Interfaces (3rd ed.) — Tidwell, Brewer, Valencia
- `[UXB]` UX for Beginners — Joel Marsh
- `[MOM]` The Mom Test — Rob Fitzpatrick
- `[CBD]` Change by Design — Tim Brown / IDEO
- `[IOC]` Interaction of Color — Albers
- `[C&L]` Colour and Light — Hardin / Klarén / Arnkil (Swedish Academy)
- `[WCAG]` Web Content Accessibility Guidelines 2.2

---

## Part I — The Mindset

1. **Design is how it works, not how it looks.** Prove it with results, not opinion. `[UXB]`
2. **If it's not solving a user's problem, it's not UX.** Style without utility is decoration. `[UXB]`
3. **Hold three lenses in tension**: Desirability (people), Feasibility (tech), Viability (business). Drop one and the product fails. `[CBD]`
4. **Iterate in cycles**: Inspiration → Ideation → Implementation, looping, never linear. `[CBD]`
5. **Fail early to succeed sooner.** A prototype that teaches you something beats one that works flawlessly. `[CBD]`
6. **Design only what you're prepared to build.** Feature bloat is a decision, not a default. `[RUI]`
7. **Start with a feature, not a layout.** Layouts emerge from real functions. `[RUI]`
8. **Design in grayscale first.** Color is the last decision, not the first. `[RUI]`
9. **Limit choices upfront.** Decision fatigue kills consistency. Define a system (spacing, type, color) before you open the canvas. `[RUI]`

---

## Part II — Talk to Users Before You Touch Pixels

The cheapest UX improvement is not designing the wrong thing. `[MOM]`

**The three rules of good conversations**
1. Talk about **their** life, not your idea.
2. Ask about **specific past events**, not generic futures.
3. **Listen more than you talk.**

**The three bad signals to watch for in user talk**
- **Compliments** — cost nothing, reveal nothing. Deflect: "I got excited; how are you actually dealing with this now?"
- **Fluff** — "I usually / I would / I might." Anchor to a specific last-time-this-happened.
- **Ideas & feature requests** — people know their pain, not the solution. Dig: "Why do you want that? What's it blocking?"

**Good questions**
- "Talk me through the last time that happened."
- "Why do you bother?"
- "What are the implications of that problem?"
- "What have you already tried?"
- "How much time/money does this cost you?"
- "Who else should I talk to?"

**Bad questions to avoid**
- "Do you think it's a good idea?"
- "Would you buy a product that did X?"
- "How much would you pay for X?"

**Signals = commitments**, not words. A real signal is time, reputation, or cash — the rest is fluff. A meeting without a clear next step was pointless.

**Note-taking shorthand (Mom Test):** ⚡ pain · 🎯 goal · ☐ obstacle · ⤴ workaround · ☑ feature request · ＄ money · ♀ person/company · ☆ follow-up.

---

## Part III — How Users Actually Behave

Design for the real human, not the rational one.

### Krug's laws `[DMMT]`
- **Law 1: Don't make me think.** If a screen requires a decision about what it is, you've failed.
- **Law 2: Number of clicks doesn't matter — number of *unclear* clicks does.** 3 thoughtful clicks beat 1 ambiguous click.

### Universal user behaviors
- **Users scan, they don't read.** Optimize for glanceability. `[DMMT]`
- **Users satisfice.** First plausible option wins; they don't compare carefully. `[DMMT][DI]`
- **Users don't read instructions.** They muddle through. `[DMMT]`
- **Users teleport** into deep pages from search/social/email — Home is not the entry point. Every page must orient. `[DMMT]`
- **Users follow scent.** Scent-rich links name their destination; ambiguous links lose them. `[DMMT]`
- **Users never go backwards voluntarily.** A back-button click is a confusion signal. Design loops, not dead ends. `[UXB]`

### Tidwell's user-behavior palette — design to support each `[DI]`
- **Safe Exploration** — undo/reversibility so users will try things.
- **Instant Gratification** — new users must succeed inside seconds.
- **Satisficing** — the first obvious option should be the right one.
- **Changes in Midstream** — escape routes and re-entry points for when goals shift.
- **Deferred Choices** — allow "skip for now"; don't force every decision upfront.
- **Incremental Construction** — enable iterative build-up with live feedback.
- **Habituation** — repeat gestures in the same place; never move shortcuts.
- **Microbreaks** — support tiny task chunks on poor attention budgets.
- **Spatial Memory** — keep controls in predictable locations.
- **Prospective Memory** — open tabs and bookmarks are passive reminders; don't auto-clean.
- **Streamlined Repetition** — one-key solutions for repetitive tasks.
- **Keyboard-Only** — full app reachable without a mouse.

### Laws from cognitive science `[UXB]`
- **Hick's Law** — more visible options slow decisions. Categorize or reduce.
- **Fitts's Law** — targets get easier as they get larger and closer. Mobile thumb zones.
- **Miller's Law (7±2)** — short-term memory has ~7 slots. Chunk, group, hide.
- **Cognitive load ("bricks")** — every requirement is a brick; too many = abandonment.
- **Hyperbolic discounting** — a benefit now beats a larger benefit later. Design rewards accordingly.
- **Conscious vs. subconscious experience** — trust is built silently; delight is loud. Good UX feels invisible.

### Motivations that move users `[UXB]`
Users are moved by: safety, homeostasis, sex, love, **status**, **justice**, **curiosity**. Of these, digital UX most often exploits status (autonomy/authority/leveling), justice (fairness/respect), and curiosity (unknowns).

---

## Part IV — Information Architecture & Navigation

- **4 IA shapes**: Category (most sites), Task (goal apps), Search (UGC-heavy), Time (feeds/email). Don't mix without reason. `[UXB]`
- **Breadth over depth**, but with clarity. Three mindless clicks is fine; one thoughtful click is not. `[DMMT]`
- **Persistent nav** on every page: site ID (logo → Home), main nav, utilities (search/login/help), breadcrumbs. `[DMMT]`
- **Site ID is a Home button.** Users will click the logo to escape. Make it work. `[DMMT]`
- **Offer both browsing and searching.** Users split into two camps; never force one. `[DMMT]`
- **Breadcrumbs** rescue teleported users. `[DMMT][DI]`
- **Deep links** — capture state in the URL so anything can be bookmarked and shared. `[DI]`
- **Escape Hatch on every screen.** No mode should trap the user. `[DI]`

### Home / Landing must answer in 5 seconds `[DMMT]`
1. What is this?
2. What can they do here?
3. Why here and not somewhere else?
4. Where do I start?

Three expression points: **tagline** (6–8 words), **welcome blurb** (specific, no corporate speak), **teases** (sample content via headlines).

---

## Part V — Visual Hierarchy & Layout

### Hierarchy rules `[RUI][DMMT]`
- **Hierarchy is everything.** It's the single biggest lever for "feeling designed".
- **Use weight and color, not size alone**, to express importance.
- **Emphasize by de-emphasizing.** Reduce the competition, not the winner.
- **Treat labels as secondary**; value + context together.
- **Action hierarchy**: primary action prominent, secondary subdued, destructive actions require confirmation.

### Layout rules `[RUI][DI]`
- **Start with excessive whitespace, then trim.** Cluttered defaults are hard to undo.
- **Fixed spacing scale** (e.g., 4/8/12/16/24/32/48/64). Never arbitrary pixel values.
- **Scale is non-linear** — smaller steps at small sizes, larger steps as you grow.
- **Don't fill the screen.** Content width should match reading comfort, not viewport width.
- **Grid of Equals** for items of equal weight; **Center Stage** for one dominant task. `[DI]`
- **Titled Sections** + **Accordion** + **Module Tabs** for dense IA. `[DI]`
- **Visual Framework**: same layout, palette, type, and chrome across every page. `[DI]`

---

## Part VI — Typography

- **One neutral sans-serif with 5+ weights** is the safest default. `[RUI]`
- **Modular scale** (e.g., 1.125 / 1.25 / 1.333 / 1.5 ratios), hand-tweaked as needed. `[RUI]`
- **Use px or rem, not em.** em compounds unpredictably. `[RUI]`
- **Line length 45–75 characters.** Longer = fatigue; shorter = choppy. `[RUI]`
- **Line-height scales inversely with font size.** Big text needs tighter leading. `[RUI]`
- **Align mixed-size text by baseline**, not center. `[RUI]`
- **Tighten letter-spacing** for large headlines; loosen for all-caps. `[RUI]`
- **Subtle links** — not every link needs a bright color; underline on hover suffices in text. `[RUI]`
- **Headings** carry the outline; use semantic `<h1>…<h6>`, never fake them with `<div>`. `[DMMT][WCAG]`

---

## Part VII — Color

### Systemic palette `[RUI]`
- **8–10 grey shades.** Warm or cool greys; pick one and stick with it.
- **1–2 primary hues × 5–10 shades each.**
- **Accent hues** for status (success, warning, danger, info) — each with its shade set.
- **Work in HSL, not hex.** Manipulate lightness/saturation intuitively.
- **Define all shades upfront.** No on-the-fly color invention in components.

### Perception rules — the non-negotiable physics
- **Color is relative.** A color on one background is not the same color on another. Test in context. `[IOC]`
- **Value contrast (luminance) > hue contrast** for legibility and hierarchy. `[IOC][C&L]`
- **Simultaneous contrast**: two adjacent colors shift each other's appearance. Check every neighbor. `[IOC]`
- **Color constancy**: if you tint the whole scene (dark mode, night mode), shift *all* colors together — not just some. `[IOC][C&L]`
- **Equal-value hues merge visually.** If two hues have the same luminance, their boundary dissolves — bad for legibility. `[IOC]`
- **Don't rely on hue alone for meaning.** Color blindness, low light, and glare will defeat it. Pair color with icons, labels, shapes. `[RUI][WCAG]`
- **Warm light ⇒ cool shadows; cool light ⇒ warm shadows.** Shadows reflect ambient light, not the object's hue. `[C&L]`
- **Saturation is light-dependent.** Desaturate in dim UI modes; boost in bright modes. `[C&L]`
- **Avoid pure #000 and #FFF.** Real surfaces reflect 5–85% — absolute black/white look artificial and increase eye strain. `[C&L]`

### Harmony isn't rules, it's observation `[IOC]`
Skip prescriptive color-wheel dogma. Test in context and trust your eye, informed by contrast principles.

---

## Part VIII — Depth, Light, Shadows, Surfaces

- **Light comes from above.** Raised elements are lighter on top, darker on bottom. `[RUI]`
- **Shadow = elevation.** Small tight shadows for slight lift; larger soft shadows for prominence. `[RUI]`
- **Dual-shadow technique**: a soft wide shadow for depth + a tight inner shadow for edge clarity. `[RUI]`
- **Shadows should be tinted**, not pure black. Show the ambient light's color. `[C&L]`
- **Gradients signal form.** Value-only gradients feel flat; add a subtle hue shift for roundness. `[C&L]`
- **Replace borders with shadows or color differences where possible.** Borders often over-separate. `[RUI]`
- **Glass/translucency**: must show what's behind. Blur + tint the substrate; pure transparency reads as "empty". `[C&L]`
- **Surface mode signals** — matte (diffuse light), glossy (specular highlight), translucent (scatter). Be consistent. `[C&L]`

---

## Part IX — Forms & Input

- **Forgiving Format** — accept phone numbers as `1234567890` or `(123) 456-7890`. Parse, don't reject. `[DI]`
- **Structured Format** — use masks when rigidity helps (credit card, date). `[DI]`
- **Fill-in-the-Blanks** — conversational sentences with inline inputs for short forms. `[DI]`
- **Input Hints & Prompts** — placeholder text or inline help for format expectations. `[DI]`
- **Good Defaults** — prefill with last-used, most-likely, or contextual values. `[DI]`
- **Autocompletion** — reduce typing; make the full vocabulary searchable. `[DI]`
- **Password Strength Meter** + **Accessible Authentication** (see WCAG 2.2 §3.3.8). `[DI][WCAG]`
- **Progressive disclosure** — only ask what's needed now; don't confront users with 20 fields. `[DMMT]`
- **Error messages**: specific, actionable, blame-free, adjacent to the field. `[DI]`
- **Smart menu items** — disable/enable based on state. `[DI]`
- **Cancelability & Multilevel Undo** — nothing final until the user commits. `[DI]`
- **Minimize asked-for info** — every field not strictly needed erodes trust. `[DMMT]`

---

## Part X — The Tidwell Pattern Catalog (quick reference)

> 50+ patterns, grouped. One line each. Pull this when stuck on a layout. `[DI]`

### Page-level / IA
Feature-Search-Browse · Streams & Feeds · Media Browser · Dashboard · Canvas + Palette · Wizard · Settings Editor · Alternative Views · Many Workspaces · Help Systems · Tags.

### Navigation
Clear Entry Points · Menu Page · Pyramid · Modal Panel · Deep Links · Escape Hatch · Fat Menus · Sitemap Footer · Sign-In Tools · Progress Indicator · Breadcrumbs · Annotated Scroll Bar · Animated Transition.

### Layout
Visual Framework · Center Stage · Grid of Equals · Titled Sections · Module Tabs · Accordion · Collapsible Panels · Movable Panels.

### Lists & Data
Two-Panel Selector (split view) · One-Window Drilldown · List Inlay · Cards · Thumbnail Grid · Carousel · Pagination · Jump to Item · Alpha/Numeric Scroller · New-Item Row · Datatips · Data Spotlight · Dynamic Queries · Data Brushing · Multi-Y Graph · Small Multiples.

### Forms & Input
Forgiving Format · Structured Format · Fill-in-the-Blanks · Input Hints · Input Prompt · Password Strength Meter · Autocompletion · Drop-down Chooser · List Builder · Good Defaults · Error Messages.

### Controls & Actions
Button Groups · Hover / Pop-up Tools · Action Panel · Prominent "Done" · Smart Menu Items · Preview · Spinners · Cancelability · Multilevel Undo · Command History · Macros.

### Mobile-first
Vertical Stack · Filmstrip · Touch Tools · Bottom Navigation · Collections & Cards · Infinite List · Generous Borders · Loading Indicators · Richly Connected Apps · Make It Mobile (not a shrunk desktop).

---

## Part XI — Mobile

- **Mobile-first is a design discipline**, not a responsive breakpoint. `[DMMT]`
- **Touch targets ≥ 44×44 pt (iOS) / 48×48 dp (Android)**; WCAG 2.2 §2.5.8 minimum: 24×24 CSS px. Prefer the larger. `[DI][WCAG]`
- **No hover states on touch.** Every hover affordance needs a tap alternative. `[DMMT]`
- **Bottom navigation** for thumb-zone ergonomics on large phones. `[DI]`
- **Generous borders** around tap targets — fingers are imprecise. `[DI]`
- **Provide a Full Site toggle** when a mobile version omits features. `[DMMT]`
- **Performance is accessibility on mobile.** 3G/4G is not universal. Optimize aggressively. `[DMMT]`

---

## Part XII — WCAG 2.2 Accessibility

Accessibility is not an optional layer — it's correctness. WCAG is organized around **four principles (POUR)** and three conformance levels (**A**, **AA**, **AAA**). **Target AA** for public products; treat many AAA criteria as stretch goals.

### Principle 1 — Perceivable `[WCAG]`
- **1.1.1 Non-text Content (A)** — every image, icon, control has a text alternative. Decorative images use `alt=""`.
- **1.2.x Media** — captions for video (AA), audio descriptions (AA), transcripts for audio-only.
- **1.3.1 Info and Relationships (A)** — structure conveyed through semantic markup (headings, lists, tables, labels), not just visuals.
- **1.3.5 Identify Input Purpose (AA)** — use HTML autocomplete attributes (`autocomplete="name"`, `email`, `tel`…).
- **1.4.3 Contrast (Minimum) (AA)** — text ≥ **4.5:1**; large text (≥18pt or 14pt bold) ≥ **3:1**.
- **1.4.4 Resize Text (AA)** — text resizable to 200% without loss of content or function.
- **1.4.10 Reflow (AA)** — content reflows at 320 CSS px wide without horizontal scroll.
- **1.4.11 Non-text Contrast (AA)** — UI components and graphical info ≥ **3:1** against adjacent colors.
- **1.4.12 Text Spacing (AA)** — users can override line-height (1.5×), paragraph spacing (2×), letter-spacing (0.12×), word-spacing (0.16×) without clipping.
- **1.4.13 Content on Hover or Focus (AA)** — tooltips/popovers must be dismissible, hoverable, and persistent.

### Principle 2 — Operable `[WCAG]`
- **2.1.1 Keyboard (A)** — every function reachable and operable via keyboard.
- **2.1.2 No Keyboard Trap (A)** — Tab can always exit.
- **2.1.4 Character Key Shortcuts (A)** — single-key shortcuts can be turned off or remapped.
- **2.2.1 Timing Adjustable (A)** — any time limit can be extended/turned off (except real-time like auctions).
- **2.3.1 Three Flashes (A)** — nothing flashes more than 3×/sec.
- **2.4.1 Bypass Blocks (A)** — provide a "Skip to main content" link.
- **2.4.3 Focus Order (A)** — Tab order matches visual/logical order.
- **2.4.4 / 2.4.9 Link Purpose (A/AAA)** — link text alone describes destination.
- **2.4.6 Headings and Labels (AA)** — descriptive, not generic.
- **2.4.7 Focus Visible (AA)** — keyboard focus has a visible indicator (never `outline: none` without a replacement).
- **🆕 2.4.11 Focus Not Obscured (Minimum) (AA)** — focused element is not fully hidden by other content (e.g., sticky headers).
- **🆕 2.4.12 Focus Not Obscured (Enhanced) (AAA)** — focused element is not hidden at all.
- **🆕 2.4.13 Focus Appearance (AAA)** — focus indicator ≥ 2 CSS px perimeter and ≥ 3:1 contrast against unfocused state.
- **2.5.1 Pointer Gestures (A)** — any multi-point or path-based gesture has a single-pointer alternative.
- **2.5.2 Pointer Cancellation (A)** — actions trigger on up-event, allowing abort by dragging off.
- **2.5.3 Label in Name (A)** — accessible name contains the visible label text.
- **2.5.4 Motion Actuation (A)** — any shake/tilt input has a UI alternative.
- **🆕 2.5.7 Dragging Movements (AA)** — anything achievable with a drag has a single-pointer click/tap alternative (e.g., a kanban card has a move button, not only drag-and-drop).
- **🆕 2.5.8 Target Size (Minimum) (AA)** — interactive targets ≥ **24×24 CSS px** (with spacing exceptions). Aim for 44×44 for real comfort.

### Principle 3 — Understandable `[WCAG]`
- **3.1.1 Language of Page (A)** — `<html lang="en">`.
- **3.2.1 On Focus (A)** & **3.2.2 On Input (A)** — no surprise context changes just from focus or input.
- **3.2.3 Consistent Navigation (AA)** — nav appears in the same relative order on every page.
- **3.2.4 Consistent Identification (AA)** — same function → same label/icon site-wide.
- **🆕 3.2.6 Consistent Help (A)** — if help mechanisms exist (contact info, chat, FAQ), they appear in the same relative location across pages.
- **3.3.1 Error Identification (A)** — errors described in text, not color alone.
- **3.3.2 Labels or Instructions (A)** — every input has a visible label.
- **3.3.3 Error Suggestion (AA)** — suggest a fix when known.
- **3.3.4 Error Prevention (Legal/Financial) (AA)** — reversible, checked, or confirmed.
- **🆕 3.3.7 Redundant Entry (A)** — information previously entered in the same session is auto-filled or selectable (don't make users retype email/address).
- **🆕 3.3.8 Accessible Authentication (Minimum) (AA)** — no cognitive function test (puzzles, memorizing passwords) unless there's an alternative: password manager support, copy-paste allowed, object/person recognition, biometric, etc.
- **🆕 3.3.9 Accessible Authentication (Enhanced) (AAA)** — same, but no object recognition either.

### Principle 4 — Robust `[WCAG]`
- **4.1.2 Name, Role, Value (A)** — all UI components expose name, role, state via the accessibility tree (native HTML or correct ARIA).
- **4.1.3 Status Messages (AA)** — toasts, form updates, loading changes announced via `role="status"` / `aria-live` without stealing focus.
- *(4.1.1 Parsing was removed in WCAG 2.2.)*

### WCAG 2.2: the new stuff in one table

| # | Criterion | Level | One-liner |
|---|---|---|---|
| 2.4.11 | Focus Not Obscured (Min) | AA | Focused element not fully covered |
| 2.4.12 | Focus Not Obscured (Enh) | AAA | Focused element not covered at all |
| 2.4.13 | Focus Appearance | AAA | Visible focus ring is thick + contrasty |
| 2.5.7 | Dragging Movements | AA | Provide a non-drag alternative |
| 2.5.8 | Target Size (Min) | AA | ≥ 24×24 CSS px |
| 3.2.6 | Consistent Help | A | Help in consistent location |
| 3.3.7 | Redundant Entry | A | Don't make me type it twice |
| 3.3.8 | Accessible Authentication (Min) | AA | No memory/puzzle tests required |
| 3.3.9 | Accessible Authentication (Enh) | AAA | Same + no object recognition |

---

## Part XIII — Testing & Iteration

- **Test with 3 users, monthly.** Beats 50 users once a year. `[DMMT]`
- **Testing proves problems, not absence of problems.** Qualitative signal is enough to drive fixes. `[DMMT]`
- **Three tasks per session**, concrete not exploratory ("Find the price of…", not "Browse around"). `[DMMT]`
- **Observers must watch live.** Seeing one user struggle rewires a team. `[DMMT]`
- **Debrief immediately.** Pick the top 3 problems, fix before next round. `[DMMT]`
- **Never blame the user.** Their failure is a design failure. `[UXB]`
- **Sample size rule of thumb**: obvious issues surface in 4–5 users; subtle issues need 30–40. `[UXB]`
- **Use both subjective and objective data**; interpretation is where UX lives. `[UXB]`
- **Recruit broadly when strict personas slow you down** — bad usability hurts everyone. `[DMMT]`
- **Prototype to learn, not to ship.** Low-fi on paper beats hi-fi in Figma. `[CBD]`
- **"How Might We..." framing** unlocks team brainstorming. `[CBD]`
- **Divergent before convergent.** Open the solution space first; narrow second. `[CBD]`

---

## Part XIV — The 60-Second Pre-ship Checklist

Before you call a screen done, walk through:

### Clarity
- [ ] Can a new user tell what this screen is within 5 seconds? `[DMMT]`
- [ ] Is the primary action the most prominent element? `[RUI]`
- [ ] Are labels descriptive, not generic ("Submit payment" not "Submit")? `[WCAG]`

### Hierarchy & layout
- [ ] Does weight/color carry hierarchy — not just size? `[RUI]`
- [ ] Is spacing from a fixed scale? `[RUI]`
- [ ] Is there whitespace to breathe, or does it feel cluttered? `[RUI]`

### Color
- [ ] Text contrast ≥ 4.5:1 (normal) / 3:1 (large)? `[WCAG]`
- [ ] UI/non-text contrast ≥ 3:1? `[WCAG]`
- [ ] Does anything rely on color alone to convey meaning? `[WCAG]`
- [ ] Tested in dark mode / low light / color-blind simulation? `[IOC]`

### Keyboard & focus
- [ ] Every control reachable by Tab? `[WCAG]`
- [ ] Focus ring visible everywhere, ≥ 3:1 contrast? `[WCAG]`
- [ ] Focus never hidden behind sticky chrome? `[WCAG]`
- [ ] No keyboard trap? `[WCAG]`

### Touch & pointer
- [ ] Tap targets ≥ 24×24 CSS px (prefer 44×44)? `[WCAG]`
- [ ] Any drag-only interaction has a click alternative? `[WCAG]`
- [ ] Any hover-only affordance has a tap alternative? `[DMMT]`

### Forms
- [ ] Every input has a visible label (not just placeholder)? `[WCAG]`
- [ ] Errors identified in text, with suggestion? `[WCAG]`
- [ ] No information re-entry required in the same session? `[WCAG]`
- [ ] Autocomplete attributes on standard fields? `[WCAG]`

### Semantics & screen reader
- [ ] Headings use `<h1>...<h6>` in order? `[WCAG]`
- [ ] `<html lang>` set? `[WCAG]`
- [ ] Interactive elements use native HTML or correct ARIA? `[WCAG]`
- [ ] Status messages announced without stealing focus? `[WCAG]`

### Mobile
- [ ] Reflows at 320 px wide with no horizontal scroll? `[WCAG]`
- [ ] Text resizes to 200% without clipping? `[WCAG]`
- [ ] Touch targets, thumb zones comfortable? `[DI]`

### Content & feedback
- [ ] Copy is human, jargon-free, action-oriented? `[UXB]`
- [ ] Every action gives immediate feedback? `[DI]`
- [ ] Empty states designed (not blank)? `[RUI]`
- [ ] All destructive actions reversible or confirmed? `[DI]`

### Research reality-check
- [ ] Did I talk to a real user about the last time this problem occurred? `[MOM]`
- [ ] Am I designing for what they actually do, or what I wish they'd do? `[MOM]`

---

## Appendix — Memorable Maxims

> "Hierarchy is the most effective tool you have for making something feel designed." — `[RUI]`

> "Don't make me think." — `[DMMT]`

> "Color is the most relative medium in art." — `[IOC]`

> "A successful prototype isn't one that works flawlessly; it's one that teaches us something." — `[CBD]`

> "Opinions are worthless. People know their problems, not the solution." — `[MOM]`

> "Design is how it works. It's something you can prove." — `[UXB]`

> "Fail early to succeed sooner." — `[CBD]`

> "There's more information in a 'meh' than a 'Wow!'" — `[MOM]`

---

*Last compiled: 2026-04-19 — from the PDFs in `ui/`, extracted via `scripts/read_pdf.py` to `ui/*_extracted/*.md`. Update this file when new reference material is added.*
