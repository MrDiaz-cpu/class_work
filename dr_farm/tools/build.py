"""Refresh trusted copies and build the single student download. Run from any folder."""
from pathlib import Path
import shutil
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
TRUSTED = ("farm.py", "levels.py", "runner.py")
STUDENT = ("tutorial.py", "level1.py", "level2.py", "level3.py")
WEB = ("index.html", "style.css", "app.js", "scene.js", "sprites.js")


def build():
    for level in range(1, 4):
        dest = ROOT / f"level{level}"
        for name in TRUSTED:
            shutil.copyfile(GAME / name, dest / name)
        shutil.copyfile(ROOT / "tools/_grade.py", dest / "_grade.py")
    sources = [(GAME / n, n) for n in TRUSTED + STUDENT + ("play.py",)]
    sources += [(GAME / "web" / n, "web/" + n) for n in WEB]
    sources += [(p, "web/sprites/" + p.name) for p in sorted((GAME / "web/sprites").glob("*.png"))]
    sources += [(ROOT / n, n) for n in ("README.md", "STUDENT_INSTRUCTIONS.md")]
    output = ROOT / "dr_farm.zip"
    tmp = output.with_suffix(".zip.tmp")
    try:
        with ZipFile(tmp, "w") as archive:
            for source, name in sources:
                entry = ZipInfo("dr_farm/" + name)
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, source.read_bytes(), compress_type=ZIP_DEFLATED)
        tmp.replace(output)
    finally:
        if tmp.exists():
            tmp.unlink()
    print(f"Built {output.name} with {len(sources)} student files.")


if __name__ == "__main__":
    build()

