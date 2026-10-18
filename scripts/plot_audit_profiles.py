import os
import json
import numpy as np
import matplotlib.pyplot as plt

base_dir = r"C:\Users\Leo\Desktop\Priones de carbono\dft_orca_validation"
with open(os.path.join(base_dir, "auditoria_completa_5puntos.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

fig, axes = plt.subplots(2, 3, figsize=(18, 9.5), dpi=200, gridspec_kw={"height_ratios": [2.2, 1.0]})

titles = {
    "C20H30": "Intrínseco: 1,1'-Biadamantilo (C₂₀H₃₀)",
    "C19H29B": "Tipo p: Bora-biadamantilo (C₁₉H₂₉B)",
    "C19H29P": "Tipo n: Fosfa-biadamantilo (C₁₉H₂₉P)"
}
deq_A_map = {"C20H30": 1.596, "C19H29B": 1.635, "C19H29P": 1.643}
deq_B_map = {"C20H30": 1.577, "C19H29B": 1.581, "C19H29P": 1.588}

for idx, sys_name in enumerate(["C20H30", "C19H29B", "C19H29P"]):
    ax_top = axes[0, idx]
    ax_bot = axes[1, idx]
    pts = data["systems"][sys_name]["points"]

    d_A = [3.40, 2.92, 2.60, 2.44, 2.12, deq_A_map[sys_name]]
    d_B = [3.40, 2.92, 2.60, 2.44, 2.12, deq_B_map[sys_name]]
    d_str = [3.40, 2.92, 2.60, 2.44, 2.12]

    e_mace = [p["MACE_eV"] for p in pts]
    e_A_bs = [p["OptionA"]["dE_BS_eV"] for p in pts]
    e_A_ap = [p["OptionA"]["dE_AP_eV"] for p in pts]
    e_A_hs = [p["OptionA"]["dE_HS_eV"] for p in pts[:5]]

    e_B_bs = [p["OptionB"]["dE_BS_eV"] for p in pts]
    e_B_ap = [p["OptionB"]["dE_AP_eV"] for p in pts]
    e_B_hs = [p["OptionB"]["dE_HS_eV"] for p in pts[:5]]

    s2_A = [p["OptionA"]["S2_BS"] for p in pts]
    s2_B = [p["OptionB"]["S2_BS"] for p in pts]

    ax_top.plot(d_A, e_mace, "o--", color="#1f77b4", lw=2.2, markersize=6.5, label="MACE-MP-0 + D3 (ciego al espín)")
    ax_top.plot(d_A, e_A_bs, "s-", color="#2ca02c", lw=2.3, markersize=6.5, label="Opción A: BS-UKS ωB97X-D3 // MACE (↑↓)")
    ax_top.plot(d_A, e_A_ap, "^:", color="#17becf", lw=1.8, markersize=5.5, label="Opción A: Singlete Yamaguchi AP-UKS")
    ax_top.plot(d_B, e_B_bs, "D-", color="#ff7f0e", lw=2.3, markersize=6.0, label="Opción B: BS-UKS ωB97X-D3 // C3-B97-3c (↑↓)")
    ax_top.plot(d_str, e_A_hs, "v--", color="#d62728", lw=1.9, markersize=6.0, label="Opción A: Triplete HS-UKS (↑↑, Pauli)")
    ax_top.plot(d_str, e_B_hs, "P:", color="#9467bd", lw=1.9, markersize=6.0, label="Opción B: Triplete HS-UKS (↑↑, Pauli)")

    ax_top.axhline(0.0, color="black", lw=0.9, linestyle="-.")
    ax_top.set_title(titles[sys_name], fontsize=12, fontweight="bold")
    ax_top.invert_xaxis()
    ax_top.grid(True, alpha=0.3)
    if idx == 0:
        ax_top.set_ylabel("ΔE = E(d) − E_∞ homogeneizada (eV)", fontsize=11, fontweight="bold")
        ax_top.legend(fontsize=8.0, loc="lower left")

    ax_bot.plot(d_A, s2_A, "s-", color="#2ca02c", lw=2.2, markersize=6.5, label="⟨S²⟩_BS Opción A (// MACE)")
    ax_bot.plot(d_B, s2_B, "D--", color="#ff7f0e", lw=2.2, markersize=6.0, label="⟨S²⟩_BS Opción B (// C3-B97-3c)")
    ax_bot.axhline(1.0, color="gray", linestyle=":", lw=1.0, label="Birradical puro (⟨S²⟩ = 1.0)")
    ax_bot.axhline(0.0, color="black", linestyle="-.", lw=0.8, label="Singlete cerrado (⟨S²⟩ = 0.0)")
    ax_bot.invert_xaxis()
    ax_bot.set_ylim(-0.08, 1.12)
    ax_bot.set_xlabel("Distancia C–C Inter-Jaula d(C₀–C₂₅) (Å) [Aproximación →]", fontsize=10.5, fontweight="bold")
    ax_bot.grid(True, alpha=0.3)
    if idx == 0:
        ax_bot.set_ylabel("Valor esperado ⟨S²⟩_BS", fontsize=11, fontweight="bold")
        ax_bot.legend(fontsize=8.5, loc="lower left")

plt.suptitle("Auditoría Ab Initio Homogeneizada en ORCA 6.1.1 (BS-UKS ωB97X-D3/def2-SVP: Opción A vs Opción B vs MACE-MP-0+D3)", fontsize=13.5, fontweight="bold")
plt.tight_layout()
out_png = os.path.join(base_dir, "figura2_perfiles_homogeneizados_A_y_B.png")
plt.savefig(out_png, dpi=300)
print(f"Saved {out_png}")
