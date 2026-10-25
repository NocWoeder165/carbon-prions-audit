# STATUS.MD: ESTADO DE LA AUDITORÍA CUÁNTICA DE TRANSPORTE Y TOPOLOGÍA
**Última Actualización:** 2026-10-22 21:50 Local  
**Software:** ORCA 6.1.1 (AVX-512, 10/8 cores dedicados)  
**Autoridad de Datos:** Este archivo constituye la **única fuente oficial de números cuánticos** para la redacción del manuscrito y reportes multiescala. Todo valor numérico sin archivo fuente explícito queda invalidado.

---

## 1. Modelos Químicos y Estados de Referencia

| Especie | Fórmula | Átomos | Electrones | Multiplicidad | Método DFT | Energía Total ($E_{\text{tot}}$, Eh) | Archivo Fuente y Fecha | Estado de Convergencia |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **Adamantano Aislado** | $\text{C}_{10}\text{H}_{16}$ | 26 | 76 | 1 ($S=0$) | B97-3c / def2-mSVP | `-390.53392989` | `01_orca_quantum/rigorous_quantum_audit/opt_adamantane.out` (2026-10-21 18:40) | **SÍ (CONVERGED)** (42.9 s) |
| **Radical Adamantilo** | $\text{C}_{10}\text{H}_{15}^\bullet$ | 25 | 75 | 2 ($S=1/2$) | UKS B97-3c / def2-mSVP | `-389.86748916` | `01_orca_quantum/v_groove_audit/00_adamantyl_radical.out` (2026-10-22 05:47) | **SÍ (CONVERGED)** (8 ciclos) |
| **Tríada Anclada** | $\text{C}_{30}\text{H}_{48}$ | 78 | 228 | 1 ($S=0$) | B97-3c / def2-mSVP | `-1171.55372640` | `01_orca_quantum/test_c30h48/dft_opt.out` (2026-10-21 04:03) | Optimizado (6 anclajes basales) |
| **Tríada Anclada** | $\text{C}_{30}\text{H}_{48}$ | 78 | 228 | 1 ($S=0$) | $\omega\text{B97X-D3}$ / def2-TZVP | `-1172.26903261` | `01_orca_quantum/scan_sequential_and_lateral/wb97x_refinement/triada.out` | [SIN VERIFICAR: .out no hallado en disco] |
| **Hidrógeno Molecular** | $\text{H}_2$ | 2 | 2 | 1 ($S=0$) | B97-3c / def2-mSVP | `-1.17914025` | `01_orca_quantum/test_c30h48/opt_H2.out` (2026-10-21 04:04) | **SÍ (CONVERGED)** ($r_{\text{HH}} = 0.7355\,\text{Å}$) |
| **Hidrógeno Molecular** | $\text{H}_2$ | 2 | 2 | 1 ($S=0$) | $\omega\text{B97X-D3}$ / def2-TZVP | `-1.17462708` | `01_orca_quantum/scan_sequential_and_lateral/wb97x_refinement/h2.out` (2026-10-21 17:07) | Single Point |
| **Asíntota Desligada** | $\text{C}_{30}\text{H}_{48} + \text{H}_2$ | 80 | 230 | 1 ($S=0$) | B97-3c / def2-mSVP | `-1172.73286665` | Suma analítica de referencias | Suma de estados aislados |
| **Asíntota Desligada** | $\text{C}_{30}\text{H}_{48} + \text{H}_2$ | 80 | 230 | 1 ($S=0$) | $\omega\text{B97X-D3}$ / def2-TZVP | `-1173.44365969` | Suma analítica de referencias | Suma de estados aislados |

---

## 2. Termodinámica de Confinamiento de la Tríada $\text{C}_{30}\text{H}_{48}$

Al comparar la energía de la tríada anclada a diamante {111} frente a tres moléculas de adamantano aisladas y totalmente relajadas:

$$\Delta E = E(\text{C}_{30}\text{H}_{48}) - 3 \times E(\text{C}_{10}\text{H}_{16})$$
$$\Delta E = -1171.55372640\,\text{Eh} - 3 \times (-390.53392989\,\text{Eh}) = +0.04806327\,\text{Eh} = \mathbf{+1.3079\,\text{eV}} \quad (\mathbf{+30.16\,\text{kcal/mol}})$$

### Descomposición Energética en B97-3c:
1. **Atracción de Dispersión London D3BJ ($\Delta E_{\text{disp}}$):**
   - $E_{\text{disp}}(\text{Tríada}) = -0.240215\,\text{Eh}$ (`01_orca_quantum/test_c30h48/dft_opt.out`)
   - $3 \times E_{\text{disp}}(\text{Adamantano}) = 3 \times (-0.069233\,\text{Eh}) = -0.207700\,\text{Eh}$ (`opt_adamantane.out`)
   - $\Delta E_{\text{disp}} = -0.032515\,\text{Eh} = \mathbf{-0.8848\,\text{eV}} \quad (\mathbf{-20.40\,\text{kcal/mol}})$ (Estabilizante).
