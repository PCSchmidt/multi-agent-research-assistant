# MEMORY_CORRECTIONS.md
# Reflexion entries and calibration data

## Calibration Multiplier
Current: 2.0x (default - fewer than 3 estimation entries)

## REFLEXION Entries
(Newest first - what worked, what didn't, pattern updates)

### 2026-05-09 - v0.1 MOCKUPS APPROVED (Gate Close)
**What worked:**
- Mid-gate aesthetic pivot executed cleanly (user requested elevated vibe)
- No rework needed - pivot happened before implementation
- Design system comprehensive: colors, typography, spacing, animations, icons all locked
- Esoteric aesthetic landed well: alchemical glyphs, academic luxury, ceremonial pacing
- Wireframes covered all 10 screens (chat, auth, settings, error states)

**What didn't work / What to improve:**
- None - clean gate close

**Pattern updates:**
- This user values aesthetic direction early - "speak to exclusivity, elite, expensive"
- Symbolic design choices (alchemical glyphs vs generic icons) resonate
- User prefers confident design decisions over asking permission for minor choices
- Academic/scholarly reference frames work well (CERN, rare manuscripts, quantum labs)

**Calibration insight:**
- Design gates can handle mid-stream aesthetic pivots without timeline impact
- Estimate held (6h actual vs 6-10h estimated) despite direction change
- Clear design philosophy statement upfront saves iteration time

### 2026-05-09 - v0.0 SCOPE CONFIRMED (Gate Close)
**What worked:**
- User's comprehensive build plan saved ~1h of clarifying questions
- BYOK scope addition came during scope phase (perfect timing, no rework)
- 17-gate roadmap with tight ranges on near-term gates, wider on uncertain later gates
- Decision log captured 7 architectural choices with clear rationale
- Came in under estimate (3.5h actual vs 4-6h estimated)

**What didn't work / What to improve:**
- None - clean gate close

**Pattern updates:**
- This user prefers detailed upfront planning docs over iterative refinement
- Cost control (BYOK) is a priority - ask early on future projects
- Multi-provider support preferred over single-provider lock-in

**Calibration insight:**
- Scope phase went faster than estimated due to comprehensive prep
- Apply this learning: when user provides detailed spec upfront, reduce scope estimate by ~20%

### 2026-05-09 - Project Start
**What worked:**
- User provided comprehensive build plan document upfront
- All prerequisite setup completed before /start (API keys, Supabase, GitHub repo)
- Scope is clear and locked - minimal clarifying questions needed

**What to watch:**
- OpenAI API key is currently OpenRouter - needs replacement before embeddings gate
- This is the first multi-agent LangGraph build - estimate confidence is lower than usual

## ESTIMATION Entries
(Newest first - gate close calibration data)

Format:
```
### GATE: <version> <name>
Estimated: <hours>
Actual: <hours>
Variance: <percentage>
Driver: <what caused the variance>
```

### GATE: v0.1 MOCKUPS APPROVED
Estimated: 6-10h (midpoint 8h)
Actual: 6h
Variance: -25% (under estimate, hit low end of range)
Driver: Mid-gate aesthetic pivot (clean → esoteric luxury) but no rework needed. Design system creation went smoothly. Wireframes comprehensive but efficient (ASCII, not high-fidelity). User's clear vision ("exclusive, elite, esoteric") saved iteration time.

### GATE: v0.0 SCOPE CONFIRMED
Estimated: 4-6h (midpoint 5h)
Actual: 3.5h
Variance: -30% (under estimate)
Driver: User provided comprehensive build plan upfront, eliminating ~1h of clarifying questions and scope iteration. BYOK addition was clean (no rework needed since it came during scope phase).
