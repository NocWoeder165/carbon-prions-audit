import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set high-quality typography
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['mathtext.fontset'] = 'dejavusans'

output_dir = os.path.dirname(os.path.abspath(__file__))
figures_dir = os.path.join(output_dir, 'figures')
os.makedirs(figures_dir, exist_ok=True)

# ==============================================================================
# FIGURE 1: Thermodynamics of Monolayer Self-Limitation & Audited H2 Pore Barrier
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.8, 5.8), dpi=300)
fig.patch.set_facecolor('white')

# --- Panel (a): Frenkel-Arrhenius Residence Time & Diffusion Length vs E_des ---
kB_T = 0.038448  # eV at 446.15 K (173 °C)
tau_0 = 1.0e-13  # s
D_s = 3.441e-6   # cm^2/s = 3.441e8 nm^2/s

E_des = np.linspace(0.55, 0.85, 250)
tau_res_us = tau_0 * np.exp(E_des / kB_T) * 1e6  # microseconds
lambda_diff_nm = np.sqrt(2 * (D_s * 1e14) * (tau_res_us * 1e-6))

color1 = '#0F3880'
color2 = '#B03A2E'

ax1_twin = ax1.twinx()
l1, = ax1.semilogy(E_des, tau_res_us, color=color1, lw=2.6, label=r'Residence time $\tau_{\mathrm{res}}$ ($\mu$s)')
l2, = ax1_twin.plot(E_des, lambda_diff_nm, color=color2, lw=2.4, ls='--', label=r'Mean diffusion length $\lambda_{\mathrm{diff}}$ (nm)')

# Key audited benchmark points at 173 °C
pts_E = [0.65, 0.72, 0.75, 0.80]
pts_tau = [2.20, 13.59, 29.66, 108.87]
pts_lam = [38.91, 96.71, 142.89, 273.72]

ax1.scatter(pts_E, pts_tau, color=color1, s=60, zorder=5)
ax1_twin.scatter(pts_E, pts_lam, color=color2, s=60, marker='s', zorder=5)

# Brush synchronization window (dwell time 2.20 - 13.59 us)
span_brush = ax1.axhspan(2.20, 13.59, color='#27AE60', alpha=0.18, 
                         label=r'Synchronized brush window $\tau_{\mathrm{pulse}} = 2.20$' + '–' + r'$13.59\ \mu\mathrm{s}$')
line_ml = ax1.axhline(0.03944, color='#7F8C8D', ls=':', lw=1.8, 
                      label=r'Free 3D solid monolayer lifetime ($t_{\mathrm{ML}} = 39.44\ \mathrm{ns}$)')

bbox_blue = dict(boxstyle='round,pad=0.28', facecolor='#EBF5FB', edgecolor=color1, alpha=0.96)
ax1.annotate('Terrace Site (0.65 eV)\n' + r'$\tau = 2.20\ \mu\mathrm{s}\ \mid\ \lambda = 38.9\ \mathrm{nm}$', 
             xy=(0.65, 2.20), xytext=(0.565, 5.2),
             arrowprops=dict(arrowstyle='->', color=color1, lw=1.3), 
             fontsize=8.2, fontweight='bold', color=color1, bbox=bbox_blue)

ax1.annotate('Nominal Site (0.72 eV)\n' + r'$\tau = 13.59\ \mu\mathrm{s}\ \mid\ \lambda = 96.7\ \mathrm{nm}$', 
             xy=(0.72, 13.59), xytext=(0.575, 34.0),
             arrowprops=dict(arrowstyle='->', color=color1, lw=1.3), 
             fontsize=8.2, fontweight='bold', color=color1, bbox=bbox_blue)

ax1.annotate('Step-Edge Site (0.80 eV)\n' + r'$\tau = 108.87\ \mu\mathrm{s}\ \mid\ \lambda = 273.7\ \mathrm{nm}$', 
             xy=(0.80, 108.87), xytext=(0.615, 175.0),
             arrowprops=dict(arrowstyle='->', color=color1, lw=1.3), 
             fontsize=8.2, fontweight='bold', color=color1, bbox=bbox_blue)

