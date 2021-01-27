import regex
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from ertviz.models import (
    load_ensemble,
)

old_submit = 0


def filter_match(filter, key):
    reg_exp = ".*" + ".*".join(filter.split())
    try:
        match = bool(regex.match(reg_exp, key))
    except:
        return False
    return match


def parameter_selector_controller(parent, app):
    @app.callback(
        [
            Output(parent.uuid("parameter-selector-multi"), "options"),
            Output(parent.uuid("parameter-selector-multi"), "value"),
        ],
        [
            Input(parent.uuid("ensemble-selection-store"), "data"),
            Input(parent.uuid("parameter-selector-filter"), "value"),
            Input(parent.uuid("parameter-deactivator"), "value"),
        ],
    )
    def update_parameters_options(selected_ensembles, filter_search, selected):
        if not selected_ensembles:
            raise PreventUpdate
        selected = [] if not selected else selected

        ensemble_id, _ = selected_ensembles.popitem()
        ensemble = load_ensemble(parent, ensemble_id)
        if bool(filter_search):
            options = [
                {"label": parameter_key, "value": parameter_key}
                for parameter_key in ensemble.parameters
                if filter_match(filter_search, parameter_key)
                and parameter_key not in selected
            ]
        else:
            options = [
                {"label": parameter_key, "value": parameter_key}
                for parameter_key in ensemble.parameters
                if parameter_key not in selected
            ]
        return options, selected

    @app.callback(
        [
            Output(parent.uuid("parameter-selection-store"), "data"),
            Output(parent.uuid("parameter-deactivator"), "options"),
            Output(parent.uuid("parameter-deactivator"), "value"),
        ],
        [
            Input(parent.uuid("parameter-selector-multi"), "value"),
            Input(parent.uuid("parameter-selector-filter"), "n_submit"),
        ],
        [
            State(parent.uuid("parameter-deactivator"), "value"),
            State(parent.uuid("parameter-selector-multi"), "options"),
        ],
    )
    def update_parameter_selection(parameters, n_submit, selected_params, par_opts):
        global old_submit
        selected_params = [] if not selected_params else selected_params
        parameters = [parameters] if type(parameters) == str else parameters
        shown_parameters = selected_params
        if bool(parameters):
            shown_parameters = list(set(parameters + selected_params))
        if n_submit is not None and n_submit > old_submit:
            shown_parameters = list(
                set(selected_params + [parm["value"] for parm in par_opts])
            )
            old_submit = n_submit

        selected_opts = [{"label": param, "value": param} for param in shown_parameters]
        return shown_parameters, selected_opts, shown_parameters
