"""Wizualizacja przestrzenna mechanizmu ray-tracingu w 3D (scenariusz DeepMIMO o1_60).

Skrypt generuje rycinę eksponującą trójwymiarową naturę propagacji fal milimetrowych
w kanionie miejskim i eliminującą problem nakładania się ścieżek z rzutu 2D:
  1. Panel A: Szeroka perspektywa przestrzenna 3D (z góry kanionu) – bryły budynków,
     4 stacje bazowe, terminal użytkownika oraz pełne trajektorie promieni 3D
     z pionowymi liniami rzutowania punktów odbić na poziom terenu.
  2. Panel B: Zbliżenie perspektywiczne 3D wzdłuż kanionu ulicznego (niski kąt obserwacji) –
     wyraźne wyeksponowanie wysokości masztu stacji bazowej (z=6 m) i anteny UE (z=2 m),
     obrazujące fizyczne rozdzielenie ścieżki bezpośredniej (w powietrzu) od odbicia
     od nawierzchni jezdni (asfaltu) oraz odbić elewacyjnych.

Legenda znajduje się w dedykowanym pasie na górze ryciny.
Wygenerowany wykres jest zapisywany w outputs/figures/ray_tracing_wizualizacja.png.
"""

import argparse
import json
import os

# Konfiguracja pamięci podręcznej Matplotlib w katalogu projektu
os.environ['MPLCONFIGDIR'] = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.cache'
)

import deepmimo as dm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import scipy.io as sio


def parsuj_argumenty():
    """Parsuje opcje wiersza poleceń."""
    domyslny_katalog_projektu = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domyslny_folder_scenariuszy = os.path.join(
        domyslny_katalog_projektu, 'data', 'deepmimo_scenarios'
    )
    domyslny_plik_wyjsciowy = os.path.join(
        domyslny_katalog_projektu, 'outputs', 'figures', 'ray_tracing_wizualizacja.png'
    )

    parser = argparse.ArgumentParser(
        description='Wizualizacja propagacji ray-tracingu 3D w scenariuszu DeepMIMO o1_60.'
    )
    parser.add_argument(
        '--scenarios-folder',
        type=str,
        default=domyslny_folder_scenariuszy,
        help='Ścieżka do folderu zawierającego scenariusz o1_60.',
    )
    parser.add_argument(
        '--scenario',
        type=str,
        default='o1_60',
        help='Nazwa scenariusza DeepMIMO (domyślnie: o1_60).',
    )
    parser.add_argument(
        '--user-row',
        type=int,
        default=1100,
        help='Numer wiersza użytkownika (1-based, np. 1100).',
    )
    parser.add_argument(
        '--output',
        type=str,
        default=domyslny_plik_wyjsciowy,
        help='Ścieżka zapisu generowanego wykresu (PNG/PDF).',
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='Rozdzielczość generowanego obrazu (domyślnie: 300 DPI).',
    )
    return parser.parse_args()


def wczytaj_geometrie_budynkow(scenarios_folder: str, scenario_name: str):
    """Wczytuje wierzchołki 3D budynków z plików scenariusza."""
    scen_dir = os.path.join(scenarios_folder, scenario_name)
    objs_path = os.path.join(scen_dir, 'objects.json')
    vert_path = os.path.join(scen_dir, 'vertices.mat')

    if not os.path.exists(objs_path) or not os.path.exists(vert_path):
        raise FileNotFoundError(
            f'Nie odnaleziono plików geometrii scenariusza w katalogu: {scen_dir}'
        )

    with open(objs_path, 'r', encoding='utf-8') as f:
        objects = json.load(f)
    vertices = sio.loadmat(vert_path)['vertices']

    budynki = []
    for obj in objects:
        if obj.get('label') == 'buildings':
            idxs = obj['face_vertex_idxs']
            polygony_3d = [vertices[face] for face in idxs]
            podstawa_2d = vertices[idxs[0]][:, :2]
            z_max = max(vertices[face][:, 2].max() for face in idxs)
            budynki.append({
                'nazwa': obj['name'],
                'podstawa_2d': podstawa_2d,
                'polygony_3d': polygony_3d,
                'z_max': z_max,
            })
    return budynki


