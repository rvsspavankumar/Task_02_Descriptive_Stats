#!/usr/bin/env python3
"""
Descriptive Statistics — Pure Python Implementation (No Third-Party Libraries)

Computes column-level and grouped descriptive statistics using only the
Python standard library.  Accepts a CSV file path as a command-line
argument so the same script works on any well-formed CSV.

Usage:
    python3 pure_python_stats.py <path_to_csv>
    python3 pure_python_stats.py 2024_fb_ads_president_scored_anon.csv
"""

import csv
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

# ─── Configuration ───────────────────────────────────────────────────
MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan"}
MAX_TOP_VALUES = 5
# For grouped analysis: limit printed groups to keep output readable
MAX_GROUPS_PRINTED = 10
# Default grouping keys (used when detected in the dataset)
KNOWN_GROUP_KEYS = {
    "page_id": [["page_id"]],
    "ad_id":   [["page_id", "ad_id"]],
}

WIDTH = 76


# ─── Helpers ─────────────────────────────────────────────────────────

def normalize(value):
    """Strip whitespace and return string representation."""
    if value is None:
        return ""
    return str(value).strip()


def is_missing(value):
    """Return True if value is considered missing/null."""
    return normalize(value).lower() in MISSING_TOKENS


def try_float(value):
    """Try converting to float; return (True, number) or (False, None)."""
    try:
        return True, float(normalize(value))
    except (ValueError, TypeError):
        return False, None


# ─── Type Inference ──────────────────────────────────────────────────

def infer_value_type(value):
    """Classify a single non-missing value."""
    v = normalize(value)
    if is_missing(v):
        return "missing"

    ok, _ = try_float(v)
    if ok:
        return "numeric"

    # Date pattern: YYYY-MM-DD
    if len(v) == 10 and v[4] == "-" and v[7] == "-":
        parts = v.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            return "date"

    # Dict-like range text
    if v.startswith("{") and v.endswith("}"):
        return "range_text"

    # List-like text
    if v.startswith("[") and v.endswith("]"):
        return "list_text"

    return "text"


def infer_column_type(values):
    """Determine the dominant type of a column from its values."""
    non_missing = [normalize(v) for v in values if not is_missing(v)]
    if not non_missing:
        return "empty"

    type_counts = Counter(infer_value_type(v) for v in non_missing)
    most_common, _ = type_counts.most_common(1)[0]

    if most_common == "numeric":
        return "numeric"
    if most_common == "date":
        return "date"
    if most_common == "range_text":
        return "range_text"
    if most_common == "list_text":
        return "list_text"

    unique_ratio = len(set(non_missing)) / len(non_missing) if non_missing else 0
    if unique_ratio > 0.95 and len(non_missing) > 20:
        return "identifier"

    return "categorical"


# ─── Statistics ──────────────────────────────────────────────────────

def numeric_stats(values):
    """Compute descriptive statistics for numeric values."""
    numbers = []
    for v in values:
        ok, num = try_float(v)
        if ok and not is_missing(v):
            numbers.append(num)
    if not numbers:
        return None

    n = len(numbers)
    mean_val = sum(numbers) / n
    min_val = min(numbers)
    max_val = max(numbers)
    med_val = median(numbers)
    if n > 1:
        var = sum((x - mean_val) ** 2 for x in numbers) / (n - 1)
        std_val = math.sqrt(var)
    else:
        std_val = 0.0

    return {
        "count": n,
        "mean": mean_val,
        "min": min_val,
        "max": max_val,
        "median": med_val,
        "std_dev": std_val,
    }


def categorical_stats(values):
    """Compute descriptive statistics for categorical values."""
    clean = [normalize(v) for v in values if not is_missing(v)]
    if not clean:
        return {"count": 0, "unique": 0, "mode": None, "mode_freq": 0, "top5": []}

    counter = Counter(clean)
    mode_val, mode_freq = counter.most_common(1)[0]
    top5 = counter.most_common(MAX_TOP_VALUES)

    return {
        "count": len(clean),
        "unique": len(counter),
        "mode": mode_val,
        "mode_freq": mode_freq,
        "top5": top5,
    }


# ─── Data Loading ────────────────────────────────────────────────────

