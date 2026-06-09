# Capital-Level Factor Neutrality with Projected Partial Rebalancing

This repository accompanies the paper:

**Capital-Level Factor Neutrality with Projected Partial Rebalancing**

Paper link: [to be added]

It contains the small reference implementation, the processed support files, and
the scripts used to reproduce the reported tables and figures. The paper itself
is not stored here; this repo is for the code and replication data.

## Contents

- `src/neutral_coordinates.py` — the neutral-coordinate
  construction and projected partial rebalancing.
- `scripts/regenerate_figures.py` — regenerates the two figure PDFs
  from processed CSV files.
- `scripts/validate_processed_results.py` — checks that the processed files
  match the reported terminology and headline diagnostics.
- `data/processed/*.csv` — processed inputs for the tables and figures.

The CSV files are processed research outputs, not raw market data. Vendor- or
licence-restricted source data are not redistributed.

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
checked. Vendor- or licence-restricted source data are not redistributed, and
this repository does not grant rights to any underlying third-party data.
