import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import ertviz.assets as assets


def parameter_view(parent, index=0):
    return [
        dcc.Store(
            id={"index": index, "type": parent.uuid("parameter-id-store")}, data=index
        ),
        dbc.Row(
            className="ert-plot-options",
            children=[
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H4(index)],
                                    align="center",
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Plots:"),
                                    ],
                                    width="auto",
                                    align="center",
                                ),
                                dbc.Col(
                                    [
                                        dcc.Checklist(
                                            id={
                                                "index": index,
                                                "type": parent.uuid("hist-check"),
                                            },
                                            options=[
                                                {"label": "histogram", "value": "hist"},
                                                {"label": "kde", "value": "kde"},
                                            ],
                                            value=["hist", "kde"],
                                            persistence="session",
                                        ),
                                    ],
                                    align="center",
                                ),
                            ]
                        )
                    ],
                    width="auto",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Number of bins:", className="ert-label"
                                        ),
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dcc.Input(
                                            id={
                                                "index": index,
                                                "type": parent.uuid("hist-bincount"),
                                            },
                                            type="number",
                                            placeholder="# bins",
                                            min=2,
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                ),
                dcc.Store(
                    id={"index": index, "type": parent.uuid("bincount-store")},
                    storage_type="session",
                ),
            ],
        ),
        dcc.Graph(
            id={
                "index": index,
                "id": parent.uuid("parameter-scatter"),
                "type": parent.uuid("graph"),
            },
            config={"responsive": True},
        ),
    ]
