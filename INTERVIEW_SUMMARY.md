# Interview Summary

## Initial Idea

The starting question was simple: if an active manager wants a factor-neutral
portfolio, where should the neutrality constraint be enforced? A common workflow
residualises the alpha signal first, then sends that signal into the optimiser.
The project asks whether that is enough, or whether neutrality has to be imposed
directly on the capital weights that are actually traded.

## What I Tried

- Built a neutral-coordinate construction: given an exposure matrix, compute a
  basis for the neutral subspace and optimise only inside that subspace.
- Compared ordinary alpha, residualised alpha, the full neutral target, and
  projected partial neutral-coordinate portfolios.
- Added projected partial rebalancing to reduce turnover: first project the old
  holding into the current neutral subspace, then trade part way toward the new
  neutral target.
- Ran walk-forward checks across several processed research panels, with
  turnover, Sharpe, drawdown, exposure leakage, cost sensitivity, and
  exposure-stress diagnostics.

## What Failed and Why

- Residualising the alpha signal did not guarantee a neutral implemented
  portfolio. The risk model and optimisation step can rotate a residualised
  signal back into exposure directions, so the traded capital weights can still
  carry factor exposure.
- Direct partial rebalancing from yesterday's portfolio was also not enough.
  Yesterday's neutral portfolio may not be neutral under today's exposure
  matrix, because the universe, volatility estimates, and exposure matrix change
  over time.
- The full neutral target gave clean exposure control, but it can trade too much.
  That motivated the projected partial rule rather than a direct jump to the
  new target at every rebalance.

## What Worked

The neutral-coordinate construction enforces neutrality at the level of the
implemented weights. The projected partial rule keeps the rebalancing path inside
the current neutral subspace while reducing turnover relative to the full neutral
target. In the processed validation panels, neutral-coordinate portfolios have
exposure leakage at numerical precision, while the projected partial variants
reduce turnover under the fixed validation choices.

## How I Would Explain It in an Interview

I would say: I started from a common but slightly unsafe portfolio-construction
shortcut: neutralise the signal and hope the final portfolio is neutral. The
main lesson was that neutrality is a property of traded weights, not just of the
input signal. The optimiser, risk model, scaling, and rebalancing rule can all
change exposures. So I moved the constraint into the capital-allocation step by
optimising in neutral coordinates. Then I added a projection step for dynamic
rebalancing, because yesterday's neutral book may not be neutral under today's
exposure matrix. The result is a small construction module that is easy to audit:
after every rebalance, one can check the actual exposure of the implemented
portfolio.
