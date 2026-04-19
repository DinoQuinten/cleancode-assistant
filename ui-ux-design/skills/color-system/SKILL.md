---
name: color-system
description: Builds a complete UI color palette — 8-10 grey shades, 1-2 primary hues with 5-10 shades each, accent colors for success/warning/danger/info — following Refactoring UI's HSL method plus Albers's relativity and Colour and Light's luminance rules. Auto-activates on "build a color palette", "design a color system", "pick UI colors", "how many shades do I need", "should I use this color", "dark mode palette", or /uix:color-system. Outputs palette with HSL values, contrast ratios, and usage rules.
argument-hint: "[brand / domain / style hint]"
version: 0.1.0
allowed-tools: Read, Grep, Write
---

# color-system

Architect UI color systems. Auto-activates on palette questions or via `/uix:color-system`.

## Triggers

"build a color palette / color system" · "pick UI colors" · "how many shades do I need" · "primary color for [product]" · "grey scale" · "dark mode palette" · "accent / semantic colors (success/warning/danger)" · "is this color accessible" · "tint my greys".

## Process

1. **Gather constraints in one pass:**
   - Brand personality (professional / friendly / aggressive / luxury / playful)
   - Domain (fintech / healthcare / social / dev-tool / e-commerce / media)
   - Existing brand color(s) — hex or HSL
   - Light mode only, dark mode only, or both
   - Accessibility target (assume WCAG AA unless user says otherwise)

   Ask the minimum clarifying questions if any of the above are missing.

2. **Output a palette in this format:**
   ```
   ## Color System — <project>

   Built in HSL. All shades hand-tuned for perceptual steps — NOT linearly generated `[RUI]`.

   ### Greys (8-10 shades)
   Tint: warm / cool / neutral — why.
   | Token | HSL | Hex | Use |
   |---|---|---|---|
   | grey-50 | hsl(220 20% 98%) | #F8FAFC | App background |
   | grey-100 | ... | ... | Card background |
   | ... | ... | ... | ... |
   | grey-900 | ... | ... | Primary text |

   ### Primary — <ColorName>
   Base hue: H°. Matched saturation range. 10 shades.
   | Token | HSL | Hex | Use |
   |---|---|---|---|
   | primary-50 | ... | ... | Lightest background |
   | primary-500 | ... | ... | Base (brand color) |
   | primary-600 | ... | ... | Hover state |
   | primary-700 | ... | ... | Active/pressed state |
   | primary-900 | ... | ... | On-dark text |

   ### Accent — <ColorName> (optional second primary)
   Same structure.

   ### Semantic
   | Role | Light | Dark | Contrast pair |
   |---|---|---|---|
   | Success | green-600 | green-400 | on white / on grey-900 |
   | Warning | amber-600 | amber-400 | ... |
   | Danger | red-600 | red-400 | ... |
   | Info | blue-600 | blue-400 | ... |

   ### Contrast audit (WCAG 2.2 AA)
   Example row: `grey-900 (#0F172A) on grey-50 (#F8FAFC) = 18.1:1 — Pass AA`.
   - Body text on app-bg: [ratio] — Pass AA (≥4.5) `[WCAG SC 1.4.3]`
   - Subtle text on card-bg: [ratio] — Pass AA `[WCAG SC 1.4.3]`
   - Primary button label on primary-600: [ratio] — Pass AA `[WCAG SC 1.4.3]`
   - Focus ring on app-bg: [ratio] — Pass (≥3:1) `[WCAG SC 1.4.11]`
   - Any FAIL flagged with a fix.

   ### Usage rules
   - Primary text: grey-900 on grey-50; never grey-400 on grey-100.
   - Don't use grey text on colored backgrounds — pick contrasting colors that fit the hue `[RUI]`.
   - Color never carries meaning alone — always pair with icon or label `[WCAG SC 1.4.1]`.
   - Don't use pure #000 or #FFF — use grey-900 and grey-50 for natural surfaces `[C&L]`.
   - Shadows take the complement of the light source, tinted subtly `[C&L]`.

   ### Dark mode (if requested)
   Shift all colors by the same rule (color constancy) `[IOC]`. Reduce saturation for glowing elements. Desaturate primary by 10-20% in dark mode to prevent vibration.
   ```

3. **Follow these rules when generating shades:**
   - Work in HSL so lightness is perceptual.
   - Saturation scales non-linearly — dip saturation at mid-lightness, boost at extremes.
   - Greys with a 220° hue and 10-20% saturation read as "cool neutral"; 30° hue and similar saturation reads as "warm neutral".
   - Don't just darken/lighten a single hue linearly — adjacent hue shifts (warmer for highlights, cooler for shadows) look more natural `[C&L]`.
   - Test every color on its intended background — relativity rules `[IOC]`.

4. **If the user provides an existing brand color**, treat it as primary-500 and build the rest around it.

5. **Always run the contrast audit** and fix any failing pair before delivering.

## Ground rules

- No on-the-fly color invention in components — every shade is pre-defined here.
- Value contrast (luminance) is primary; hue contrast is secondary `[IOC][C&L]`.
- Don't rely on color alone for status — pair with icons `[WCAG SC 1.4.1]`.
- When in doubt, fewer shades > more. 8 greys and 7 primary shades beats 14 and 14.
- Never recommend a color system without a contrast check.

## Reference

`${CLAUDE_PLUGIN_ROOT}/references/UI_MASTER_GUIDE.md` Part VII (Color) and Part VIII (Depth, Light, Shadows).
