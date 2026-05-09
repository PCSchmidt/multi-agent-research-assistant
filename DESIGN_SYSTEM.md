# DESIGN_SYSTEM.md
# Visual Design System

Design system for multi-agent-research-assistant. Portfolio-grade production UI targeting technical reviewers.

---

## Design Principles

1. **Scholarly Exclusivity** - Interface conveys rare, high-value research capability
2. **Quiet Authority** - Confidence without noise, sophistication without flash
3. **Depth over Surface** - Layered information architecture, esoteric detail accessible to the initiated
4. **Academic Luxury** - Premium materials, generous spacing, typographic refinement
5. **Observability as Ritual** - Agent pipeline visible as a ceremonial process, not just a progress bar

---

## Color Palette

**Philosophy:** Deep, rich, academic tones. Dark surfaces with high-value accent colors suggesting rare materials (gold leaf, aged parchment, quantum interference patterns).

### Core Colors
```
Primary (Rare knowledge, active discovery)
- primary-50:  #FEF3E7  (Aged parchment highlight)
- primary-100: #F9E4C8
- primary-500: #D4A574  (Antique gold - main accent)
- primary-600: #B8935F
- primary-900: #6B5334  (Deep bronze)

Success (Validated knowledge, high confidence)
- success-500: #7C9885  (Oxidized copper patina)
- success-600: #5A7A65

Warning (Uncertain territory, low confidence)
- warning-500: #C9A961  (Amber - rare finding flag)
- warning-600: #A88B4F

Error (Contradiction, failed hypothesis)
- error-500: #A05A52  (Faded vermillion)
- error-600: #8B4A43

Neutral (Foundation, scholarly depth)
- neutral-50:  #F5F3F0  (Off-white, natural paper)
- neutral-100: #E8E5E0
- neutral-200: #D1CCC4
- neutral-300: #9B9388  (Graphite)
- neutral-500: #6B6358  (Charcoal)
- neutral-700: #3D3832  (Soot)
- neutral-800: #252118  (Deep slate)
- neutral-900: #0F0D0A  (Near-black, ink)
```

### Semantic Colors (Light Mode - Default)
```
Background:     neutral-50   (#F5F3F0 - Natural paper)
Surface:        #FDFCFB      (Warm white, cream)
Surface Elevated: rgba(212, 165, 116, 0.08)  (Subtle gold wash)
Border:         neutral-200  (#D1CCC4 - Subtle divide)
Border Accent:  primary-500  (#D4A574 - Gold accent lines)
Text Primary:   neutral-900  (#0F0D0A - Ink)
Text Secondary: neutral-500  (#6B6358 - Faded)
Text Tertiary:  neutral-300  (#9B9388 - Ghost text)
Link:           primary-600  (#B8935F)
Link Hover:     primary-900  (#6B5334)
```

### Scholarly Dark Mode (Optional, v1.0+)
```
Background:     neutral-900  (#0F0D0A - Deep study)
Surface:        neutral-800  (#252118 - Elevated surface)
Border:         neutral-700  (#3D3832)
Text Primary:   neutral-50   (#F5F3F0)
Accent:         primary-500  (#D4A574 - Gold glow)
```

### Agent Status Colors (Esoteric Symbolism)
```
Planner (Hypothesis, ancient wisdom):
  - Color: #7B68A6  (Deep amethyst - philosophers' stone)
  - Symbol: Alchemical sulfur ☉

Retriever (Excavation, archeological dig):
  - Color: #8B7355  (Sienna - ancient clay tablets)
  - Symbol: Magnifying lens over codex 🔍

Critic (Peer review, rigorous scrutiny):
  - Color: #A05A52  (Vermillion seal - scholar's mark)
  - Symbol: Quill striking through ✗

Synthesizer (Synthesis, unification):
  - Color: #7C9885  (Verdigris - aged copper, connections forming)
  - Symbol: Interlinked rings ∞

Evaluator (Validation, measurement):
  - Color: #C9A961  (Gold standard, metric authority)
  - Symbol: Precision scale ⚖

Active:      Full saturation + subtle glow (2px shadow)
Completed:   Desaturated + 60% opacity (faded into archive)
Pending:     neutral-300 (dormant, awaiting)
```

