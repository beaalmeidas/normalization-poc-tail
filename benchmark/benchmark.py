from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

REQUIRED_COLUMNS = ("original", "attacked", "normalized")
HISTOGRAM_MAX_BUCKETS = 15
HISTOGRAM_SHOW_ALL_THRESHOLD = 20


def _default_fixture_path() -> Path:
    return Path(__file__).resolve().parent / "fixtures" / "normalized_sample.csv"


def _normalize_header(name: str) -> str:
    return name.strip().lower()


def load_rows(path: Path) -> list[dict[str, str]]:
    """Read CSV rows; values are stripped. Keys matched case-insensitively."""
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return []
        header_map = {_normalize_header(h): h for h in reader.fieldnames}
        missing = [c for c in REQUIRED_COLUMNS if c not in header_map]
        if missing:
            raise ValueError(
                f"CSV missing required columns {missing}; found {list(reader.fieldnames)}"
            )
        rows: list[dict[str, str]] = []
        for raw in reader:
            row = {
                col: (raw.get(header_map[col]) or "").strip()
                for col in REQUIRED_COLUMNS
            }
            rows.append(row)
        return rows


def constancy_for_group(normalized_values: Sequence[str]) -> tuple[float, int, int, Counter[str]]:
    """Returns (constancy, group_size, dominant_count, counter)."""
    counter: Counter[str] = Counter(normalized_values)
    group_size = len(normalized_values)
    if group_size == 0:
        return 0.0, 0, 0, counter
    dominant_count = max(counter.values())
    return dominant_count / group_size, group_size, dominant_count, counter


def _histogram_entries(counter: Counter[str]) -> tuple[list[dict[str, int | str]], bool]:
    """Sorted by (-count, normalized); truncate if many distinct values."""
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    distinct = len(items)
    if distinct <= HISTOGRAM_SHOW_ALL_THRESHOLD:
        return [{"normalized": n, "count": c} for n, c in items], False
    truncated = items[:HISTOGRAM_MAX_BUCKETS]
    return [{"normalized": n, "count": c} for n, c in truncated], True


def _grouping_payload(
    original: str,
    constancy: float,
    dominant_normalized: str,
    dominant_count: int,
    group_size: int,
    counter: Counter[str],
) -> dict[str, object]:
    hist, truncated = _histogram_entries(counter)
    out: dict[str, object] = {
        "original": original,
        "constancy": constancy,
        "dominant_normalized": dominant_normalized,
        "dominant_count": dominant_count,
        "group_size": group_size,
        "normalized_histogram": hist,
    }
    if truncated:
        out["normalized_histogram_truncated"] = True
    return out


def compute_per_original_stats(
    rows: Iterable[Mapping[str, str]],
) -> dict[str, tuple[float, int, int, Counter[str], str]]:
    """
    Group by stripped original -> (constancy, group_size, dominant_count, counter, dominant_norm).
    dominant_norm: lexicographically smallest among ties for max count.
    """
    groups: dict[str, list[str]] = {}
    for row in rows:
        orig = (row.get("original") or "").strip()
        norm = (row.get("normalized") or "").strip()
        groups.setdefault(orig, []).append(norm)

    stats: dict[str, tuple[float, int, int, Counter[str], str]] = {}
    for original, norms in groups.items():
        constancy, group_size, dominant_count, counter = constancy_for_group(norms)
        tied = [n for n, c in counter.items() if c == dominant_count]
        dominant_norm = min(tied)
        stats[original] = (constancy, group_size, dominant_count, counter, dominant_norm)
    return stats


def build_result(rows: list[dict[str, str]]) -> dict[str, object]:
    total_rows = len(rows)
    if total_rows == 0:
        return {
            "metrics": {
                "mean_constancy": None,
                "min_constancy": None,
                "max_constancy": None,
                "num_originals": 0,
                "total_rows": 0,
                "weighted_constancy": None,
            },
            "best_grouping": None,
            "worst_grouping": None,
        }

    per = compute_per_original_stats(rows)
    originals_sorted = sorted(per.keys())
    constancies = [per[o][0] for o in originals_sorted]
    mean_constancy = sum(constancies) / len(constancies)

    sum_max = sum(per[o][2] for o in originals_sorted)
    weighted_constancy = sum_max / total_rows

    # Best: highest constancy; tie-break lexicographically smallest `original`.
    best_original = min(originals_sorted, key=lambda o: (-per[o][0], o))
    worst_original = min(
        originals_sorted,
        key=lambda o: (per[o][0], o),
    )

    def pack(orig: str) -> dict[str, object]:
        cty, gsz, dcount, counter, dnorm = per[orig]
        return _grouping_payload(orig, cty, dnorm, dcount, gsz, counter)

    return {
        "metrics": {
            "mean_constancy": mean_constancy,
            "min_constancy": min(constancies),
            "max_constancy": max(constancies),
            "num_originals": len(per),
            "total_rows": total_rows,
            "weighted_constancy": weighted_constancy,
        },
        "best_grouping": pack(best_original),
        "worst_grouping": pack(worst_original),
    }


def write_results(data: dict[str, object], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    out_path.write_text(text + "\n", encoding="utf-8")


def run(input_path: Path, out_path: Path) -> dict[str, object]:
    rows = load_rows(input_path)
    result = build_result(rows)
    write_results(result, out_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark normalization constancy from CSV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=_default_fixture_path(),
        help="Input CSV with columns original, attacked, normalized (default: bundled fixture).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results.json"),
        help="Output JSON path (default: results.json in cwd).",
    )
    args = parser.parse_args(argv)

    input_path: Path = args.input
    out_path: Path = args.out

    if not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        run(input_path.resolve(), out_path.resolve())
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"wrote {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
