import os
import json
import webbrowser
import plotly.graph_objects as go

def resolve_path(*relative_parts):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(base_dir, "..", "..", *relative_parts))


def plot_energy_velocity_toggle(sim_path: str, num, output_dir: str = "visual_output"):
    sim_path = resolve_path(sim_path)
    output_dir = resolve_path(output_dir)

    if not os.path.exists(sim_path):
        print(f"❌ 시뮬레이션 파일을 찾을 수 없습니다:\n{sim_path}")
        return

    with open(sim_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fids = sorted(data.keys(), key=lambda x: float(x))
    distances = [data[fid].get("cumulative_distance", 0) for fid in fids]
    energies = [data[fid].get("energy_total_kWh", 0) for fid in fids]
    velocities = [data[fid].get("velocity_kph", 0) for fid in fids]

    # 🔀 한 Figure에 두 Trace 추가
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=distances, y=energies,
        name="Energy (kWh)",
        line=dict(color="crimson"),
        visible=True  # 기본 표시
    ))

    fig.add_trace(go.Scatter(
        x=distances, y=velocities,
        name="Velocity (kph)",
        line=dict(color="royalblue"),
        visible=False  # 기본 숨김
    ))

    # 📌 버튼 설정 (Energy, Velocity, Both)
    fig.update_layout(
        title="Energy and Velocity over Distance",
        xaxis_title="Cumulative Distance (m)",
        yaxis_title="Value",
        template="plotly_white",
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=[
                    dict(label="Energy", method="update", args=[{"visible": [True, False]}]),
                    dict(label="Velocity", method="update", args=[{"visible": [False, True]}]),
                    dict(label="Both", method="update", args=[{"visible": [True, True]}])
                ],
                active=num,
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            ),
        ]
    )

    # ✅ 저장 및 실행
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "energy_velocity_toggle.html")
    fig.write_html(save_path)
    print(f"✅ 토글 가능한 그래프 저장 완료: {save_path}")

    return save_path


# # ✅ 단독 실행
# if __name__ == "__main__":
#     plot_energy_velocity_toggle("algorithms/simulation_results/final_simulation(Lucinda).json")
