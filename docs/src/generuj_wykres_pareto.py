"""
Skrypt generujący profesjonalny wykres Frontu Pareto dla pytania badawczego PB2
do prezentacji KRK L2 (slajd 17).
Wizualizuje kompromis pomiędzy złożonością modelu (rozmiar/parametry oraz czas inferencji)
a osiąganą efektywnością spektralną netto.
"""

import json
import matplotlib.pyplot as plt
import numpy as np

def generuj_pareto():
    json_path = "/home/finch/repo/DeepLearning-CoordinatedBeamforming-python/outputs_pb2/tables/porownanie_architektur_pb2.json"
    with open(json_path, "r", encoding="utf-8") as f:
        wyniki = json.load(f)

    genie_rate = 5.6156
    baseline_rate = 3.6264

    # Kolory dla rodzin
    kolory_rodzin = {
        "Gęsta (MLP)": "#1f77b4",
        "Splotowa 1D": "#2ca02c",
        "Splotowa 2D": "#17becf",
        "Rezydualna (ResNet)": "#9467bd",
        "Atencyjna (Attention)": "#d62728",
        "Klasyfikacyjna": "#ff7f0e",
    }

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 13,
        "mathtext.fontset": "cm"
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2), facecolor="#F8F9FA")

    # Dane do wykresów
    names = [r["nazwa"].split("(")[0].strip() for r in wyniki]
    rates = [r["net_rate_bps_hz"] for r in wyniki]
    params_k = [r["params_1bs"] / 1e3 for r in wyniki]
    latencies = [r["infer_batch_us"] for r in wyniki]
    colors = [kolory_rodzin.get(r["rodzina"], "#333333") for r in wyniki]

    # --- PANEL 1: Parametry vs Efektywność ---
    ax1.set_facecolor("#FFFFFF")
    for x, y, c, n in zip(params_k, rates, colors, names):
        ax1.scatter(x, y, s=180, color=c, edgecolor="black", lw=1.2, zorder=5)
        # Adnotacje
        offset_y = 7 if n != "MLP" else -14
        offset_x = 6 if n != "ResMLP" else -45
        ax1.annotate(n, (x, y), textcoords="offset points", xytext=(offset_x, offset_y),
                     fontsize=9.5, fontweight="bold", color="#222222")

    # Linia frontu Pareto: 2D-CNN (161k, 5.08) -> 1D-CNN (196k, 5.25) -> MLP Classifier (461k, 5.44)
    pareto_x1 = [160.992, 196.320, 460.544]
    pareto_y1 = [5.0754, 5.2501, 5.4435]
    ax1.plot(pareto_x1, pareto_y1, color="#E63946", ls="--", lw=2.4, zorder=4, label="Front Pareto (rozwiązania optymalne)")
    ax1.fill_between(pareto_x1, pareto_y1, 4.8, color="#E63946", alpha=0.06)

    ax1.axhline(genie_rate, color="black", ls=":", lw=1.5, label=f"Genie-Aided ({genie_rate:.2f} bit/s/Hz)")
    ax1.set_xlabel("Liczba parametrów modelu na 1 stację BS [tys. wag]", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("Efektywność spektralna netto [bit/s/Hz]", fontsize=10.5, fontweight="bold")
    ax1.set_title("A. Kompromis: Rozmiar pamięciowy vs Efektywność", fontsize=11.5, fontweight="bold", pad=8)
    ax1.set_ylim(4.88, 5.72)
    ax1.set_xlim(120, 640)
    ax1.grid(True, ls=":", alpha=0.6)
    ax1.legend(loc="lower right", fontsize=9, framealpha=0.92)

    # Wskazanie kierunku optymalizacji
    ax1.annotate("Kierunek optymalizacji\n(mniej wag, wyższy transfer)",
                 xy=(180, 5.52), xytext=(260, 5.58),
                 arrowprops=dict(arrowstyle="->", lw=1.6, color="#1D3557"),
                 fontsize=8.5, fontweight="bold", color="#1D3557")

    # --- PANEL 2: Czas inferencji vs Efektywność ---
    ax2.set_facecolor("#FFFFFF")
    for x, y, c, n in zip(latencies, rates, colors, names):
        ax2.scatter(x, y, s=180, color=c, edgecolor="black", lw=1.2, zorder=5)
        offset_y = 7 if n != "MLP Classifier" else -14
        offset_x = 6 if "CNN" not in n else -50
        ax2.annotate(n, (x, y), textcoords="offset points", xytext=(offset_x, offset_y),
                     fontsize=9.5, fontweight="bold", color="#222222")

    # Linia frontu Pareto dla latencji: MLP (40.7 us, 5.43) / MLP Classifier (42.9 us, 5.44)
    # W latencji MLP jest najszybszy i ma najwyższy transfer!
    pareto_x2 = [40.68, 42.85]
    pareto_y2 = [5.4258, 5.4435]
    ax2.plot(pareto_x2, pareto_y2, color="#E63946", ls="--", lw=2.4, zorder=4, label="Front Pareto (najniższa latencja)")

    ax2.axhline(genie_rate, color="black", ls=":", lw=1.5, label=f"Genie-Aided ({genie_rate:.2f})")
    ax2.set_xlabel("Czas inferencji wsadowej na użytkownika [µs/UE]", fontsize=10.5, fontweight="bold")
    ax2.set_ylabel("Efektywność spektralna netto [bit/s/Hz]", fontsize=10.5, fontweight="bold")
    ax2.set_title("B. Kompromis: Czas inferencji vs Efektywność", fontsize=11.5, fontweight="bold", pad=8)
    ax2.set_ylim(4.88, 5.72)
    ax2.set_xlim(30, 135)
    ax2.grid(True, ls=":", alpha=0.6)
    ax2.legend(loc="lower right", fontsize=9, framealpha=0.92)

    plt.suptitle("PB2: Analiza frontu Pareto (Złożoność obliczeniowa vs Efektywność spektralna CoMP)",
                 fontsize=12.5, fontweight="bold", y=0.98, color="#1D3557")

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)

    out_path = "/home/finch/repo/praca-koncowa-zieba/docs/figures/pb2_front_pareto.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Zapisano wykres Frontu Pareto do: {out_path}")

if __name__ == "__main__":
    generuj_pareto()