2. **Energía No Dispersiva (incluye deformación de esqueleto, anclajes basales y gCP):**
   - $\Delta E_{\text{no dispersiva}} = \Delta E_{\text{tot}} - \Delta E_{\text{disp}} = +1.3079\,\text{eV} - (-0.8848\,\text{eV}) = \mathbf{+2.1927\,\text{eV}} \quad (\mathbf{+50.57\,\text{kcal/mol}})$.

---

## 3. Auditoría de la Tríada Cosida $\text{C}_{30}\text{H}_{42}$ (Cierre del Modelo A vs. Modelo B)

Balance termoquímico de formación de la tríada cosida a partir de la tríada anclada:
$$\text{C}_{30}\text{H}_{48} \to \text{C}_{30}\text{H}_{42} + 3\,\text{H}_2$$
$$\Delta E_{\text{rxn}} = E(\text{C}_{30}\text{H}_{42}) + 3\,E(\text{H}_2) - E(\text{C}_{30}\text{H}_{48})$$
$$\Delta E_{\text{por enlace}} = \frac{\Delta E_{\text{rxn}}}{3}$$

### Resultados Cuánticos B97-3c / def2-mSVP:

| Modelo | $E(\text{C}_{30}\text{H}_{42})$ (Eh) | $\Delta E_{\text{rxn}}$ Total | $\Delta E_{\text{por enlace}}$ | Convergencia | Ciclos | Distancias C–C Inter-Jaula (Å) | Ángulos C–C–C / Propiedades | Archivo Fuente |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| **1A: Central Libre (C8–C16–C24)** | **-1167.64772956** | **+10.0295 eV** (+231.29 kcal/mol) | **+3.3432 eV/enlace** | **SÍ (CONVERGED)** | 25 | **C8–C16: 1.5282**<br>**C16–C24: 1.5328**<br>**C8–C24: 1.3568** | 52.7°, 63.8°, 63.5° (anillo $\text{C}_3$ cerrado) | `01_orca_quantum/rigorous_quantum_audit/model1_central_c30h42/opt_c30h42_model1A_free.out` |
| **1A_no_anchors: Central Sin Anclajes** | **-1167.94511507** | **+1.9372 eV** (+44.67 kcal/mol, vs. anclado)<br>**+3.2451 eV** (+74.83 kcal/mol, vs. libre) | **+0.6457 eV/enlace**<br>**+1.0817 eV/enlace** | **SÍ (CONVERGED)** | 26 | **C8–C16: 1.5317**<br>**C16–C24: 1.5334**<br>**C8–C24: 1.5315** | $\langle S^2 \rangle = 0.0000$; base contrae a $3.124\,\text{Å}$ ($\Delta d = -1.921\,\text{Å}$) | `01_orca_quantum/rigorous_quantum_audit/model1_central_c30h42/opt_c30h42_model1A_no_anchors.out` |
| **1A_unbiased: UKS BrokenSym 1,1 SIN anclajes (sin Constraints en `.inp`), inicio $3.241\,\text{Å}$; terminó con ⟨S²⟩=0 (capa cerrada)** | **-1167.94512505** | **+1.9369 eV** (+44.67 kcal/mol, vs. anclado)<br>**+3.2448 eV** (+74.83 kcal/mol, vs. libre) | **+0.6456 eV/enlace**<br>**+1.0816 eV/enlace** | **SÍ (CONVERGED)** | 31 | **C8–C16: 1.5321**<br>**C16–C24: 1.5321**<br>**C8–C24: 1.5319** | $\langle S^2 \rangle = 0.0000$; cierre espontáneo a ciclopropano $C_{3v}$ | `01_orca_quantum/rigorous_quantum_audit/model1_central_c30h42/opt_c30h42_model1A_unbiased.out` |
| **1A_anch_unbiased: UKS BrokenSym 1,1 CON anclajes, inicio $3.241\,\text{Å}$** | **-1167.58628820** | **+11.7014 eV** (+269.84 kcal/mol, vs. anclado)<br>**+13.0093 eV** (+300.00 kcal/mol, vs. libre) | **+3.9005 eV/enlace**<br>**+4.3364 eV/enlace** | **SÍ (CONVERGED)** | 18 | **C8–C16: 2.9230**<br>**C16–C24: 2.9270**<br>**C8–C24: 2.9215** | $\langle S^2 \rangle = 0.0000$; permanece ABIERTO a $\sim 2.92\,\text{Å}$ (no cierra a ciclopropano) | `01_orca_quantum/rigorous_quantum_audit/model1_central_c30h42/opt_c30h42_model1A_anch_unbiased.out` |
| **1B: Central Forzado (1.540 Å)** | **-1167.63077767** | **+10.4908 eV** (+241.92 kcal/mol) | **+3.4969 eV/enlace** | **SÍ (CONVERGED)** | 20 | C8–C16: 1.5400<br>C16–C24: 1.5400<br>C8–C24: 1.5400 | 60.0°, 60.0°, 60.0° (equilátero) | `01_orca_quantum/rigorous_quantum_audit/model1_central_c30h42/opt_c30h42_model1B_forced.out` |
| **1A_bs: Broken Symmetry UKS(1,1)** | **-1167.67370764** | **+9.3226 eV** (+214.98 kcal/mol) | **+3.1075 eV/enlace** | Single Point | - | (Geometría 1A libre) | $\Delta E(\text{BS}-\text{RKS}) = \mathbf{-0.7069\,\text{eV}}$ (-16.30 kcal/mol) | `01_orca_quantum/rigorous_quantum_audit/model1_central_c30h42/sp_c30h42_model1A_bs.out` |
| **2A: Cabezas de Puente Libre** | -1167.65626575 | **+9.7972 eV** (+225.93 kcal/mol) | **+3.2657 eV/enlace** | **NO** ($g_{\max}=1.48 \times 10^{-4}$) | 80 | **C0–C21: 3.837**<br>**C1–C10: 4.219**<br>C11–C20: 1.607 | 96.8°, 140.5°, 80.3°, 146.3°, 142.7°, 101.1° | `01_orca_quantum/rigorous_quantum_audit/opt_c30h42_basal.out` (2026-10-21 19:30) |
| **2B: Cabezas de Puente Forzado** | -1167.45543542 | **+15.2621 eV** (+351.95 kcal/mol) | **+5.0874 eV/enlace** | **SÍ (CONVERGED)** | 25 | C0–C21: 1.540<br>C1–C10: 1.540<br>C11–C20: 1.540 | 121.1°, 121.1°, 118.5°, 120.4°, 120.4°, 118.5° | `01_orca_quantum/rigorous_quantum_audit/opt_c30h42_forced_covalent.out` (2026-10-21 19:47) |

