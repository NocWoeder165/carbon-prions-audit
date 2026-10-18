# Carbon Prions: Directed Conformational Nucleation and Quantum Dimerization of Doped Diamondoids at Low Temperature

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23427695.svg)](https://doi.org/10.5281/zenodo.23427695)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ORCA](https://img.shields.io/badge/ORCA-6.1.1-blue.svg)](https://orcaforum.kofo.mpg.de/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)

Computational chemistry dataset, open-shell broken-symmetry DFT benchmark, and equivariant neural network audit scripts accompanying the pre-print:

> **"Carbon Prions: Directed Conformational Nucleation and Quantum Dimerization of Doped Diamondoids at Low Temperature"**  
> **Author:** César Leonardo Rodríguez García (*Dark Horse / NocWoeder165*)  
> **Affiliation:** Universidad Tecnológica de Nayarit (UTNAY), Xalisco, Nayarit, México  
> **Laboratory:** Project Tharos -- Condensed Matter Physics and Vacuum Systems  
> **Pre-print DOI:** [10.5281/zenodo.23427695](https://doi.org/10.5281/zenodo.23427695)

---

## 🔬 Scientific Overview

For seven decades, diamond synthesis has relied on brute-force thermodynamic regimes (HPHT at gigapascal pressures or thermal plasma MPCVD at &gt;900 °C). However, the *sp*<sup>3</sup> unit cell of diamond already exists at ambient conditions inside adamantane (C<sub>10</sub>H<sub>16</sub>).

This repository provides the complete computational audit demonstrating that:

1. **Resolution of Neural Network Artifact:** An apparent steric barrier of 0.251 to 0.642 eV between 2.60 and 2.44 Å observed with the foundational equivariant neural network potential **MACE-MP-0 + D3** was an artifact of the spin-blind potential tracking the repulsive **Triplet manifold (S = 1, &uarr;&uarr;)** dominated by Pauli exclusion.
2. **Barrierless Singlet Dimerization:** In the **Antiferromagnetic Singlet channel (M<sub>S</sub> = 0, &uarr;&darr;)**, audited via 27 open-shell broken-symmetry calculations in **ORCA 6.1.1** (`BS-UKS` &omega;B97X-D3/def2-SVP with Yamaguchi spin projection `AP-UKS`), exchange stabilization overcomes equatorial shoulder repulsion, resulting in **zero activation barrier** and deep covalent potential wells (&Delta;E = -3.65 to -3.92 eV).
3. **Quantum Spin Statistics (1:3):** In an unpolarized thermal molecular beam in vacuum, only **25%** of collisions enter through the barrierless singlet channel (&uarr;&darr;), while **75%** collide in the repulsive triplet manifold (&uarr;&uarr;) and suffer elastic Pauli rebound unless surface-assisted spin relaxation occurs.
4. **Crystallographic Accuracy:** Structural optimization with `UKS B97-3c` reproduces the single-crystal X-ray diffraction central bond length of 1,1'-biadamantyl (1.578 Å, Alden et al., 1968) to within **-0.06%** (1.5771 Å, -0.0009 Å deviation).

<p align="center">
  <img src="figures/figura2_perfiles_homogeneizados_A_y_B.png" width="96%" alt="Homogenized Ab Initio Audit in ORCA 6.1.1">
  <br>
  <em>Figure: Homogenized Ab Initio Audit in ORCA 6.1.1 (Option A vs Option B vs MACE-MP-0). Top: Triplet repulsion wall vs barrierless Singlet covalent well. Bottom: Continuous collapse of the spin expectation value &lang;S&sup2;&rang;.</em>
</p>

---

## 📊 Summary Results Table

### Table 1: Structural and Energetic Parameters in Equilibrium (d<sub>eq</sub>)

| System | Chemical Formula | d<sub>eq</sub> (MACE) [Å] | d<sub>eq</sub> (B97-3c) [Å] | XRD Dev. (B97-3c) | &Delta;E (MACE) [eV] | &Delta;E (Option A) [eV] | &Delta;E (Option B) [eV] |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intrinsic** | C<sub>20</sub>H<sub>30</sub> | 1.596 | **1.5771** | **-0.06%** | -2.577 | -4.524 | **-3.921** |
| **Boron-Doped** | C<sub>19</sub>H<sub>29</sub>B | 1.635 | **1.5810** | +0.19% | -1.439 | -3.863 | **-3.651** |
| **Phosphorus-Doped** | C<sub>19</sub>H<sub>29</sub>P | 1.643 | **1.5880** | +0.63% | -1.859 | -4.210 | **-3.727** |

*Note: Option A evaluates MACE geometries against isolated MACE monomers; Option B evaluates UKS B97-3c geometries against isolated UKS B97-3c monomers.*

<p align="center">
  <img src="figures/figura1_relaxed_pes_auditada.png" width="90%" alt="Tier 1 MACE-MP-0 Exploration">
  <br>
  <em>Figure: Tier 1 Exploration (MACE-MP-0 + D3, float64). 13-step constrained scan showing the apparent steric crests.</em>
</p>

---

## 📁 Repository Structure

```text
carbon-prions-audit/
├── LICENSE                    # MIT Open Source License
├── README.md                  # Comprehensive scientific and usage guide
├── .gitignore                 # Filters ORCA scratch and wavefunction binaries
│
├── data/                      # Consolidated numeric tables and JSON records
│   ├── tabla_auditoria_completa_mace_vs_orca_A_y_B.csv
│   ├── auditoria_completa_5puntos.json
│   ├── resumen_validacion_dft_orca.json
│   ├── datos_crudos_pes_auditoria.csv
│   └── resumen_metricas_auditoria.json
│
├── figures/                   # High-resolution publication plots
│   ├── figura1_relaxed_pes_auditada.png
│   ├── figura2_perfiles_homogeneizados_A_y_B.png
│   └── figura2_reactor_tharos.png
│
├── geometries/                # Cartesian coordinates (.xyz)
│   ├── monomer_adamantane_radical.xyz
│   ├── monomer_bora_adamantane_radical.xyz
│   ├── monomer_phospha_adamantane_radical.xyz
│   ├── dimer_biadamantyl_relaxed.xyz
│   ├── dimer_bora_biadamantyl_relaxed.xyz
│   ├── dimer_phospha_biadamantyl_relaxed.xyz
│   └── optB_*.xyz (coaxial and relaxed scans)
│
├── orca_audit/                # 27 ab initio ORCA 6.1.1 inputs, outputs, and properties
│   ├── optA_*.inp / optA_*.out
│   ├── optB_*.inp / optB_*.out
│   └── vdw_*.inp / vdw_*.out
│
├── manuscript/                # LaTeX sources and PDF preprint
│   ├── preprint_priones_carbono_.pdf      (Published v1.0 PDF in Spanish)
│   ├── preprint_priones_de_carbono.tex    (Spanish LaTeX source)
│   ├── preprint_carbon_prions_EN.tex      (English LaTeX source)
│   └── preprint_carbon_prions_EN.md       (English Markdown manuscript)
│
└── scripts/                   # Simulation, orchestration, and analysis scripts
    ├── simulacion_paper1_priones_carbono.py  (Tier 1 MACE-MP-0 + D3 scan)
    ├── setup_both_options_orca.py            (Tier 2 ORCA generator)
    └── plot_audit_profiles.py                (Option A vs B comparison plot)
```

---

## 🛠️ Reproduction Instructions

### 1. Environment Setup
```bash
git clone https://github.com/NocWoeder165/carbon-prions-audit.git
cd carbon-prions-audit

# Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install torch ase mace-torch torch-dftd3 matplotlib pandas
```

### 2. Run Tier 1 MACE-MP-0 Exploration
```bash
python scripts/simulacion_paper1_priones_carbono.py
```

### 3. Run Tier 2 Quantum Audit (ORCA 6.1.1)
To run a representative broken-symmetry point (e.g., d = 2.44 Å for intrinsic adamantyl dimer):
```bash
orca orca_audit/optB_C20H30_244.inp > orca_audit/optB_C20H30_244.out
```

---

## 📜 Citation

If you use this dataset, coordinates, or simulation scripts, please cite the permanent Zenodo record:

```bibtex
@misc{rodriguez_garcia_2026_zenodo_23427695,
  author       = {Rodríguez García, César Leonardo},
  title        = {{Carbon Prions: Directed Conformational Nucleation and 
                   Quantum Dimerization of Doped Diamondoids at Low 
                   Temperature}},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23427695},
  url          = {https://doi.org/10.5281/zenodo.23427695}
}
```

---

## ⚖️ License
* **Code, Scripts, and Coordinates:** Released under the [MIT License](LICENSE).
* **Preprint Text and Figures:** Released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
