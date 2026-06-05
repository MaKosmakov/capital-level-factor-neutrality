# Processed Support Files

This folder contains processed CSV files used to support the manuscript tables,
figures, and appendix diagnostics.

The files are table-level and figure-level replication outputs. They are not
raw market data. Vendor-restricted or license-restricted source data are not
redistributed in this repository.

The strategy identifiers use the terminology of the manuscript:

- `full_neutral_target`
- `defensive_momentum_nc`
- `ensemble_continuous_nc`
- `reversal_continuous_nc`
- `ordinary_alpha`
- `residualised_alpha`

Run the validation script from the repository root with:

```bash
python3 scripts/validate_processed_results.py
```
