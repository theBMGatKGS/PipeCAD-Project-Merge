# Changelog

## 00.01.001 (2026-10-12)
Redesign. Merge logic, merged output and design check are unchanged (verified byte-for-byte against 00.01.000, `tools/verify_merge.py` PROBLEMS 0).
- On-screen "underground" dark mode; sticky step bar (Add · Order · Names · Download · Check) with per-step status.
- Drag rows to reorder files; the first file is pinned as the header (↑/↓ kept for keyboard use).
- One rename table for repeated names, floor/detector renames and pipe-run renames, with **Leave all** / **Number all**.
- Side panel: merged file name, **Download** with the reason when it is disabled, and grouped must-fix (red) / review (yellow) messages that jump to their item.
- PASS/FAIL strip with a Print / Save .html / Save .csv group.
- Printed and saved difference report in the KGS palette (navy #102645, red #AC242A, light blue #0C77BC, neutrals, PASS green #1b7a3a) with summary tiles.
- `.superdesign/` working files are git-ignored.

## 00.01.000 (2026-10-12)
See README "Versions".
