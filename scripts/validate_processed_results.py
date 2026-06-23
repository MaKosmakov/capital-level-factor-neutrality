#!/usr/bin/env python3
"""Validate processed support files against the reported paper diagnostics."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_aggregate_table() -> None:
    rows = read_csv("aggregate_benchmark.csv")
    strategy_ids = {row["strategy_id"] for row in rows}
    expected = {
        "ordinary_alpha",
        "residualised_alpha",
        "full_neutral_target",
        "defensive_momentum_nc",
        "ensemble_continuous_nc",
        "reversal_continuous_nc",
    }
    require(strategy_ids == expected, "aggregate_benchmark.csv has unexpected strategy ids")

    neutral_rows = [
        row
        for row in rows
        if row["strategy_id"] == "full_neutral_target" or row["strategy_id"].endswith("_nc")
    ]
    for row in neutral_rows:
        require(
            float(row["max_exposure"]) < 1.0e-8,
            f"neutral exposure too large for {row['strategy_id']}",
        )


def validate_structural_counts() -> None:
    rows = {row["experiment"]: row for row in read_csv("structural_summary.csv")}
    expected = {
        "Order sweep exact neutrality": (24, 24),
        "Signal sweep beats residualisation": (32, 36),
        "Exposure-stress robustness": (96, 96),
    }
    for experiment, (passed, total) in expected.items():
        row = rows.get(experiment)
        require(row is not None, f"missing structural diagnostic {experiment}")
        require(int(row["pass"]) == passed and int(row["total"]) == total, experiment)


def validate_data_scope() -> None:
    rows = read_csv("data_quality_audit.csv")
    large_cap = [row for row in rows if row["universe"] == "US large-cap sample"]
    require(len(large_cap) == 1, "US large-cap sample row is missing or duplicated")
    require(int(large_cap[0]["n_assets"]) == 48, "US large-cap sample should have 48 assets")
    require("source_path" not in rows[0], "data_quality_audit.csv should not expose local paths")


def validate_exposure_sensitivity() -> None:
    for row in read_csv("exposure_sensitivity.csv"):
        require(int(row["rank_failures"]) == 0, "rank failures found in exposure sensitivity sweep")
        require(float(row["max_exposure"]) < 1.0e-8, "exposure sensitivity leakage is too large")


def validate_cost_sensitivity() -> None:
    for row in read_csv("cost_sensitivity_aggregate.csv"):
        require(float(row["max_abs_exposure"]) < 1.0e-8, "cost sensitivity leakage is too large")


def main() -> None:
    validate_aggregate_table()
    validate_structural_counts()
    validate_data_scope()
    validate_exposure_sensitivity()
    validate_cost_sensitivity()
    print("Processed support files passed diagnostic checks.")


if __name__ == "__main__":
    main()