> Poblaciones de espín Mulliken (`sp_c30h42_model1A_bs.out`): C0 +0.9138, C20 -0.9127; C8 +0.0087, C16 +0.0229, C24 -0.0186.

---

## 4. Reglas Topológicas y Pérdida de Hidrógenos POR MODELO

> **Regla Topológica por Modelo:**
> - **Modelo A (Fusión Central de Metilenos C8–C16–C24):** El estrechamiento del poro en $\text{C}_{30}\text{H}_{48}$ lo forman **H43, H55 y H67**. Al coser este modelo, estos 3 H (y los 3 H laterales H42, H54, H66) se pierden, por lo que el poro **no existe en el producto cosido**.
> - **Modelo B (Cabezas de Puente C0–C21, C1–C10, C11–C20, corridas 2A/2B):** **NO pierde los H del poro.** Los hidrógenos H43, H55 y H67 **permanecen intactos**. Se pierden los 6 H superiores de cabeza de puente.

---

## 5. Auditoría de Datasets Cuánticos de Transporte de $\text{H}_2$

### Dataset 1: Escaneo No-Secuencial (`scan_h2_pore_production`, 2026-10-21 04:05)
- **Todos los puntos relajados tienen `Conv=False` (detenidos en ciclo 40).**
- El pico de $+2.2542\,\text{eV}$ en `rel_par_Zp0.50.out` finalizó con $g_{\max} = 5.65 \times 10^{-3}\,\text{Eh/bohr}$ (~19 veces la tolerancia). Es un **artefacto numérico no convergido**.

### Dataset 2: Escaneo Secuencial Continuado (`sequential_scan`, 2026-10-21 17:22)
- Continuación secuencial con `MaxIter 35`.
- Los picos aparentes en $Z = 0.00\,\text{Å}$ (+1.7451 eV y +1.8396 eV) **no convergieron** ($g_{\max} = 0.89\text{--}2.90 \times 10^{-3}\,\text{Eh/bohr}$).

---

