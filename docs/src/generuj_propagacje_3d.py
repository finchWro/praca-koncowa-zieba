"""
Skrypt generujący trójwymiarową (3D) infografikę fizyki propagacji:
Panel 1: Łącze w górę (Uplink) — Fala kulista w 3D (bezpośrednia oraz odbite czoła fal) i 5 geometrycznych promieni (Rays).
Panel 2: Łącze w dół (Downlink) — Trójwymiarowa skupiona wiązka ołówkowa (3D Pencil Beam) ze stacji Massive MIMO.
Bez nakładających się napisów — czytelna numeracja i estetyczna legenda.
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def rysuj_prostopadloscian(ax, x0, y0, z0, dx, dy, dz, color, alpha=0.25, edge_color="#64748B"):
    """Rysuje prostopadłościan (budynek) w przestrzeni 3D."""
    # 8 wierzchołków
    v = np.array([
        [x0, y0, z0],
        [x0 + dx, y0, z0],
        [x0 + dx, y0 + dy, z0],
        [x0, y0 + dy, z0],
        [x0, y0, z0 + dz],
        [x0 + dx, y0, z0 + dz],
        [x0 + dx, y0 + dy, z0 + dz],
        [x0, y0 + dy, z0 + dz]
    ])
    # 6 ścian
    faces = [
        [v[0], v[1], v[2], v[3]], # dół
        [v[4], v[5], v[6], v[7]], # góra
        [v[0], v[1], v[5], v[4]], # przód
        [v[2], v[3], v[7], v[6]], # tył
        [v[0], v[3], v[7], v[4]], # lewo
        [v[1], v[2], v[6], v[5]]  # prawo
    ]
    poly = Poly3DCollection(faces, facecolors=color, linewidths=1.0, edgecolors=edge_color, alpha=alpha)
    ax.add_collection3d(poly)

def generuj_3d():
    fig = plt.figure(figsize=(18, 9), facecolor="#F8FAFC")

    # =========================================================================
    # PARAMETRY GEOMETRII KANIONU ULICY (w metrach)
    # =========================================================================
    # Ulica: szerokość X od 0 do 24 m, długość Y od 0 do 45 m
    # Budynek Lewy: X od -10 do 0, Y 0..45, Z 0..16
    # Budynek Prawy: X od 24 do 34, Y 0..45, Z 0..16
    # Stacja bazowa BS: X = 0.5 (na ścianie lewego), Y = 38, Z = 6.0
    # Telefon UE: X = 15, Y = 6, Z = 1.5

    ue_pos = np.array([15.0, 6.0, 1.5])
    bs_pos = np.array([0.5, 38.0, 6.0])

    # Punkty odbić w 3D:
    # 2. Odbicie prawe (na ścianie X = 24)
    odb_prawa = np.array([24.0, 21.0, 3.8])
    # 3. Odbicie od asfaltu (Z = 0)
    odb_grunt = np.array([10.0, 22.0, 0.0])
    # 4. Odbicie lewe (na ścianie X = 0)
    odb_lewa = np.array([0.0, 18.0, 3.2])
    # 5. Podwójne odbicie (prawo -> lewo -> BS)
    odb_5a = np.array([24.0, 12.0, 2.5])
    odb_5b = np.array([0.0, 28.0, 4.5])

    # Ustawienia widoku 3D
    elev_ang = 28
    azim_ang = -55

    for ax_idx, title in enumerate([
        "A. Faza Pomiaru (Uplink): Kula falowa w 3D i 5 promieni fizycznych\n(Rozchodzące się sfery bezpośrednie oraz fale po odbiciu od ścian i jezdni)",
        "B. Faza Transmisji Danych (Downlink): Skupiona wiązka ołówkowa (3D Pencil Beam)\n(Energia z 256 anten skupiona w wąski stożek 4° w stronę telefonu)"
    ]):
        ax = fig.add_subplot(1, 2, ax_idx + 1, projection="3d")
        ax.set_facecolor("#FFFFFF")

        # Rysowanie kanionu ulicy
        rysuj_prostopadloscian(ax, -12, 0, 0, 12, 45, 16, "#E2E8F0", alpha=0.3, edge_color="#94A3B8")
        rysuj_prostopadloscian(ax, 24, 0, 0, 12, 45, 16, "#E2E8F0", alpha=0.3, edge_color="#94A3B8")

        # Jezdnia
        asfalt = Poly3DCollection([
            [[0, 0, 0], [24, 0, 0], [24, 45, 0], [0, 45, 0]]
        ], facecolors="#F8FAFC", edgecolors="#CBD5E1", alpha=0.8, linewidths=1.2)
        ax.add_collection3d(asfalt)

        # Pas jezdni
        for yy in range(2, 44, 5):
            ax.plot([12, 12], [yy, yy + 2.5], [0.02, 0.02], color="#CBD5E1", lw=2)

        # Telefon UE
        ax.scatter([ue_pos[0]], [ue_pos[1]], [ue_pos[2]], color="#2563EB", s=140, edgecolors="black", lw=1.5, zorder=10)
        ax.text(ue_pos[0], ue_pos[1] - 3.5, ue_pos[2], "Telefon (UE)\nZ = 1,5 m", color="#1D4ED8",
                fontsize=8.5, fontweight="bold", ha="center")

        # Maszt stacji bazowej BS
        ax.plot([bs_pos[0], bs_pos[0]], [bs_pos[1], bs_pos[1]], [0, bs_pos[2]], color="#64748B", lw=3)
        ax.scatter([bs_pos[0]], [bs_pos[1]], [bs_pos[2]], color="#DC2626", s=160, marker="s", edgecolors="black", lw=1.5, zorder=10)
        ax.text(bs_pos[0] + 1, bs_pos[1] + 1.5, bs_pos[2] + 1.2, "Stacja BS\n(Panel 256 anten, Z=6m)",
                color="#B91C1C", fontsize=8.5, fontweight="bold")

        # Etykiety budynków
        ax.text(-6, 22.5, 16.5, "Budynek A (lewy)", color="#64748B", fontsize=8.5, fontweight="bold", ha="center")
        ax.text(30, 22.5, 16.5, "Budynek B (prawy)", color="#64748B", fontsize=8.5, fontweight="bold", ha="center")

        if ax_idx == 0:
            # =================================================================
            # PANEL 1: FALA KULISTA + ODBITE SFERY + 5 PROMIENI
            # =================================================================
            # 1. Bezpośrednie fale kuliste z telefonu (łuki w przestrzeni 3D)
            for r in np.linspace(5, 35, 7):
                phi = np.linspace(-np.pi/3, np.pi/3, 50)
                for th in [0.2, 0.4, 0.6]:
                    arc_x = ue_pos[0] + r * np.sin(th) * np.sin(phi)
                    arc_y = np.full_like(arc_x, ue_pos[1] + r * np.cos(th))
                    arc_z = ue_pos[2] + r * np.sin(th) * np.cos(phi) * 0.4
                    valid = (arc_x >= 0) & (arc_x <= 24) & (arc_y >= 0) & (arc_y <= 45) & (arc_z >= 0)
                    if np.any(valid):
                        ax.plot(arc_x[valid], arc_y[valid], arc_z[valid], color="#38BDF8", ls="--", lw=1.0, alpha=0.55)

            # 2. Odbite fale kuliste (rozchodzące się od punktu odbicia na prawej ścianie)
            for r_ref in [4, 9, 15, 22]:
                phi_ref = np.linspace(np.pi/2, 3*np.pi/2, 40)
                arc_rx = odb_prawa[0] - r_ref * np.cos(phi_ref) * 0.7
                arc_ry = odb_prawa[1] + r_ref * np.sin(phi_ref)
                arc_rz = np.full_like(arc_rx, odb_prawa[2]) + r_ref * 0.25 * np.cos(phi_ref)
                valid_ref = (arc_rx >= 0) & (arc_rx <= 24) & (arc_ry >= 0) & (arc_ry <= 45) & (arc_rz >= 0)
                if np.any(valid_ref):
                    ax.plot(arc_rx[valid_ref], arc_ry[valid_ref], arc_rz[valid_ref], color="#FDBA74", ls=":", lw=1.3, alpha=0.7)

            # 3. 5 Najsilniejszych Promieni (Rays) w 3D
            # Promień 1: LoS
            ax.plot([ue_pos[0], bs_pos[0]], [ue_pos[1], bs_pos[1]], [ue_pos[2], bs_pos[2]],
                    color="#DC2626", lw=3.2, label="[1] Ścieżka bezpośrednia LoS (80% energii)")
            ax.text((ue_pos[0] + bs_pos[0])/2 - 1, (ue_pos[1] + bs_pos[1])/2, (ue_pos[2] + bs_pos[2])/2 + 1.5,
                    "[1] LoS", color="#DC2626", fontsize=9, fontweight="bold")

            # Promień 2: Odbicie prawe
            ax.plot([ue_pos[0], odb_prawa[0], bs_pos[0]],
                    [ue_pos[1], odb_prawa[1], bs_pos[1]],
                    [ue_pos[2], odb_prawa[2], bs_pos[2]],
                    color="#EA580C", lw=2.2, label="[2] Odbicie od prawej ściany (12% energii)")
            ax.scatter([odb_prawa[0]], [odb_prawa[1]], [odb_prawa[2]], color="#EA580C", s=60, marker="o")
            ax.text(odb_prawa[0] - 2, odb_prawa[1], odb_prawa[2] + 1.2, "[2]", color="#EA580C", fontsize=9, fontweight="bold")

            # Promień 3: Odbicie od ziemi (asfalt)
            ax.plot([ue_pos[0], odb_grunt[0], bs_pos[0]],
                    [ue_pos[1], odb_grunt[1], bs_pos[1]],
                    [ue_pos[2], odb_grunt[2], bs_pos[2]],
                    color="#0284C7", lw=1.8, ls="-.", label="[3] Odbicie od jezdni (5% energii)")
            ax.scatter([odb_grunt[0]], [odb_grunt[1]], [odb_grunt[2]], color="#0284C7", s=50, marker="s")
            ax.text(odb_grunt[0], odb_grunt[1] - 1.5, odb_grunt[2] + 1.0, "[3]", color="#0284C7", fontsize=9, fontweight="bold")

            # Promień 4: Odbicie lewe
            ax.plot([ue_pos[0], odb_lewa[0], bs_pos[0]],
                    [ue_pos[1], odb_lewa[1], bs_pos[1]],
                    [ue_pos[2], odb_lewa[2], bs_pos[2]],
                    color="#16A34A", lw=1.5, ls=":", label="[4] Odbicie od lewej ściany (2% energii)")
            ax.scatter([odb_lewa[0]], [odb_lewa[1]], [odb_lewa[2]], color="#16A34A", s=50, marker="^")
            ax.text(odb_lewa[0] + 1.5, odb_lewa[1], odb_lewa[2] + 1.2, "[4]", color="#16A34A", fontsize=9, fontweight="bold")

            # Promień 5: Podwójne odbicie
            ax.plot([ue_pos[0], odb_5a[0], odb_5b[0], bs_pos[0]],
                    [ue_pos[1], odb_5a[1], odb_5b[1], bs_pos[1]],
                    [ue_pos[2], odb_5a[2], odb_5b[2], bs_pos[2]],
                    color="#9333EA", lw=1.2, ls="--", label="[5] Podwójne odbicie (<1% energii)")
            ax.text(odb_5a[0] - 2, odb_5a[1], odb_5a[2] + 1.0, "[5]", color="#9333EA", fontsize=9, fontweight="bold")

            # Legenda z czytelnym zestawieniem promieni
            leg = ax.legend(loc="upper left", bbox_to_anchor=(-0.15, 1.0), fontsize=8.2, framealpha=0.95,
                            edgecolor="#CBD5E1", title="5 Najsilniejszych Ścieżek (Multipath):", title_fontsize=8.8)
            leg.get_title().set_fontweight("bold")

        else:
            # =================================================================
            # PANEL 2: SKUPIONA WIĄZKA 3D (BEAMFORMING)
            # =================================================================
            # Generowanie trójwymiarowego stożka wiązki (Pencil Beam)
            v_dir = ue_pos - bs_pos
            length = np.linalg.norm(v_dir)
            v_unit = v_dir / length

            # Baza ortogonalna dla przekroju wiązki
            if abs(v_unit[2]) < 0.9:
                u1 = np.cross(v_unit, [0, 0, 1])
            else:
                u1 = np.cross(v_unit, [0, 1, 0])
            u1 /= np.linalg.norm(u1)
            u2 = np.cross(v_unit, u1)

            # Promień wiązki o kącie ~4 stopnie
            t_steps = np.linspace(0, 1, 25)
            theta_cone = np.linspace(0, 2*np.pi, 30)

            # Powierzchnia stożka 3D
            T, TH = np.meshgrid(t_steps, theta_cone)
            radius_cone = T * (length * np.tan(np.radians(2.5)))

            cone_x = bs_pos[0] + T * v_dir[0] + radius_cone * (np.cos(TH) * u1[0] + np.sin(TH) * u2[0])
            cone_y = bs_pos[1] + T * v_dir[1] + radius_cone * (np.cos(TH) * u1[1] + np.sin(TH) * u2[1])
            cone_z = bs_pos[2] + T * v_dir[2] + radius_cone * (np.cos(TH) * u1[2] + np.sin(TH) * u2[2])

            ax.plot_surface(cone_x, cone_y, cone_z, color="#EF4444", alpha=0.35, edgecolor="#DC2626", lw=0.3)

            # Rdzeń wiązki
            ax.plot([bs_pos[0], ue_pos[0]], [bs_pos[1], ue_pos[1]], [bs_pos[2], ue_pos[2]],
                    color="#B91C1C", lw=3.8, label="Główny rdzeń wiązki (Maksymalna moc)")

            # Ramka informacyjna dla panelu B
            ax.text(12, 10, 13.5,
                    "WŁAŚCIWOŚCI WIĄZKI 3D:\n"
                    "• Skupienie energii: stożek ~4°\n"
                    "• Zysk szyku 256 anten: moc wzrasta x256\n"
                    "• Zero strat energii w niebo i puste ściany!",
                    fontsize=8.5, fontweight="bold", color="#B91C1C",
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF2F2", edgecolor="#FECACA", lw=1.2))

            leg2 = ax.legend(loc="upper left", bbox_to_anchor=(-0.1, 1.0), fontsize=8.5, framealpha=0.95,
                             edgecolor="#CBD5E1", title="Downlink Beamforming:", title_fontsize=8.8)
            leg2.get_title().set_fontweight("bold")

        ax.set_title(title, fontsize=11, fontweight="bold", pad=12, color="#0F172A")
        ax.set_xlim(-12, 36)
        ax.set_ylim(-2, 46)
        ax.set_zlim(0, 18)
        ax.view_init(elev=elev_ang, azim=azim_ang)

        # Usunięcie zbędnych cyfr osi dla czystości rysunku
        ax.set_xlabel("Szerokość kanionu [m]", fontsize=8.5, labelpad=4)
        ax.set_ylabel("Długość ulicy [m]", fontsize=8.5, labelpad=4)
        ax.set_zlabel("Wysokość [m]", fontsize=8.5, labelpad=2)
        ax.grid(True, ls=":", alpha=0.4)

    plt.suptitle("Zjawisko Propagacji 3D w Kanionie Miejskim 5G mmWave (60 GHz)\nOd fali sferycznej i odbić wielodrogowych do skupionej wiązki przestrzennej",
                 fontsize=13.5, fontweight="bold", y=0.98, color="#0F172A")

    plt.tight_layout()
    plt.subplots_adjust(top=0.88)

    out_path = "/home/finch/repo/praca-koncowa-zieba/docs/figures/propagacja_3d_kula_i_wiazka.png"
    plt.savefig(out_path, dpi=160, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Zapisano grafikę 3D do: {out_path}")

if __name__ == "__main__":
    generuj_3d()
