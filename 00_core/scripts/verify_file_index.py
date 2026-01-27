#!/usr/bin/env python3
# verify_file_index.py
# Vérifie que chaque entrée de FILE_INDEX_SHA256.txt existe et que le SHA256 correspond.
# Sortie non-compensable : OK / MISSING / MISMATCH.
from __future__ import annotations
import argparse, hashlib
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root")
    ap.add_argument("--index", default="FILE_INDEX_SHA256.txt", help="index file")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    index_path = root / args.index
    if not index_path.exists():
        print(f"INDEX_MISSING: {index_path}")
        return 2

    missing, mismatch, ok = [], [], 0
    for ln in index_path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            h, rel = ln.split(None, 1)
            rel = rel.strip()
        except ValueError:
            print(f"INDEX_LINE_INVALID: {ln}")
            return 2

        p = root / rel
        if not p.exists():
            missing.append(rel)
            continue

        real = sha256_file(p)
        if real.lower() != h.lower():
            mismatch.append((rel, h, real))
        else:
            ok += 1

    print(f"OK={ok}  MISSING={len(missing)}  MISMATCH={len(mismatch)}")
    if missing:
        print("\n[MISSING]")
        for r in missing:
            print(r)
    if mismatch:
        print("\n[MISMATCH]")
        for r, exp, got in mismatch:
            print(f"{r}\n  expected={exp}\n  got     ={got}")
    return 0 if (not missing and not mismatch) else 1

if __name__ == "__main__":
    raise SystemExit(main())