ax1.set_xlabel(r'Estimated vdW desorption activation energy $E_{\mathrm{des}}$ (eV)', fontsize=10.2, fontweight='bold')
ax1.set_ylabel(r'Surface residence time $\tau_{\mathrm{res}}$ ($\mu$s)', fontsize=10.2, fontweight='bold', color=color1)
ax1_twin.set_ylabel(r'Mean surface diffusion length $\lambda_{\mathrm{diff}}$ (nm)', fontsize=10.2, fontweight='bold', color=color2)
ax1.set_ylim(0.015, 500)
ax1_twin.set_ylim(0, 320)
ax1.grid(True, which='both', ls='--', alpha=0.35)
ax1.set_title(r'(a) Monolayer Self-Limitation & Diffusion at $173\ ^\circ\mathrm{C}$ (446.15 K)', fontsize=10.8, fontweight='bold', pad=10)

handles_a = [l1, l2, span_brush, line_ml]
labels_a = [h.get_label() for h in handles_a]
ax1.legend(handles_a, labels_a, loc='lower right', fontsize=8.0, framealpha=0.96)

# --- Panel (b): Audited H2 Pore Barrier in C30H48 (Datasets 3 and 4, ORCA 6.1.1) ---
z_dense = np.array([-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00, 1.50])
# Dataset 3: Longitudinal (theta_Z = 5.82 deg)
E_d3_down = np.array([0.8809, 1.1352, 1.3577, 1.5297, 1.6476, 1.7256, 1.5902, 1.4218, 1.2427, 0.8938])
E_d3_up   = np.array([0.8811, 1.1354, 1.3580, 1.5363, 1.6557, 1.7146, 1.5894, 1.4218, 1.2440, 0.8933])
# Dataset 4: Perpendicular (theta_Z = 95.60 deg)
E_d4_down = np.array([0.8915, 1.1661, 1.4046, 1.5839, 1.7077, 1.7688, 1.6129, 1.4272, 1.2453, 0.9082])
E_d4_up   = np.array([0.8918, 1.1684, 1.4077, 1.5848, 1.7050, 1.7673, 1.6119, 1.4265, 1.2451, 0.9083])

p_d3_down, = ax2.plot(z_dense, E_d3_down, 'o-', color='#1B4F72', lw=2.4, markersize=6.0, zorder=6,
                      label=r'Dataset 3 Longitudinal Desc. (B97-3c, max $+1.7256$ eV)')
p_d3_up,   = ax2.plot(z_dense, E_d3_up, 's--', color='#2980B9', lw=1.8, markersize=5.0, zorder=5,
                      label=r'Dataset 3 Longitudinal Asc. (B97-3c, max $+1.7146$ eV)')
p_d4_down, = ax2.plot(z_dense, E_d4_down, '^-', color='#C0392B', lw=2.2, markersize=6.0, zorder=7,
                      label=r'Dataset 4 Perpendicular Desc./Asc. (max $+1.769/+1.767$ eV)')
p_wb97x = ax2.scatter([0.25], [1.6690], color='#1E8449', marker='D', s=85, zorder=9,
                      label=r'$\omega$B97X-D3/def2-TZVP Refinement ($Z=+0.25\ \mathrm{\AA}$: $+1.669$ eV)')

ax2.axvline(0.25, color='#7F8C8D', ls=':', lw=1.4, zorder=2)

ax2.annotate('Perpendicular Maximum (Dataset 4, 20/20 conv.)\n' + 
             r'$Z = +0.25\ \mathrm{\AA}:\ \mathbf{+1.769\ /\ +1.767\ \mathrm{eV}}$ (21 & 10 cyc.)',
             xy=(0.25, 1.7688), xytext=(0.40, 2.15),
             arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.3),
             fontsize=7.6, fontweight='bold', color='#922B21',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.96), zorder=10)

