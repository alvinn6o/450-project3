from dash import Dash, dcc, html, Input, Output

<<<<<<< HEAD
<<<<<<< Updated upstream
#Data to use
=======
from plots import make_sequence_index_figure, get_top_3_gaze_percentages_filtered, AOI_names, load_table
from data import AOI
>>>>>>> Stashed changes
=======
from plots import make_sequence_index_figure
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484

app = Dash(__name__)

<<<<<<< HEAD
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
        
=======
app.layout = html.Div(
    [
        html.H2("Sequence Plot for AOIs"),
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484
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
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484

                html.Div(
                    [
                        html.Label("AOI A (No AOI)"),
                        dcc.RadioItems(
                            id="exclude-a-radio",
                            options=[
                                {"label": "Include A", "value": "include"},
                                {"label": "Exclude A", "value": "exclude"},
                            ],
                            value="exclude",
                            inline=True,
                        ),
                    ],
                    style={"marginRight": "2rem"},
                ),

                html.Div(
                    [
                        html.Label("Rank"),
                        dcc.RadioItems(
                            id="metric-radio",
                            options=[
                                {"label": "Frequency", "value": "frequency"},
                                {"label": "Sequence support", "value": "seq_support"},
                            ],
                            value="frequency",
                            inline=True,
                            inputStyle={"margin-right": "5px", "margin-left": "10px"},
                        ),
                    ],
                    style={"marginRight": "2rem"},
                ),

                html.Div(
                    [
                        html.Label("Top K patterns"),
                        dcc.Slider(
                            id="top-k-slider",
                            min=5,
                            max=100,
                            step=1,
                            value=10,
                            marks={
                                5: "5",
                                10: "10",
                                20: "20",
                                30: "30",
                                40: "40",
                                50: "50",
                                60: "60",
                                70: "70",
                                80: "80",
                                90: "90",
                                100: "100",
                            },
                        ),
                        dcc.Checklist(
                            id="show-all-checklist",
                            options=[{"label": " Show all patterns", "value": "all"}],
                            value=[],
                            style={"marginTop": "0.4rem"},
                        ),
                    ],
                    style={"flex": "1 1 300px", "maxWidth": "420px"},
                ),
            ],
            style={"display": "flex", "flexWrap": "wrap", "marginBottom": "1rem"},
        ),

        html.Div(
            [
                html.H3("Successful Pilots", style={"marginTop": "1.5rem"}),
                dcc.Graph(id="success-graph"),

                html.H3("Unsuccessful Pilots", style={"marginTop": "2rem"}),
                dcc.Graph(id="unsuccess-graph"),
            ]
        )

    ],
    style={"padding": "1.5rem"},
)

<<<<<<< HEAD
<<<<<<< Updated upstream
fig.show()
=======
=======
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484

@app.callback(
    Output("success-graph", "figure"),
    Output("unsuccess-graph", "figure"),
<<<<<<< HEAD
    Output("top-3-summary", "children"),
=======
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484
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
<<<<<<< HEAD
    
    metric_col_map = {
        "frequency": "Frequency",
        "seq_support": "Sequence Support",
    }
    metric_col = metric_col_map[metric]
=======
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484

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
<<<<<<< HEAD
    
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
=======
    return fig_success, fig_unsuccess
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484



if __name__ == "__main__":
    app.run(debug=True)
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
>>>>>>> ec8d41e77fa6984f18f3ef53d131d41e118a3484
