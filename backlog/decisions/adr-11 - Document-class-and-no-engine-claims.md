---
id: ADR-11
status: accepted
date: 2026-11-21
---

# ADR-11: Deliver a document class, and claim no engine until it is tested

## Context

SPEC-LTX had to choose between a document class, a style package, and a set of components, and had to decide what may be claimed about engines and editors.

The verified rules in SPEC-SOURCE constrain the document as a whole: page geometry (SRC-001–SRC-003), body and heading typography (SRC-002, SRC-004–SRC-006), paragraph form (SRC-007), page numbering (SRC-008), front-matter order (SRC-010), title-page fields (SRC-012), and caption geometry (SRC-015–SRC-019). Separately, the only engine ever executed in this repository is Tectonic, and only against a dummy main that does not use any class.

## Decision

1. Ship **one document class**, `umcswnozigp.cls`, as the public surface. Internal files may be split later; the public interface stays one class and one option list.
2. Require the `cycle` option explicitly rather than defaulting it, because the three thesis types have different structural expectations.
3. Fix caption placement and float counters in the class rather than leaving them to the author, since the rules fix them.
4. Treat Tectonic's CI smoke build as evidence about the **build pipeline only**. It is not evidence of class compatibility.
5. **Claim no supported engine.** pdfLaTeX, LuaLaTeX and XeLaTeX are candidates; each becomes supported only after TASK-8 runs the class on it and records the result.
6. **Claim no editor compatibility.** Overleaf stays untested and unadvertised until a clean import test exists.
7. Record the Times New Roman tension openly: SRC-002 names a proprietary font, so every engine choice involves either requiring that font or substituting a metric-compatible clone.

## Consequences

- TASK-9 implements against a written API instead of inventing one.
- No release note or README may describe the class as working on a named engine or editor until the corresponding test is recorded.
- The font substitution question is a blocking open question in SPEC-LTX rather than a footnote, because it changes glyph metrics and therefore page breaks.
- If Annexes 1–5 (SRC-041) show a layout the class cannot express, the class changes; the specification does not get bent around an implementation.