ax2.annotate('Longitudinal Maximum (Dataset 3, 18/20 conv.)\n' + 
             r'$Z = +0.25\ \mathrm{\AA}:\ \mathbf{+1.7256\ \mathrm{eV}}$ (16 cyc.) / $\mathbf{+1.7146\ \mathrm{eV}}$ (19 cyc.)' + '\n' +
             r'Hysteresis $\Delta E = 0.011\ \mathrm{eV}$ ($\sim 45\ k_B T$ at $173\ ^\circ\mathrm{C}$)',
             xy=(0.25, 1.7256), xytext=(-1.11, 1.88),
             arrowprops=dict(arrowstyle='->', color='#1F618D', lw=1.3, connectionstyle='arc3,rad=0.18'),
             fontsize=7.5, fontweight='bold', color='#1F618D',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#EBF5FB', edgecolor='#1F618D', alpha=0.96), zorder=10)

ax2.annotate(r'$\omega\mathrm{B97X}$' + '–' + r'$\mathrm{D3/def2}$' + '–' + r'$\mathrm{TZVP}$' + '\n' +
             r'$\mathbf{+1.6690\ \mathrm{eV}}$ ($43.5\ k_B T$)' + '\n' +
             r'Boltzmann: $3\times 10^{-20}$' + '–' + r'$1.4\times 10^{-19}$',
             xy=(0.25, 1.6690), xytext=(0.64, 1.68),
             arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.3),
             fontsize=7.8, fontweight='bold', color='#1E8449',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#EAFAF1', edgecolor='#1E8449', alpha=0.96), zorder=10)

ax2.set_xlabel(r'Axial coordinate relative to pore $Z$ ($\mathrm{\AA}$, geometric $r_{\mathrm{pore}} = -0.13\ \mathrm{\AA}$)', 
               fontsize=10.2, fontweight='bold')
ax2.set_ylabel(r'Interaction potential energy $\Delta E_{\mathrm{int}}(Z)$ (eV)', fontsize=10.2, fontweight='bold', color='#1F618D')
ax2.set_xlim(-1.15, 1.82)
ax2.set_ylim(0.50, 2.40)
ax2.grid(True, ls='--', alpha=0.35)
ax2.set_title(r'(b) Audited $\mathrm{H}_2$ Exclusion Barrier in $\mathrm{C}_{30}\mathrm{H}_{48}$ (Datasets 3 & 4)', 
              fontsize=10.8, fontweight='bold', pad=10)
ax2.legend(loc='lower left', fontsize=7.6, framealpha=0.96)

plt.tight_layout()
fig1_path = os.path.join(figures_dir, 'fig1_thermodynamics_pore_barrier_173C_EN.png')
plt.savefig(fig1_path, dpi=300)
plt.close()
print(f"[+] Saved Figure 1 (EN) -> {fig1_path}")


# ==============================================================================
# FIGURE 2: VUV Photoabsorption Spectrum vs Electron Beam Stopping Profile
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.8, 5.8), dpi=300)
fig.patch.set_facecolor('white')

# --- Panel (a): Absolute VUV Photoabsorption Cross-Section of Adamantane ---
hv = np.linspace(6.2, 12.5, 700)
sigma_base = 68.0 / (1.0 + np.exp(-(hv - 8.95) / 0.55)) * (hv >= 6.35)
peak_649 = 6.5 * np.exp(-((hv - 6.49) / 0.12)**2)
peak_713 = 22.0 * np.exp(-((hv - 7.13) / 0.18)**2)
peak_823 = 31.5 * np.exp(-((hv - 8.23) / 0.22)**2)
sigma_vuv = sigma_base + peak_649 + peak_713 + peak_823

ax1.plot(hv, sigma_vuv, color='#5B2C6F', lw=2.6, zorder=4, 
         label=r'$\sigma_{\mathrm{abs}}(h\nu)$ Gas-phase Adamantane $\mathrm{C}_{10}\mathrm{H}_{16}$ (Marder et al. 2023)')
ax1.axvspan(6.49, 9.25, color='#2ECC71', alpha=0.18, 
           label=r'Sub-threshold Rydberg MGR ($6.49$' + '–' + r'$9.25\ \mathrm{eV}$)' + '\n' + r'C–H selectivity $>99.8\%\ sp^3$, zero charge')
ax1.axvspan(9.25, 10.0, color='#3498DB', alpha=0.18, 
           label=r'Soft supra-threshold ($9.25$' + '–' + r'$10.0\ \mathrm{eV}$)' + '\n' + r'Cold $\mathrm{Ad}^{\bullet+}$ ($\Delta E_{\mathrm{int}} \leq 0.75\ \mathrm{eV}$, $\sigma_{\mathrm{act}} \approx 40\ \mathrm{Mb}$)')
