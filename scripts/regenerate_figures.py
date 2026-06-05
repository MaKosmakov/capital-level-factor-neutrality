#!/usr/bin/env python3
"""Regenerate manuscript figures from processed CSV support files."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"


PAPER_LABELS = {
    "defensive_momentum_nc": "Defensive\nmomentum",
    "ensemble_continuous_nc": "Ensemble continuous",
    "reversal_continuous_nc": "Reversal continuous",
}

COLORS = {
    "defensive_momentum_nc": "#0047ff",
    "ensemble_continuous_nc": "#d7191c",
    "reversal_continuous_nc": "#a66a33",
}


def style_axes(ax: plt.Axes) -> None:
    ax.grid(True, color="#d9d9d9", linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#777777")


def save_tradeoff_scatter() -> None:
    table = pd.read_csv(DATA / "aggregate_benchmark.csv")
    full_target_sharpe = float(table.loc[table["strategy_id"] == "full_neutral_target", "avg_sharpe"].iloc[0])
    rows = table[table["strategy_id"].isin(PAPER_LABELS)].copy()
    rows["delta_sharpe"] = rows["avg_sharpe"] - full_target_sharpe

    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    for _, row in rows.iterrows():
        strategy = row["strategy_id"]
        x = float(row["turnover_reduction"])
        y = float(row["delta_sharpe"])
        marker_size = 260.0 + 1_200.0 * max(float(row["maxdd_improvement"]), 0.0)
        ax.scatter(
            x,
            y,
            s=marker_size,
            color=COLORS[strategy],
            edgecolor="black",
            linewidth=0.8,
            zorder=3,
        )

        if strategy == "defensive_momentum_nc":
            ax.annotate(
                PAPER_LABELS[strategy],
                xy=(x, y),
                xytext=(-18, -2),
                textcoords="offset points",
                ha="right",
                va="center",
            )
        else:
            ax.annotate(
                PAPER_LABELS[strategy],
                xy=(x, y),
                xytext=(18, 2),
                textcoords="offset points",
                ha="left",
                va="center",
            )

    ax.set_title("Projected partial neutral-coordinate tradeoff", pad=12)
    ax.set_xlabel("Average turnover reduction vs full neutral target")
    ax.set_ylabel("Average Sharpe improvement vs full neutral target")
    ax.set_xlim(0.05, 0.96)
    ax.set_ylim(0.17, 0.39)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "neutral_coordinate_tradeoff_scatter.pdf")
    plt.close(fig)


def save_cost_sensitivity() -> None:
    table = pd.read_csv(DATA / "cost_sensitivity_aggregate.csv")
    rows = table[table["strategy_id"].isin(PAPER_LABELS)].copy()
    rows = rows.sort_values(["strategy_id", "realised_cost_bps"])

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for strategy, group in rows.groupby("strategy_id", sort=False):
        label = PAPER_LABELS[strategy].replace("\n", " ")
        ax.plot(
            group["realised_cost_bps"],
            group["avg_delta_sharpe_vs_full_target"],
            marker="o",
            linewidth=2.0,
            markersize=5.0,
            color=COLORS[strategy],
            label=label,
        )

    ax.axhline(0.0, color="#555555", linewidth=0.8)
    ax.set_title("Transaction-cost sensitivity", pad=12)
    ax.set_xlabel("Realised cost, bps")
    ax.set_ylabel("Average delta Sharpe vs full neutral target")
    ax.set_xlim(-2.0, 102.0)
    style_axes(ax)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(FIGURES / "cost_sensitivity_delta_sharpe.pdf")
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    save_tradeoff_scatter()
    save_cost_sensitivity()
    print("Regenerated manuscript figures in figures/")


if __name__ == "__main__":
    main()
