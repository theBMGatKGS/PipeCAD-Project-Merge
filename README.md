# PipeCAD Project Merge

ModuLaser Tools · **v00.01.001** (2026-10-12)

Combines several PipeCAD `.pl` project files into one `.pl` that opens in PipeCAD with the design unchanged, then proves it: every floor and detector is fingerprinted and compared with the originals, and the difference report can be printed or saved.
For example, separate files for each floor or building can be merged into one project.
It is an installable, offline-capable web app (PWA). Everything runs in the browser and no file is uploaded.

> **⚠ Disclaimer: experimental tool.** PipeCAD Project Merge is experimental software, provided as is, without warranty of any kind. It is not affiliated with or endorsed by the publisher of PipeCAD.
> Before a merged file is used for design, submittal, quotation, installation or commissioning, the user must open it in PipeCAD and verify that every design has been properly preserved according to the intended performance and coverage of the original drawings. That covers floors, detectors, pipe networks, sampling holes, alarm settings and calculated results.
> **The user assumes all risks** arising from the use of this tool and of any file it produces. The original files are never changed; keep them as the reference.

- **Web app:** https://thebmgatkgs.github.io/PipeCAD-Project-Merge/ (GitHub Pages from `main`, root).
- **Windows installer:** download `PipeCAD-Project-Merge-Setup-<version>.exe` from the [latest release](https://github.com/theBMGatKGS/PipeCAD-Project-Merge/releases/latest).

## Quick Start
1. Open the app and click **Choose .pl files**, or drop PipeCAD project files on the box. Add two or more.
2. **Order** the files by dragging the rows (or ↑ and ↓). The first file (pinned as **header**) supplies the project details, units and pipe type.
3. **Names.** A floor whose name is already used by an earlier file gets a copy number (`Area A (2)`). Detectors and pipe runs keep their names. Decide whether to leave or number any repeated detector names, and set a naming convention if you want one. Every change is listed, and you can type a different name.
4. **Review and download.** Set the file name in the side panel and click **Download merged .pl**. If it is disabled, the panel says why, and each message jumps to the item to fix.
5. **Design check.** Read the PASS/FAIL strip, then **Print** (or save as PDF), **Save .html** or **Save .csv**.
6. Open the file in PipeCAD and **verify** every design against the original drawings (see the disclaimer above).

The original files are never changed.

## Help in the app
**Help** in the toolbar opens a guide with these sections:
- Quick Start
- How the merge works
- Naming rules
- Design check & report
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
- **Names.** Names change only when they must, or when the user asks:
  - **Floors** must be unique in the project. A floor whose name is already used by an earlier file gets the next copy number: `Area A → Area A (2)`, and `Area A (2) → Area A (3)`.
  - **Detectors** only need unique names on their own floor, so they're never renamed automatically.
  - **Repeated names** in one place of an original file (for example four detectors called `Detector` on one floor) are flagged. The user chooses **Leave as is** or **Number them** (`Detector, Detector 2, Detector 3`; `MASD 01 → MASD 02`).
  - **Pipe runs** are locked unless the user sets a pipe naming convention. Exhaust runs always keep `Exhaust` first.
  - **Naming conventions:** one for the whole project, or one per file. For floors, detectors and pipe runs, choose **Prefix / suffix** or **Find & replace** (case-sensitive). Prefix, suffix and replacement can use `{file}`, `{floor}` and `{detector}`. **Match pipe names to detector** sets the pipe prefix to `{detector} `.
  - **Typed names:** any changed floor or detector name can be overtyped. A floor name must not match another floor, and a detector name must not match another detector on its floor.
  - **Length limit:** PipeCAD allows at most 32 characters, spaces included, for floor, detector and pipe-run names, and new names are held to that. When a copy number or numbering would pass the limit, the name is cut and ends in `...(n)`, n being the copy number (`Boyers Roadway 2 x Pipes/MASD → Boyers Roadway 2 x Pipes/M...(2)`). An over-long convention or typed name is refused.
- **Refused:** files in different units, or with a different pipe bore or material, because their airflow results would change.
- **Flagged:** a different stick length, OD or part number. PipeCAD keeps one pipe type per project, so socket counts and part numbers follow the first file's pipe if PipeCAD recalculates.
- **Version.** The merged file is marked with the newest PipeCAD version among the inputs.
- **Output format** matches PipeCAD's own: XML declaration, indentation, `<Tag />` empty elements and CRLF line endings.

## Design check and difference report
After every merge the merged file is read back and compared with the source files:
- **Fingerprints.** Each floor and detector gets a SHA-256 fingerprint of its whole design: pipe runs, pipes, coordinates, sampling holes, end caps, T-pieces, detector settings, outlines, labels and the saved PipeCAD results that belong to it. Only floor, detector and pipe-run names and PipeCAD's internal ID and tree numbers are left out (IDs are renumbered in order of appearance). Matching fingerprints mean an identical design.
- **ID shift.** Each source file's IDs must have moved by one constant amount, so every saved result still points at the same pipe or hole.
- **Completeness.** Nothing may be missing or extra, saved results not attached to a detector must match, and the project settings must come from one of the files.
- **Report.** It lists each file with its SHA-256 checksum and ID shift, then every floor and detector with its original and merged name, the reason for any name change (copy number, naming convention, numbered repeat or typed by the user), pipe-run renames, contents (pipe runs, pipes, holes, end caps, labels, saved results), both fingerprints and the result (Identical, Identical (moved), Changed with the first differing values, or Missing). **Print report** prints it or saves it as PDF, **Save report (.html)** keeps a copy that opens in any browser, and **Save table (.csv)** opens in Excel.
- **Check an existing merged file.** Add the original files in step 1 (any order), then use **Choose merged .pl** at the bottom of the page.

The check reads the file's contents. It doesn't replace opening the merged file in PipeCAD.

## Windows installer (Electron)
`electron/` wraps the same `index.html` in a desktop app. The **Windows installer** workflow (`.github/workflows/windows-installer.yml`) builds an NSIS installer on GitHub's Windows runners:
- **On every push to `main` and every PR:** the `.exe` is available under the run's *Artifacts*.
- **When a GitHub release is published:** the `.exe` is attached to the release automatically.
- **Version:** the installer takes its version from `Version MM.mm.rrr` in `index.html`.

To build locally on Windows:
```
cd electron
npm ci
npm run dist
```
The output is `dist/PipeCAD-Project-Merge-Setup-<version>.exe`.

## Messages
- **Red (merge blocked):**
  - Different units. Set all the projects to the same units in PipeCAD and save again.
  - Different pipe bore or material. Airflow depends on the bore, so these projects can't share one pipe type.
  - A typed name that's already used. Choose a different name.
  - A new name over the length limit. Shorten the prefix, suffix, replacement or typed name.
  - A pipe naming convention that would give two different runs on one detector the same name.
- **Yellow (check before you download):**
  - Repeated names need a decision: leave them or number them.
  - Different pipe stick length, OD or part number. Airflow is unchanged, but socket counts and part numbers follow the first file's pipe if PipeCAD recalculates.
  - Different default detector type. Each detector keeps its own type.
- **Notes:** project details that were not carried over, ID shifts and the version stamp.
- **Design check:** green means every floor and detector is identical apart from the listed name changes; red means something is changed, missing or extra, and the merged file shouldn't be used.

## FAQs
- **Will the design or the calculated performance change?** No. Every value in every floor, detector, pipe, hole and saved result is copied exactly. Only internal IDs and the names listed in step 3 change. The design check after each merge confirms this, and `tools/verify_merge.py` checks it independently.
- **Can I merge two revisions of the same project?** Yes. The later file's floors get copy numbers (`Area A (2)`), so both versions sit side by side. A per-file floor suffix such as ` Rev B` marks them more clearly.
- **Can I merge a merged file again?** Yes. It's an ordinary PipeCAD project.
- **Which PipeCAD versions?** Files from 3.5.0.132 and 3.6.2.139 have been merged and opened in PipeCAD.
- **MASD Field Report?** A merged file imports with **Import PipeCAD (.pl)**, one sheet per detector. Detectors on different floors can share a name; a detector prefix such as `{floor} ` keeps the sheets apart.
- **Can I check a merged file later?** Yes, with **Check an existing merged file**.

## Checking a merge
```
python3 tools/verify_merge.py merged.pl source1.pl source2.pl ...
```
This compares every floor and saved result with its source after undoing the offsets. `PROBLEMS 0` means nothing changed apart from the listed floor, detector and pipe-run renames. It is independent of the in-app design check.

Validated on six real PipeCAD 3.5.0.132 / 3.6.2.139 projects (49 detectors, 17 floors), and the merged files were opened in PipeCAD.
`.pl` files are client data and are git-ignored.

## Versions
`vMM.mm.rrr`. Releases are tagged by hand in GitHub.
- **00.01.001** (2026-10-12): redesign; merge logic and output unchanged. Dark on-screen UI with a sticky step bar and per-step status; drag-to-reorder files with the first file pinned as header; one rename table with Leave all / Number all; side panel with file name, Download (with the reason when disabled) and grouped must-fix / review messages that jump to their item; PASS/FAIL strip with Print / Save .html / Save .csv; printed and saved difference report in the KGS palette with summary tiles.
- **00.01.000** (2026-10-12): design check with SHA-256 fingerprints, ID-shift and file checksums; difference report (print/PDF, HTML, CSV); check for existing merged files; copy-number floor names (`Area A (2)`); detectors unique per floor; repeated names flagged to leave or number; prefix/suffix and find & replace naming conventions for floors, detectors and pipe runs, project-wide or per file; exhaust runs keep “Exhaust” first; new names held to PipeCAD's 32-character limit; Help and Quick Start updated.
- **00.00.001** (2026-10-09): first release. Merge, rename review and edit, pipe/unit checks, Quick Start and Help, the experimental-tool disclaimer, PWA install and offline use.
