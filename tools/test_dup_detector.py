"""00.01.002 regression: duplicate detector names across files are renamed on merge, and the merged design is otherwise unchanged.
Run: python3 tools/test_dup_detector.py [a.pl b.pl]   (default: Brent's Hoistway MiniLaser .pl merged with a copy of itself)
Needs playwright (chromium)."""
import asyncio, os, re, shutil, subprocess, sys, tempfile
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get('ML_FIXTURE', '/workspace/qa/minilaser/minilaser.pl')
tmp = tempfile.mkdtemp(prefix='pcm-dup-')
if len(sys.argv) >= 3: A, B = sys.argv[1], sys.argv[2]
else: A = os.path.join(tmp, 'hoistway-a.pl'); B = os.path.join(tmp, 'hoistway-b.pl'); shutil.copy(SRC, A); shutil.copy(SRC, B)
R = []
def ok(n, c, i=''): R.append(bool(c)); print('PASS' if c else 'FAIL', n, str(i)[:300])
def det_names(xml): return re.findall(r'<Detector>\s*(?:<[^>]+>[^<]*</[^>]+>\s*)*?<name>([^<]*)</name>', xml)
async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(); pg = await b.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto('file://' + ROOT + '/index.html'); await pg.set_input_files('#pick', [A, B]); await pg.wait_for_timeout(1000)
    xml = await pg.evaluate("typeof merged!=='undefined' && merged && merged.xml")
    ok('merge produced a file', bool(xml))
    names = det_names(xml or '')
    ok('two "Detector" → "Detector" and "Detector 2"', names == ['Detector', 'Detector 2'], names)
    ok('detector names unique in the merged file', len(set(names)) == len(names), names)
    txt = await pg.evaluate("document.body.innerText")
    ok('rename table lists the detector copy number', 'Detector 2' in txt)
    out = os.path.join(tmp, 'merged.pl'); open(out, 'w').write(xml or '')
    v = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'verify_merge.py'), out, A, B], capture_output=True, text=True)
    ok('verify_merge: design and saved results unchanged (PROBLEMS 0)', 'PROBLEMS 0' in v.stdout, v.stdout[-300:])
    # single-file names that don't clash stay unchanged
    await pg.goto('file://' + ROOT + '/index.html'); await pg.evaluate('localStorage.clear()')
    ok('no page errors', not errs, errs)
    await b.close()
  print(f'SUMMARY {sum(R)} / {len(R)}'); sys.exit(0 if all(R) else 1)
asyncio.run(main())
