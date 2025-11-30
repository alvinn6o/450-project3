import numpy as np
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

from data import load_table, AOI, AOI_ENUMERATED

AOI_names = {
    "A": "Noi AOI",
    "B": "Alt_VSI",
    "C": "AI",
    "D": "TI_HSI",
    "E": "SSI",
    "F": "ASI",
    "G": "RPM",
    "H": "Window",
}

def get_top_3_gaze_percentages(group_key: str, exclude_a: bool) -> list:
    """
    Calculate the top 3 AOIs by gaze percentage for a given pilot group.
    Returns a list of tuples: [(AOI, percentage), ...]
    """
    df = load_table("collapsed", group_key, exclude_a)
    
    # Get all AOI characters from patterns
    all_aoi = [a for p in df["Pattern String"] for a in str(p)]
    aoi_counts = Counter(all_aoi)
    total_gaze = sum(aoi_counts.values())
    
    # Calculate percentages
    aoi_percentages = {
        aoi: (aoi_counts[aoi] / total_gaze) * 100 
        for aoi in AOI if aoi_counts[aoi] > 0
    }
    
    # Sort and get top 3
    top_3 = sorted(aoi_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_3


def get_top_3_gaze_percentages_filtered(
    patterns: pd.Series, exclude_a: bool
) -> list:
    """
    Calculate the top 3 AOIs by gaze percentage from a filtered set of patterns.
    Returns a list of tuples: [(AOI, percentage), ...]
    """
    # Get all AOI characters from the provided patterns
    all_aoi = [a for p in patterns for a in str(p)]
    aoi_counts = Counter(all_aoi)
    total_gaze = sum(aoi_counts.values())
    
    if total_gaze == 0:
        return []
    
    # Calculate percentages
    aoi_percentages = {
        aoi: (aoi_counts[aoi] / total_gaze) * 100 
        for aoi in AOI if aoi_counts[aoi] > 0
    }
    
    # Sort and get top 3
    top_3 = sorted(aoi_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_3
def build_sequence_matrix(patterns: pd.Series, freqs: pd.Series, overall_pct, index_pct):
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
                    f"AOI: {aoi} - {AOI_names.get(aoi, '')}<br>"
                    f"Index: {pos + 1}<br>"
                    f"Frequency: {freq}<br>"
                    f"Overall AOI Gaze Percentage:{overall_pct[aoi]:.1f}%<br>"
                    f"AOI Gaze Percentage at Index {pos + 1}: {index_pct[pos][aoi]:.1f}%"
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

    #Compute AOI percentages overall
    all_aoi = [a for p in df_sorted["Pattern String"] for a in str(p)]
    overall_counts = Counter(all_aoi)
    overall_total = sum(overall_counts.values())
    overall_pct = {
        aoi: (overall_counts[aoi] / overall_total) * 100 if overall_total else 0 for aoi in AOI
    }

    #Compute AOI percentages by index
    max_len = max(len(str(p)) for p in df_sorted["Pattern String"])
    index_counts = [Counter() for _ in range(max_len)]
    index_totals = [0 for _ in range(max_len)]

    for p in df_sorted["Pattern String"]:
        p = str(p)
        for idx, a in enumerate(p):
            if a in AOI:
                index_counts[idx][a] += 1
                index_totals[idx] += 1

    index_pct = [
        {
            aoi: (index_counts[i][aoi] / index_totals[i]) * 100 if index_totals[i] else 0 for aoi in AOI
         }
        for i in range(max_len)
    ]

    # sequence matrix for the graph
    z, y_labels, x_vals, text = build_sequence_matrix(
        df_sorted["Pattern String"],
        df_sorted["Frequency"],
        overall_pct,
        index_pct,
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
    
    # Discrete colorscale with definitive colors for each AOI
    colorscale = []
    for i, c in enumerate(colors):
        lower_v = i / len(colors)
        upper_v = (i + 1) / len(colors)
        colorscale.append([lower_v, c])
        colorscale.append([upper_v, c])

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
            ticktext=[f"{aoi} - {AOI_names[aoi]}" for aoi in AOI],
            thickness=20,
            len=0.7,
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
