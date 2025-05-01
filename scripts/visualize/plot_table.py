import os
import json
import threading
import webbrowser
import pandas as pd
import dash
from dash import Dash, html, dash_table, Input, Output, callback_context


def resolve_path(*relative_parts):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, *relative_parts)


def plot_interactive_table_dash(sim_path: str):
    sim_path = resolve_path(sim_path)

    if not os.path.exists(sim_path):
        print(f"❌ 시뮬레이션 파일을 찾을 수 없습니다:\n{sim_path}")
        return

    with open(sim_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    fids = sorted(raw_data.keys(), key=lambda x: float(x))
    df = pd.DataFrame([raw_data[fid] for fid in fids])

    # ✅ 컬럼 라벨 매핑
    column_labels = {
        "cumulative_distance": "Cumulative Distance (m)",
        "velocity_kph": "Velocity (kph)",
        "energy_total_kWh": "Energy (kWh)",
        "energy_regen_kWh": "Regen Energy (kWh)",
        "energy_stored_kWh": "Stored Energy (kWh)",
        "R_total": "Total Resistance (N)",
        "acceleration": "Acceleration (m/s²)",
        "a_slope": "a_slope (rad)",
        "curvature_kappa": "curvature_kappa",
        "P_engine_kw": "Engine Power (kW)",
        "mass_kg": "Mass (kg)",
        "R_curve": "R_curve (N)",
        "R_davis": "R_davis (N)"
    }

    df = df.rename(columns=column_labels)

    # ✅ 필드 그룹 정의
    base_fields = [
        "Cumulative Distance (m)", "Velocity (kph)", "Energy (kWh)",
        "Regen Energy (kWh)", "Stored Energy (kWh)", "Total Resistance (N)",
        "Acceleration (m/s²)"
    ]
    energy_fields = [
        "Energy (kWh)", "Regen Energy (kWh)", "Stored Energy (kWh)"
    ]
    velocity_fields = ["Velocity (kph)", "Acceleration (m/s²)"]
    resistance_fields = ["Total Resistance (N)", "R_curve (N)", "R_davis (N)"]
    all_fields = list(df.columns)

    app = Dash(__name__)
    app.title = "Simulation Table"

    app.layout = html.Div([
        html.H2("Simulation Data Table"),
        html.Div([
            html.Button("Base Fields", id="btn-base", n_clicks=0),
            html.Button("Show All Fields", id="btn-all", n_clicks=0),
            html.Button("Energy Fields", id="btn-energy", n_clicks=0),
            html.Button("Velocity Fields", id="btn-velocity", n_clicks=0),
            html.Button("Resistance Fields", id="btn-resist", n_clicks=0),
        ], style={"marginBottom": "12px"}),

        dash_table.DataTable(
            id="sim-table",
            data=df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in base_fields],
            page_size=20,
            filter_action="native",
            sort_action="native",
            fixed_rows={"headers": True},
            style_table={"overflowX": "auto", "maxHeight": "70vh"},
            style_cell={
                "textAlign": "left",
                "padding": "8px",
                "fontSize": 13,
                "minWidth": "130px",
                "whiteSpace": "normal"
            },
            style_header={
                "backgroundColor": "#f4f4f4",
                "fontWeight": "bold",
                "borderBottom": "1px solid #ccc"
            },
            style_data={
                "backgroundColor": "white",
                "borderBottom": "1px solid #eee"
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#fafafa"
                },
                {
                    # 👉 마우스를 올렸을 때 hover 효과
                    "if": {"state": "active"},
                    "backgroundColor": "#fff3e0",  # 연한 주황
                    "border": "1px solid #ffa726",
                    "cursor": "pointer"
                },
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "#ffe0b2",  # 더 진한 주황
                    "border": "1px solid #fb8c00"
                },
            ]

        )
    ])

    @app.callback(
        Output("sim-table", "columns"),
        Input("btn-base", "n_clicks"),
        Input("btn-all", "n_clicks"),
        Input("btn-energy", "n_clicks"),
        Input("btn-velocity", "n_clicks"),
        Input("btn-resist", "n_clicks"),
    )
    def update_table_columns(n1, n2, n3, n4, n5):
        ctx = callback_context
        if not ctx.triggered:
            return [{"name": col, "id": col} for col in base_fields]
        btn_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if btn_id == "btn-base":
            return [{"name": col, "id": col} for col in base_fields]
        elif btn_id == "btn-all":
            return [{"name": col, "id": col} for col in all_fields]
        elif btn_id == "btn-energy":
            return [{"name": col, "id": col} for col in ["Cumulative Distance (m)"] + energy_fields]
        elif btn_id == "btn-velocity":
            return [{"name": col, "id": col} for col in ["Cumulative Distance (m)"] + velocity_fields]
        elif btn_id == "btn-resist":
            return [{"name": col, "id": col} for col in ["Cumulative Distance (m)"] + resistance_fields]
        return [{"name": col, "id": col} for col in base_fields]

    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8050")).start()
    app.run(debug=False)


if __name__ == "__main__":
    plot_interactive_table_dash("algorithms/simulation_results/final_simulation(Lucinda).json")