ax1.axvspan(11.5, 12.5, color='#E74C3C', alpha=0.20, 
           label=r'C–C Cage rupture ($>11.5\ \mathrm{eV}$)' + '\n' + r'$sp^2$ fragmentation (Destructive)')
ax1.axvline(9.25, color='#1B4F72', ls='--', lw=1.6)
ax1.axvline(11.5, color='#922B21', ls='--', lw=1.6)

# Key electronic transition points
pts_hv = [6.49, 7.13, 8.23, 9.25]
pts_sig = [float(np.interp(x, hv, sigma_vuv)) for x in pts_hv]
ax1.scatter(pts_hv, pts_sig, color='#5B2C6F', s=55, zorder=6)

ax1.annotate(r'$\mathrm{HOMO}\to\mathrm{LUMO}\ (3s)$' + '\n' + r'$6.49\ \mathrm{eV}$',
             xy=(6.49, pts_sig[0]), xytext=(6.23, 26.5),
             arrowprops=dict(arrowstyle='->', color='#5B2C6F', lw=1.2),
             fontsize=7.8, fontweight='bold', color='#5B2C6F',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#F5EEF8', edgecolor='#5B2C6F', alpha=0.96), zorder=10)

ax1.annotate(r'$\mathrm{HOMO}\to\mathrm{LUMO}+1\ (3p)$' + '\n' + r'$7.13\ \mathrm{eV}\ (\mathrm{Xe}_2^*\ 172\ \mathrm{nm})$',
             xy=(7.13, pts_sig[1]), xytext=(7.18, 53.0),
             arrowprops=dict(arrowstyle='->', color='#5B2C6F', lw=1.2),
             fontsize=7.8, fontweight='bold', color='#5B2C6F',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#F5EEF8', edgecolor='#5B2C6F', alpha=0.96), zorder=10)

ax1.annotate(r'$\mathrm{HOMO}\to\mathrm{LUMO}+2\ (3d/4s)$' + '\n' + r'$8.23\ \mathrm{eV}\ (\sim 46\ \mathrm{Mb})$',
             xy=(8.23, pts_sig[2]), xytext=(9.42, 32.0),
             arrowprops=dict(arrowstyle='->', color='#5B2C6F', lw=1.3),
             fontsize=7.8, fontweight='bold', color='#5B2C6F',
             bbox=dict(boxstyle='round,pad=0.22', facecolor='#F5EEF8', edgecolor='#5B2C6F', alpha=0.96), zorder=10)

ax1.text(9.08, 6.0, r'$\mathrm{IE}_{\mathrm{ad}} = 9.25\ \mathrm{eV}$', fontsize=8.2, fontweight='bold', color='#1B4F72', rotation=90,
         bbox=dict(boxstyle='round,pad=0.18', facecolor='white', edgecolor='none', alpha=0.80))
ax1.text(11.30, 6.0, r'Cage Rupture Threshold ($11.5\ \mathrm{eV}$)', fontsize=8.2, fontweight='bold', color='#922B21', rotation=90,
         bbox=dict(boxstyle='round,pad=0.18', facecolor='white', edgecolor='none', alpha=0.80))

ax1.set_xlabel(r'VUV Photon energy $h\nu$ (eV)', fontsize=10.2, fontweight='bold')
ax1.set_ylabel(r'Photoabsorption cross-section $\sigma_{\mathrm{abs}}$ ($\mathrm{Mb} = 10^{-18}\ \mathrm{cm}^2$)', fontsize=10.2, fontweight='bold')
ax1.set_xlim(6.2, 12.5)
ax1.set_ylim(0, 90)
ax1.grid(True, ls='--', alpha=0.35)
ax1.set_title(r'(a) VUV Photoabsorption Spectrum of Adamantane ($\mathrm{C}_{10}\mathrm{H}_{16}$)', fontsize=10.8, fontweight='bold', pad=10)
ax1.legend(loc='upper left', fontsize=7.6, framealpha=0.96)

# --- Panel (b): Subsurface Energy Deposition Profile ---
z_depth = np.linspace(0, 25, 350)  # nm
ebeam_profile = 3653.4 * (0.4 + 1.45 * (z_depth / 19.12) * np.exp(-((z_depth - 7.5) / 6.2)**2)) * (z_depth <= 19.12)
ebeam_profile[z_depth > 19.12] = 0.0
vuv_profile = 450.0 * np.exp(-z_depth / 10.0)

ax2.plot(z_depth, ebeam_profile, color='#C0392B', lw=2.6, 
         label=r'Electron Beam $1.0\ \mathrm{keV}$ ($R_{\mathrm{KO}} = 19.12\ \mathrm{nm}$, $-dE/ds = 3653\ \mathrm{eV/nm}$)')
ax2.plot(z_depth, vuv_profile * 5.0, color='#2980B9', lw=2.5, ls='-.', 
         label=r'VUV Photons $6.49$' + '–' + r'$10.0\ \mathrm{eV}$ ($\delta_{\mathrm{opt}} \approx 10\ \mathrm{nm}$, magnified $\times 5$)')
ax2.axvspan(0, 0.74, color='#F39C12', alpha=0.35, label=r'Physisorbed Ad monolayer ($0.74\ \mathrm{nm}$, 1 ML)')

ax2.annotate('1.0 keV Electron Beam:\n' +
             r'$\bullet\ \mathrm{SEY}\ \delta \approx 20$ in NEA diamond' + '\n' +
             r'$\bullet\ >20$' + '–' + r'$70\ \mathrm{eV}$ tail breaks C–C ($8$' + '–' + r'$15\%\ sp^2$)' + '\n' +
             r'$\bullet\ Q_1$ hole buildup (collapse at $D_{c1} = 0.2\ \mathrm{mC/cm}^2$)',
             xy=(11.0, 3550), xytext=(12.0, 2600),
             arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.3),
             fontsize=7.8, bbox=dict(boxstyle='round,pad=0.30', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.96), zorder=10)

ax2.annotate('VUV Photons (6.49–10.0 eV):\n' +
             r'$\bullet\ $Slow internal photoelectrons ($2$' + '–' + r'$4.5\ \mathrm{eV}$)' + '\n' +
             r'$\bullet\ $Zero cascades $>10\ \mathrm{eV}$ ($>99.8\%\ sp^3$ selectivity)' + '\n' +
             r'$\bullet\ $Immune to electrostatic surface charging',
             xy=(5.0, 1340), xytext=(7.0, 700),
             arrowprops=dict(arrowstyle='->', color='#2980B9', lw=1.3),
             fontsize=7.8, bbox=dict(boxstyle='round,pad=0.30', facecolor='#EBF5FB', edgecolor='#2980B9', alpha=0.96), zorder=10)

ax2.set_xlabel(r'Subsurface penetration depth in diamond substrate $z$ (nm)', fontsize=10.2, fontweight='bold')
ax2.set_ylabel(r'Linear stopping power / energy deposition $-dE/ds$ (eV/nm)', fontsize=10.2, fontweight='bold')
ax2.set_xlim(0, 24.5)
ax2.set_ylim(0, 4500)
ax2.grid(True, ls='--', alpha=0.35)
ax2.set_title(r'(b) Subsurface Depth Distribution: E-Beam ($1.0\ \mathrm{keV}$) vs. VUV Photons', fontsize=10.8, fontweight='bold', pad=10)
ax2.legend(loc='upper right', fontsize=7.8, framealpha=0.96)

plt.tight_layout()
fig2_path = os.path.join(figures_dir, 'fig2_diet_ebeam_vs_vuv_contrast_EN.png')
plt.savefig(fig2_path, dpi=300)
plt.close()
print(f"[+] Saved Figure 2 (EN) -> {fig2_path}")


# ==============================================================================
# FIGURE 3: Synchronized Brush Kinetics & Inverted Pyramid Architecture
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.2, 6.0), dpi=300)
fig.patch.set_facecolor('white')