### Dataset 3: Escaneo Secuencial Denso Longitudinal ($\theta_Z = 5.82^\circ$, ID: `RUN_DENSE_AUDIT_20261021_1839`, COMPLETADO)
- **Directorio Fuente:** `01_orca_quantum/rigorous_quantum_audit/dense_scan/`
- **Archivo CSV Fuente:** `dense_sequential_scan.csv`
- **Fecha de Corrida:** 2026-10-21 19:50 a 2026-10-22 01:15 Local
- **Método:** Continuación secuencial en malla fina con `MaxIter 80` y TightSCF en B97-3c / def2-mSVP.
- **Auditoría Completa de Convergencia y Gradientes (20 puntos):**

| Archivo de Salida | Rama | $Z$ Relativo (Å) | $E_{\text{tot}}$ (Eh) | $\Delta E_{\text{int}}$ (eV) | $\Delta E_{\text{int}}$ (kcal/mol) | Convergido | Ciclos | $g_{\max}$ (Eh/bohr) | $g_{\text{RMS}}$ (Eh/bohr) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `opt_down_Zp1.50.out` | Desc. | $+1.50$ | -1172.70001919 | +0.8938 | +20.61 | **NO** | 80 | $3.18 \times 10^{-4}$ | $5.32 \times 10^{-5}$ |
| `opt_down_Zp1.00.out` | Desc. | $+1.00$ | -1172.68719994 | +1.2427 | +28.66 | **SÍ** | 38 | $8.68 \times 10^{-5}$ | $1.76 \times 10^{-5}$ |
| `opt_down_Zp0.75.out` | Desc. | $+0.75$ | -1172.68061564 | +1.4218 | +32.79 | **SÍ** | 23 | $8.83 \times 10^{-5}$ | $1.87 \times 10^{-5}$ |
| `opt_down_Zp0.50.out` | Desc. | $+0.50$ | -1172.67442917 | +1.5902 | +36.67 | **SÍ** | 20 | $8.86 \times 10^{-5}$ | $1.87 \times 10^{-5}$ |
| `opt_down_Zp0.25.out` | Desc. | **$+0.25$** | **-1172.66945047** | **+1.7256** | **+39.79** | **SÍ** | 16 | **$9.84 \times 10^{-5}$** | **$2.05 \times 10^{-5}$** |
| `opt_down_Zp0.00.out` | Desc. | $0.00$ | -1172.67231852 | +1.6476 | +37.99 | **SÍ** | 50 | $1.18 \times 10^{-4}$ | $2.31 \times 10^{-5}$ |
| `opt_down_Zm0.25.out` | Desc. | $-0.25$ | -1172.67665257 | +1.5297 | +35.27 | **SÍ** | 11 | $1.37 \times 10^{-4}$ | $2.59 \times 10^{-5}$ |
| `opt_down_Zm0.50.out` | Desc. | $-0.50$ | -1172.68297137 | +1.3577 | +31.31 | **SÍ** | 17 | $8.11 \times 10^{-5}$ | $1.92 \times 10^{-5}$ |
| `opt_down_Zm0.75.out` | Desc. | $-0.75$ | -1172.69114733 | +1.1352 | +26.18 | **SÍ** | 22 | $9.76 \times 10^{-5}$ | $2.03 \times 10^{-5}$ |
| `opt_down_Zm1.00.out` | Desc. | $-1.00$ | -1172.70049359 | +0.8809 | +20.31 | **SÍ** | 37 | $8.87 \times 10^{-5}$ | $2.22 \times 10^{-5}$ |
| `opt_up_Zm1.00.out` | Asc. | $-1.00$ | -1172.70048572 | +0.8811 | +20.32 | **NO** | 80 | $2.22 \times 10^{-4}$ | $3.57 \times 10^{-5}$ |
| `opt_up_Zm0.75.out` | Asc. | $-0.75$ | -1172.69114149 | +1.1354 | +26.18 | **SÍ** | 15 | $1.33 \times 10^{-4}$ | $2.75 \times 10^{-5}$ |
| `opt_up_Zm0.50.out` | Asc. | $-0.50$ | -1172.68295994 | +1.3580 | +31.32 | **SÍ** | 23 | $1.11 \times 10^{-4}$ | $2.31 \times 10^{-5}$ |
| `opt_up_Zm0.25.out` | Asc. | $-0.25$ | -1172.67640984 | +1.5363 | +35.43 | **SÍ** | 13 | $1.55 \times 10^{-4}$ | $2.69 \times 10^{-5}$ |
| `opt_up_Zp0.00.out` | Asc. | $0.00$ | -1172.67202109 | +1.6557 | +38.18 | **SÍ** | 13 | $1.08 \times 10^{-4}$ | $2.19 \times 10^{-5}$ |
| `opt_up_Zp0.25.out` | Asc. | **$+0.25$** | **-1172.66985626** | **+1.7146** | **+39.54** | **SÍ** | 19 | **$9.66 \times 10^{-5}$** | **$2.09 \times 10^{-5}$** |
| `opt_up_Zp0.50.out` | Asc. | $+0.50$ | -1172.67445826 | +1.5894 | +36.65 | **SÍ** | 71 | $9.87 \times 10^{-5}$ | $2.03 \times 10^{-5}$ |
| `opt_up_Zp0.75.out` | Asc. | $+0.75$ | -1172.68061662 | +1.4218 | +32.79 | **SÍ** | 18 | $8.94 \times 10^{-5}$ | $1.86 \times 10^{-5}$ |
| `opt_up_Zp1.00.out` | Asc. | $+1.00$ | -1172.68715061 | +1.2440 | +28.69 | **SÍ** | 25 | $1.60 \times 10^{-4}$ | $2.49 \times 10^{-5}$ |
| `opt_up_Zp1.50.out` | Asc. | $+1.50$ | -1172.70003745 | +0.8933 | +20.60 | **SÍ** | 41 | $9.68 \times 10^{-5}$ | $1.86 \times 10^{-5}$ |