def load_csv(file_path):
    """Load CSV and return (list_of_row_dicts, list_of_column_names)."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = list(reader)
    return rows, columns


def columns_dict(rows, col_names):
    """Organize rows into a {col_name: [values]} mapping."""
    cols = {c: [] for c in col_names}
    for row in rows:
        for c in col_names:
            cols[c].append(normalize(row.get(c, "")))
    return cols


# ─── Printing ────────────────────────────────────────────────────────

def fmt(value, decimals=6):
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)


def print_header(title):
    print("\n" + "=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def print_dataset_overview(rows, col_names, label="DATASET"):
    print_header(f"{label} OVERVIEW")
    print(f"  Total rows   : {len(rows)}")
    print(f"  Total columns: {len(col_names)}")
    print("\n  Column names:")
    for c in col_names:
        print(f"    - {c}")


def print_missing_summary(cols):
    print_header("MISSING VALUES BY COLUMN")
    total = len(next(iter(cols.values()))) if cols else 0
    for name, values in cols.items():
        miss = sum(1 for v in values if is_missing(v))
        pct = (miss / total * 100) if total else 0
        print(f"  {name}: {miss} ({pct:.2f}%)")


def print_column_analysis(cols, heading="COLUMN-BY-COLUMN DESCRIPTIVE STATISTICS"):
    print_header(heading)
    total = len(next(iter(cols.values()))) if cols else 0

    for name, values in cols.items():
        col_type = infer_column_type(values)
        miss = sum(1 for v in values if is_missing(v))
        non_miss = total - miss

        print("\n" + "-" * WIDTH)
        print(f"  Column                 : {name}")
        print(f"  Inferred type          : {col_type}")
        print(f"  Non-missing count      : {non_miss}")
        print(f"  Missing count          : {miss}")

        if col_type == "numeric":
            stats = numeric_stats(values)
            if stats is None:
                print("  (no valid numeric values)")
            else:
                print(f"  Count                  : {stats['count']}")
                print(f"  Mean                   : {fmt(stats['mean'])}")
                print(f"  Min                    : {fmt(stats['min'])}")
                print(f"  Max                    : {fmt(stats['max'])}")
                print(f"  Median                 : {fmt(stats['median'])}")
                print(f"  Std Dev                : {fmt(stats['std_dev'])}")
        else:
            stats = categorical_stats(values)
            print(f"  Count                  : {stats['count']}")
            print(f"  Unique values          : {stats['unique']}")
            print(f"  Mode                   : {stats['mode']}")
            print(f"  Mode frequency         : {stats['mode_freq']}")
            print(f"  Top {MAX_TOP_VALUES} values:")
            for val, freq in stats["top5"]:
                display = val if len(val) <= 60 else val[:57] + "..."
                print(f"    - {display}: {freq}")


# ─── Grouped Analysis ────────────────────────────────────────────────

def group_rows(rows, group_keys):
    """
    Partition rows into groups keyed by the given column(s).
    Returns dict: tuple_of_key_values -> [rows_in_group]
    """
    groups = defaultdict(list)
    for row in rows:
        key = tuple(normalize(row.get(k, "")) for k in group_keys)
        groups[key].append(row)
    return groups


def print_grouped_analysis(rows, col_names, group_keys):
    key_label = " + ".join(group_keys)
    print_header(f"GROUPED ANALYSIS BY: {key_label}")

    groups = group_rows(rows, group_keys)
    print(f"  Total groups: {len(groups)}")

    # Sort groups by size descending and print top N
    sorted_groups = sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True)

    # Determine which columns to aggregate (exclude the group keys themselves)
    agg_cols = [c for c in col_names if c not in group_keys]

    for idx, (key_vals, group_rows_list) in enumerate(sorted_groups):
        if idx >= MAX_GROUPS_PRINTED:
            remaining = len(sorted_groups) - MAX_GROUPS_PRINTED
            print(f"\n  ... and {remaining} more groups (omitted for brevity)")
            break

        key_display = " | ".join(
            f"{k}={v[:40]}" for k, v in zip(group_keys, key_vals)
        )
        print(f"\n{'~' * WIDTH}")
        print(f"  Group: {key_display}")
        print(f"  Rows : {len(group_rows_list)}")

        # Build column data for this group
        group_cols = {c: [] for c in agg_cols}
        for row in group_rows_list:
            for c in agg_cols:
                group_cols[c].append(normalize(row.get(c, "")))

        # Print only numeric column summaries for groups (to keep output manageable)
        for c in agg_cols:
            col_type = infer_column_type(group_cols[c])
            if col_type == "numeric":
                stats = numeric_stats(group_cols[c])
                if stats and stats["count"] > 0:
                    print(f"    {c}:")
                    print(f"      count={stats['count']}  mean={fmt(stats['mean'],2)}"
                          f"  min={fmt(stats['min'],2)}  max={fmt(stats['max'],2)}"
                          f"  median={fmt(stats['median'],2)}  std={fmt(stats['std_dev'],2)}")
            elif col_type == "categorical":
                stats = categorical_stats(group_cols[c])
                if stats["count"] > 0 and stats["unique"] <= 20:
                    print(f"    {c}: unique={stats['unique']}  mode={stats['mode']} ({stats['mode_freq']})")


# ─── Main ────────────────────────────────────────────────────────────

def detect_group_keys(col_names):
    """Detect applicable grouping strategies based on available columns."""
    strategies = []
    if "page_id" in col_names:
        strategies.append(["page_id"])
    if "page_id" in col_names and "ad_id" in col_names:
        strategies.append(["page_id", "ad_id"])
    return strategies


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pure_python_stats.py <path_to_csv>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    print(f"\nLoading: {file_path}")
    rows, col_names = load_csv(file_path)
    cols = columns_dict(rows, col_names)

    # ── Dataset-level analysis ──
    print_dataset_overview(rows, col_names, label=file_path.stem)
    print_missing_summary(cols)
    print_column_analysis(cols)

    # ── Grouped analysis ──
    group_strategies = detect_group_keys(col_names)
    for keys in group_strategies:
        print_grouped_analysis(rows, col_names, keys)

    print("\n" + "=" * WIDTH)
    print("Analysis complete.")
    print("=" * WIDTH)


if __name__ == "__main__":
    main()
