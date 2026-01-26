
import argparse
import json
from pathlib import Path
import yaml
from typing import List, Dict, Any

def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".", help="Repo root containing tests/")
    ap.add_argument("--profiles", default="tests/profiles", help="Directory with profile YAMLs")
    ap.add_argument("--update-expected", action="store_true", help="Write expected snapshots")
    ap.add_argument("--out", default="tests/results.json", help="Aggregated results JSON")
    return ap.parse_args()

def load_profiles(profiles_dir: Path):
    profiles = []
    for p in sorted(profiles_dir.glob("*.yaml")):
        with open(p, 'r', encoding="utf-8") as f:
            profile = yaml.safe_load(f)
        profiles.append(profile)
    return profiles

def run_tests_for_profiles(profiles: List[Dict[str, Any]], repo_root: Path, update_expected: bool):
    results = []
    for profile in profiles:
        result = run_case(profile, repo_root, update_expected=update_expected)
        results.append(result)
    return results

def write_results_to_file(results: List[Dict[str, Any]], out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def generate_summary(results: List[Dict[str, Any]]):
    summary = {}
    for result in results:
        sid = result["meta"]["profile_id"]
        summary[sid] = result.get("expected_status", "OK")
    return summary

def main():
    args = parse_arguments()
    repo_root = Path(args.repo_root).resolve()
    profiles_dir = (repo_root / args.profiles).resolve()

    profiles = load_profiles(profiles_dir)
    results = run_tests_for_profiles(profiles, repo_root, update_expected=args.update_expected)

    out_path = repo_root / args.out
    write_results_to_file(results, out_path)

    # Generate and print human-readable summary
    summary = generate_summary(results)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