---

### Dataset 4: Escaneo Secuencial Denso Perpendicular ($\theta_Z = 95.60^\circ$, COMPLETADO AL 100%)
- **Directorio Fuente:** `01_orca_quantum/rigorous_quantum_audit/dense_scan_perp/`
- **Archivo CSV Fuente:** `dense_perp_scan.csv`
- **Orientación:** Vector $\text{H}-\text{H}$ estrictamente en el plano del poro ($\mathbf{u}_{\text{perp}} \cdot \mathbf{n} = 8.77 \times 10^{-19}$, $\theta_Z = 95.60^\circ$).
- **Auditoría Completa de Convergencia (20 puntos: 10 Descendentes + 10 Ascendentes):**

| Archivo de Salida | Rama | $Z$ Relativo (Å) | $E_{\text{tot}}$ (Eh) | $\Delta E_{\text{int}}$ (eV) | $\Delta E_{\text{int}}$ (kcal/mol) | Convergido | Ciclos | $g_{\text{RMS}}$ (Eh/bohr) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `opt_down_Zp1p50_cont1.out` | Desc. | $+1.50$ | -1172.69947588 | +0.9082 | +20.94 | **SÍ** | 80 + 1 | $3.33 \times 10^{-5}$ |
| `opt_down_Zp1p00.out` | Desc. | $+1.00$ | -1172.68708614 | +1.2453 | +28.72 | **SÍ** | 46 | $2.24 \times 10^{-5}$ |
| `opt_down_Zp0p75.out` | Desc. | $+0.75$ | -1172.68040144 | +1.4272 | +32.91 | **SÍ** | 22 | $2.51 \times 10^{-5}$ |
| `opt_down_Zp0p50.out` | Desc. | $+0.50$ | -1172.67357790 | +1.6129 | +37.19 | **SÍ** | 21 | $2.91 \times 10^{-5}$ |
| `opt_down_Zp0p25.out` | Desc. | **$+0.25$** | **-1172.66784803** | **+1.7688** | **+40.79** | **SÍ** | 21 | **$3.24 \times 10^{-5}$** |
| `opt_down_Zp0p00_cont1.out` | Desc. | $0.00$ | -1172.67009235 | +1.7077 | +39.38 | **SÍ** | 80 + 1 | $3.24 \times 10^{-5}$ |
| `opt_down_Zm0p25.out` | Desc. | $-0.25$ | -1172.67464395 | +1.5839 | +36.52 | **SÍ** | 42 | $2.10 \times 10^{-5}$ |
| `opt_down_Zm0p50.out` | Desc. | $-0.50$ | -1172.68123208 | +1.4046 | +32.39 | **SÍ** | 16 | $2.01 \times 10^{-5}$ |
| `opt_down_Zm0p75.out` | Desc. | $-0.75$ | -1172.68999488 | +1.1661 | +26.89 | **SÍ** | 37 | $2.40 \times 10^{-5}$ |
| `opt_down_Zm1p00.out` | Desc. | $-1.00$ | -1172.70008927 | +0.8915 | +20.56 | **SÍ** | 45 | $1.30 \times 10^{-5}$ |
| `opt_up_Zm1p00_cont1.out` | Asc. | $-1.00$ | -1172.70007636 | +0.8918 | +20.57 | **SÍ** | 80 + 68 | $2.36 \times 10^{-5}$ |
| `opt_up_Zm0p75.out` | Asc. | $-0.75$ | -1172.68991141 | +1.1684 | +26.94 | **SÍ** | 20 | $1.99 \times 10^{-5}$ |
| `opt_up_Zm0p50.out` | Asc. | $-0.50$ | -1172.68111722 | +1.4077 | +32.46 | **SÍ** | 29 | $2.58 \times 10^{-5}$ |
| `opt_up_Zm0p25.out` | Asc. | $-0.25$ | -1172.67460884 | +1.5848 | +36.55 | **SÍ** | 46 | $1.91 \times 10^{-5}$ |
| `opt_up_Zp0p00.out` | Asc. | $0.00$ | -1172.67019373 | +1.7050 | +39.32 | **SÍ** | 17 | $1.86 \times 10^{-5}$ |
| `opt_up_Zp0p25.out` | Asc. | **$+0.25$** | **-1172.66790186** | **+1.7673** | **+40.76** | **SÍ** | 10 | **$2.38 \times 10^{-5}$** |
| `opt_up_Zp0p50.out` | Asc. | $+0.50$ | -1172.67361222 | +1.6119 | +37.17 | **SÍ** | 70 | $2.34 \times 10^{-5}$ |
| `opt_up_Zp0p75.out` | Asc. | $+0.75$ | -1172.68042774 | +1.4265 | +32.90 | **SÍ** | 28 | $1.74 \times 10^{-5}$ |
| `opt_up_Zp1p00.out` | Asc. | $+1.00$ | -1172.68709393 | +1.2451 | +28.71 | **SÍ** | 25 | $1.81 \times 10^{-5}$ |
| `opt_up_Zp1p50.out` | Asc. | $+1.50$ | -1172.69947038 | +0.9083 | +20.95 | **SÍ** | 53 | $2.02 \times 10^{-5}$ |

