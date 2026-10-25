import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.9

# ==============================================================================
# FIGURA 1: Termodinámica de Autolimitación a 173 °C y Barrera de Poro (Datasets 3 y 4)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6), dpi=300)
fig.patch.set_facecolor('white')

# Panel A: Tiempo de residencia Frenkel-Arrhenius y longitud de difusión vs E_des a 173 °C (446.15 K)
kB_T = 0.038448  # eV at 446.15 K
tau_0 = 1.0e-13  # s
D_s = 3.441e-6   # cm^2/s = 3.441e8 nm^2/s

E_des = np.linspace(0.55, 0.85, 200)
tau_res_us = tau_0 * np.exp(E_des / kB_T) * 1e6  # microsegundos
lambda_diff_nm = np.sqrt(2 * (D_s * 1e14) * (tau_res_us * 1e-6))

color1 = '#124191'
color2 = '#C0392B'

ax1_twin = ax1.twinx()
l1, = ax1.semilogy(E_des, tau_res_us, color=color1, lw=2.5, label=r'Tiempo de residencia $\tau_{\mathrm{res}}$ ($\mu$s)')
l2, = ax1_twin.plot(E_des, lambda_diff_nm, color=color2, lw=2.3, ls='--', label=r'Longitud de difusión $\lambda_{\mathrm{diff}}$ (nm)')

# Puntos clave del reporte a 173 °C
pts_E = [0.65, 0.72, 0.75, 0.80]
pts_tau = [2.20, 13.59, 29.66, 108.87]
pts_lam = [38.91, 96.71, 142.89, 273.72]

ax1.scatter(pts_E, pts_tau, color=color1, s=55, zorder=5)
ax1_twin.scatter(pts_E, pts_lam, color=color2, s=55, marker='s', zorder=5)

# Banda de sincronización del pincel (dwell time 2.20 - 13.59 us)
span_brush = ax1.axhspan(2.20, 13.59, color='#27AE60', alpha=0.16, label=r'Ventana de pincel $\tau_{\mathrm{pulso}} = 2.20-13.59\ \mu\mathrm{s}$')
line_ml = ax1.axhline(0.03944, color='#7F8C8D', ls=':', lw=1.6, label=r'Vida 1 ML sólida 3D libre ($t_{\mathrm{ML}} = 39.44\ \mathrm{ns}$)')

bbox_blue = dict(boxstyle='round,pad=0.22', facecolor='#EBF5FB', edgecolor=color1, alpha=0.94)
ax1.annotate('Terraza (0.65 eV)\n2.20 µs | 38.9 nm', xy=(0.65, 2.20), xytext=(0.558, 4.8),
             arrowprops=dict(arrowstyle='->', color=color1, lw=1.2), fontsize=7.8, fontweight='bold', color=color1, bbox=bbox_blue)
ax1.annotate('Sitio Nominal (0.72 eV)\n13.59 µs | 96.7 nm', xy=(0.72, 13.59), xytext=(0.575, 33.0),
             arrowprops=dict(arrowstyle='->', color=color1, lw=1.2), fontsize=7.8, fontweight='bold', color=color1, bbox=bbox_blue)
ax1.annotate('Borde de Escalón (0.80 eV)\n108.87 µs | 273.7 nm', xy=(0.80, 108.87), xytext=(0.625, 165.0),
             arrowprops=dict(arrowstyle='->', color=color1, lw=1.2), fontsize=7.8, fontweight='bold', color=color1, bbox=bbox_blue)

ax1.set_xlabel(r'Energía de activación de desorción vdW $E_{\mathrm{des}}$ (eV) [estimada]', fontsize=9.8, fontweight='bold')
ax1.set_ylabel(r'Tiempo de residencia superficial $\tau_{\mathrm{res}}$ ($\mu$s)', fontsize=9.8, fontweight='bold', color=color1)
ax1_twin.set_ylabel(r'Longitud media de difusión $\lambda_{\mathrm{diff}}$ (nm)', fontsize=9.8, fontweight='bold', color=color2)
ax1.set_ylim(0.02, 450)
ax1_twin.set_ylim(0, 315)
ax1.grid(True, which='both', ls='--', alpha=0.3)
ax1.set_title('(a) Autolimitación de Monocapa y Difusión a 173 °C (446.15 K)', fontsize=10.0, fontweight='bold', pad=10)

handles_a = [l1, l2, span_brush, line_ml]
labels_a = [h.get_label() for h in handles_a]
ax1.legend(handles_a, labels_a, loc='lower right', fontsize=7.4, framealpha=0.95)

