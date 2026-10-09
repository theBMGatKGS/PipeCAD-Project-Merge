# PipeCAD Project Merge

ModuLaser Tools · **v00.00.001** (2026-10-09)

Combines several PipeCAD `.pl` project files into one `.pl` that opens in PipeCAD with the design unchanged.
For example, separate files for each floor or building can be merged into one project.
It is an installable, offline-capable web app (PWA). Everything runs in the browser and no file is uploaded.

> **⚠ Disclaimer: experimental tool.** PipeCAD Project Merge is experimental software, provided as is, without warranty of any kind. It is not affiliated with or endorsed by the publisher of PipeCAD.
> Before a merged file is used for design, submittal, quotation, installation or commissioning, the user must open it in PipeCAD and verify that every design has been properly preserved according to the intended performance and coverage of the original drawings. That covers floors, detectors, pipe networks, sampling holes, alarm settings and calculated results.
> **The user assumes all risks** arising from the use of this tool and of any file it produces. The original files are never changed; keep them as the reference.

Live: https://thebmgatkgs.github.io/PipeCAD-Project-Merge/ (GitHub Pages from `main`, root).
A Windows `.exe` (Electron) build is planned.

## Quick Start
1. Open the app and click **Choose .pl files**, or drop PipeCAD project files on the box. Add two or more.
2. **Order** the files with ↑ and ↓. The first file (marked **header**) supplies the project details, units and pipe type.
3. **Review** the merged floors and detectors. Any floor or detector whose name clashes with an earlier file is listed under **Renamed**, and you can type a different name there.
4. Set the file name, click **Download merged .pl**, open the file in PipeCAD, and **verify** every design against the original drawings (see the disclaimer above).

The original files are never changed.

## Help in the app
**Help** in the toolbar opens a guide with these sections:
- Quick Start
- How the merge works
- Naming rules
- Project settings (which file goes first)
- Messages (what a red block or a yellow warning means)
- FAQs
- Install & privacy
- Disclaimer
- Revision log

Each step on the page has a link to the matching Help section. The Quick Start panel can be hidden, and the **Quick Start** button brings it back.

## Install and privacy
- The tool runs entirely in the browser. Files are read on the device and never uploaded.
- After the first visit it works offline.
- To install it as an app:
  - Chrome or Edge: click the install icon in the address bar.
  - iPhone or iPad: Share → Add to Home Screen.

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

## Messages
- **Red (merge blocked):**
  - Different units. Set all the projects to the same units in PipeCAD and save again.
  - Different pipe bore or material. Airflow depends on the bore, so these projects can't share one pipe type.
  - A typed name that's already used. Choose a different name.
- **Yellow (check before you download):**
  - Different pipe stick length, OD or part number. Airflow is unchanged, but socket counts and part numbers follow the first file's pipe if PipeCAD recalculates.
  - Different default detector type. Each detector keeps its own type.
- **Notes:** project details that were not carried over, ID shifts and the version stamp.

## FAQs
- **Will the design or the calculated performance change?** No. Every value in every floor, detector, pipe, hole and saved result is copied exactly. Only internal IDs and clashing names change. `tools/verify_merge.py` proves this for any merge.
- **Can I merge two revisions of the same project?** Yes. The later file's matching floors and detectors are renamed, so both versions sit side by side.
- **Can I merge a merged file again?** Yes. It's an ordinary PipeCAD project.
- **Which PipeCAD versions?** Files from 3.5.0.132 and 3.6.2.139 have been merged and opened in PipeCAD.
- **MASD Field Report?** A merged file imports with **Import PipeCAD (.pl)**, one sheet per detector.

## Checking a merge
```
python3 tools/verify_merge.py merged.pl source1.pl source2.pl ...
```
This compares every floor and saved result with its source after undoing the offsets. `PROBLEMS 0` means nothing changed apart from the listed renames.

Validated on six real PipeCAD 3.5.0.132 / 3.6.2.139 projects (49 detectors, 17 floors), and the merged files were opened in PipeCAD.
`.pl` files are client data and are git-ignored.

## Versions
`vMM.mm.rrr`. Releases are tagged by hand in GitHub.
- **00.00.001** (2026-10-09): first release. Merge, rename review and edit, pipe/unit checks, Quick Start and Help, the experimental-tool disclaimer, PWA install and offline use.
