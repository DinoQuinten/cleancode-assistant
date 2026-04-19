---
name: user-research
description: Generates Mom-Test-compliant user interview plans, drafts screener questions, reviews planned questions for "bad data" signals (compliments/fluff/ideas), and analyzes interview notes to extract real signals (pain, commitments, workarounds) from noise. Auto-activates on "write interview questions", "plan user interviews", "review my questions", "analyze user interview notes", "talk to users", or /uix:user-research. Grounded in The Mom Test + UX for Beginners.
argument-hint: "[plan | review | analyze] [topic]"
version: 0.1.0
allowed-tools: Read, Grep, Write
---

# user-research

Coach the user through Mom-Test-compliant user research. Auto-activates on interview/research queries or via `/uix:user-research`.

## Triggers

"write interview questions" · "plan user interviews" · "interview guide" · "discovery questions" · "review my questions" · "analyze interview notes / transcript" · "customer conversation" · "talk to users about [topic]" · "validate [idea] with users".

## Process

Three modes — detect which one from the user's message:

- Topic / problem space only → **Mode A** (plan).
- A list of draft questions → **Mode B** (review).
- Raw notes / transcript / interview bullets → **Mode C** (analyze).
- If ambiguous, ask one clarifying question before proceeding.

### Mode A — Plan interviews
Input: topic / product idea / problem space.

Output:
```
## Interview plan — <topic>

### Goal (one line)
What you need to learn — not confirm.

### Top 3 learning questions (the ones you're scared to ask)
1. ...
2. ...
3. ...

### Who to talk to
- Persona or segment · where to find them · how to recruit · screener.

### Interview guide (30-45 min)
Warm-up (3 min) — casual rapport; don't mention your idea yet.

Their life & current workflow (15 min)
- "Talk me through the last time <problem> happened."
- "Why do you bother?"
- "What have you already tried to fix this?"
- "How are you dealing with it now?"
- "What are the implications when it goes wrong?"

Pain and priority (10 min)
- "Where does the money come from for <workflow>?"  (B2B)
- "How often does this happen?"
- "What else is competing for your time / budget?"

Advance the ball (5-10 min) — optional idea reveal
- Only reveal your idea if it emerges naturally or near the end.
- Push for a commitment: time, reputation, or cash (next meeting · intro · LOI · trial).

Close (2 min)
- "Is there anything I should have asked?"
- "Who else should I talk to?"

### Note-taking symbols
⚡ pain · 🎯 goal · ☐ obstacle · ⤴ workaround · ☑ feature request · ＄ money · ♀ person · ☆ follow-up.

### Before you start — Mom-Test self-check
- [ ] Not fishing for compliments.
- [ ] All questions ask about past, not future.
- [ ] Not pitching unless explicitly asked.
- [ ] Pressing for a commitment at the end.
```

### Mode B — Review draft questions
Input: the user's draft question list.

For each question:
- **PASS / FLUFF / LEADING / HYPOTHETICAL / COMPLIMENT-BAIT / PITCH-TRAP**
- If not PASS, rewrite it.

Tag the common failures from `${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part II:
- **Hypothetical** ("Would you use...") → rewrite to past-tense ("Tell me about the last time...").
- **Opinion** ("Do you think...") → rewrite to behavior ("What did you do when...").
- **Compliment bait** ("Isn't this cool?") → remove or reframe.
- **Leading** ("Don't you hate when...") → rewrite neutrally.
- **Fluff generator** ("I usually..." follow-ups) → anchor to a specific past instance.

Output:
```
## Question review

| # | Original | Verdict | Rewrite |
|---|---|---|---|
| 1 | ... | FLUFF | ... |

### General fixes
- ...
- ...

### Missing questions you should add
- ...
```

### Mode C — Analyze interview notes
Input: raw notes, transcript excerpts, or bullet summaries from an interview.

Output:
```
## Interview analysis — <interviewee>

### Real signals (high-trust — rooted in past behavior or commitments)
- ⚡ Pain: ...
- 🎯 Goal: ...
- ⤴ Current workaround: ...
- ＄ Money / time cost: ...
- Commitment observed: [time / reputation / cash] — ...

### Suspect signals (fluff, opinions, hypotheticals — downweight these)
- Compliment: "..." — discount.
- Hypothetical: "..." — needs past-tense anchor.
- Feature request: "..." — dig: what problem?

### Priority score (subjective)
- Pain frequency: high / medium / low
- Pain severity: high / medium / low
- Current workaround cost: $ / hour / frustration score

### Gaps / next questions
- What I still don't know: ...
- Follow-up interview should ask: ...

### Product/UX implications
- If the signal holds across N interviews, this changes: [feature / flow / messaging].
- Nothing should change yet if N = 1. Quote this person, don't generalize from them.
```

## Ground rules

- Never replace specific past-tense questions with generic future-tense ones.
- Compliments and feature requests are not validation — downweight ruthlessly `[MOM]`.
- A research finding from one user is a hypothesis, not a decision. Say so.
- Don't design on interview output alone — triangulate with analytics or usability testing.
- Remember: a meeting without a clear next step was pointless. Always push for a commitment.

## Reference

`${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part II (Talk to users) has the full question playbook and bad-data signals.
