import json
import matplotlib.pyplot as plt
import os

def generate_track_plot(track_json_path: str, output_image_path: str):
    with open(track_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    x_coords = []
    y_coords = []

    for segment in data.values():
        x_coords.append(segment["XStart"])
        y_coords.append(segment["YStart"])
        x_coords.append(segment["XFinish"])
        y_coords.append(segment["YFinish"])

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, color='blue', linewidth=2.5, linestyle='-')

    plt.title("Track Map", fontsize=16, weight='bold', pad=15)
    plt.xlabel("X Coordinate (m)", fontsize=12)
    plt.ylabel("Y Coordinate (m)", fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # 배경 흰색
    fig = plt.gcf()
    fig.patch.set_facecolor('white')

    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=120)
    plt.close()