---

## Typography

**Philosophy:** Academic authority through typographic refinement. Serif for authority, mono for precision.

### Font Stack
```css
Serif (Headings, authority):    'Crimson Pro', 'Spectral', 'Iowan Old Style', 'Palatino Linotype', serif
Sans-serif (UI, readability):   'Inter', 'SF Pro Text', system-ui, sans-serif
Monospace (citations, data):    'IBM Plex Mono', 'Söhne Mono', 'Berkeley Mono', monospace
Ancient/Symbolic (optional):    'Noto Serif', 'EB Garamond' (for esoteric headings)
```

### Type Scale (Generous, authoritative)
```
Display (Hero sections):         56px / 3.5rem, font-light (300), neutral-900, Crimson Pro
Heading 1 (Page titles):         40px / 2.5rem, font-normal (400), neutral-900, Crimson Pro
Heading 2 (Major sections):      32px / 2rem, font-normal (400), neutral-700, Crimson Pro
Heading 3 (Subsections):         24px / 1.5rem, font-medium (500), neutral-700, Crimson Pro
Body Large (Primary content):    18px / 1.125rem, font-normal, neutral-900, Inter
Body (Default):                  16px / 1rem, font-normal, neutral-900, Inter
Small (Metadata, annotations):   14px / 0.875rem, font-normal, neutral-500, Inter
Tiny (Labels, micro):            11px / 0.6875rem, font-medium, uppercase, tracking-wide, neutral-500

Line height: 1.7 (body - generous for readability), 1.2 (headings)
Letter spacing: -0.02em (headings, tight), 0.05em (uppercase labels)
```

### Font Weights
```
Light:       300 (Display headings, quiet authority)
Normal:      400 (Body, natural reading)
Medium:      500 (UI emphasis, subheadings)
Semibold:    600 (Rare, only for critical CTAs)
Bold:        700 (Avoided - use size/color for hierarchy instead)
```

### Typographic Details
```
Drop caps:         First letter of long-form content (72px, Crimson Pro)
Small caps:        Proper nouns in body text (font-variant-caps: small-caps)
Ligatures:         Enabled for serif fonts (ff, fi, fl)
Quotation marks:   Typographic quotes " " ' ' (not straight quotes)
Em dash:           — (proper em-dash for parenthetical)
Ellipsis:          … (not three periods)
```

---

## Spacing Scale

**Philosophy:** Generous breathing room = luxury. Based on 8px base unit (more spacious than standard 4px).

```
0:   0px
1:   8px    (tight inline elements)
2:   16px   (component internal padding)
3:   24px   (component spacing)
4:   32px   (section dividers)
6:   48px   (major section breaks)
8:   64px   (page-level margins)
12:  96px   (hero section spacing)
16:  128px  (dramatic separation)
```

### Layout Grid
```
Max content width:   1440px (wider canvas for authority)
Reading width:       720px (optimal for long-form content)
Sidebar width:       400px (source panel - room for detail)
Gutter:              48px (generous column separation)
Page margins:        64px horizontal, 48px vertical (breathing room)
```

### Rhythm & Vertical Spacing
```
Baseline grid:       8px
Paragraph spacing:   32px (1.7 line-height × 16px + 4px)
Section spacing:     64px
Chapter spacing:     128px (dramatic breaks between major sections)
```

---

## Component Patterns

**Philosophy:** Refined materials, subtle affordances, premium feel. Less "web app" more "rare archive interface."

### Cards (Research Panels)
```
Background:   Surface (#FDFCFB) with subtle texture (paper grain, 2% opacity)
Border:       1px solid primary-500/20 (gold accent, very subtle)
Border Top:   2px solid primary-500 (signature accent line)
Radius:       2px (minimal rounding, architectural)
Padding:      32px (generous internal space)
Shadow:       0 4px 24px rgba(15,13,10,0.08), 0 1px 4px rgba(15,13,10,0.04)  (elevated, soft)
Hover:        Subtle lift (transform translateY(-2px)), shadow intensifies
```