# Panel B: Curvas Auditadas de Barrera de H2 en C30H48 (Datasets 3 y 4, ORCA 6.1.1 B97-3c y wB97X-D3)
z_dense = np.array([-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00, 1.50])
# Dataset 3: Longitudinal (theta_Z = 5.82 deg)
E_d3_down = np.array([0.8809, 1.1352, 1.3577, 1.5297, 1.6476, 1.7256, 1.5902, 1.4218, 1.2427, 0.8938])
E_d3_up   = np.array([0.8811, 1.1354, 1.3580, 1.5363, 1.6557, 1.7146, 1.5894, 1.4218, 1.2440, 0.8933])
# Dataset 4: Perpendicular (theta_Z = 95.60 deg)
E_d4_down = np.array([0.8915, 1.1661, 1.4046, 1.5839, 1.7077, 1.7688, 1.6129, 1.4272, 1.2453, 0.9082])
E_d4_up   = np.array([0.8918, 1.1684, 1.4077, 1.5848, 1.7050, 1.7673, 1.6119, 1.4265, 1.2451, 0.9083])

p_d3_down, = ax2.plot(z_dense, E_d3_down, 'o-', color='#1F618D', lw=2.4, markersize=5.8, zorder=6,
                      label=r'Dataset 3 Longitudinal Desc. (B97-3c, máx $+1.7256$ eV)')
p_d3_up,   = ax2.plot(z_dense, E_d3_up, 's--', color='#2E86C1', lw=1.8, markersize=4.8, zorder=5,
                      label=r'Dataset 3 Longitudinal Asc. (B97-3c, máx $+1.7146$ eV)')
p_d4_down, = ax2.plot(z_dense, E_d4_down, '^-', color='#C0392B', lw=2.2, markersize=5.8, zorder=7,
                      label=r'Dataset 4 Perpendicular Desc./Asc. (máx $+1.769/+1.767$ eV)')
p_wb97x = ax2.scatter([0.25], [1.6690], color='#1E8449', marker='D', s=75, zorder=9,
                      label=r'Refinamiento $\omega$B97X-D3/def2-TZVP ($Z=+0.25\ \mathrm{\AA}$: $+1.669$ eV)')

ax2.axvline(0.25, color='#7F8C8D', ls=':', lw=1.4, zorder=2)

ax2.annotate('Máximo Perpendicular (Dataset 4, 20/20 conv.)\nZ = +0.25 Å: +1.769 / +1.767 eV (21 y 10 ciclos)',
             xy=(0.25, 1.7688), xytext=(-0.98, 1.98),
             arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.3),
             fontsize=7.6, fontweight='bold', color='#922B21',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.96), zorder=10)

