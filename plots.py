import numpy as np
import plotly.graph_objects as go
import pandas as pd

from data import load_table, AOI, AOI_ENUMERATED

def build_sequence_matrix(patterns: pd.Series, freqs: pd.Series):
    """
    Turn the patterns into matrix to plot with z (2d array of patterns x max length),
    y_labels for rows, x_vals for the indexes, and hover feature
    """
    patterns = [str(p) for p in patterns]
    if not patterns:
        return np.array([]), [], [], []

    max_len = max(len(p) for p in patterns)

    # z 2d array: rows are patterns, columns are position
    z = []
    text = []
    y_labels = []

    for rank, (pattern, freq) in enumerate(zip(patterns, freqs), start=1):
        row_vals = []
        row_text = []

        for pos in range(max_len):
            if pos < len(pattern):
                aoi = pattern[pos]
                val = AOI_ENUMERATED.get(aoi, np.nan)
                row_vals.append(val)
                row_text.append(
                    f"Rank: {rank}<br>"
                    f"Pattern: {pattern}<br>"
                    f"AOI: {aoi}<br>"
                    f"Index: {pos + 1}<br>"
                    f"Frequency: {freq}"
                )
            else:
                # if pattern length less than max length, turn into nan vals to pad
                row_vals.append(np.nan)
                row_text.append("")

        z.append(row_vals)
        text.append(row_text)
        y_labels.append(f"{rank}. {pattern} (n={freq})")

    x_vals = list(range(1, max_len + 1))
    return np.array(z, dtype=float), y_labels, x_vals, text


def make_sequence_index_figure(
    pattern_type: str,
    group_key: str,
    exclude_a: bool,
    metric: str,
    top_k: int,
    show_all: bool,
) -> go.Figure:

    df = load_table(pattern_type, group_key, exclude_a)

    metric_col_map = {
        "frequency": "Frequency",
        "seq_support": "Sequence Support",
    }

    metric_col = metric_col_map[metric]
    df_sorted = df.sort_values(metric_col, ascending=False)

    if not show_all and top_k is not None:
        df_sorted = df_sorted.head(int(top_k))

    # sequence matrix for the graph
    z, y_labels, x_vals, text = build_sequence_matrix(
        df_sorted["Pattern String"],
        df_sorted["Frequency"],
    )

    if z.size == 0:
        return go.Figure().update_layout(
            title="None",
            xaxis_title="Index in pattern",
            yaxis_title="Pattern",
        )

    # in order from A-H
    colors = [
        "#5E68FD",  
        "#E45238", 
        "#00CC33",  
        "#AB63FA",  
        "#FFA15A",  
        "#3CDEF3", 
        "#FF8EAE", 
        "#BEEE8C", 
    ]
    n_colors = len(colors) - 1 if len(colors) > 1 else 1

    colorscale = []
    for i, c in enumerate(colors):
        v = i / n_colors
        colorscale.append([v, c])

    heatmap = go.Heatmap(
        z=z,
        x=x_vals,
        y=y_labels,
        text=text,
        hoverinfo="text",
        colorscale=colorscale,
        zmin=0,
        zmax=len(AOI) - 1,
        colorbar=dict(
            title="AOI",
            tickmode="array",
            tickvals=list(range(len(AOI))),
            ticktext=AOI,
        ),
    )

    title = (
        f"Sequence index plot – {group_key.title()} pilots · "
        f"{'Collapsed' if pattern_type == 'collapsed' else 'Expanded'} patterns · "
        f"{'Excluding' if exclude_a else 'Including'} AOI A"
    )

    fig = go.Figure(data=[heatmap])
    fig.update_layout(
        title=title,
        xaxis_title="Index in pattern",
        yaxis_title="Pattern/Sequence",
        yaxis=dict(autorange="reversed"),
        height=600,
        margin=dict(l=160, r=40, t=60, b=40),
    )

    return fig
