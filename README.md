# Capital-Level Factor Neutrality with Projected Partial Rebalancing

This repository contains the double-blind manuscript source for the paper:

**Capital-Level Factor Neutrality with Projected Partial Rebalancing**

The manuscript studies neutral-coordinate portfolio construction, where factor neutrality is imposed on implemented capital weights rather than on the input alpha signal. It also includes a projected partial-rebalancing rule that preserves neutrality while controlling turnover.

## Contents

- `capital_level_factor_neutrality.tex` — main LaTeX manuscript source.
- `capital_level_factor_neutrality.pdf` — compiled manuscript PDF.
- `figures/neutral_coordinate_tradeoff_scatter.pdf` — turnover/Sharpe tradeoff figure.
- `figures/cost_sensitivity_delta_sharpe.pdf` — transaction-cost sensitivity figure.

The bibliography is embedded in the manuscript source. No external `.bib` file is required.

## Build

From the repository root:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error capital_level_factor_neutrality.tex
```

The source has been checked to compile with TeX Live 2024.