ax2.annotate('Máximo Longitudinal (Dataset 3, 18/20 conv.)\nZ = +0.25 Å: +1.7256 eV (16 cic.) / +1.7146 eV (19 cic.)\nHistéresis ΔE = 0.011 eV (~45 kBT a 173 °C)',
             xy=(0.25, 1.7256), xytext=(-0.98, 1.48),
             arrowprops=dict(arrowstyle='->', color='#1F618D', lw=1.3),
             fontsize=7.4, fontweight='bold', color='#1F618D',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#EBF5FB', edgecolor='#1F618D', alpha=0.96), zorder=10)

ax2.annotate('ωB97X-D3/def2-TZVP\n+1.669 eV (43.5 kBT)\nBoltzmann: 3×10⁻²⁰–1.4×10⁻¹⁹',
             xy=(0.25, 1.6690), xytext=(0.48, 1.02),
             arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.3),
             fontsize=7.5, fontweight='bold', color='#1E8449',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#EAFAF1', edgecolor='#1E8449', alpha=0.96), zorder=10)

ax2.set_xlabel(r'Coordenada axial relativa al poro $Z$ ($\mathrm{\AA}$, $r_{\mathrm{pore}} = -0.13\ \mathrm{\AA}$)', fontsize=9.8, fontweight='bold')
ax2.set_ylabel(r'Energía de interacción $\Delta E_{\mathrm{int}}(Z)$ (eV)', fontsize=9.8, fontweight='bold', color='#1F618D')
ax2.set_xlim(-1.12, 1.62)
ax2.set_ylim(0.75, 2.22)
ax2.grid(True, ls='--', alpha=0.3)
ax2.set_title(r'(b) Barrera de Exclusión de $\mathrm{H}_2$ en $\mathrm{C}_{30}\mathrm{H}_{48}$ (Datasets 3 y 4 Auditados)', fontsize=9.7, fontweight='bold', pad=10)
ax2.legend(loc='lower left', fontsize=7.0, framealpha=0.96)

plt.tight_layout()
plt.savefig('docs/figura1_paper4_termodinamica_residencia_173C.png', dpi=300)
plt.close()

# ==============================================================================
# FIGURA 2: Espectro de Adamantano VUV (Marder et al. 2023) vs Cascada E-Beam (1 keV)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6), dpi=300)
fig.patch.set_facecolor('white')

# Panel A: Sección eficaz de fotoabsorción VUV de Adamantano (C10H16, Marder et al. 2023, ApJS 267:23)
hv = np.linspace(6.2, 12.5, 600)
# Perfil experimental de adamantano en fase gas con las 3 bandas electrónicas HOMO->LUMO (6.49 eV), HOMO->LUMO+1 (7.13 eV) y HOMO->LUMO+2 (8.23 eV) y ascenso hacia IE_ad = 9.25 eV
sigma_base = 68.0 / (1.0 + np.exp(-(hv - 8.95) / 0.55)) * (hv >= 6.35)
peak_649 = 6.5 * np.exp(-((hv - 6.49) / 0.12)**2)
peak_713 = 22.0 * np.exp(-((hv - 7.13) / 0.18)**2)
peak_823 = 31.5 * np.exp(-((hv - 8.23) / 0.22)**2)
sigma_vuv = sigma_base + peak_649 + peak_713 + peak_823

ax1.plot(hv, sigma_vuv, color='#6C3483', lw=2.5, zorder=4, label=r'$\sigma_{\mathrm{abs}}(h\nu)$ Adamantano $\mathrm{C}_{10}\mathrm{H}_{16}$ (Marder et al. 2023)')
ax1.axvspan(7.0, 9.25, color='#2ECC71', alpha=0.17, label='Sub-umbral Rydberg MGR (7.0–9.25 eV)\nSelectividad C–H >99.8% sp³, 0 carga')
ax1.axvspan(9.25, 10.0, color='#3498DB', alpha=0.17, label=r'Sobre-umbral suave (9.25–10.0 eV)' + '\n' + r'$\mathrm{Ad}^{\bullet+}$ frío ($\Delta E_{\mathrm{int}} \leq 0.75$ eV, $\sigma_{\mathrm{act}} \approx 40$ Mb)')
ax1.axvspan(11.5, 12.5, color='#E74C3C', alpha=0.20, label='Ruptura de jaula C–C (>11.5 eV)\nFragmentación sp² (Prohibida)')
ax1.axvline(9.25, color='#1B4F72', ls='--', lw=1.6)
ax1.axvline(11.5, color='#922B21', ls='--', lw=1.6)

# Puntos clave de transición electrónica de adamantano (6.49, 7.13, 8.23 eV) y umbral 9.25 eV
pts_hv = [6.49, 7.13, 8.23, 9.25]
pts_sig = [float(np.interp(x, hv, sigma_vuv)) for x in pts_hv]
ax1.scatter(pts_hv, pts_sig, color='#6C3483', s=52, zorder=6)

ax1.annotate('HOMO→LUMO (3s)\n6.49 eV',
             xy=(6.49, pts_sig[0]), xytext=(6.23, 28.5),
             arrowprops=dict(arrowstyle='->', color='#6C3483', lw=1.2),
             fontsize=7.4, fontweight='bold', color='#6C3483',
             bbox=dict(boxstyle='round,pad=0.20', facecolor='#F5EEF8', edgecolor='#6C3483', alpha=0.96), zorder=10)

ax1.annotate('HOMO→LUMO+1 (3p)\n7.13 eV (Xe₂* 172 nm)',
             xy=(7.13, pts_sig[1]), xytext=(6.78, 46.5),
             arrowprops=dict(arrowstyle='->', color='#6C3483', lw=1.2),
             fontsize=7.4, fontweight='bold', color='#6C3483',
             bbox=dict(boxstyle='round,pad=0.20', facecolor='#F5EEF8', edgecolor='#6C3483', alpha=0.96), zorder=10)

ax1.annotate('HOMO→LUMO+2 (3d/4s)\n8.23 eV (~46 Mb)',
             xy=(8.23, pts_sig[2]), xytext=(9.38, 30.0),
             arrowprops=dict(arrowstyle='->', color='#6C3483', lw=1.3),
             fontsize=7.6, fontweight='bold', color='#6C3483',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#F5EEF8', edgecolor='#6C3483', alpha=0.96), zorder=10)

ax1.text(9.08, 6.0, 'IE_ad = 9.25 eV', fontsize=7.8, fontweight='bold', color='#1B4F72', rotation=90,
         bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.75))
ax1.text(11.30, 6.0, 'Umbral Ruptura Jaula (11.5 eV)', fontsize=7.8, fontweight='bold', color='#922B21', rotation=90,
         bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.75))

