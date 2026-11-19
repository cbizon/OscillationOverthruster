# Instructions

One file per day, `YYYY-MM-DD.md`, written by the daily debrief after the
scientist approves it, dated by the evening the night starts. Old
instructions stay as the record of how the program was steered.

The night runs only the lines the instruction has a section for (and lines
with open challenges from the checker). Each line's section is headed with
its id and name, and has two parts:

```
Anything here, above the first line, applies to every line.

## L0013 Phase diagram

### Asked
1. ...

### Details
- ...
```

- `### Asked`: a numbered list of what the scientist asked for this line,
  in the scientist's own words. The run answers each item as it was asked,
  and the checker and the next debrief hold it to that wording.
- `### Details`: how to carry the items out, written by the debrief for the
  agent. Details add to what was asked; they don't narrow it.

A day with no instruction runs only lines with open challenges.
