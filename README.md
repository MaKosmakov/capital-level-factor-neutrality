# Capital-Level Factor Neutrality with Projected Partial Rebalancing

This repository contains replication materials for the paper:

**Capital-Level Factor Neutrality with Projected Partial Rebalancing**

Paper link: [to be added]

This repository contains the reference implementation, processed support files,
and scripts used to reproduce the reported tables and figures from the processed
research panels.

## Contents

- `src/neutral_coordinates.py` — reference implementation of neutral-coordinate
  construction and projected partial rebalancing.
- `scripts/regenerate_figures.py` — regenerates the two reported figure PDFs
  from processed CSV files.
- `scripts/validate_processed_results.py` — checks processed support files
  against paper terminology and headline diagnostics.
- `data/processed/*.csv` — processed table and figure support files.

The processed CSV files are not raw market data. Vendor-restricted or
license-restricted source data are not redistributed.

## Replication Checks

Install the Python dependency set if needed:

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

The validation script checks that the processed files use the paper terminology,
have no local path leakage, preserve numerical-level exposure leakage for
neutral-coordinate candidates, and retain the reported structural diagnostic
counts.

## License

The code and repository documentation are released under the MIT License. The
processed support files are included for replication of the reported tables and
figures. Vendor-restricted or license-restricted source data are not
redistributed, and this repository does not grant rights to any underlying
third-party source data.
