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
    c0 = mo.ui.slider(100, 400, step=10, value=250, label="$c_0$", show_value=True)
    c1 = mo.ui.slider(0.1, 0.8, step=0.05, value=0.6, label="$c_1$", show_value=True)
    T = mo.ui.slider(1000, 4000, step=50, value=2500, label="$T$", show_value=True)
    G = mo.ui.slider(1000, 4000, step=50, value=1700, label="$G$", show_value=True)
    I0 = mo.ui.slider(0, 2000, step=50, value=900, label="$\\bar{I}$", show_value=True)
    ibar = mo.ui.slider(0.5, 15, step=0.25, value=5, label="$\\bar{i}$", show_value=True)
    return G, I0, T, c0, c1, ibar


@app.cell(hide_code=True)
def _(G, I0, T, c0, c1, ibar, mo, np, plt):
    # --- Model -------------------------------------------------------------
    beta = 100

    def _autonomous(c0, c1, T, I0, G):
        # everything in demand that depends neither on Y nor on i
        return c0 - c1 * T + I0 + G

    def _is_curve(Y, A, c1, beta):
        # IS solved for i (in %): i = beta / ((1 - c1) Y - A), only right of the asymptote
        # Solved for $i$: &nbsp; $i = \dfrac{100}{(1 - c_1)\,Y - (c_0 - c_1 T + \bar{I} + G)}$
        denom = (1 - c1) * Y - A
        return np.where(denom > 0, beta / np.where(denom > 0, denom, 1) * 100, np.nan)

    def _equilibrium(A, c1, beta, i):
        # flat LM: plug i into IS and solve for Y
        return (A + beta / i) / (1 - c1)

    _A = _autonomous(c0.value, c1.value, T.value, I0.value, G.value)
    _i = ibar.value / 100  # slider is in %, the model works with decimals
    _Ystar = _equilibrium(_A, c1.value, beta, _i)
    _Y_asym = _A / (1 - c1.value)  # vertical asymptote of the IS curve
    _invest = I0.value + beta / _i

    _valid = _Ystar > 0
    _xmax = 20000
    _ymax = 15  # percent
    _Y = np.linspace(0, _xmax, 2000)

    # --- Plot --------------------------------------------------------------
    _fig, _ax = plt.subplots(figsize=(6.5, 6))
    _ax.plot(_Y, _is_curve(_Y, _A, c1.value, beta), color="tab:blue", lw=2.5, label="IS")
    _ax.axhline(ibar.value, color="tab:orange", lw=2.5, label="LM")

    if _valid:
        _ax.plot(_Ystar, ibar.value, "o", color="tab:red", ms=8, zorder=5)
        _ax.vlines(_Ystar, 0, ibar.value, color="tab:red", ls=":", lw=1)
        _ax.annotate("Equilibrium", (_Ystar, ibar.value), xytext=(8, 6), textcoords="offset points", color="tab:red")

    _ax.set_xlim(0, _xmax)
    _ax.set_ylim(0, _ymax)
    _ax.set_xlabel("Output, Y")
    _ax.set_ylabel("Interest rate, i (%)")
    _ax.set_title("IS-LM Model")
    _ax.legend(loc="upper right")
    _ax.grid(alpha=0.1)
    plt.close(_fig)

    # --- Layout ------------------------------------------------------------
    if not _valid:
        _stats = mo.md("⚠️ No positive equilibrium for these values.")
    else:
        _stats = mo.md(
            f"**Equilibrium output Y\\*:** {_Ystar:,.0f}  \n"
            f"**Interest rate i:** {ibar.value:.2f} %  \n"
            f"**Investment I(i):** {_invest:,.0f}"
        )

    mo.hstack(
        [mo.vstack([c0, c1, T, G, I0, ibar, _stats], gap=1), mo.as_html(_fig)],
        widths=[1.2, 2],
        align="center",
        gap=2,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### IS: $Y=C(\underset{+}{Y}−\underset{-}{T})+I(\underset{+}{Y},\, \underset{-}{i})$
    ##### LM: $i = \bar{i}$ &nbsp;

    - $c_0$ autonomous consumption
    - $c_1$ marginal propensity to consume
    - $T$ taxes
    - $G$ government spending
    - $\bar{I}$ investment
    - $\bar{i}$ policy rat (in %), set by the central bank
    """)
    return


if __name__ == "__main__":
    app.run()
