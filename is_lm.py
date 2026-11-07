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
    mo.md(r"""
    IS: $Y = c_0 + c_1 (Y - T) + \bar{I} - b\,i + G$

    LM: $\dfrac{M}{P} = Y\,(k - h\,i)$ &nbsp; with $k = 0.5,\; h = 2.5$

    <small>$c_0$ autonomous consumption · $c_1$ marginal propensity to consume · $T$ taxes · $G$ government spending · $\bar{I}$ autonomous investment · $b$ interest sensitivity of investment · $M/P$ real money supply</small>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    c0 = mo.ui.slider(100, 400, step=10, value=200, label="$c_0$", show_value=True)
    c1 = mo.ui.slider(0.1, 0.8, step=0.05, value=0.6, label="$c_1$", show_value=True)
    T = mo.ui.slider(1000, 4000, step=50, value=2000, label="$T$", show_value=True)
    G = mo.ui.slider(1000, 4000, step=50, value=2000, label="$G$", show_value=True)
    I0 = mo.ui.slider(0, 2000, step=50, value=500, label="$\\bar{I}$", show_value=True)
    b = mo.ui.slider(1000, 10000, step=250, value=5000, label="$b$", show_value=True)
    m = mo.ui.slider(200, 1500, step=25, value=600, label="$M/P$", show_value=True)
    return G, I0, T, b, c0, c1, m


@app.cell(hide_code=True)
def _(G, I0, T, b, c0, c1, m, mo, np, plt):
    _k, _h = 0.5, 2.5

    def _eq(c0, c1, T, G, I0, b, m):
        """Solve IS-LM. Returns (Y*, i*) with i in decimals, respecting i >= 0."""
        A = c0 - c1 * T + I0 + G
        B = A - b * _k / _h
        Y = (B + np.sqrt(B**2 + 4 * (1 - c1) * b * m / _h)) / (2 * (1 - c1))
        i = (_k - m / Y) / _h
        if i < 0:  # LM is flat at the zero lower bound
            i, Y = 0.0, A / (1 - c1)
        return Y, i, A

    _Ystar, _istar, _A = _eq(c0.value, c1.value, T.value, G.value, I0.value, b.value, m.value)
    _Yb, _ib, _Ab = _eq(200, 0.6, 2000, 2000, 500, 5000, 600)

    _valid = _Ystar > 0
    _xmax = max(6000, 1.5 * _Ystar) if _valid else 6000
    _ymax = 25  # percent
    _Y = np.linspace(1, _xmax, 400)

    def _is(Y, A, c1, b):
        return (A - (1 - c1) * Y) / b * 100

    def _lm(Y, m):
        return np.maximum((_k - m / Y) / _h, 0) * 100

    _fig, _ax = plt.subplots(figsize=(6.5, 6))
    _ax.plot(_Y, _is(_Y, _Ab, 0.6, 5000), color="grey", ls="--", lw=1, label="IS / LM (baseline)")
    _ax.plot(_Y, _lm(_Y, 600), color="grey", ls="--", lw=1)
    _ax.plot(_Y, _is(_Y, _A, c1.value, b.value), color="tab:blue", lw=2.5, label="IS")
    _ax.plot(_Y, _lm(_Y, m.value), color="tab:orange", lw=2.5, label="LM")

    # Equilibrium
    if _valid:
        _ax.plot(_Ystar, _istar * 100, "o", color="tab:red", ms=8, zorder=5)
        _ax.vlines(_Ystar, 0, _istar * 100, color="tab:red", ls=":", lw=1)
        _ax.hlines(_istar * 100, 0, _Ystar, color="tab:red", ls=":", lw=1)
        _ax.annotate("A", (_Ystar, _istar * 100), xytext=(8, 6), textcoords="offset points", color="tab:red")

    _ax.set_xlim(0, _xmax)
    _ax.set_ylim(0, _ymax)
    _ax.set_xlabel("Output, Y")
    _ax.set_ylabel("Interest rate, i (%)")
    _ax.set_title("IS-LM Model")
    _ax.legend(loc="upper right")
    _ax.grid(alpha=0.3)
    plt.close(_fig)

    if not _valid:
        _stats = mo.md("⚠️ No positive equilibrium for these values.")
    else:
        _stats = mo.md(
            f"**Equilibrium output Y\\*:** {_Ystar:,.0f}  \n"
            f"**Equilibrium interest rate i\\*:** {_istar * 100:.2f} %"
            + ("\n\n⚠️ Economy at the zero lower bound (i = 0)." if _istar == 0 else "")
        )

    mo.hstack(
        [mo.vstack([c0, c1, T, G, I0, b, m, _stats], gap=1), mo.as_html(_fig)],
        widths=[1.2, 2],
        align="center",
        gap=2,
    )
    return


if __name__ == "__main__":
    app.run()
