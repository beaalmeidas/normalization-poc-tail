# Benchmark constancy (`benchmark/`)

## Overview

Add a self-contained `benchmark/` package with `benchmark.py` that reads a three-column CSV, computes per-original constancy (max frequency of identical `normalized` / group size), writes `results.json` (default path; overridable) with aggregate metrics plus `best_grouping` and `worst_grouping` examples, and ships small fixtures plus automated tests.

## Tasks

- [ ] Create `benchmark/__init__.py`, `benchmark/benchmark.py` with CSV load, per-original constancy, write `results.json` with metrics + best/worst examples
- [ ] Add `benchmark/fixtures/normalized_sample.csv` (50% example + second original)
- [ ] Add `tests/test_benchmark.py` (constancy assertions + parse written `results.json`)
- [ ] Add `requirements-dev.txt` with pytest for local test runs

## Context

The repo may be minimal ([README.md](README.md) only). The attacker and normalizer are out of scope for this plan; this work only adds the benchmark and tests.

## Constancy definition (confirmed)

- Group rows by **`original`**.
- Within each group, count occurrences of each **`normalized`** string (exact string match after read; strip surrounding whitespace on load).
- **Constancy for that original** = `(max count among normalized values) / (number of rows in that group)`.

Example: two normalized values each with count 2 of 4 → max = 2 → **constancy = 0.5 (50%)**.

Ties for “most frequent” normalized value do not change the ratio: constancy uses **max count** only.

## Input contract

- CSV path passed as CLI argument (e.g. `python -m benchmark.benchmark path/to/file.csv`), with a sensible default pointing at the bundled mock fixture so `python -m benchmark.benchmark` runs without args in dev.
- Expected headers (case-insensitive, trim): **`original`**, **`attacked`**, **`normalized`**. `attacked` is read for completeness but **not** used in the constancy formula (unless you later ask to incorporate it).
- Filename: support **`normalize.csv`** in docs/fixtures; CLI accepts any path (pipeline can use `normalized.csv` or `normalize.csv` interchangeably).

## Output: `results.json` (RESULTADO)

Write **one JSON file** (default filename **`results.json`** in the process working directory; override with **`--out PATH`**). Same compact schema everywhere — **no full row dump** of the CSV.

Top-level keys:

- **`metrics`**: e.g. `mean_constancy` (unweighted mean across originals), `min_constancy`, `max_constancy`, `num_originals`, `total_rows`, optionally `weighted_constancy` (max_count sum / total rows) — document which mean you use; recommend **macro mean** (each original counts equally).
- **`best_grouping`**: example of the **best** normalization grouping — the `original` with **highest** constancy. Include `original`, `constancy`, `dominant_normalized`, `dominant_count`, `group_size`, and a compact `normalized_histogram` (all buckets if the group is small, else top-N by count) so the example is readable without listing every `attacked` row.
- **`worst_grouping`**: same shape for the **worst** constancy (lowest ratio).

If multiple originals tie for best or worst, pick deterministically (e.g. lexicographic `original`).

**Stdout:** optional one-line confirmation with the resolved output path (helps CI/logs); do not duplicate the full JSON on stdout unless you add a `--print` flag later.

Use UTF-8 encoding and `indent=2` (prefer **indented** for human inspection of `results.json`).

## Layout

```text
benchmark/
  __init__.py          # optional; enables python -m benchmark.benchmark
  benchmark.py         # CSV load, group, compute, write results.json
  fixtures/
    normalized_sample.csv   # mock data including your 50% case + at least one other original
tests/
  test_benchmark.py    # pytest: constancy on fixture, ties, single-row group, CLI smoke
```

## Implementation notes

- Use **`csv` + `collections.Counter`** (stdlib only) unless you add a project-wide `requirements.txt`; keep the benchmark dependency-free for now.
- Normalize keys when grouping: strip `original` for grouping key if you want `"a "` and `"a"` to merge — **default: strip whitespace only**, no case-folding unless you specify later.
- Edge cases: empty file → JSON error or explicit zero metrics; one row per original → constancy `1.0`; blank `normalized` → counts as its own bucket.

## Test plan

- **Unit**: given a small in-memory table or the fixture CSV, assert constancy for the “coca cola” block is **0.5** and a second original has expected value.
- **Integration**: run `python -m benchmark.benchmark --input ... --out <tmp>/results.json` against `benchmark/fixtures/normalized_sample.csv`, read the file, assert `metrics`, `best_grouping`, and `worst_grouping` keys, constancy ordering (best ≥ worst), and expected shapes (histogram lists, counts).

Add root **`requirements-dev.txt`** with **`pytest`** for dev installs; no README change required unless you want install docs later.

## CLI sketch

`python -m benchmark.benchmark [--input PATH] [--out results.json]`

Default **`--out results.json`** (relative to cwd). Tests use a temp path to avoid clobbering the repo.