- **Comparación Directa Longitudinal vs. Perpendicular en el Máximo ($Z = +0.25\,\text{Å}$):**
  - **Longitudinal ($\theta = 5.82^\circ$, casi colineal con $Z$):** $\Delta E_{\max} = \mathbf{+1.7256\,\text{eV}}$ ($+39.79\,\text{kcal/mol}$, Desc.) / $\mathbf{+1.7146\,\text{eV}}$ ($+39.54\,\text{kcal/mol}$, Asc.).
  - **Perpendicular ($\theta = 95.60^\circ$, en plano del poro):** $\Delta E_{\max} = \mathbf{+1.7688\,\text{eV}}$ ($+40.79\,\text{kcal/mol}$, Desc.) / $\mathbf{+1.7673\,\text{eV}}$ ($+40.76\,\text{kcal/mol}$, Asc.).
  - **Histéresis Descendente vs. Ascendente (Perpendicular en $Z = +0.25\,\text{Å}$):** $\Delta E_{\text{hist}} = \mathbf{0.0015\,\text{eV}}$ ($\mathbf{0.03\,\text{kcal/mol}}$).
  - **Diferencia de Energía Rotacional:** $\Delta\Delta E = +1.7688 - 1.7256 = \mathbf{+0.0432\,\text{eV}}$ ($\mathbf{+1.00\,\text{kcal/mol}}$).

---

### Refinamiento $\omega\text{B97X-D3}$/def2-TZVP sobre el Máximo del Escaneo Restringido ($Z = +0.25\,\text{Å}$):
- **Archivo Fuente:** `01_orca_quantum/rigorous_quantum_audit/wb97x_dense_peak/sp_peak_wb97x.out` (2026-10-22 01:14)
- **Geometría Base:** `opt_down_Zp0.25.xyz` (convergida).
- **Energía Total:** $E = -1173.38232395\,\text{Eh}$.
- **Asíntota Desligada:** $E_{\text{ref}} = -1173.44365969\,\text{Eh}$.
- **Barrera Refinada:**
  $$\Delta E_{\text{int}} = (-1173.38232395 - (-1173.44365969)) \times 27.211386245988 = \mathbf{+1.6690\,\text{eV}} \quad (\mathbf{+38.49\,\text{kcal/mol}})$$
  *(Reduce la barrera en $0.057\,\text{eV}$ respecto a B97-3c, una corrección de $-3.3\%$).*

---

## 6. Cinética de Transporte TST en Condiciones de Proceso MLE ($T = 453.15\,\text{K}$)

- **Temperatura:** $T = 453.15\,\text{K}$ ($180^\circ\text{C}$).
- **Prefactor Eyring:** $\nu_0 = \frac{k_B T}{h} = \mathbf{9.4421 \times 10^{12}\,\text{s}^{-1}}$.
- **Energía térmica:** $k_B T = 0.0390492\,\text{eV}$.
- Nota: Z = -1.0 Å no está demostrado como mínimo; los tiempos de escape son cotas sujetas a estado inicial supuesto.

