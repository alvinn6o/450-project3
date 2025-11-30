import pandas as pd
import plotly.graph_objects as go
from collections import Counter

<<<<<<< Updated upstream
#Data to use
=======
from plots import make_sequence_index_figure, get_top_3_gaze_percentages_filtered, AOI_names, load_table
from data import AOI
>>>>>>> Stashed changes

file = "Expanded Patterns (Group).xlsx"

<<<<<<< Updated upstream
use_excluding_a = True #Make false to include AOI A (Just for testing)
=======
app.layout = html.Div(
    [
        html.H2("Sequence Plot for AOIs"),
        
        # Top 3 Gaze Percentages Summary
        html.Div(
            id="top-3-summary",
            style={"marginBottom": "2rem", "padding": "1rem", "backgroundColor": "#f5f5f5", "borderRadius": "4px"}
        ),
        
        html.Div(
            [
                #html.Div(
                    #[
                       # html.Label("Pilot group"),
                        #dcc.RadioItems(
                           # id="group-radio",
                           # options=[
                              #  {"label": "Successful", "value": "successful"},
                               # {"label": "Unsuccessful", "value": "unsuccessful"},
                           # ],
                            #value="successful",
                            #inline=True,
                       # ),
                  #  ],
                   # style={"marginRight": "2rem"},
                #),
                html.Div(
                    [
                        html.Label("Pattern type"),
                        dcc.RadioItems(
                            id="pattern-type-radio",
                            options=[
                                {"label": "Collapsed", "value": "collapsed"},
                                {"label": "Expanded", "value": "expanded"},
                            ],
                            value="collapsed",
                            inline=True,
                        ),
                    ],
                    style={"marginRight": "2rem"},
                ),
>>>>>>> Stashed changes

if use_excluding_a:
    s_sheet = "Succesful Excluding No AOI(A)"
    u_sheet = "Unsuccesful Excluding No AOI(A)"
else:
    s_sheet = "Succesful"
    u_sheet = "Unsuccesful"

df_success = pd.read_excel(file, sheet_name=s_sheet)
df_unsuccess = pd.read_excel(file, sheet_name=u_sheet)

#AOI Labels
aoi_labels = {
    "A": "A - No AOI",
    "B": "B - Alt_VSI",
    "C": "C - AI",
    "D": "D - TI_HSI",
    "E": "E - SSI",
    "F": "F - ASI",
    "G": "G - RPM",
    "H": "H - Window"
}

#AOI Colormap
aoi_colors = {
    "A": "lightgray",
    "B": "steelblue",
    "C": "darkorange",
    "D": "darkcyan",
    "E": "mediumpurple",
    "F": "firebrick",
    "G": "olivedrab",
    "H": "skyblue"
}

#Compute weighted AOI transitions between consecutive AOIs
def extract_transitions(df):
    transitions = Counter()

    for _, row in df.iterrows():
        pattern = str(row["Pattern String"]).strip()
        freq = int(row["Frequency"])
        seq = list(pattern)

        #Record transition pairs
        for i in range(len(seq) - 1):
            src = seq[i]
            tgt = seq[i+1]
            transitions[(src, tgt)] += freq

    return transitions

trans_success = extract_transitions(df_success)
trans_unsuccess = extract_transitions(df_unsuccess)

#Build node list
letters = sorted(set(
    [s for s, _ in trans_success] +
    [t for _, t in trans_success] +
    [s for s, _ in trans_unsuccess] +
    [t for _, t in trans_unsuccess]
))

nodes = [aoi_labels[l] for l in letters]
node_colors = [aoi_colors[l] for l in letters]
letter_to_index = {ltr: i for i, ltr in enumerate(letters)}

#Build link arrays with tooltips
def build_links(transitions, total_count):
    sources, targets, values, tooltips, link_colors = [], [], [], [], []

    for (src, tgt), count in transitions.items():
        sources.append(letter_to_index[src])
        targets.append(letter_to_index[tgt])
        values.append(count)

        pct = (count / total_count) * 100

        tooltip = (
            f"{aoi_labels[src]}: {aoi_labels[tgt]}<br>"
            f"Count: {count}<br>"
            f"Percentage: {pct:.2f}%"
        )
        tooltips.append(tooltip)

        link_colors.append(aoi_colors[src])

    return sources, targets, values, tooltips, link_colors

#Totals
total_success = sum(trans_success.values())
total_unsuccess = sum(trans_unsuccess.values())

#Build arrays
s_src, s_tgt, s_val, s_label, s_colors = build_links(trans_success, total_success)
u_src, u_tgt, u_val, u_label, u_colors = build_links(trans_unsuccess, total_unsuccess)

#Reposition Nodes
node_x = [
    0.10, 0.25, 0.40, 0.40, 0.55, 0.55, 0.70, 0.85
]

node_y = [
    0.50, 0.10, 0.30, 0.70, 0.20, 0.60, 0.40, 0.50
]

#Dual Sankey with tooltips
fig = go.Figure()

#Successful Pilot Sankey
fig.add_trace(go.Sankey(
    domain=dict(x=[0.05, 0.45]),
    node=dict(
        label=[ltr for ltr in letters],
        customdata=[aoi_labels[l] for l in letters],
        hovertemplate="%{customdata}<extra></extra>",
        x=node_x,
        y=node_y,
        pad=15,
        thickness=18,
        color=node_colors
    ),
    link=dict(
        source=s_src,
        target=s_tgt,
        value=s_val,
        label=s_label,
        color=s_colors,
        hovertemplate="%{label}<extra></extra>"
    ),
    name="Successful"
))

#Unsuccessful Pilot Sankey
fig.add_trace(go.Sankey(
    domain=dict(x=[0.55, 0.95]),
    node=dict(
        label=[ltr for ltr in letters],
        customdata=[aoi_labels[l] for l in letters],
        hovertemplate="%{customdata}<extra></extra>",
        x=node_x,
        y=node_y,
        pad=15,
        thickness=18,
        color=node_colors
    ),
    link=dict(
        source=u_src,
        target=u_tgt,
        value=u_val,
        label=u_label,
        color=u_colors,
        hovertemplate="%{label}<extra></extra>"
    ),
    name="Unsuccessful"
))

fig.update_layout(
    title_text=None,
    font_size=12,
    width=1600,
    height=1050,
    margin=dict(t=250),
    annotations=[
        # Main TItle
        dict(
            x=0.5, y=1.25,
            xref="paper", yref="paper",
            text="AOI Transition Comparison - Successful vs. Unsuccessful Pilots",
            showarrow=False,
            font=dict(size=26, color="black")
        ),
        # Left Subtitle
        dict(
            x=0.25, y=1.18,
            xref="paper", yref="paper",
            text="Successful AOI Transitions",
            showarrow=False,
            font=dict(size=20)
        ),
        # Right Subtitle
        dict(
            x=0.75, y=1.18,
            xref="paper", yref="paper",
            text="Unsuccessful AOI Transitions",
            showarrow=False,
            font=dict(size=20)
        )
    ]
)

<<<<<<< Updated upstream
fig.show()
=======

@app.callback(
    Output("success-graph", "figure"),
    Output("unsuccess-graph", "figure"),
    Output("top-3-summary", "children"),
    #Input("group-radio", "value"),
    Input("pattern-type-radio", "value"),
    Input("exclude-a-radio", "value"),
    Input("metric-radio", "value"),
    Input("top-k-slider", "value"),
    Input("show-all-checklist", "value"),
)
def update_sequence_index_plot(
    #group_value,
    pattern_type,
    exclude_a_value,
    metric,
    top_k,
    show_all_values,
):
    exclude_a = (exclude_a_value == "exclude")
    show_all = "all" in (show_all_values or [])
    
    metric_col_map = {
        "frequency": "Frequency",
        "seq_support": "Sequence Support",
    }
    metric_col = metric_col_map[metric]

    fig_success = make_sequence_index_figure(
        pattern_type=pattern_type,
        group_key="successful",
        exclude_a=exclude_a,
        metric=metric,
        top_k=top_k,
        show_all=show_all,
    )

    fig_unsuccess = make_sequence_index_figure(
        pattern_type=pattern_type,
        group_key="unsuccessful",
        exclude_a=exclude_a,
        metric=metric,
        top_k=top_k,
        show_all=show_all,
    )
    
    # Get filtered patterns to compute top 3 from currently displayed patterns
    df_success = load_table(pattern_type, "successful", exclude_a)
    df_unsuccess = load_table(pattern_type, "unsuccessful", exclude_a)
    
    df_success_sorted = df_success.sort_values(metric_col, ascending=False)
    df_unsuccess_sorted = df_unsuccess.sort_values(metric_col, ascending=False)
    
    if not show_all and top_k is not None:
        df_success_sorted = df_success_sorted.head(int(top_k))
        df_unsuccess_sorted = df_unsuccess_sorted.head(int(top_k))
    
    # Calculate top 3 for displayed patterns
    top_3_success = get_top_3_gaze_percentages_filtered(df_success_sorted["Pattern String"], exclude_a)
    top_3_unsuccess = get_top_3_gaze_percentages_filtered(df_unsuccess_sorted["Pattern String"], exclude_a)
    
    # Create summary display
    summary = html.Div([
        html.Div([
            html.H4("Successful Pilots - Top 3 AOI Gaze %", style={"marginTop": 0}),
            html.Ul([
                html.Li(f"{aoi} - {AOI_names[aoi]}: {pct:.1f}%") 
                for aoi, pct in top_3_success
            ])
        ], style={"display": "inline-block", "marginRight": "3rem", "verticalAlign": "top"}),
        
        html.Div([
            html.H4("Unsuccessful Pilots - Top 3 AOI Gaze %", style={"marginTop": 0}),
            html.Ul([
                html.Li(f"{aoi} - {AOI_names[aoi]}: {pct:.1f}%") 
                for aoi, pct in top_3_unsuccess
            ])
        ], style={"display": "inline-block", "verticalAlign": "top"})
    ])
    
    return fig_success, fig_unsuccess, summary



if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> Stashed changes