# --- Panel (a): Covalent Capture Efficiency vs Damköhler Number Da_DIET ---
Da = np.logspace(-7, 1, 500)
eff_capture = (1.0 - np.exp(-Da)) * 100.0

ax1.semilogx(Da, eff_capture, color='#1E8449', lw=2.8, 
             label=r'Covalent fixation per pass $\eta_{\mathrm{pin}} = 1 - \exp(-\mathrm{Da}_{\mathrm{DIET}})$')
ax1.axvspan(1e-7, 1e-4, color='#E74C3C', alpha=0.18, 
           label=r'Flood / Simultaneous Mode ($\mathrm{Da} = 10^{-7}$' + '–' + r'$10^{-4}$)' + '\n' + r'VUV ($10^{-7}$' + '–' + r'$10^{-5}$) & E-Beam ($10^{-6}$' + '–' + r'$10^{-4}$): loss $>99.99\%$')
ax1.axvspan(0.5, 5.0, color='#A9DFBF', alpha=0.25, 
           label=r'Broad Brush Range ($\mathrm{Da} = 0.5$' + '–' + r'$5.0 \Rightarrow 39\%$' + '–' + r'$99\%$)')
ax1.axvspan(1.6, 3.9, color='#27AE60', alpha=0.32, 
           label=r'Nominal Target Window ($\mathrm{Da} = 1.6$' + '–' + r'$3.9 \Rightarrow 80\%$' + '–' + r'$98\%$, $\mathrm{Pe} \sim 1$)')

