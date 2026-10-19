"""Resumable CC0 Poly Haven acquisition: complete assets, not component-file counts.
Powered by Poly Haven. API terms/provenance retained. Raw library stays .gdignore'd.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import threading
import time
from urllib.parse import unquote, urlparse
import requests

ROOT = Path(__file__).resolve().parents[1]
BATCH = "phase025_bulk_20261019"
META = ROOT / "asset_library/manifests" / BATCH
DEST = ROOT / "asset_library/original_downloads" / BATCH
LICENSE = ROOT / "asset_library/licenses" / BATCH
HEADERS = {"User-Agent": "BreakoutNoWayBackAssetLibrary/0.25 (local game development; Powered by Poly Haven)"}
lock = threading.Lock()
api_lock = threading.Lock()
api_last = 0.0
local = threading.local()


def session():
    if not hasattr(local, "session"):
        local.session = requests.Session()
        local.session.headers.update(HEADERS)
    return local.session


def get(url, stream=False):
    global api_last
    for attempt in range(4):
        if "api.polyhaven.com" in url:
            with api_lock:
                delay = 0.3 - (time.monotonic() - api_last)
                if delay > 0:
                    time.sleep(delay)
                api_last = time.monotonic()
        try:
            response = session().get(url, timeout=(15, 90), stream=stream)
            if response.status_code in (429, 500, 502, 503, 504):
                pause = min(60, max(2 ** attempt, int(response.headers.get("Retry-After", "0"))))
                response.close()
                time.sleep(pause)
                continue
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("Retry budget exhausted for " + url)


def json_cache(url, path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    data = get(url).json()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def digests(path):
    md5, sha = hashlib.md5(), hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            md5.update(chunk)
            sha.update(chunk)
    return md5.hexdigest(), sha.hexdigest()


def atomic_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, indent=2), encoding="utf-8")
    # OneDrive/indexers can briefly hold the destination without delete sharing.
    for attempt in range(5):
        try:
            temp.replace(path)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.25 * 2 ** attempt)


def download(info, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    expected = info.get("md5")
    if path.exists() and path.stat().st_size == info.get("size"):
        md5, sha = digests(path)
        if not expected or md5 == expected:
            return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size,
                    "md5": md5, "sha256": sha, "url": info["url"]}
    temp = path.with_name(path.name + ".part")
    with get(info["url"], stream=True) as response, temp.open("wb") as file:
        for chunk in response.iter_content(512 * 1024):
            if chunk:
                file.write(chunk)
    md5, sha = digests(temp)
    if expected and md5 != expected:
        raise RuntimeError("MD5 mismatch " + info["url"])
    if info.get("size") and temp.stat().st_size != info["size"]:
        raise RuntimeError("Size mismatch " + info["url"])
    temp.replace(path)
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size,
            "md5": md5, "sha256": sha, "url": info["url"]}


def priority(aid, data):
    text = " ".join([aid, data.get("name", ""), *data.get("tags", []), *data.get("categories", [])]).lower()
    weights = {"industrial": 30, "concrete": 25, "metal": 22, "steel": 22, "brick": 20,
               "pipe": 25, "electri": 25, "cabinet": 18, "locker": 30, "door": 22,
               "fence": 28, "laundry": 40, "washer": 40, "dryer": 40, "security": 35,
               "prison": 50, "light": 18, "wall": 18, "floor": 18, "fabric": 16,
               "tool": 25, "chair": 12, "table": 12, "container": 15, "wood": 8,
               "pavement": 15, "asphalt": 15, "rust": 20, "machine": 30,
               "rock": 5, "coast": 10, "gravel": 8, "ground": 6}
    return sum(weight for term, weight in weights.items() if term in text)


def existing_ids():
    # Existing source URLs and actual downloaded provider basenames both exclude re-acquisition.
    ids = set()
    for path in (ROOT / "asset_library/manifests").rglob("*.json"):
        if BATCH in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
            ids.update(re.findall(r"polyhaven\.com/a/([A-Za-z0-9_-]+)", text))
        except (UnicodeError, OSError):
            pass
    for base in [ROOT / "assets", ROOT / "asset_library/original_downloads"]:
        for path in base.rglob("*"):
            if path.is_file() and BATCH not in path.parts:
                ids.add(re.sub(r"_(?:1k|2k|4k|8k)(?:\..*)?$", "", path.stem))
    return ids


def acquire(aid, data):
    if shutil.disk_usage(ROOT).free < 25 * 1024 ** 3:
        raise RuntimeError("Disk reserve reached: preserving 25GiB free")
    files = json_cache("https://api.polyhaven.com/files/" + aid, META / "api_files" / (aid + ".json"))
    kind = "models" if data["type"] == 2 else "materials"
    folder = DEST / kind / aid
    complete = []
    if kind == "models":
        resolutions = files.get("gltf", {})
        resolution = next((r for r in ["1k", "2k", "4k"] if r in resolutions), None)
        if not resolution:
            raise RuntimeError("No glTF complete model package")
        entry = resolutions[resolution]["gltf"]
        name = Path(unquote(urlparse(entry["url"]).path)).name
        complete.append(download(entry, folder / name))
        for relative, info in entry.get("include", {}).items():
            path = folder / relative
            if not path.resolve().is_relative_to(folder.resolve()):
                raise RuntimeError("Unsafe dependency path")
            complete.append(download(info, path))
        gltf = json.loads((folder / name).read_text())
        for resource in gltf.get("buffers", []) + gltf.get("images", []):
            uri = resource.get("uri", "")
            if uri and not uri.startswith("data:") and not (folder / unquote(uri)).is_file():
                raise RuntimeError("Missing glTF dependency " + uri)
        if not gltf.get("meshes"):
            raise RuntimeError("No meshes in model")
    else:
        resolution = "2k"
        material_maps = {}
        for channel in ["Diffuse", "nor_gl", "Rough"]:
            variants = files.get(channel, {}).get(resolution, {})
            fmt = next((fmt for fmt in ["jpg", "png"] if fmt in variants), None)
            if not fmt:
                raise RuntimeError("No complete 2K PBR set: " + channel)
            entry = variants[fmt]
            name = Path(unquote(urlparse(entry["url"]).path)).name
            complete.append(download(entry, folder / name))
            material_maps[channel] = name
        for channel in ["Metal", "AO"]:
            variants = files.get(channel, {}).get(resolution, {})
            if "jpg" in variants:
                entry = variants["jpg"]
                name = Path(unquote(urlparse(entry["url"]).path)).name
                complete.append(download(entry, folder / name))
                material_maps[channel] = name
        (folder / "pbr_maps.json").write_text(json.dumps(material_maps, indent=2))
    record = {"asset_id": "PH025_" + aid, "provider_id": aid, "name": data["name"], "kind": kind,
              "source_url": "https://polyhaven.com/a/" + aid, "authors": data.get("authors", {}),
              "license": "CC0-1.0", "license_url": "https://polyhaven.com/license", "download_date": "2026-10-19",
              "resolution": resolution, "categories": data.get("categories", []), "tags": data.get("tags", []),
              "priority_score": priority(aid, data), "files": complete, "bytes": sum(f["bytes"] for f in complete),
              "status": "DOWNLOADED_CHECKSUM_VERIFIED", "godot_import_status": "NOT TESTED",
              "visual_status": "NOT REVIEWED", "runtime_integration": "NOT INTEGRATED"}
    (folder / "asset_record.json").write_text(json.dumps(record, indent=2))
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    META.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    LICENSE.mkdir(parents=True, exist_ok=True)
    (DEST / ".gdignore").write_text("")
    for name, url in [("POLY_HAVEN_LICENSE.html", "https://polyhaven.com/license"),
                      ("API_TERMS.md", "https://raw.githubusercontent.com/Poly-Haven/Public-API/master/ToS.md")]:
        path = LICENSE / name
        if not path.exists():
            path.write_text(get(url).text, encoding="utf-8")
    (LICENSE / "README.md").write_text("# Powered by Poly Haven\n\nCC0-1.0 assets for BREAKOUT. API terms and original metadata retained. Downloaded/checksummed is separate from art review, Godot import and runtime integration. Each provider asset counts once; textures/dependencies/variants do not inflate the asset count.\n")
    catalog = json_cache("https://api.polyhaven.com/assets", META / "catalog.json")
    excluded = existing_ids()
    downloaded = {}
    for path in DEST.rglob("asset_record.json"):
        record = json.loads(path.read_text())
        if all((ROOT / f["path"]).exists() and (ROOT / f["path"]).stat().st_size == f["bytes"] for f in record["files"]):
            downloaded[record["provider_id"]] = record
    candidates = [(aid, data) for aid, data in catalog.items() if data["type"] in [1, 2] and aid not in excluded and aid not in downloaded]
    models = sorted((x for x in candidates if x[1]["type"] == 2), key=lambda x: (-priority(*x), x[0]))
    materials = sorted((x for x in candidates if x[1]["type"] == 1), key=lambda x: (-priority(*x), x[0]))
    # Interleave relevant objects and surface sets; leave low-priority fallback candidates for failures.
    queue = []
    while models or materials:
        for source in [models, materials, materials]:
            if source:
                queue.append(source.pop(0))
    (META / "selection.json").write_text(json.dumps({"target": args.target, "excluded_existing_ids": sorted(excluded),
        "queue": [{"id": aid, "type": data["type"], "score": priority(aid, data)} for aid, data in queue]}, indent=2))
    errors = []
    start = time.monotonic()
    def checkpoint():
        rows = sorted(downloaded.values(), key=lambda row: row["provider_id"])
        status = {"target": args.target, "completed": len(rows), "models": sum(r["kind"] == "models" for r in rows),
                  "materials": sum(r["kind"] == "materials" for r in rows), "bytes": sum(r["bytes"] for r in rows),
                  "failures": len(errors), "elapsed_seconds": round(time.monotonic() - start, 1),
                  "status": "COMPLETE_DOWNLOAD_ONLY" if len(rows) >= args.target else "DOWNLOADING",
                  "validation_scope": "Official MD5+size, SHA256 inventory, glTF local dependencies/PBR required channels; not engine/visual/gameplay acceptance"}
        for filename, value in [("inventory.json", rows), ("progress.json", status), ("failures.json", errors)]:
            path = META / filename
            atomic_json(path, value)
        print(json.dumps({k: status[k] for k in ["completed", "models", "materials", "bytes", "failures", "elapsed_seconds", "status"]}), flush=True)
    checkpoint()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        active = {}
        while len(downloaded) < args.target and (queue or active):
            while queue and len(active) < args.workers and len(downloaded) + len(active) < args.target:
                aid, data = queue.pop(0)
                active[executor.submit(acquire, aid, data)] = aid
            finished, _ = wait(active, timeout=15, return_when=FIRST_COMPLETED)
            for future in finished:
                aid = active.pop(future)
                try:
                    downloaded[aid] = future.result()
                except Exception as error:
                    errors.append({"id": aid, "error": str(error)})
            if (finished and len(downloaded) % 10 < len(finished)) or not active:
                checkpoint()
    checkpoint()
    if len(downloaded) < args.target:
        raise SystemExit("Target not reached; see failures.json")


if __name__ == "__main__":
    main()
