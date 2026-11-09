import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    c0 = mo.ui.slider(100, 400, step=10, value=200, label="$c_0$", show_value=True)
    c1 = mo.ui.slider(0.1, 0.8, step=0.05, value=0.6, label="$c_1$", show_value=True)
    T = mo.ui.slider(1000, 4000, step=50, value=2000, label="$T$", show_value=True)
    I = mo.ui.slider(0, 2000, step=50, value=500, label="$I$", show_value=True)
    G = mo.ui.slider(1000, 4000, step=50, value=2000, label="$G$", show_value=True)
    return G, I, T, c0, c1


@app.cell(hide_code=True)
def _(G, I, T, c0, c1, mo, np, plt):
    # Baseline (default values) as grey reference line, so shifts are visible
    _base_c1 = 0.6
    _base_auto = 200 - _base_c1 * 2000 + 500 + 2000

    _auto = c0.value - c1.value * T.value + I.value + G.value
    _mult = 1 / (1 - c1.value)
    _Ystar = _mult * _auto

    _ymax = max(8000, 1.2 * _Ystar)
    _Y = np.linspace(0, _ymax, 200)

    _fig, _ax = plt.subplots(figsize=(6.5, 6))
    _ax.plot(_Y, _Y, color="black", lw=1.5, label="Y = Z (45° line)")
    _ax.plot(_Y, _auto + c1.value * _Y, color="tab:blue", lw=2.5, label="ZZ")

    # Equilibrium (only drawn if positive)
    if _Ystar > 0:
        _ax.plot(_Ystar, _Ystar, "o", color="tab:red", ms=8, zorder=5)
        _ax.vlines(_Ystar, 0, _Ystar, color="tab:red", ls=":", lw=1)
        _ax.hlines(_Ystar, 0, _Ystar, color="tab:red", ls=":", lw=1)
        _ax.annotate("A", (_Ystar, _Ystar), xytext=(8, -14), textcoords="offset points", color="tab:red")

    _ax.set_xlim(0, _ymax)
    _ax.set_ylim(0, _ymax)
    _ax.set_xlabel("Income, Y")
    _ax.set_ylabel("Demand, Z / Production, Y")
    _ax.set_title("Goods Market Equilibrium")
    _ax.legend(loc="upper left")
    _ax.grid(alpha=0.3)
    plt.close(_fig)

    _stats = mo.md(
        f"**Autonomous spending:** {_auto:,.0f}  \n"
        f"**Multiplier:** {_mult:.2f}  \n"
        f"**Equilibrium output Y\\*:** {_Ystar:,.0f}"
        + ("" if _Ystar > 0 else "\n\n⚠️ No positive equilibrium for these values.")
    )

    mo.hstack(
        [mo.vstack([c0, c1, T, I, G, _stats], gap=1), mo.as_html(_fig)],
        widths=[1.2, 2],
        align="center",
        gap=2,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Demand: $Z = c_0 + c_1 (Y - T) + I + G$
    ### Equilibrium: $Y^* = \dfrac{1}{1 - c_1}\,\big(c_0 - c_1 T + I + G\big)$

    - $c_0$ autonomous consumption
    - $c_1$ marginal propensity to consume
    - $T$ taxes
    - $I$ investment
    - $G$ government spending
    """)
    return


if __name__ == "__main__":
    app.run()