pts_da = [1e-6, 1e-5, 1.60, 3.91]
pts_eff = [(1.0 - np.exp(-d)) * 100.0 for d in pts_da]
ax1.scatter(pts_da, pts_eff, color=['#C0392B', '#C0392B', '#1E8449', '#117A65'], s=65, zorder=6)

ax1.annotate('Flood Mode (VUV / E-Beam)\n' + r'($<0.05\%$ capture efficiency)',
             xy=(3e-6, 0.5), xytext=(6e-7, 24),
             arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.3),
             fontsize=8.2, fontweight='bold', color='#C0392B',
             bbox=dict(boxstyle='round,pad=0.26', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.96))

ax1.annotate('Synchronized Brush Regime:\n' + r'Target $\mathrm{Da} = 1.6$' + '–' + r'$3.9\ (\mathbf{80\%}$' + '–' + r'$\mathbf{98\%})$' + '\n' +
             r'[Broad range $0.5$' + '–' + r'$5.0:\ 39\%$' + '–' + r'$99\%$]',
             xy=(1.60, 79.8), xytext=(4e-4, 73.0),
             arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.3),
             fontsize=8.0, fontweight='bold', color='#1E8449',
             bbox=dict(boxstyle='round,pad=0.26', facecolor='#EAFAF1', edgecolor='#1E8449', alpha=0.96))

ax1.set_xlabel(r'DIET Damköhler number ($\mathrm{Da}_{\mathrm{DIET}} = \tau_{\mathrm{res}} / \tau_{\mathrm{act,brush}} = \sigma_{\mathrm{DIET}}^{\mathrm{act}} F_{\mathrm{pulse}}$)', 
               fontsize=10.2, fontweight='bold')
ax1.set_ylabel('Adamantane precursor utilization efficiency (%)', fontsize=10.2, fontweight='bold')
ax1.set_xlim(1e-7, 10)
ax1.set_ylim(-4, 108)
ax1.grid(True, which='both', ls='--', alpha=0.35)
ax1.set_title('(a) Kinetic Phase Transition: Flood vs. Synchronized Brush Mode', fontsize=10.8, fontweight='bold', pad=10)
ax1.legend(loc='center left', fontsize=7.6, framealpha=0.96)

# --- Panel (b): Inverted Pyramid Architecture (Coaxial Brush & 300 VUV Channels) ---
ax2.set_xlim(0, 10.0)
ax2.set_ylim(0, 10.2)
ax2.axis('off')
ax2.set_title('(b) Inverted Pyramid Architecture (Vertical Wafer, 300-Cavity Array)', fontsize=10.8, fontweight='bold', pad=10)

# Inverted pyramid template (lower half of octahedron)
pyramid_outer = patches.Polygon([[1.6, 8.2], [8.4, 8.2], [5.0, 1.6]], closed=True, 
                                facecolor='#EAEDED', edgecolor='#2C3E50', lw=2.2, zorder=1)
ax2.add_patch(pyramid_outer)

# Layer-by-layer growth ("Russian dolls")
layer1 = patches.Polygon([[2.25, 8.2], [7.75, 8.2], [5.0, 2.8]], closed=True, 
                         facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.5, ls='--', zorder=2)
layer2 = patches.Polygon([[2.90, 8.2], [7.10, 8.2], [5.0, 4.0]], closed=True, 
                         facecolor='#EBF5FB', edgecolor='#1F618D', lw=1.5, ls='--', zorder=2)