### Buttons

**Primary (Discovery actions - "Submit Query")**
```
Background:   linear-gradient(135deg, primary-600, primary-500)  (Gold gradient)
Text:         neutral-900 (dark text on gold, high contrast)
Font:         14px, medium, uppercase, tracking-wide
Padding:      16px 40px (substantial, confident)
Radius:       2px (architectural)
Border:       1px solid primary-900/30 (definition)
Hover:        Brightness increase, subtle scale (1.02)
Active:       Inset shadow (pressed)
Icon:         24px, right-aligned (→ arrow, suggesting forward motion)
```

**Secondary (Refinement actions - "Filter", "Adjust")**
```
Background:   transparent
Text:         neutral-700
Border:       1px solid neutral-300
Font:         14px, medium, normal case
Padding:      14px 32px
Hover:        Border → primary-500, text → primary-700
```

**Ghost (Subtle actions - icon-only controls)**
```
Background:   transparent
Text/Icon:    neutral-500
Padding:      8px (icon only, 24px icon size)
Hover:        Background → primary-500/10, icon → primary-600
```

### Inputs (Query field, settings)
```
Background:   Surface with 1px inset shadow (recessed feel)
Border:       1px solid neutral-200
Border Bottom: 2px solid neutral-300 (weighted base)
Radius:       2px
Padding:      16px 20px (generous touch targets)
Font:         16px Inter (body size for readability)
Focus:        Border bottom → 2px solid primary-500
              Subtle glow: 0 0 0 4px primary-500/10
Placeholder:  neutral-400, italic
```

### Badges (Eval scores, status indicators)
```
Shape:        Rounded rectangle (4px radius, not fully rounded)
Padding:      6px 14px
Font:         11px, medium, uppercase, tracking-wide
Border:       1px solid (matching background color, darker shade)
Background:   Semi-transparent (agent color at 15% opacity)
Text:         Agent color at full saturation
Icon:         12px, left-aligned (● for status, ✓/✗ for pass/fail)
```

### Dividers
```
Horizontal:   1px solid neutral-200, centered with ornamental mark (⬥ in primary-500)
Vertical:     1px solid neutral-200/60 (subtle column separation)
Section:      64px margin top/bottom, ornamental divider optional
```

---

## Animation & Transitions

**Philosophy:** Slow, deliberate, ceremonial. Research is a process, not instant gratification.

### Timing
```
Instant:  0ms     (Avoid - nothing should be instant)
Fast:     200ms   (Hover acknowledgment, micro-feedback)
Normal:   400ms   (Modal entry, panel slides)
Slow:     800ms   (Page transitions, agent node activation)
Ritual:   1200ms  (Full pipeline visualization, dramatic reveals)

Easing:   cubic-bezier(0.25, 0.46, 0.45, 0.94)  (Refined ease-out, confident deceleration)
```

### Streaming Content (The Ritual of Discovery)
```
Streaming text:
  - Cursor: Slow blink (1.2s interval, fade in/out 400ms)
  - Text reveal: Character-by-character with subtle fade-in (20ms per char)
  - Line completion: Subtle underline slide-in (400ms) to mark completed thought

Agent progress:
  - Activation: Glow pulse (3s loop, breathing rhythm)
  - Completion: Fade to muted + checkmark slide-in from left (600ms)
  - Connection lines: Draw from completed node to next (800ms, stroke-dashoffset)

Loading states:
  - Skeleton: Subtle shimmer (2.5s linear, slow sweep)
  - Spinner: Slow rotation (2s per revolution, not frantic)
  - Progress bar: Smooth fill with gradient leading edge (no choppy steps)
```

