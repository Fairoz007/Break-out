"""Separate on-disk verification of the completed 1,000-asset acquisition manifest."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "asset_library/manifests/phase025_bulk_20261019"


def official_files(value, result):
    if isinstance(value, dict):
        if "url" in value and "md5" in value:
            result[value["url"]] = value
        for child in value.values():
            official_files(child, result)
    elif isinstance(value, list):
        for child in value:
            official_files(child, result)


def main():
    records = json.loads((META / "inventory.json").read_text())
    excluded = set(json.loads((META / "selection.json").read_text())["excluded_existing_ids"])
    failures, inspected = [], []
    provider_ids = [row["provider_id"] for row in records]
    if len(records) != 1000 or len(set(provider_ids)) != 1000:
        failures.append("Expected exactly1000 unique provider assets")
    if len(set(aid.lower() for aid in provider_ids)) != len(provider_ids):
        failures.append("Case-insensitive provider ID collision")
    if set(provider_ids) & excluded:
        failures.append("Previously inventoried provider IDs reacquired")
    total_files, total_bytes = 0, 0
    for record in records:
        aid = record["provider_id"]
        original = {}
        official_files(json.loads((META / "api_files" / (aid + ".json")).read_text()), original)
        row_errors = []
        if record["license"] != "CC0-1.0":
            row_errors.append("Unexpected license")
        for data in record["files"]:
            path = ROOT / data["path"]
            md5, sha = hashlib.md5(), hashlib.sha256()
            with path.open("rb") as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b""):
                    md5.update(chunk)
                    sha.update(chunk)
            source = original.get(data["url"], {})
            if path.stat().st_size != data["bytes"] or path.stat().st_size != source.get("size"):
                row_errors.append("Size mismatch " + path.name)
            if sha.hexdigest() != data["sha256"] or md5.hexdigest() != source.get("md5"):
                row_errors.append("Checksum mismatch " + path.name)
            if path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                try:
                    with Image.open(path) as image:
                        image.verify()
                except Exception as error:
                    row_errors.append("Image corruption " + str(error))
            if path.suffix == ".gltf":
                gltf = json.loads(path.read_text())
                if not gltf.get("meshes") or not gltf.get("accessors"):
                    row_errors.append("Missing mesh/accessors")
                for item in gltf.get("buffers", []) + gltf.get("images", []):
                    uri = item.get("uri", "")
                    if uri and not uri.startswith("data:"):
                        dependency = (path.parent / unquote(uri)).resolve()
                        if not dependency.is_relative_to(path.parent.resolve()) or not dependency.is_file():
                            row_errors.append("Missing/unsafe dependency " + uri)
                        elif "byteLength" in item and dependency.stat().st_size < item["byteLength"]:
                            row_errors.append("Truncated geometry buffer")
            total_files += 1
            total_bytes += path.stat().st_size
        inspected.append({"id": aid, "kind": record["kind"], "pass": not row_errors, "errors": row_errors})
        if row_errors:
            failures.append({"id": aid, "errors": row_errors})
    result = {"asset_count": len(records), "unique_provider_ids": len(set(provider_ids)),
              "kinds": dict(Counter(row["kind"] for row in records)), "files": total_files,
              "bytes": total_bytes, "failed": len(failures), "failures": failures, "assets": inspected,
              "scope": "Separate re-read of every physical payload: SHA256 and official MD5/size, image integrity, glTF dependencies and buffer presence. Not Godot import, collision, rig, animation or artistic acceptance."}
    (META / "verification.json").write_text(json.dumps(result, indent=2))
    with (META / "inventory.csv").open("w", newline="", encoding="utf-8-sig") as file:
        fields = ["provider_id", "name", "kind", "license", "source_url", "resolution", "bytes", "status", "godot_import_status", "visual_status", "runtime_integration"]
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps({key: result[key] for key in ["asset_count", "unique_provider_ids", "kinds", "files", "bytes", "failed"]}))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