| Proceso y Ruta | Estado Inicial Asumido | $\Delta E^{\ddagger}$ (eV) | Barrera ($\Delta E^{\ddagger} / k_B T$) | Constante $k$ ($\text{s}^{-1}$) | Tiempo Característico $\tau$ | Archivo Base / Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Entrada desde Vacío** (B97-3c, $Z=+0.25$) | Asíntota Vacío ($Z \to \infty$) | $+1.7256$ | $44.2\,k_B T$ | $6.075 \times 10^{-7}$ | $19.05\,\text{días}$ | `opt_down_Zp0.25.out` |
| **Entrada desde Vacío** ($\omega\text{B97X-D3}$, $Z=+0.25$) | Asíntota Vacío ($Z \to \infty$) | $+1.6690$ | $42.7\,k_B T$ | $2.588 \times 10^{-6}$ | $4.47\,\text{días}$ | `sp_peak_wb97x.out` |
| **Escape: Cota A (Confinamiento supuesto)** | Bolsillo supuesto $Z = -1.0\,\text{Å}$ | $+0.8447$ | $21.6\,k_B T$ | $3.807 \times 10^{3}$ | $\mathbf{262.7\,\mu\text{s}}$ | `opt_down_Zm1.00.out` (hipotético) |
| **Escape: Cota B (Sin confinamiento / terraza)** | Referencia abierta ($Z \le -2.0\,\text{Å}$) | $+1.67\text{ a }+1.73$ | $42.7\text{--}44.2\,k_B T$ | $2.6 \times 10^{-6}\text{ a }6.1 \times 10^{-7}$ | $\mathbf{4.5\text{ a }19.0\,\text{días}}$ | Extrapolación de cota desligada |

---

## 7. Facetado y Confinamiento Cuántico: Opción B (Escalón {111} sobre Terraza (111)) y Control Planar

### Diagnóstico Cristalográfico Riguroso (SVD y Base Cúbica):
- **Orientación del Escalón:** Eje del escalón a lo largo de $X = [1, -1, 0]$ (dirección de empaquetamiento denso $\langle 110 \rangle$ en red diamante $Fd\bar{3}m$, $a = 3.567\,\text{Å}$).
- **Terraza Inferior (111):** Normal cartesiana $[0.0000, 0.0000, 1.0000]$, proyección cúbica $[1, 1, 1]/\sqrt{3}$ $\implies$ **Miller (1, 1, 1)** exacto.
- **Cara del Escalón (1, 1, -1):** Normal cartesiana $[0.0000, 2\sqrt{2}/3, 1/3] = [0.0000, 0.9428, 0.3333]$, proyección cúbica $[1, 1, -1]/\sqrt{3}$ $\implies$ **Miller (1, 1, -1)** exacto ({111}).
- **Ángulo Diedro Teórico y Ajustado:**
  - Ángulo diedro agudo (reentrante de fondo): $\arccos(1/3) = \mathbf{70.5288^\circ}$ (esperado $70.53^\circ$).
  - Ángulo diedro obtuso (borde superior del escalón): $180^\circ - 70.5288^\circ = \mathbf{109.4712^\circ}$ (esperado $109.47^\circ$).

### Protocolo de Modelado y Control:
1. **Control Planar:** Terraza {111} plana con 2 bicapas completas (`01_flat_clean_radical.xyz`: 81 átomos, 32 C, 49 H; 17 C congelados), idéntica área basal y espesor que la terraza inferior del escalón.
2. **Escalón {111} (Opción B):** Escalón mono-bicapa con cara (1, 1, -1). Verificado en `01_step_clean_radical.xyz`: 102 átomos (45 C, 57 H); 17 C congelados. [Las cifras previas "47 C, 61 H" eran incorrectas.]
3. **Guardián Estérico de Adsorción (Radical Adamantilo $\text{C}_{10}\text{H}_{15}^\bullet$ a $d_{\text{CC}} = 1.56\,\text{Å}$):**
   - Escalón {111}: $\text{dist}(\text{H}\cdots\text{H}) \ge 2.00\,\text{Å}$, $\text{dist}(\text{C}\cdots\text{H}) \ge 1.85\,\text{Å}$, $\text{dist}(\text{C}\cdots\text{C}) \ge 1.85\,\text{Å}$.
   - Terraza {111} Plana: $\text{dist}(\text{H}\cdots\text{H}) \ge 2.00\,\text{Å}$, $\text{dist}(\text{C}\cdots\text{H}) \ge 1.85\,\text{Å}$, $\text{dist}(\text{C}\cdots\text{C}) \ge 1.85\,\text{Å}$.
