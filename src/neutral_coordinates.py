"""Reference implementation of neutral-coordinate portfolio construction.

The functions in this module follow the notation of the manuscript:

* ``F`` is the monitored exposure matrix.
* ``Q`` is an orthonormal basis of ``ker(F.T)``.
* ``u`` is the implemented capital-weight vector.
* ``theta`` is the coordinate vector inside the neutral subspace.
* ``beta`` is the projected partial-rebalancing coefficient.

This is a compact, paper-facing implementation.  It is intended to document the
construction layer and support replication checks, not to replace a production
trading system or a full data pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


Array = np.ndarray


@dataclass
class NeutralBasis:
    """Computed basis for the current neutral subspace."""

    q: Array
    rank: int
    tolerance: float
    residual_norm: float

    @property
    def dimension(self) -> int:
        return int(self.q.shape[1])


@dataclass
class PartialRebalanceResult:
    """Result of one projected partial neutral-coordinate rebalance."""

    portfolio: Array
    beta: float
    objective: float
    turnover: float
    projected_turnover: float
    max_abs_exposure: float
    full_neutral_target: Array
    projected_previous: Array
    basis: NeutralBasis


def as_vector(values: Iterable[float] | Array) -> Array:
    """Return a one-dimensional floating-point array."""

    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1:
        raise ValueError("expected a one-dimensional vector")
    return vector


def standardize_cross_section(values: Iterable[float] | Array) -> Array:
    """Center and scale one cross-section.

    A zero-dispersion cross-section is returned as zeros.  This convention keeps
    exposure construction deterministic when a characteristic is constant.
    """

    vector = as_vector(values)
    centered = vector - np.nanmean(vector)
    scale = np.nanstd(centered)
    if not np.isfinite(scale) or scale <= 0.0:
        return np.zeros_like(centered)
    return centered / scale


def build_polynomial_exposures(
    characteristic: Iterable[float] | Array,
    *,
    degree: int = 3,
    include_intercept: bool = True,
    standardize_columns: bool = True,
) -> Array:
    """Build ``[1, x, x^2, ..., x^degree]`` exposure columns.

    In the manuscript implementation, ``characteristic`` is the trailing
    volatility characteristic.  The construction itself works for any monitored
    characteristic chosen by the portfolio manager.
    """

    if degree < 1:
        raise ValueError("degree must be at least one")

    x = as_vector(characteristic)
    columns: list[Array] = []
    if include_intercept:
        columns.append(np.ones_like(x))

    for power in range(1, degree + 1):
        column = np.power(x, power)
        if standardize_columns:
            column = standardize_cross_section(column)
        columns.append(column)

    return np.column_stack(columns)


def compute_neutral_basis(
    exposures: Array,
    *,
    tolerance: float | None = None,
    relative_tolerance: bool = True,
) -> NeutralBasis:
    """Compute an orthonormal basis of ``ker(F.T)`` by singular value decomposition."""

    f = np.asarray(exposures, dtype=float)
    if f.ndim != 2:
        raise ValueError("exposures must be a two-dimensional matrix")

    _, singular_values, vt = np.linalg.svd(f.T, full_matrices=True)
    leading = float(singular_values[0]) if singular_values.size else 0.0

    if tolerance is None:
        absolute_tolerance = np.finfo(float).eps * max(f.shape) * max(leading, 1.0)
    elif relative_tolerance:
        absolute_tolerance = float(tolerance) * max(leading, 1.0)
    else:
        absolute_tolerance = float(tolerance)

    rank = int(np.sum(singular_values > absolute_tolerance))
    q = vt[rank:].T.copy()
    residual_norm = float(np.linalg.norm(f.T @ q, ord=2)) if q.size else 0.0
    return NeutralBasis(q=q, rank=rank, tolerance=absolute_tolerance, residual_norm=residual_norm)


def project_to_neutral(portfolio: Iterable[float] | Array, q: Array) -> Array:
    """Project a portfolio into the neutral subspace spanned by ``Q``."""

    u = as_vector(portfolio)
    q = np.asarray(q, dtype=float)
    if q.ndim != 2 or q.shape[0] != u.size:
        raise ValueError("basis dimension does not match portfolio length")
    return q @ (q.T @ u)


def gross_scale(portfolio: Iterable[float] | Array, gross_limit: float | None) -> Array:
    """Scale a portfolio to a gross-exposure limit when requested."""

    u = as_vector(portfolio)
    if gross_limit is None:
        return u
    gross = float(np.sum(np.abs(u)))
    if gross <= 0.0:
        return u
    return u * (float(gross_limit) / gross)


def solve_neutral_markowitz(
    alpha: Iterable[float] | Array,
    covariance: Array,
    q: Array,
    *,
    gamma: float,
    ridge: float = 1.0e-8,
    gross_limit: float | None = None,
) -> Array:
    """Solve the unconstrained neutral-coordinate Markowitz target.

    The objective is ``alpha.T @ u - gamma / 2 * u.T @ covariance @ u`` with
    ``u = Q theta``.  Optional gross scaling is scalar, so it preserves
    neutrality.
    """

    a = as_vector(alpha)
    sigma = np.asarray(covariance, dtype=float)
    q = np.asarray(q, dtype=float)
    if sigma.shape != (a.size, a.size):
        raise ValueError("covariance shape does not match alpha length")
    if q.ndim != 2 or q.shape[0] != a.size:
        raise ValueError("basis dimension does not match alpha length")
    if gamma <= 0.0:
        raise ValueError("gamma must be positive")
    if q.shape[1] == 0:
        return np.zeros_like(a)

    restricted_covariance = q.T @ sigma @ q
    if ridge > 0.0:
        restricted_covariance = restricted_covariance + float(ridge) * np.eye(q.shape[1])

    theta = np.linalg.solve(restricted_covariance, q.T @ a) / float(gamma)
    return gross_scale(q @ theta, gross_limit)


def rebalance_objective(
    beta: float,
    *,
    alpha: Array,
    covariance: Array,
    previous_holding: Array,
    projected_previous: Array,
    direction: Array,
    gamma: float,
    turnover_cost: float,
) -> float:
    """Evaluate the one-dimensional projected partial-rebalancing objective."""

    portfolio = projected_previous + float(beta) * direction
    markowitz = float(alpha @ portfolio - 0.5 * gamma * portfolio @ covariance @ portfolio)
    cost = float(turnover_cost) * float(np.sum(np.abs(portfolio - previous_holding)))
    return markowitz - cost


def choose_partial_rebalance_beta(
    *,
    alpha: Iterable[float] | Array,
    covariance: Array,
    previous_holding: Iterable[float] | Array,
    projected_previous: Iterable[float] | Array,
    full_neutral_target: Iterable[float] | Array,
    gamma: float,
    turnover_cost: float,
    beta_max: float = 1.0,
) -> tuple[float, float]:
    """Choose the globally optimal partial-rebalancing coefficient on ``[0, beta_max]``.

    The search uses the finite candidate set from the paper: endpoints,
    sign-change breakpoints of the turnover term, and interval-wise critical
    points.
    """

    a = as_vector(alpha)
    sigma = np.asarray(covariance, dtype=float)
    old = as_vector(previous_holding)
    u0 = as_vector(projected_previous)
    target = as_vector(full_neutral_target)

    if not (0.0 <= beta_max <= 1.0):
        raise ValueError("beta_max must lie in [0, 1]")
    if gamma <= 0.0:
        raise ValueError("gamma must be positive")
    if turnover_cost < 0.0:
        raise ValueError("turnover_cost must be non-negative")

    d = target - u0
    risk_along_direction = float(d @ sigma @ d)
    slope_without_turnover = float(a @ d - gamma * d @ sigma @ u0)

    breakpoints: list[float] = []
    for u0_i, d_i, old_i in zip(u0, d, old):
        if abs(d_i) <= 1.0e-15:
            continue
        beta_i = (old_i - u0_i) / d_i
        if 0.0 < beta_i < beta_max:
            breakpoints.append(float(beta_i))

    grid = sorted({0.0, float(beta_max), *breakpoints})
    candidates = set(grid)

    if risk_along_direction > 1.0e-15:
        for left, right in zip(grid[:-1], grid[1:]):
            if right - left <= 1.0e-15:
                continue
            midpoint = 0.5 * (left + right)
            signs = np.sign(u0 + midpoint * d - old)
            critical = (slope_without_turnover - turnover_cost * float(signs @ d)) / (
                gamma * risk_along_direction
            )
            if left < critical < right:
                candidates.add(float(critical))

    best_beta = 0.0
    best_value = -np.inf
    for candidate in sorted(candidates):
        value = rebalance_objective(
            candidate,
            alpha=a,
            covariance=sigma,
            previous_holding=old,
            projected_previous=u0,
            direction=d,
            gamma=gamma,
            turnover_cost=turnover_cost,
        )
        if value > best_value:
            best_beta = float(candidate)
            best_value = float(value)

    return best_beta, best_value


def projected_partial_rebalance(
    *,
    alpha: Iterable[float] | Array,
    covariance: Array,
    exposures: Array,
    previous_holding: Iterable[float] | Array,
    gamma: float,
    turnover_cost: float,
    beta_max: float = 1.0,
    gross_limit: float | None = None,
    ridge: float = 1.0e-8,
) -> PartialRebalanceResult:
    """Run one projected partial neutral-coordinate rebalance."""

    a = as_vector(alpha)
    sigma = np.asarray(covariance, dtype=float)
    f = np.asarray(exposures, dtype=float)
    old = as_vector(previous_holding)

    basis = compute_neutral_basis(f)
    projected_previous = project_to_neutral(old, basis.q)
    full_neutral_target = solve_neutral_markowitz(
        a,
        sigma,
        basis.q,
        gamma=gamma,
        ridge=ridge,
        gross_limit=gross_limit,
    )
    beta, objective = choose_partial_rebalance_beta(
        alpha=a,
        covariance=sigma,
        previous_holding=old,
        projected_previous=projected_previous,
        full_neutral_target=full_neutral_target,
        gamma=gamma,
        turnover_cost=turnover_cost,
        beta_max=beta_max,
    )

    portfolio = projected_previous + beta * (full_neutral_target - projected_previous)
    max_abs_exposure = float(np.max(np.abs(f.T @ portfolio))) if f.size else 0.0
    turnover = float(np.sum(np.abs(portfolio - old)))
    projected_turnover = float(np.sum(np.abs(portfolio - projected_previous)))

    return PartialRebalanceResult(
        portfolio=portfolio,
        beta=beta,
        objective=objective,
        turnover=turnover,
        projected_turnover=projected_turnover,
        max_abs_exposure=max_abs_exposure,
        full_neutral_target=full_neutral_target,
        projected_previous=projected_previous,
        basis=basis,
    )
