#!/usr/bin/env python3
"""
BinLookup Delta Reference App — B' = R

Demonstrates how a customer can validate that a BinLookup delta correctly
transforms their local base snapshot into the current live BIN ranges:

    B' = R

Where:
    B  — the customer's locally stored base snapshot CSV.
    D  — the delta retrieved for B's snapshot ID.
    B' — the local result of applying D to B (computed by this script).
    R  — the current live BIN ranges, downloaded from /bin-ranges.

The script fetches D and R from the API, applies D to B to compute B', then
compares B' against R. If they match exactly, the delta is valid.

Usage:
python Examples/delta-example.py \
    --config Examples/config.json \
    --input-snapshot-base Examples/snapshot_3355.csv \
    --save-csv
"""
import argparse
import os
import re
import sys
from copy import deepcopy

from delta_example_helpers import (
    make_signer,
    fetch_delta, download_snapshot_r,
    apply_delta,
    build_field_mapping, normalize_row, compare,
    write_csv_file, load_csv,
)
from delta_example_helpers.config import load_config as _load_config, get_signer_from_block


def snapshot_id_from_filename(path):
    """
    Extract the snapshot ID embedded in a base snapshot's filename.

    The tutorial expects filenames such as ``snapshot_3355.csv``, where the
    trailing integer (3355) is the snapshot ID used to look up its delta via
    ``/bin-ranges/deltas/snapshots/{snapshotId}``.

    Raises:
        ValueError: if the filename does not contain an integer.
    """
    match = re.search(r"(\d+)", os.path.basename(path))
    if not match:
        raise ValueError(
            f"Cannot derive snapshot ID from '{os.path.basename(path)}'. "
            "Filename must contain an integer (e.g. snapshot_3355.csv)."
        )
    return int(match.group(1))


def load_config(path):
    """
    Load and validate the tutorial's config.json.

    This tutorial only ever authenticates as a standard customer (it never
    calls admin-only internal snapshot endpoints), so the config must
    contain a valid 'customer' credentials block.
    """
    config = _load_config(path)
    get_signer_from_block(
        {
            "consumerKey": config["consumerKey"],
            "keystoreP12Path": config["keystoreP12Path"],
            "keystorePassword": config["keystorePassword"],
        },
        "customer",
    )
    return config


def main():
    """Run the full B' = R validation workflow and exit 0 on PASS, 1 on FAIL."""
    parser = argparse.ArgumentParser(description="BinLookup Delta Ref App — B' = R")
    parser.add_argument(
        "--config", required=True,
        help="Path to the JSON config file containing the API host and customer credentials.",
    )
    parser.add_argument(
        "--input-snapshot-base", required=True,
        help="Path to the base snapshot CSV (B), e.g. snapshot_3355.csv.",
    )
    parser.add_argument(
        "--save-csv", action="store_true",
        help="Save D, R and B' as CSV files next to the input snapshot for inspection.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    base_url = config["host"]
    signer = make_signer(
        config["consumerKey"],
        config["keystoreP12Path"],
        config["keystorePassword"],
    )
    snapshot_id = snapshot_id_from_filename(args.input_snapshot_base)
    output_dir = os.path.dirname(os.path.abspath(args.input_snapshot_base))

    # Step 1 — Load B (the base snapshot) from the local CSV file.
    _, base_rows = load_csv(args.input_snapshot_base)
    print(f"[1/4] Loading B from {args.input_snapshot_base}...  {len(base_rows)} rows")

    # Step 2 — Fetch D (the delta) for this snapshot ID from the API.
    delta_items, _ = fetch_delta(base_url, snapshot_id, signer)
    operation_counts = {
        op: sum(1 for item in delta_items if item.get("operation") == op)
        for op in "IUD"
    }
    print(f"[2/4] Fetching delta D (snapshot {snapshot_id})...  "
        f"{len(delta_items)} items  "
        f"I={operation_counts['I']} U={operation_counts['U']} D={operation_counts['D']}")

    # Step 3 — Download R (the current live snapshot) via /bin-ranges.
    live_rows_raw = download_snapshot_r(base_url, signer)
    print(f"[3/4] Downloading R via /bin-ranges...  {len(live_rows_raw)} rows")

    # Step 4 — Align B's field names with R's, apply D to B to compute B',
    # then compare B' against R.
    base_fields = list(base_rows[0].keys()) if base_rows else []
    live_fields = list(live_rows_raw[0].keys()) if live_rows_raw else []
    field_mapping = build_field_mapping(base_fields, live_fields)

    base_rows_normalized = [normalize_row(row, field_mapping) for row in base_rows]
    live_rows_normalized = [
        {field: str(row.get(field, "") or "") for field in live_fields}
        for row in live_rows_raw
    ]
    result_rows = deepcopy(base_rows_normalized)  # this becomes B'

    stats = apply_delta(result_rows, delta_items, field_mapping)

    print(f"[4/4] Applying D to B -> B' and comparing...  {len(result_rows)} rows")
    print(f"      Applied: I={stats['I']} U={stats['U']} D={stats['D']} skipped={stats['skip']}")

    only_in_result, only_in_live, mismatches = compare(result_rows, live_rows_normalized)

    print(f"\n  Rows only in B':   {len(only_in_result)}")
    print(f"  Rows only in R:    {len(only_in_live)}")
    print(f"  Field mismatches:  {len(mismatches)}")

    # Optional: persist D, R and B' as CSV files so a failure can be
    # inspected offline without repeating the API calls.
    if args.save_csv:
        write_csv_file(
            os.path.join(output_dir, f"D_{snapshot_id}.csv"),
            [
                {field_name: str(field_value or "") for field_name, field_value in item.items()}
                for item in delta_items
            ],
        )
        write_csv_file(os.path.join(output_dir, f"R_{snapshot_id}.csv"), live_rows_normalized)
        write_csv_file(os.path.join(output_dir, f"B_prime_{snapshot_id}.csv"), result_rows)

    passed = not (only_in_result or only_in_live or mismatches)
    verdict = "✅ PASS: B' = R" if passed else "❌ FAIL: B' ≠ R"
    print(f"\n{verdict}\n")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
