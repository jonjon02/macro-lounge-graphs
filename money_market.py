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
    M = mo.ui.slider(200, 1500, step=25, value=600, label="$M$", show_value=True)
    Y = mo.ui.slider(1000, 4000, step=50, value=2000, label="$\\$Y$", show_value=True)
    P = mo.ui.slider(1, 10, step=0.5, value=5, label="$\\$Y$", show_value=True)
    return M, Y, P


@app.cell(hide_code=True)
def _(M, P, Y, mo, np, plt):
    _k = 0.5
    h = 0.2


    # Baseline (default values) as grey reference curve
    _base_Y, _base_h, _base_M = 2000, 2.5, 600

    _i_star = (_k - M.value / Y.value * P.value) / h.value
    _trap = _i_star < 0
    _i_plot = max(_i_star, 0.0)

    _xmax = 2000
    _ymax = 25  # percent

    _fig, _ax = plt.subplots(figsize=(6.5, 6))

    # Money demand curves (i in percent on the y-axis)
    _i = np.linspace(0, _k / h.value, 200)
    _ax.plot(((P.value * Y.value) / 5 * M.value) , color="tab:blue", lw=2.5, label="Money demand $M^d$")

    # Money supply (vertical)
    _ax.axvline(M.value, color="black", lw=1.5, label="Money supply $M^s$")
    _ax.axvline(_base_M, color="grey", ls=":", lw=1)

    # Equilibrium
    _ax.plot(M.value, _i_plot * 100, "o", color="tab:red", ms=8, zorder=5)
    _ax.hlines(_i_plot * 100, 0, M.value, color="tab:red", ls=":", lw=1)
    _ax.annotate("A", (M.value, _i_plot * 100), xytext=(8, 6), textcoords="offset points", color="tab:red")

    _ax.set_xlim(0, _xmax)
    _ax.set_ylim(0, _ymax)
    _ax.set_xlabel("Money, M")
    _ax.set_ylabel("Interest rate, i (%)")
    _ax.set_title("Money Market Equilibrium")
    _ax.legend(loc="upper right")
    _ax.grid(alpha=0.3)
    plt.close(_fig)

    _stats = mo.md(
        f"**Money supply M:** {M.value:,.0f}  \n"
        f"**Nominal income \\$Y:** {Y.value:,.0f}  \n"
        f"**Equilibrium interest rate i\\*:** {_i_plot * 100:.2f} %"
        + ("\n\n⚠️ Money supply exceeds demand even at i = 0 (zero lower bound)." if _trap else "")
    )

    mo.hstack(
        [mo.vstack([M, Y, h, _stats], gap=1), mo.as_html(_fig)],
        widths=[1.2, 2],
        align="center",
        gap=2,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Money demand: $M^d = \$Y \, L(i) = \$Y \,(k - h\,i)$
    ### Equilibrium: $M = \$Y\,(k - h\,i) \;\Rightarrow\; i^* = \dfrac{1}{h}\left(k - \dfrac{M}{\$Y}\right)$

    - $M$ money supply, set by the central bank
    - $\$Y$ nominal income
    - $h$ interest sensitivity of money demand
    - $k$ money demand per unit of nominal income at $i = 0$, fixed at $0.5$
    """)
    return


if __name__ == "__main__":
    app.run()
