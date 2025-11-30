from dash import Dash, dcc, html, Input, Output

from plots import make_sequence_index_figure

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Sequence Plot for AOIs"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Pilot group"),
                        dcc.RadioItems(
                            id="group-radio",
                            options=[
                                {"label": "Successful", "value": "successful"},
                                {"label": "Unsuccessful", "value": "unsuccessful"},
                            ],
                            value="successful",
                            inline=True,
                        ),
                    ],
                    style={"marginRight": "2rem"},
                ),

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

        dcc.Graph(id="sequence-index-graph"),
    ],
    style={"padding": "1.5rem"},
)


@app.callback(
    Output("sequence-index-graph", "figure"),
    Input("group-radio", "value"),
    Input("pattern-type-radio", "value"),
    Input("exclude-a-radio", "value"),
    Input("metric-radio", "value"),
    Input("top-k-slider", "value"),
    Input("show-all-checklist", "value"),
)
def update_sequence_index_plot(
    group_value,
    pattern_type,
    exclude_a_value,
    metric,
    top_k,
    show_all_values,
):
    exclude_a = (exclude_a_value == "exclude")
    show_all = "all" in (show_all_values or [])

    fig = make_sequence_index_figure(
        pattern_type=pattern_type,
        group_key=group_value,
        exclude_a=exclude_a,
        metric=metric,
        top_k=top_k,
        show_all=show_all,
    )
    return fig



if __name__ == "__main__":
    app.run(debug=True)