def generuj_wizualizacje_3d(
    scenarios_folder: str,
    scenario_name: str,
    user_row: int,
    output_path: str,
    dpi: int = 300,
):
    """Generuje dwupanelowy wykres skupiony w pełni na przestrzeni trójwymiarowej (3D)."""
    dm.config('scenarios_folder', scenarios_folder)

    aktywne_tx_ids = [4, 7, 3, 6]
    stacje_etykiety = {
        4: 'BS 3 (TX_3)',
        7: 'BS 4 (TX_4)',
        3: 'BS 5 (TX_5)',
        6: 'BS 6 (TX_6)',
    }

    print(f'Wczytywanie danych ray-tracingu dla scenariusza {scenario_name}...')
    dataset = dm.load(
        scenario_name,
        tx_sets=aktywne_tx_ids,
        rx_sets=[0],
        max_paths=5,
    )

    ue_row_idxs = dataset[0].get_idxs('row', row_idxs=[user_row])
    ue_idx_w_wierszu = len(ue_row_idxs) // 2
    ue_global_idx = ue_row_idxs[ue_idx_w_wierszu]

    rx_pos = dataset[0]['rx_pos'][ue_global_idx]
    print(f'Wybrany użytkownik wiersza R{user_row}: położenie = {rx_pos}')

    ds_bs5 = None
    for d in dataset:
        if d.txrx.tx_set_id == 3:
            ds_bs5 = d
            break
    if ds_bs5 is None:
        ds_bs5 = dataset[0]

    tx_pos = ds_bs5['tx_pos'][0]

    # Ekstrakcja 5 ścieżek ray-tracingu
    kolory_promieni = ['#00802b', '#e67300', '#0066cc', '#9900cc', '#cc0000']
    style_promieni = ['-', '--', '-.', ':', '-']

    opisy_sciezek = {
        0: 'Ścieżka bezpośrednia (LOS, w powietrzu)',
        1: 'Odbicie od ściany zachodniej (z=5,5 m)',
        2: 'Odbicie od nawierzchni jezdni (asfalt, z=0,4 m)',
        3: 'Odbicie podwójne: ściana → podłoże → UE',
        4: 'Odbicie podwójne: ściana zach. → wschodnia → UE',
    }

    sciezki = []
    for p in range(5):
        pwr = ds_bs5['power'][ue_global_idx, p]
        delay = ds_bs5['delay'][ue_global_idx, p]
        inter = ds_bs5['inter'][ue_global_idx, p]
        inter_pts = ds_bs5['inter_pos'][ue_global_idx, p]

        if np.isnan(pwr):
            continue

        valid_bounces = inter_pts[~np.isnan(inter_pts).any(axis=1)]

        punkty = [tx_pos]
        for pt in valid_bounces:
            punkty.append(pt)
        punkty.append(rx_pos)
        punkty = np.array(punkty)

        opis = opisy_sciezek.get(p, f'Odbicie {p}. rzędu')

        sciezki.append({
            'id': p + 1,
            'punkty': punkty,
            'punkty_odbic': valid_bounces,
            'moc_dbm': pwr,
            'opoznienie_ns': delay * 1e9,
            'typ_interakcji': inter,
            'opis': f"{opis} ({pwr:.1f} dBm, {delay * 1e9:.1f} ns)",
            'kolor': kolory_promieni[p % len(kolory_promieni)],
            'styl': style_promieni[p % len(style_promieni)],
        })

    budynki = wczytaj_geometrie_budynkow(scenarios_folder, scenario_name)

    # %% Tworzenie kompozycji ryciny: górna belka legendy + dwa panele 3D
    fig = plt.figure(figsize=(18, 9.5), dpi=dpi)
    gs = fig.add_gridspec(2, 1, height_ratios=[0.11, 0.89], hspace=0.10)

    # Dedykowany wiersz na legendę u góry (gwarantuje zero kolizji z osiami)
    ax_leg = fig.add_subplot(gs[0])
    ax_leg.axis('off')

    # Dwa panele 3D obok siebie
    gs_plots = gs[1].subgridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.16)
    ax_3d_a = fig.add_subplot(gs_plots[0, 0], projection='3d')
    ax_3d_b = fig.add_subplot(gs_plots[0, 1], projection='3d')

    konfiguracje_paneli = [
        (
            ax_3d_a,
            26,
            -52,
            'A. Widok perspektywiczny 3D z góry (geometria kanionu i odbicia)',
            (160, 360),
            (470, 615),
            True,  # czy pokazać pozostałe stacje BS
        ),
        (
            ax_3d_b,
            13,
            -78,
            'B. Widok 3D wzdłuż kanionu (rozdzielenie wysokości: LOS vs podłoże vs ściany)',
            (180, 340),
            (490, 605),
            False,
        ),
    ]

    for ax, elev, azim, tytul, xlim, ylim, pokaz_inne_bs in konfiguracje_paneli:
        ax.set_title(tytul, fontsize=11.5, fontweight='bold', pad=12)

        # 1. Rysowanie nawierzchni ulicy / terenu na poziomie z=0
        xx, yy = np.meshgrid(np.linspace(242.4, 278.4, 10), np.linspace(ylim[0], ylim[1], 10))
        zz = np.zeros_like(xx)
        ax.plot_surface(xx, yy, zz, color='#e6ecf2', alpha=0.35, zorder=1)

        # 2. Rysowanie brył budynków w 3D
        for b in budynki:
            if 150 <= b['podstawa_2d'][:, 0].mean() <= 370 and 450 <= b['podstawa_2d'][:, 1].mean() <= 630:
                for face_pts in b['polygony_3d']:
                    poly_3d = Poly3DCollection(
                        [face_pts],
                        facecolors='#d8d8d8',
                        edgecolors='#707070',
                        linewidths=0.6,
                        alpha=0.32,
                        zorder=2,
                    )
                    ax.add_collection3d(poly_3d)

        # 3. Rysowanie współpracujących stacji bazowych (jeśli włączone)
        if pokaz_inne_bs:
            for d in dataset:
                tx_p = d['tx_pos'][0]
                tx_id = d.txrx.tx_set_id
                if tx_id != ds_bs5.txrx.tx_set_id:
                    etykieta = stacje_etykiety.get(tx_id, f'BS_{tx_id}')
                    ax.scatter(
                        [tx_p[0]], [tx_p[1]], [tx_p[2]],
                        c='#004c99', marker='^', s=120, edgecolors='black', linewidth=1.1, zorder=5,
                    )
                    ax.plot(
                        [tx_p[0], tx_p[0]], [tx_p[1], tx_p[1]], [0, tx_p[2]],
                        color='#004c99', linestyle='--', linewidth=1.5, zorder=4,
                    )
                    ax.text(
                        tx_p[0] + (6 if tx_p[0] > 250 else -28), tx_p[1], tx_p[2] + 2.0,
                        f'{etykieta}\n(z=6 m)',
                        fontsize=7.5, fontweight='bold', color='#004c99', zorder=6,
                    )

        # 4. Aktywny nadajnik BS 5 (TX_5)
        ax.scatter(
            [tx_pos[0]], [tx_pos[1]], [tx_pos[2]],
            c='#b30000', marker='^', s=170, edgecolors='black', linewidth=1.3, zorder=6,
            label='Aktywna stacja bazowa BS 5 (maszt z=6.0 m)',
        )
        ax.plot(
            [tx_pos[0], tx_pos[0]], [tx_pos[1], tx_pos[1]], [0, tx_pos[2]],
            color='#b30000', linestyle='-', linewidth=2.8, zorder=5,
        )
        ax.text(
            tx_pos[0] - 12, tx_pos[1], tx_pos[2] + 3.0,
            'BS 5 (TX_5)\nz=6.0 m',
            fontsize=8.5, fontweight='bold', color='#b30000', zorder=7,
        )

        # 5. Odbiornik użytkownika (UE)
        ax.scatter(
            [rx_pos[0]], [rx_pos[1]], [rx_pos[2]],
            c='#e41a1c', marker='*', s=260, edgecolors='black', linewidth=1.3, zorder=6,
            label=f'Odbiornik UE (wiersz R{user_row}, dach pojazdu z=2.0 m)',
        )
        ax.plot(
            [rx_pos[0], rx_pos[0]], [rx_pos[1], rx_pos[1]], [0, rx_pos[2]],
            color='#e41a1c', linestyle='-', linewidth=2.2, zorder=5,
        )
        ax.text(
            rx_pos[0] + 6, rx_pos[1] - 4, rx_pos[2] + 2.2,
            f'UE (R{user_row})\nz=2.0 m',
            fontsize=8.5, fontweight='bold', color='#990000', zorder=7,
        )

        # 6. Promienie wielodrogowości z liniami rzutowania wysokości odbić
        for s in sciezki:
            pts = s['punkty']
            ax.plot(
                pts[:, 0], pts[:, 1], pts[:, 2],
                linestyle=s['styl'],
                color=s['kolor'],
                linewidth=2.4,
                alpha=0.92,
                zorder=4,
                label=s['opis'] if pokaz_inne_bs else None,
            )

            # Oznaczenie punktów odbić oraz pionowych linii rzutowania na podłoże
            if len(s['punkty_odbic']) > 0:
                for pt in s['punkty_odbic']:
                    # Kropka punktu odbicia na ścianie lub podłożu
                    ax.scatter(
                        [pt[0]], [pt[1]], [pt[2]],
                        facecolors='white', edgecolors=s['kolor'],
                        marker='o', s=65, linewidth=2.2, zorder=6,
                    )
                    # Pionowa linia rzutu punktu odbicia na poziom terenu (z=0)
                    ax.plot(
                        [pt[0], pt[0]], [pt[1], pt[1]], [0, pt[2]],
                        color=s['kolor'], linestyle=':', linewidth=1.2, alpha=0.65, zorder=3,
                    )

        ax.set_xlim(xlim[0], xlim[1])
        ax.set_ylim(ylim[0], ylim[1])
        ax.set_zlim(0, 32)
        ax.set_xlabel('X – szerokość [m]', fontsize=9.5, fontweight='bold', labelpad=7)
        ax.set_ylabel('Y – długość [m]', fontsize=9.5, fontweight='bold', labelpad=7)
        ax.set_zlabel('Z – wysokość [m]', fontsize=9.5, fontweight='bold', labelpad=7)
        ax.view_init(elev=elev, azim=azim)

    # -------------------------------------------------------------
    # WSPÓLNA LEGENDA NA GÓRZE RYCINY
    # -------------------------------------------------------------
    uchwyty, etykiety = ax_3d_a.get_legend_handles_labels()
    # Dodanie oznaczenia współpracujących stacji CoMP do legendy
    komp_uchwyt = plt.Line2D(
        [0], [0],
        marker='^', color='w', markerfacecolor='#004c99',
        markeredgecolor='black', markersize=10, linewidth=0,
    )
    uchwyty.insert(1, komp_uchwyt)
    etykiety.insert(1, 'Współpracujące stacje bazowe BS (CoMP, z=6 m)')

    ax_leg.legend(
        uchwyty,
        etykiety,
        loc='center',
        bbox_to_anchor=(0.5, 0.45),
        ncol=3,
        fontsize=9.5,
        frameon=True,
        facecolor='#ffffff',
        edgecolor='#d0d0d0',
        framealpha=0.98,
        columnspacing=1.6,
        handletextpad=0.7,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    plt.close()
    print(f'Pomyślnie wygenerowano i zapisano wykres 3D w: {output_path}')


def main():
    args = parsuj_argumenty()
    generuj_wizualizacje_3d(
        scenarios_folder=args.scenarios_folder,
        scenario_name=args.scenario,
        user_row=args.user_row,
        output_path=args.output,
        dpi=args.dpi,
    )


if __name__ == '__main__':
    main()