ax2.add_patch(layer1)
ax2.add_patch(layer2)

# Dual coaxial VUV beams targeting deposition zone
vuv_beam1 = patches.Polygon([[3.35, 9.1], [3.68, 9.1], [4.65, 4.4], [4.35, 4.4]], closed=True, 
                            facecolor='#8E44AD', alpha=0.45, zorder=3)
vuv_beam2 = patches.Polygon([[6.32, 9.1], [6.65, 9.1], [5.65, 4.4], [5.35, 4.4]], closed=True, 
                            facecolor='#8E44AD', alpha=0.45, zorder=3)
ax2.add_patch(vuv_beam1)
ax2.add_patch(vuv_beam2)

# Central coaxial brush body and active dispensing nozzle
brush_body = patches.Rectangle((4.40, 5.2), 1.20, 3.7, facecolor='#2C3E50', edgecolor='#1A252F', lw=1.8, zorder=4)
brush_tip = patches.Polygon([[4.40, 5.2], [5.60, 5.2], [5.0, 4.05]], closed=True, 
                            facecolor='#E67E22', edgecolor='#D35400', lw=1.8, zorder=4)
ax2.add_patch(brush_body)
ax2.add_patch(brush_tip)

# Wavy mesh toolpath (laminar step-flow welding)
x_wave = np.linspace(3.25, 6.75, 150)
y_wave = 4.55 + 0.36 * np.abs(x_wave - 5.0) + 0.13 * np.sin(15.0 * x_wave)
ax2.plot(x_wave, y_wave, color='#1E8449', lw=2.4, zorder=5)

# High-contrast, crystal-clear annotation cards in English (zero overlap)
ax2.text(5.0, 9.55, '1 Dedicated VUV Channel per Cavity (Array: 300 Cavities × 300 VUVs)',
         ha='center', va='center', fontsize=8.4, fontweight='bold', color='#5B2C6F',
         bbox=dict(boxstyle='round,pad=0.30', facecolor='#F5EEF8', edgecolor='#8E44AD', lw=1.3), zorder=10)

ax2.text(5.0, 7.05, 'Central Coaxial Brush\n(Occupies core void:\nzero unguided space)',
         ha='center', va='center', fontsize=8.0, fontweight='bold', color='white',
         bbox=dict(boxstyle='round,pad=0.30', facecolor='#1C2833', edgecolor='#F39C12', lw=1.4, alpha=0.98), zorder=10)

ax2.annotate('Layer-by-layer growth\n(“Russian dolls” on {111}\npyramidal template)',
             xy=(3.15, 5.65), xytext=(0.08, 2.75),
             arrowprops=dict(arrowstyle='->', color='#1F618D', lw=1.4, connectionstyle='arc3,rad=-0.12'),
             fontsize=8.0, fontweight='bold', color='#1F618D',
             bbox=dict(boxstyle='round,pad=0.28', facecolor='#EBF5FB', edgecolor='#2980B9', alpha=0.96), zorder=10)

ax2.annotate('Wavy mesh toolpath:\nLaminar step-flow welding\n(zero frontal collision)',
             xy=(5.95, 4.95), xytext=(6.38, 2.55),
             arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.4, connectionstyle='arc3,rad=0.12'),
             fontsize=8.0, fontweight='bold', color='#1E8449',
             bbox=dict(boxstyle='round,pad=0.28', facecolor='#EAFAF1', edgecolor='#1E8449', alpha=0.96), zorder=10)

ax2.text(5.0, 0.65, r'Rotating Vertical Wafer at $173\ ^\circ\mathrm{C}$ (Azimuthal Synchronization + Axial $Z$-Retraction)',
         ha='center', va='center', fontsize=8.4, fontweight='bold', color='#1B4F72',
         bbox=dict(boxstyle='round,pad=0.30', facecolor='#EBF5FB', edgecolor='#2980B9', lw=1.3), zorder=10)

plt.tight_layout()
fig3_path = os.path.join(figures_dir, 'fig3_brush_kinetics_inverted_pyramid_EN.png')
plt.savefig(fig3_path, dpi=300)
plt.close()
print(f"[+] Saved Figure 3 (EN) -> {fig3_path}")
