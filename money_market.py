import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    M = mo.ui.slider(1000, 5000, step=25, value=1500, label="$M$", show_value=True)
    Y = mo.ui.slider(1000, 4000, step=50, value=2000, label="$Y$", show_value=True)
    P = mo.ui.slider(1, 10, step=0.5, value=5, label="$P$", show_value=True)
    return M, P, Y


@app.cell(hide_code=True)
def _(M, P, Y, mo, np, plt):
    a = 10
    b = 1.8*a

    _i_star = (P.value * a*Y.value) / (b*M.value)
    _i_plot = max(_i_star, 0.0)

    _fig, _ax = plt.subplots(figsize=(6.5, 6))

    # Money demand curves (i in percent on the y-axis)
    _i = np.linspace(0, 25, 200)
    _ax.plot((P.value * a*Y.value) / (b*_i), _i , color="tab:blue", lw=2.5, label="Money demand $M^d$")

    # Money supply (vertical)
    _ax.axvline(M.value, color="black", lw=1.5, label="Money supply $M^s$")

    # Equilibrium
    _ax.plot(M.value, _i_plot, "o", color="tab:red", ms=8, zorder=5)
    _ax.hlines(_i_plot, 0, M.value, color="tab:red", ls=":", lw=1)
    _ax.annotate(f"{round(_i_star, 2)}%", (M.value, _i_plot), xytext=(8, 6), textcoords="offset points", color="tab:red")

    _ax.set_xlim(0, 5000)
    _ax.set_ylim(0, 25)
    _ax.set_xlabel("Money, M")
    _ax.set_ylabel("Interest rate, i (%)")
    _ax.set_title("Money Market Equilibrium")
    _ax.legend(loc="upper right")
    _ax.grid(alpha=0.3)
    plt.close(_fig)

    _stats = mo.md(
        f"**Money supply M:** {M.value:,.0f}  \n"
        f"**Real income \\Y:** {Y.value:,.0f}  \n"
        f"**Price Level \\P:** {P.value:,.2f}  \n"
        f"**Equilibrium interest rate i\\*:** {_i_plot:.2f} %"
    )

    mo.hstack(
        [mo.vstack([M, Y, P, _stats], gap=1), mo.as_html(_fig)],
        widths=[1.2, 2],
        align="center",
        gap=2,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Nominal Money demand: $M^D = YPL(i) = €\underset{+}{Y}L(\underset{-}{i}$
    ### Equilibrium: $M^D = M^S$

    - $M$ money supply, set by the central bank
    - $Y$ nominal income, €Y real income
    - $P$ price level
    - $i$ nominal interest rate
    """)
    return


if __name__ == "__main__":
    app.run()