### Micro-interactions
```
Citation hover:     Gentle lift (translateY(-1px), 200ms) + gold underline thickens
Source panel open:  Slide from right (600ms) with backdrop fade-in (400ms)
Agent node active:  Gentle scale pulse (1.0 → 1.05 → 1.0, 3s loop)
Eval badge appear:  Fade up from bottom (600ms) with slight overshoot (spring)
```

---

## Iconography

**Philosophy:** Esoteric symbolism, academic marks, alchemical glyphs. Custom or carefully sourced.

### Icon Set
**Custom SVG glyphs** inspired by alchemical symbols, academic notation, quantum diagrams
Fallback: **Phosphor Icons** (duotone for depth, thin stroke for refinement)

### Icon Sizes
```
Micro:   12px  (Inline notation marks)
Small:   16px  (Inline with body text)
Medium:  24px  (UI controls, agent nodes)
Large:   40px  (Section headers, major actions)
Hero:    72px  (Empty states, ceremonial moments)
```

### Agent Node Glyphs (Custom/Symbolic)
```
Planner (Hypothesis):
  - Glyph: Alchemical sulfur ☉ or Eye of Providence △
  - Style: 24px, stroke weight 1.5px, primary-500
  - Meaning: Vision, foresight, initial spark

Retriever (Excavation):
  - Glyph: Ouroboros fragment 🜔 or Ancient scroll 📜
  - Style: 24px, sienna tone
  - Meaning: Unearthing, recovery, archeological precision

Critic (Scrutiny):
  - Glyph: Crossed quills ✗ or Scholar's seal 🔏
  - Style: 24px, vermillion
  - Meaning: Peer review, rigorous validation

Synthesizer (Unification):
  - Glyph: Borromean rings ⚭ or Conjunction symbol ☌
  - Style: 24px, verdigris
  - Meaning: Synthesis, connection, emergence

Evaluator (Measurement):
  - Glyph: Precision balance ⚖ or Phi ratio φ
  - Style: 24px, gold
  - Meaning: Metric authority, validation
```

### UI Icons (Refined, minimal)
```
Citation:         Superscript in brackets [¹] (old-style numerals if available)
Source:           Manuscript leaf 🍂 or Codex pages
User query:       Quill feather ✒
AI response:      Constellation ✦ (not sparkles - more timeless)
Settings:         Astrolabe or Gear (precision mechanism)
Search:           Loupe (antique magnifying glass)
Close:            × (thin, refined stroke)
Expand:           ⌄ (chevron, subtle)
External link:    ↗ (arrow, understated)
```

### Ornamental Marks
```
Section divider:   ⬥ (diamond, centered)
List bullets:      • (en-dash –, not dot)
Footnote:          * † ‡ (traditional academic marks)
Ellipsis:          … (proper ellipsis character)
```

---

## Responsive Breakpoints

```
Mobile:   < 640px   (sm)
Tablet:   ≥ 640px   (md)
Desktop:  ≥ 1024px  (lg)
Wide:     ≥ 1280px  (xl)
```

### Layout Behavior
```
Mobile:   Single column, collapsible source panel (modal)
Tablet:   Two columns (chat + timeline), source panel overlays
Desktop:  Three columns (chat | timeline | source panel)
```

---

## Accessibility

### Contrast Ratios
```
Normal text:  4.5:1 minimum (WCAG AA)
Large text:   3:1 minimum
UI elements:  3:1 minimum
```

### Focus States
```
Visible focus ring: 2px solid primary-500, 2px offset
Skip to main content link (keyboard users)
ARIA labels on all interactive elements
```

### Screen Reader
```
Agent status announced on change
Streaming content marked as aria-live="polite"
Citations linked to sources with aria-describedby
```

---

## Dark Mode (Deferred to post-v1.0)

Color inversions noted for future implementation:
- Background: neutral-900
- Surface: neutral-800
- Text: neutral-100
- Borders: neutral-700

---

**Design system established:** 2026-05-09  
**Next:** FRONTEND_SPEC.md (component hierarchy and state patterns)