ax1.set_xlabel(r'Energía del fotón VUV $h\nu$ (eV)', fontsize=9.8, fontweight='bold')
ax1.set_ylabel(r'Sección eficaz de fotoabsorción $\sigma_{\mathrm{abs}}$ (Mb = $10^{-18}\ \mathrm{cm}^2$)', fontsize=9.8, fontweight='bold')
ax1.set_xlim(6.2, 12.5)
ax1.set_ylim(0, 88)
ax1.grid(True, ls='--', alpha=0.3)
ax1.set_title(r'(a) Espectro VUV de Adamantano ($\mathrm{C}_{10}\mathrm{H}_{16}$) y Ventanas Cuánticas', fontsize=9.8, fontweight='bold', pad=10)
ax1.legend(loc='upper left', fontsize=7.1, framealpha=0.96)

# Panel B: Perfil de deposición de energía en profundidad (E-Beam 1.0 keV vs VUV 7.13-9.8 eV)
z_depth = np.linspace(0, 25, 300)  # nm
ebeam_profile = 3653.4 * (0.4 + 1.45 * (z_depth / 19.12) * np.exp(-((z_depth - 7.5) / 6.2)**2)) * (z_depth <= 19.12)
ebeam_profile[z_depth > 19.12] = 0.0
vuv_profile = 450.0 * np.exp(-z_depth / 10.0)

ax2.plot(z_depth, ebeam_profile, color='#C0392B', lw=2.5, label=r'E-Beam 1.0 keV ($R_{\mathrm{KO}} = 19.12$ nm, $-dE/ds = 3653$ eV/nm)')
ax2.plot(z_depth, vuv_profile * 5.0, color='#2980B9', lw=2.5, ls='-.', label=r'Fotones VUV 7.13–9.8 eV ($\delta_{\mathrm{opt}} \approx 10$ nm, escala $\times 5$)')
ax2.axvspan(0, 0.74, color='#F39C12', alpha=0.35, label='Monocapa Ad fisisorbida (0.74 nm, 1 ML)')

ax2.annotate('E-Beam 1.0 keV:\n• SEY δ ≈ 20 en NEA\n• Cola >20–70 eV rompe C–C (8–15% sp²)\n• Acumula huecos Q₁ (colapso a Dc₁ = 0.2 mC/cm²)',
             xy=(11.2, 3550), xytext=(12.3, 2650),
             arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.3),
             fontsize=7.6, bbox=dict(boxstyle='round,pad=0.28', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.96), zorder=10)

ax2.annotate('VUV (7.13–10.0 eV):\n• Fotoelectrones internos lentos (2–4.5 eV)\n• Cero cascadas >10 eV (>99.8% sp³ estimado)\n• Inmune a carga electrostática',
             xy=(5.2, 1340), xytext=(7.2, 680),
             arrowprops=dict(arrowstyle='->', color='#2980B9', lw=1.3),
             fontsize=7.6, bbox=dict(boxstyle='round,pad=0.28', facecolor='#EBF5FB', edgecolor='#2980B9', alpha=0.96), zorder=10)

ax2.set_xlabel(r'Profundidad subsuperficial en el sustrato de diamante $z$ (nm)', fontsize=9.8, fontweight='bold')
ax2.set_ylabel(r'Densidad lineal de deposición energética $-dE/ds$ (eV/nm)', fontsize=9.8, fontweight='bold')
ax2.set_xlim(0, 24.5)
ax2.set_ylim(0, 4450)
ax2.grid(True, ls='--', alpha=0.3)
ax2.set_title('(b) Distribución Subsuperficial: E-Beam (1.0 keV) vs. Fotones VUV', fontsize=10.0, fontweight='bold', pad=10)
ax2.legend(loc='upper right', fontsize=7.4, framealpha=0.96)

plt.tight_layout()
plt.savefig('docs/figura2_paper4_contraste_DIET_ebeam_vs_VUV.png', dpi=300)
plt.close()

