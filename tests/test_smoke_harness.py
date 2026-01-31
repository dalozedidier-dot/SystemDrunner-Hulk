from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_harness_runs_and_produces_json(tmp_path: Path) -> None:
    """Smoke: run the multisector harness and ensure results JSON is produced.

    This is structural: it does not assert semantic values of results, only that:
    - the harness executes successfully
    - output is valid JSON (list of cases)
    """
    repo_root = Path(__file__).resolve().parents[1]
    out = tmp_path / "results.json"

    cmd = [
        "python",
        str(repo_root / "harness.py"),
        "--repo-root",
        str(repo_root),
        "--profiles",
        "01_tests_multisector/tests/profiles",
        "--out",
        str(out),
    ]
    subprocess.run(cmd, check=True, cwd=str(repo_root), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

    assert out.is_file(), "harness did not produce results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, list), "results.json is not a list"
    assert len(data) > 0, "results.json is empty"
