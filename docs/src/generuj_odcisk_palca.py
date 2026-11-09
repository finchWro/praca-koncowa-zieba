import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

# Ścieżki
mat_path = '/home/finch/repo/DeepLearning-CoordinatedBeamforming-python/DLCB_dataset/DLCB_input.mat'
out_path = '/home/finch/repo/praca-koncowa-zieba/docs/figures/rf_fingerprint_frequency.png'

print("Wczytywanie DLCB_input.mat...")
mat = sio.loadmat(mat_path)
dl_input = mat['DL_input']  # shape: (54481, 256) complex128
num_samples = dl_input.shape[0]
data = dl_input.reshape(num_samples, 4, 64)

# Znormalizowana moc w dB oraz faza w radianach
power_db = 10 * np.log10(np.abs(data)**2 + 1e-12)
phase_rad = np.angle(data)

# Wybrany użytkownik w kanionie (środek ulicy przy BS 3/4)
col_idx = 90
row_idx = 70
sample_user_idx = row_idx * 181 + col_idx

subcarriers = np.arange(64)

# Tworzenie klasycznego wykresu analizy spektralnej (Góra: Amplituda, Dół: Faza)
plt.style.use('default')
fig, (ax_amp, ax_phase) = plt.subplots(2, 1, figsize=(11.5, 5.2), dpi=200, sharex=True)

colors = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd']
bs_labels = ['BS 3 (LoS)', 'BS 4 (LoS)', 'BS 5 (odległa)', 'BS 6 (NLoS/tłumiona)']

# --- GÓRA: WIDMO AMPLITUDOWE ---
for bs in range(4):
    ax_amp.plot(subcarriers, power_db[sample_user_idx, bs, :], 
                label=bs_labels[bs], color=colors[bs], lw=2.0, alpha=0.9)

ax_amp.set_title('1. Widmo amplitudowe |H[k]| (Selektywne tłumienie wielodrogowe)', 
                 fontsize=10.5, fontweight='bold', pad=6, color='#111')
ax_amp.set_ylabel('Moc względna [dB]', fontsize=9.5)
ax_amp.grid(True, linestyle='--', alpha=0.5)
ax_amp.legend(loc='lower right', frameon=True, fontsize=8.5, ncol=4)
ax_amp.set_ylim([-36, -6])

# --- DÓŁ: WIDMO FAZOWE ---
for bs in range(4):
    ax_phase.plot(subcarriers, phase_rad[sample_user_idx, bs, :], 
                  label=bs_labels[bs], color=colors[bs], lw=1.8, alpha=0.85, 
                  marker='o', markersize=2.5, markevery=4)

ax_phase.set_title('2. Widmo fazowe ∠H[k] (Kąt nadejścia fali i opóźnienie czasowe)', 
                   fontsize=10.5, fontweight='bold', pad=6, color='#111')
ax_phase.set_xlabel('Indeks podnośnej OFDM (k = 0..63) [wycinek pasma 31,25 MHz]', fontsize=9.5)
ax_phase.set_ylabel('Faza [radiany]', fontsize=9.5)
ax_phase.grid(True, linestyle='--', alpha=0.5)
ax_phase.set_xlim([0, 63])
ax_phase.set_ylim([-np.pi - 0.2, np.pi + 0.2])
ax_phase.set_yticks([-np.pi, 0, np.pi])
ax_phase.set_yticklabels([r'$-\pi$', r'$0$', r'$\pi$'])

# Podpis pod wykresem
plt.figtext(0.5, 0.015, 
            'Klasyczna analiza spektralna (DSP): Widmo amplitudowe (góra) i fazowe (dół) tworzą unikalny odcisk palca kanału radiowego dla każdej stacji BS.',
            ha='center', fontsize=8.5, style='italic', color='#333333')

plt.tight_layout(rect=[0, 0.035, 1, 0.98])

os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=200, bbox_inches='tight')
print(f"Pomyślnie wygenerowano klasyczny wykres spektralny: {out_path}")
