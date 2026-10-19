"""Reproducible contact sheets for shot still review; never motion/contact approval."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="tests/phase025/evidence/shots_full_normal")
    parser.add_argument("--output", default="tests/phase025/evidence/shot_sheets")
    args = parser.parse_args()
    source, output = ROOT / args.source, ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    groups, found = {}, {}
    for path in sorted(source.glob("*shot_activated_*.png")):
        shot = path.stem.split("shot_activated_")[-1]
        mission = shot.split("_CS")[0]
        groups.setdefault(mission, []).append((shot, path))
        found[shot] = path.relative_to(ROOT).as_posix()
    for mission, rows in groups.items():
        canvas = Image.new("RGB", (1280, ((len(rows) + 1) // 2) * 390), "#17191c")
        for i, (shot, path) in enumerate(rows):
            x, y = (i % 2) * 640, (i // 2) * 390
            with Image.open(path) as image:
                canvas.paste(image.resize((640, 360)), (x, y))
            ImageDraw.Draw(canvas).text((x + 8, y + 366), shot, fill="white")
        canvas.save(output / (mission + ".jpg"), quality=92)
    expected = [shot["id"] for shot in json.loads((ROOT / "data/ch01/shots.json").read_text())["shots"]]
    report = {"scope": "Captured still presence and contact sheets only; activation and a still cannot prove framing across an entire shot, motion, prop contact or performance.",
              "expected": len(expected), "captured": len(found), "missing": sorted(set(expected) - set(found)),
              "shots": [{"id": shot, "evidence": found.get(shot), "motion_acceptance": "NOT VERIFIED"} for shot in expected]}
    (output / "coverage.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"expected": len(expected), "captured": len(found), "missing": report["missing"]}))


if __name__ == "__main__":
    main()
