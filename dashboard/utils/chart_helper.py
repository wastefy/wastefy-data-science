import matplotlib.pyplot as plt

def annotate_bars(ax, fmt="{:.0f}", is_float=False):
    for p in ax.patches:
        val = p.get_height()
        label = f"{val:.2f}" if is_float else f"{int(val):,}"
        ax.annotate(
            label,
            (p.get_x() + p.get_width() / 2, val),
            ha="center", va="bottom", fontweight="bold"
        )

def bar_and_pie(series, title_bar, title_pie, colors, fig_size=(12, 5)):
    fig, axes = plt.subplots(1, 2, figsize=fig_size)

    series.plot(kind="bar", ax=axes[0], color=colors[:len(series)],
                edgecolor="white", width=0.5)
    axes[0].set(title=title_bar, ylabel="Jumlah")
    axes[0].tick_params(axis="x", rotation=0)
    annotate_bars(axes[0])

    axes[1].pie(series, labels=series.index, autopct="%1.1f%%",
                startangle=90, colors=colors[:len(series)])
    axes[1].set_title(title_pie)

    plt.tight_layout()
    return fig