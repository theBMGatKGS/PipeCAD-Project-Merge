# PipeCAD Project Merge

ModuLaser Tools · **v00.00.001** (2026-10-09)

Combines several PipeCAD `.pl` project files into one `.pl` that opens in PipeCAD with the design unchanged.
For example, separate files for each floor or building can be merged into one project.
It is an installable, offline-capable web app (PWA). Everything runs in the browser and no file is uploaded.

Live: https://thebmgatkgs.github.io/PipeCAD-Project-Merge/ (GitHub Pages from `main`, root).
A Windows `.exe` (Electron) build is planned.

## Use
1. Pick or drop two or more `.pl` files.
2. Order them. The **first** file supplies the project header: project details, units, pipe type, default options and snap grid.
3. Review the floors and detectors. Edit any renamed floor or detector if you want a different name.
4. Click **Download merged .pl** and open the file in PipeCAD.

## What the merge changes and what it keeps
- **The design is copied unchanged.** That covers every floor, detector, pipe run, sampling hole, end cap, T-piece, outline, label and saved PipeCAD result.
- **IDs.** PipeCAD numbers each file's detectors, pipes and holes from 0, and its saved results refer to them by:
  - `detectorId`
  - the `<int>` lists under `objectsList`: `pipeIds`, `holeIds`, `ancillaryIds`, and each T-piece's `pipeDatabase1/2` and `holeDatabase1/2`.

  Each later file shifts all of these, plus its `layerTag` tree numbers, by one offset, so nothing collides. A `0` in those lists is an empty slot and is left as is. Bend, socket and clip counts are never touched.
- **Names.** Only names that clash with an earlier file change:
  - Detectors continue their own numbering: `MASD 01 → MASD 05`, `MASD 1-2 → MASD 1-7`, `Detector → Detector 2`.
  - Floors keep their description: `Area A → Area B`, `Floor 1 → Floor 2`, otherwise `Name (2)`.
  - Pipe names belong to their detector and never clash.
- **Refused:** files in different units, or with a different pipe bore or material, because their airflow results would change.
- **Flagged:** a different stick length, OD or part number. PipeCAD keeps one pipe type per project, so socket counts and part numbers follow the first file's pipe if PipeCAD recalculates.
- **Version.** The merged file is marked with the newest PipeCAD version among the inputs.
- **Output format** matches PipeCAD's own: XML declaration, indentation, `<Tag />` empty elements and CRLF line endings.

## Checking a merge
```
python3 tools/verify_merge.py merged.pl source1.pl source2.pl ...
```
This compares every floor and saved result with its source after undoing the offsets. `PROBLEMS 0` means nothing changed apart from the listed renames.

Validated on six real PipeCAD 3.5.0.132 / 3.6.2.139 projects (49 detectors, 17 floors), and the merged files were opened in PipeCAD.
`.pl` files are client data and are git-ignored.

## Versions
`vMM.mm.rrr`. Releases are tagged by hand in GitHub.
- **00.00.001** (2026-10-09): first release. Merge, rename review and edit, pipe/unit checks, PWA install and offline use.
