# Diagram style (user rule, 2026-11-05)

When the user asks to draw or show an architecture/flow, answer **directly in the chat** with a plain-ASCII diagram inside a
```text fence, so it renders aligned in the terminal:

- Boxes with `+`, `-`, `|` and `=` only; arrows `->`, `<-`, `v`, `^`. No Unicode box characters (they misalign).
- Labels inside boxes in English without diacritics (Vietnamese accents break column alignment); explanations in Vietnamese
  go outside the fence.
- Keep the width at or below about 90 columns; one diagram per view (system, network, data flow), each in its own fence.
- Status tags in brackets: `[OK]` measured/bench, `[SIM]` simulation only, `[--]` not built; explain the tags once above.
- Do not create a separate .md file for a drawing unless the user asks; when a design document needs the figure, put the same
  ASCII block in that document.