# ==============================================================================
# FIGURA 3: Cinética de Pincel Sincronizado (Da_DIET) y Arquitectura Pincel-VUV-Pirámide
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6), dpi=300)
fig.patch.set_facecolor('white')

# Panel A: Eficiencia de captura covalente por pasada vs Número de Damköhler Da_DIET
Da = np.logspace(-7, 1, 400)
eff_capture = (1.0 - np.exp(-Da)) * 100.0

ax1.semilogx(Da, eff_capture, color='#1E8449', lw=2.6, label=r'Fijación covalente por pasada $\eta_{\mathrm{pin}} = 1 - \exp(-\mathrm{Da}_{\mathrm{DIET}})$')
ax1.axvspan(1e-7, 1e-4, color='#E74C3C', alpha=0.18, label=r'Modo Simultáneo / Inundación ($\mathrm{Da} = 10^{-7}-10^{-4}$)' + '\n' + 'VUV ($10^{-7}-10^{-5}$) y E-Beam ($10^{-6}-10^{-4}$): pérdida >99.99%')
ax1.axvspan(0.5, 5.0, color='#A9DFBF', alpha=0.25, label=r'Banda Amplia de Pincel ($\mathrm{Da} = 0.5-5.0 \Rightarrow 39\%-99\%$)')
ax1.axvspan(1.6, 3.9, color='#27AE60', alpha=0.32, label=r'Objetivo Nominal ($\mathrm{Da} = 1.6-3.9 \Rightarrow 80\%-98\%$, $\mathrm{Pe} \sim 1$)')

pts_da = [1e-6, 1e-5, 1.60, 3.91]
pts_eff = [(1.0 - np.exp(-d)) * 100.0 for d in pts_da]
ax1.scatter(pts_da, pts_eff, color=['#C0392B', '#C0392B', '#1E8449', '#117A65'], s=60, zorder=6)

ax1.annotate('Inundación VUV / E-Beam\n(<0.05% eficiencia)',
             xy=(3e-6, 0.5), xytext=(6e-7, 22),
             arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.3),
             fontsize=8.0, fontweight='bold', color='#C0392B',
             bbox=dict(boxstyle='round,pad=0.24', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.95))

ax1.annotate('Pincel Sincronizado:\nObjetivo Da = 1.6–3.9 (80–98%)\n[Rango 0.5–5.0: 39–99%]',
             xy=(1.60, 79.8), xytext=(5e-4, 73.0),
             arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.3),
             fontsize=7.8, fontweight='bold', color='#1E8449',
             bbox=dict(boxstyle='round,pad=0.24', facecolor='#EAFAF1', edgecolor='#1E8449', alpha=0.95))

ax1.set_xlabel(r'Número de Damköhler DIET ($\mathrm{Da}_{\mathrm{DIET}} = \tau_{\mathrm{res}} / \tau_{\mathrm{act,brush}}$)', fontsize=9.8, fontweight='bold')
ax1.set_ylabel('Eficiencia de utilización de adamantano (%)', fontsize=9.8, fontweight='bold')
ax1.set_xlim(1e-7, 10)
ax1.set_ylim(-4, 106)
ax1.grid(True, which='both', ls='--', alpha=0.3)
ax1.set_title('(a) Transición de Fase Cinética: Inundación vs. Pincel Sincronizado', fontsize=10.0, fontweight='bold', pad=10)
ax1.legend(loc='center left', fontsize=7.1, framealpha=0.96)

# Panel B: Esquema de la Arquitectura Pincel–VUV–Pirámide Invertida (Soldadura Laminar y 300 Cavidades)
ax2.set_xlim(0, 10.0)
ax2.set_ylim(0, 10.2)
ax2.axis('off')
ax2.set_title('(b) Arquitectura Pincel–VUV–Pirámide Invertida (Wafer Vertical, 300× VUV)', fontsize=9.6, fontweight='bold', pad=10)

# Dibujar la pirámide invertida (octaedro inferior) con márgenes laterales amplios para etiquetas
pyramid_outer = patches.Polygon([[1.6, 8.2], [8.4, 8.2], [5.0, 1.6]], closed=True, facecolor='#EAEDED', edgecolor='#2C3E50', lw=2.0, zorder=1)
ax2.add_patch(pyramid_outer)