4. **Configuración de Fragmentos para BrokenSym 1,1:**
   - Fragmento 1: Sustrato (diamante H-pasivado con centro radical).
   - Fragmento 2: Radical adamantilo ($\text{C}_{10}\text{H}_{15}^\bullet$).
   - Archivos generados: `01_orca_quantum/v_groove_audit/02B_step_plus_adamantyl_BS.xyz` y `02_flat_terrace_plus_adamantyl_BS.xyz`.

### Resultados de Optimización Cuántica (UKS B97-3c / def2-mSVP + D3BJ):

| Sistema / Modelo | Archivo Fuente (`01_orca_quantum/v_groove_audit/`) | $E_{\text{tot}}$ (Eh) | $E_{\text{disp}}$ (Eh) | $\langle S^2 \rangle$ | Ciclos | Convergido | $\Delta E_{\text{ads}}^{\text{tot}}$ (eV) | $\Delta E_{\text{disp}}$ (eV) | $\Delta E_{\text{ads}}^{\text{no-disp}}$ (eV) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Radical Adamantilo Libre** | `00_adamantyl_radical.out` | -389.86748916 | -0.06792918 | 0.7544 | 8 | **SÍ** | — | — | — |
| **Terraza {111} Plana (Radical)** | `01_flat_clean_radical.out` | -1248.31894380 | -0.25151089 | 0.7545 | 15 | **SÍ** | — | — | — |
| **Escalón {111}/(11-1) (Radical)** | `01_step_clean_radical.out` | -1748.34531757 | -0.39457979 | 0.7545 | 15 | **SÍ** | — | — | — |
| **Terraza Plana + Adamantilo (BS 1,1)** | `02_flat_terrace_plus_adamantyl_BS.out` | -1638.25291235 | -0.35687136 | 0.0000 | 28 | **SÍ** | **-1.8090** (-41.72 kcal/mol) | **-1.0186** (-23.49 kcal/mol) | **-0.7904** (-18.23 kcal/mol) |
| **Escalón {111} + Adamantilo (BS 1,1)** | `02B_step_plus_adamantyl_BS.out` | -2138.27585196 | -0.50300991 | 0.0000 | 72 | **SÍ** (gmax 9.79e-5, grms 1.35e-5 Eh/bohr) | **-1.7155** (-39.56 kcal/mol) | **-1.1021** (-25.41 kcal/mol) | **-0.6135** (-14.15 kcal/mol) |
| **Diferencia (Escalón − Terraza)** | `step_vs_terrace_summary.json` | — | — | — | — | — | **+0.0934** (+2.15 kcal/mol) | **-0.0835** (-1.93 kcal/mol) | **+0.1769** |

---

## 8. Calibración del Protocolo de Adsorción (B97-3c / def2-mSVP, ORCA 6.1.1)

Fuente: `01_orca_quantum/calibration_batch/calibration_summary.csv`

| Sistema | Archivo Fuente (`01_orca_quantum/calibration_batch/`) | $E_{\text{tot}}$ (Eh) | $\Delta E_{\text{ads}}$ (eV) | $\Delta E_{\text{disp}}$ (eV) | Resto no-disp (eV) | Convergido | Ciclos | $g_{\max}$ (Eh/bohr) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dímero Adamantilo (Eclipsado)** | `cal_a_dimero_eclipsado.out` | -779.86588422 | -3.5621 | -0.5696 | -2.9925 | **SÍ** | 9 | $2.92 \times 10^{-4}$ |
| **Dímero Adamantilo (Alternado)** | `cal_a_dimero_alternado.out` | -779.86588449 | -3.5621 | -0.5696 | -2.9925 | **SÍ** | 14 | $1.35 \times 10^{-4}$ |
| **$\text{CH}_3$ + Terraza Plana** | `cal_b_CH3_terraza.out` | -1288.26952803 | -3.6881 | -0.4178 | -3.2702 | **SÍ** | 13 | $3.67 \times 10^{-5}$ |
| **$\text{CH}_3$ Radical Libre** | `cal_b_CH3_radical.out` | -39.81881768 | — | -0.0051 | — | **SÍ** | 4 | $8.82 \times 10^{-6}$ |
| **Adamantilo + Terraza (BS 1,1)** | `02_flat_terrace_plus_adamantyl_BS.out` | -1638.25291235 | -1.8090 | -1.0186 | -0.7904 | **SÍ** | 28 | $1.37 \times 10^{-4}$ |
| **RKS SP sobre Complejo BS** | `cal_c_complejo_RKS_SP.out` | -1638.25291230 | — | — | — | SP | 0 | — |

- **Estabilidad de capa cerrada en complejo adamantilo/terraza:** $\Delta E(\text{RKS SP} - \text{BS opt}) = \mathbf{+0.00000\,\text{eV}}$ (la solución BS colapsó a singlete de capa cerrada puro).

