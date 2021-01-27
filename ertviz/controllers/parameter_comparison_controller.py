from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from ertviz.models import (
    load_ensemble,
    ParallelCoordinates,
)


def parameter_comparison_controller(parent, app):
    @app.callback(
        Output(
            {"id": parent.uuid("parallel-coor"), "type": parent.uuid("graph")},
            "figure",
        ),
        [
            Input(parent.uuid("parameter-selection-store"), "data"),
        ],
        [
            State(parent.uuid("ensemble-selection-store"), "data"),
        ],
    )
    def _update_parallel_coor(selected_parameters, selected_ensembles):
        if not selected_ensembles:
            raise PreventUpdate
        selected_parameters = [] if not selected_parameters else selected_parameters

        data = {}
        colors = {}

        # if no parameters selected take up to the first 5 by default
        # if not bool(parameters):
        #    parameters = [option["value"] for option in parameter_options][:5]
        for idx, (ensemble_id, color) in enumerate(selected_ensembles.items()):
            ensemble = load_ensemble(parent, ensemble_id)
            ens_key = str(ensemble)
            df = ensemble.parameters_df(selected_parameters)
            df["ensemble_id"] = idx
            data[ens_key] = df.copy()
            colors[ens_key] = color["color"]
        parent.parallel_plot = ParallelCoordinates(data, colors)

        return parent.parallel_plot.repr