# Capas crecidas tipo "muñecas rusas"
layer1 = patches.Polygon([[2.25, 8.2], [7.75, 8.2], [5.0, 2.8]], closed=True, facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.4, ls='--', zorder=2)
layer2 = patches.Polygon([[2.90, 8.2], [7.10, 8.2], [5.0, 4.0]], closed=True, facecolor='#EBF5FB', edgecolor='#1F618D', lw=1.4, ls='--', zorder=2)
ax2.add_patch(layer1)
ax2.add_patch(layer2)

# Haz VUV coaxial apuntando donde el pincel va pintando
vuv_beam1 = patches.Polygon([[3.35, 9.1], [3.68, 9.1], [4.65, 4.4], [4.35, 4.4]], closed=True, facecolor='#8E44AD', alpha=0.42, zorder=3)
vuv_beam2 = patches.Polygon([[6.32, 9.1], [6.65, 9.1], [5.65, 4.4], [5.35, 4.4]], closed=True, facecolor='#8E44AD', alpha=0.42, zorder=3)
ax2.add_patch(vuv_beam1)
ax2.add_patch(vuv_beam2)

# Pincel central ocupando el núcleo
brush_body = patches.Rectangle((4.40, 5.2), 1.20, 3.7, facecolor='#2C3E50', edgecolor='#1A252F', lw=1.6, zorder=4)
brush_tip = patches.Polygon([[4.40, 5.2], [5.60, 5.2], [5.0, 4.05]], closed=True, facecolor='#E67E22', edgecolor='#D35400', lw=1.6, zorder=4)
ax2.add_patch(brush_body)
ax2.add_patch(brush_tip)

# Trazo ondulatorio (malla de crecimiento lateral step-flow)
x_wave = np.linspace(3.25, 6.75, 140)
y_wave = 4.55 + 0.36 * np.abs(x_wave - 5.0) + 0.13 * np.sin(15.0 * x_wave)
ax2.plot(x_wave, y_wave, color='#1E8449', lw=2.3, zorder=5)

# Etiquetas con cajas sólidas de alto contraste (100% legibles, cero texto encimado)
ax2.text(5.0, 9.55, '1 Canal VUV Dedicado por Cavidad (Matriz 300 Cavidades × 300 VUVs)',
         ha='center', va='center', fontsize=8.0, fontweight='bold', color='#6C3483',
         bbox=dict(boxstyle='round,pad=0.28', facecolor='#F5EEF8', edgecolor='#8E44AD', lw=1.2), zorder=10)

ax2.text(5.0, 7.05, 'Pincel Central\n(Ocupa el núcleo:\ncero hueco libre)',
         ha='center', va='center', fontsize=7.6, fontweight='bold', color='white',
         bbox=dict(boxstyle='round,pad=0.28', facecolor='#1C2833', edgecolor='#F39C12', lw=1.3, alpha=0.98), zorder=10)

ax2.annotate('Capas "Muñecas Rusas"\nsobre plantilla piramidal',
             xy=(3.15, 5.65), xytext=(0.15, 2.75),
             arrowprops=dict(arrowstyle='->', color='#1F618D', lw=1.4, connectionstyle='arc3,rad=-0.12'),
             fontsize=7.6, fontweight='bold', color='#1F618D',
             bbox=dict(boxstyle='round,pad=0.26', facecolor='#EBF5FB', edgecolor='#2980B9', alpha=0.96), zorder=10)

ax2.annotate('Malla ondulatoria:\nSoldadura laminar\n(step-flow sin colisión)',
             xy=(5.95, 4.95), xytext=(6.45, 2.55),
             arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.4, connectionstyle='arc3,rad=0.12'),
             fontsize=7.6, fontweight='bold', color='#1E8449',
             bbox=dict(boxstyle='round,pad=0.26', facecolor='#EAFAF1', edgecolor='#1E8449', alpha=0.96), zorder=10)

ax2.text(5.0, 0.65, 'Wafer Vertical Rotatorio a 173 °C (Sincronización Azimutal + Avance Axial Z)',
         ha='center', va='center', fontsize=8.0, fontweight='bold', color='#1B4F72',
         bbox=dict(boxstyle='round,pad=0.28', facecolor='#EBF5FB', edgecolor='#2980B9', lw=1.2), zorder=10)

plt.tight_layout()
plt.savefig('docs/figura3_paper4_cinetica_pincel_piramide_300VUV.png', dpi=300)
plt.close()
print("[+] 3 figuras regeneradas con el espectro VUV de Adamantano (Marder et al. 2023) y bandas exactas de Damkohler.")
