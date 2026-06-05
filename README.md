# Capital-Level Factor Neutrality with Projected Partial Rebalancing

This repository contains the double-blind manuscript source for the paper:

**Capital-Level Factor Neutrality with Projected Partial Rebalancing**

The manuscript studies neutral-coordinate portfolio construction, where factor neutrality is imposed on implemented capital weights rather than on the input alpha signal. It also includes a projected partial-rebalancing rule that preserves neutrality while controlling turnover.

## Contents

- `capital_level_factor_neutrality.tex` — main LaTeX manuscript source.
- `capital_level_factor_neutrality.pdf` — compiled manuscript PDF.
- `figures/neutral_coordinate_tradeoff_scatter.pdf` — turnover/Sharpe tradeoff figure.
- `figures/cost_sensitivity_delta_sharpe.pdf` — transaction-cost sensitivity figure.
- `src/neutral_coordinates.py` — compact reference implementation of the neutral-coordinate construction and projected partial rebalance.
- `scripts/regenerate_figures.py` — regenerates the two manuscript figures from processed CSV files.
- `scripts/validate_processed_results.py` — checks processed support files against the manuscript terminology and headline diagnostics.
- `data/processed/*.csv` — processed table and figure support files.

The bibliography is embedded in the manuscript source. No external `.bib` file is required. The processed CSV files are not raw market data; vendor-restricted or license-restricted source data are not redistributed.

## Replication Checks

Install the small Python dependency set if needed:

```bash
python3 -m pip install -r requirements.txt
```

Validate the processed support files:

```bash
python3 scripts/validate_processed_results.py
```

Regenerate the figures:

```bash
python3 scripts/regenerate_figures.py
```

The validation script checks that the processed files use the manuscript terminology, have no local path leakage, preserve numerical-level exposure leakage for neutral-coordinate candidates, and retain the reported structural diagnostic counts.

## Build

From the repository root:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error capital_level_factor_neutrality.tex
```

The source has been checked to compile with TeX Live 2024.
