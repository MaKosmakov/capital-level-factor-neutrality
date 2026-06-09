# Capital-Level Factor Neutrality with Projected Partial Rebalancing

This repository accompanies the paper:

**Capital-Level Factor Neutrality with Projected Partial Rebalancing**

Paper link: [to be added]

It contains the small reference implementation, the processed support files, and
the scripts used to reproduce the reported tables and figures. The paper itself
is not stored here; this repo is for the code and replication data.

## What This Project Studies

The paper looks at factor-neutral portfolio construction at the level of traded
capital weights. A common workflow removes factor exposure from the alpha signal
before optimisation. That can help interpret the signal, but later construction
steps can still change the exposures of the portfolio that is actually traded.

The implementation here uses neutral coordinates: at each rebalance, the chosen
exposure matrix defines a neutral subspace, and the portfolio optimiser works
inside that subspace. The project also includes a projected partial-rebalancing
rule: before trading part way toward a new neutral target, the old holding is
projected into the current neutral subspace.

In the processed validation panels, the neutral-coordinate portfolios have
exposure leakage at numerical precision. The projected partial variants reduce
turnover relative to the full neutral target while staying in the monitored
neutral subspace.

## Contents

- `src/neutral_coordinates.py` — the neutral-coordinate
  construction and projected partial rebalancing.
- `scripts/regenerate_figures.py` — regenerates the two figure PDFs
  from processed CSV files.
- `scripts/validate_processed_results.py` — checks that the processed files
  match the reported terminology and headline diagnostics.
- `data/processed/*.csv` — processed inputs for the tables and figures.

The CSV files are processed research outputs derived from public data sources,
not raw source downloads.

## Reproduce the Checks

Install the Python dependencies if needed:

```bash
python3 -m pip install -r requirements.txt
```

Run the consistency checks:

```bash
python3 scripts/validate_processed_results.py
```

Regenerate the figures:

```bash
python3 scripts/regenerate_figures.py
```

The validation script checks for stale terminology, local path leakage,
neutral-coordinate exposure leakage, and the reported structural diagnostic
counts.

## License

The code and repository documentation are released under the MIT License. The
processed support files are included so the reported tables and figures can be
checked. Source data were obtained from public sources; this repository
distributes the processed research outputs used for replication, not the
underlying raw downloads.
