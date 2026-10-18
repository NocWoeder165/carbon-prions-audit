# ==============================================================================
# PROYECTO THAROS - PROTOCOLO CUÁNTICO CON AUDITORÍA ESTRICTA DE CONVERGENCIA
# ==============================================================================
# Mejoras implementadas tras revisión técnica independiente:
# 1. Dispersión D3 (Grimme) estrictamente obligatoria (sin fallback silencioso).
# 2. Rotación Rodrigues-Householder en SO(3) libre de singularidad a 180° (c -> -1).
# 3. Verificación explícita de convergencia BFGS (converged=True y registro de F_max).
# 4. Estequiometría exacta en todas las etiquetas: C20H30 (50 átomos),
#    C19BH29 (49 átomos) y C19PH29 (49 átomos).
# 5. Exportación automática de coordenadas .xyz puras, tabla CSV de energías/fuerzas
#    y metadatos JSON en un único paquete ZIP verificable.
# ==============================================================================

import os
import sys
import subprocess

# Instalación automática de dependencias cuánticas si la sesión de Colab se reinició
try:
    import ase
    import mace
    import torch_dftd
except ImportError:
    print("[*] Instalando dependencias cuánticas (ASE, MACE-MP-0, torch-dftd)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "ase", "mace-torch", "torch-dftd"])
    print("[+] Dependencias listas.")

os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

import json
import csv
import zipfile
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import torch
import ase
from ase.io import read
from ase.optimize import BFGS
from ase.constraints import FixBondLength
from ase.visualize.plot import plot_atoms
import mace
from mace.calculators import mace_mp

print("[*] Verificando entorno y cargando potencial MACE-MP-0 + D3 obligatorio...")
print(f"    -> PyTorch version: {torch.__version__}")
print(f"    -> ASE version:     {ase.__version__}")
print(f"    -> MACE version:    {getattr(mace, '__version__', 'installed')}")

# 1. Inicialización estricta con dispersión D3 obligatoria (sin fallback silencioso)
calc = mace_mp(model="small", dispersion=True, default_dtype="float64")
print("[+] Calculadora MACE-MP-0 + TorchDFTD3 inicializada en float64.")

# Descargar Adamantano auténtico (PubChem CID 9238 = C10H16)
url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/9238/record/SDF/?record_type=3d"
sdf_file = "adamantane_cid9238.sdf"
if not os.path.exists(sdf_file):
    urllib.request.urlretrieve(url, sdf_file)

mol_base = read(sdf_file)


def rotar_vector_a_eje(pos, centro, vec_origen, vec_destino):
    """
    Rota coordenadas 3D en SO(3) alrededor de 'centro' para alinear 'vec_origen'
    con 'vec_destino', manejando analíticamente el caso antiparalelo de 180° (c -> -1).
    """
    u = vec_origen / np.linalg.norm(vec_origen)
    t = vec_destino / np.linalg.norm(vec_destino)
    c = float(np.dot(u, t))
    if c > 1.0 - 1e-10:
        return pos.copy()
    if c < -1.0 + 1e-10:
        # Rotación propia de 180° (det = +1) alrededor de un eje ortogonal a u
        perp = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        axis = np.cross(u, perp)
        axis /= np.linalg.norm(axis)
        rot_mat = -np.eye(3) + 2.0 * np.outer(axis, axis)
        return (pos - centro) @ rot_mat.T + centro
    v = np.cross(u, t)
    s = np.linalg.norm(v)
    vx = np.array([[0.0, -v[2], v[1]], [v[2], 0.0, -v[0]], [-v[1], v[0], 0.0]])
    rot_mat = np.eye(3) + vx + (vx @ vx) * ((1.0 - c) / (s ** 2))
    return (pos - centro) @ rot_mat.T + centro


def obtener_fmax(atoms):
    """Calcula la fuerza atómica residual máxima (eV/Å) sin restricciones."""
    forces = atoms.get_forces()
    return float(np.max(np.linalg.norm(forces, axis=1)))


def guardar_xyz_puro(nombre_archivo, atoms, comentario=""):
    """Exporta coordenadas atómicas en formato estándar XYZ puro."""
    simbolos = atoms.get_chemical_symbols()
    pos = atoms.get_positions()
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"{len(simbolos)}\n")
        f.write(f"{comentario}\n")
        for s, (x, y, z) in zip(simbolos, pos):
            f.write(f"{s:<2}  {x:14.8f}  {y:14.8f}  {z:14.8f}\n")


def construir_monomero_quimicamente_valido(mol_input, dopante=None, invertir_z=False):
    mol = mol_input.copy()
    mol.translate(-mol.get_center_of_mass())
    pos = mol.get_positions()
    symbols = np.array(mol.get_chemical_symbols())

    c_idx = np.where(symbols == 'C')[0]
    h_idx = np.where(symbols == 'H')[0]

    # Identificar los 4 sitios cabeza de puente (C unido a 1 solo H)
    bridgehead_c, bridgehead_h = [], []
    for ci in c_idx:
        dists = np.linalg.norm(pos[h_idx] - pos[ci], axis=1)
        conectados = h_idx[dists < 1.25]
        if len(conectados) == 1:
            bridgehead_c.append(ci)
            bridgehead_h.append(conectados[0])

    c_rad_orig = bridgehead_c[0]
    h_rad_orig = bridgehead_h[0]

    # Pre-orientar el eje C_rad -> H_rad hacia +Z
    vec_ch = pos[h_rad_orig] - pos[c_rad_orig]
    mol.set_positions(rotar_vector_a_eje(pos, np.zeros(3), vec_ch, np.array([0.0, 0.0, 1.0])))

    # Marcar con tag=99 el carbono cabeza de puente que tendrá el radical
    tags = np.zeros(len(mol), dtype=int)
    tags[c_rad_orig] = 99
    mol.set_tags(tags)

    h_a_eliminar = [h_rad_orig]

    # Sustitución isomórfica trivalente neutra (B o P) sin H terminal espurio
    if dopante in ['B', 'P']:
        c_dop_orig = bridgehead_c[1]
        h_dop_orig = bridgehead_h[1]
        syms = mol.get_chemical_symbols()
        syms[c_dop_orig] = dopante
        mol.set_chemical_symbols(syms)
        h_a_eliminar.append(h_dop_orig)

    for h_del in sorted(h_a_eliminar, reverse=True):
        del mol[h_del]

    idx_radical = int(np.where(mol.get_tags() == 99)[0][0])

    # Relajar el monómero aislado verificando convergencia estricta
    mol.set_cell([20.0, 20.0, 20.0])
    mol.center()
    mol.calc = calc
    opt_mono = BFGS(mol, logfile=None)
    conv_mono = bool(opt_mono.run(fmax=0.02, steps=250))
    fmax_mono = obtener_fmax(mol)
    e_monomero_relajado = float(mol.get_potential_energy())

    if not conv_mono:
        print(f"   [!] Advertencia: Monómero (dopante={dopante}) alcanzó límite de pasos con F_max={fmax_mono:.4f} eV/Å")

    # Orientar el vector (centro_de_masa -> carbono_radical) hacia +Z (o -Z si invertir_z=True)
    pos = mol.get_positions()
    com = mol.get_center_of_mass()
    vec_rad = pos[idx_radical] - com
    target_axis = np.array([0.0, 0.0, -1.0 if invertir_z else 1.0])
    mol.set_positions(rotar_vector_a_eje(pos, com, vec_rad, target_axis))

    # Rotar 60° en Z el segundo fragmento para conformación alternada (staggered)
    if invertir_z:
        theta = np.deg2rad(60.0)
        rz = np.array([[np.cos(theta), -np.sin(theta), 0.0],
                       [np.sin(theta),  np.cos(theta), 0.0],
                       [0.0,            0.0,           1.0]])
        mol.set_positions(mol.get_positions() @ rz.T)

    # Ubicar el carbono radical exactamente en el origen (0, 0, 0)
    pos = mol.get_positions()
    mol.translate(-pos[idx_radical])

    # Verificar explícitamente que la cola de la jaula apunte en la dirección correcta
    z_com_final = mol.get_center_of_mass()[2]
    if not invertir_z and z_com_final >= 0.0:
        raise RuntimeError("Error geométrico: La jaula 1 no quedó en el semiespacio Z < 0.")
    if invertir_z and z_com_final <= 0.0:
        raise RuntimeError("Error geométrico: La jaula 2 no quedó en el semiespacio Z > 0.")

    return mol, idx_radical, e_monomero_relajado, conv_mono, fmax_mono


def ejecutar_escaneo_relajado(dopante=None, nombre="Intrínseco"):
    print(f"\n=======================================================")
    print(f" ESCANEO RELAJADO AUDITADO: {nombre}")
    print(f"=======================================================")
    frag1, idx1, e1, conv1, fmax1 = construir_monomero_quimicamente_valido(mol_base, dopante=None, invertir_z=False)
    frag2, idx2_local, e2, conv2, fmax2 = construir_monomero_quimicamente_valido(mol_base, dopante=dopante, invertir_z=True)
    n1 = len(frag1)
    idx2 = n1 + idx2_local
    e_infinito = e1 + e2

    print(f" -> Monómero 1 ({frag1.get_chemical_formula()}): E = {e1:.4f} eV | F_max = {fmax1:.4f} eV/Å | Conv = {conv1}")
    print(f" -> Monómero 2 ({frag2.get_chemical_formula()}): E = {e2:.4f} eV | F_max = {fmax2:.4f} eV/Å | Conv = {conv2}")

    distancias = np.linspace(3.40, 1.48, 13)
    energias_rel = []
    registros_scan = []

    f2_init = frag2.copy()
    f2_init.translate([0.0, 0.0, distancias[0]])
    sistema = frag1.copy() + f2_init
    sistema.set_cell([24.0, 24.0, 24.0])
    sistema.center()
    sistema.calc = calc

    for d_obj in distancias:
        sistema.set_constraint()
        pos = sistema.get_positions()
        vec_12 = pos[idx2] - pos[idx1]
        d_actual = np.linalg.norm(vec_12)
        u_12 = vec_12 / d_actual
        pos[n1:] += (d_obj - d_actual) * u_12
        sistema.set_positions(pos)

        sistema.set_constraint(FixBondLength(idx1, idx2))
        opt_step = BFGS(sistema, logfile=None)
        conv_step = bool(opt_step.run(fmax=0.05, steps=200))
        fmax_step = float(np.max(np.linalg.norm(sistema.get_forces(), axis=1)))
        d_medida = float(sistema.get_distance(idx1, idx2))
        e_tot = float(sistema.get_potential_energy())
        e_actual = e_tot - e_infinito
        energias_rel.append(e_actual)

        registros_scan.append({
            "sistema": nombre,
            "formula": sistema.get_chemical_formula(),
            "d_objetivo_A": round(float(d_obj), 4),
            "d_medida_A": round(d_medida, 6),
            "E_total_eV": round(e_tot, 6),
            "dE_rel_eV": round(e_actual, 6),
            "Fmax_restringida_eV_A": round(fmax_step, 5),
            "converged": conv_step,
            "n_steps": int(opt_step.get_number_of_steps())
        })
        print(f"   [Scan] d_C-C = {d_medida:.3f} Å | ΔE = {e_actual:+.3f} eV | F_max = {fmax_step:.4f} eV/Å | Conv = {conv_step} ({opt_step.get_number_of_steps()} pasos)")

    energias_rel = np.array(energias_rel)

    # Relajación libre en el pozo covalente (cero restricciones)
    dimero_unido = sistema.copy()
    dimero_unido.set_constraint()
    dimero_unido.calc = calc
    opt_libre = BFGS(dimero_unido, logfile=None)
    conv_libre = bool(opt_libre.run(fmax=0.02, steps=300))
    fmax_libre = obtener_fmax(dimero_unido)

    d_eq_libre = float(dimero_unido.get_distance(idx1, idx2))
    e_tot_libre = float(dimero_unido.get_potential_energy())
    e_enlace_real = e_tot_libre - e_infinito

    idx_barrera = int(np.argmax(energias_rel[:8]))
    d_ts = float(distancias[idx_barrera])
    ea_aparente = float(max(0.0, energias_rel[idx_barrera] - energias_rel[0]))

    print(f" -------------------------------------------------------")
    print(f" -> Fórmula exacta del dímero:          {dimero_unido.get_chemical_formula()} ({len(dimero_unido)} átomos)")
    print(f" -> Barrera aparente del barrido (Ea):  {ea_aparente:.3f} eV (en d = {d_ts:.2f} Å)")
    print(f" -> Distancia C-C libre en el pozo:     {d_eq_libre:.3f} Å (Exp. 1,1'-biadamantilo: 1.578 Å)")
    print(f" -> Energía de enlace covalente (ΔE):   {e_enlace_real:+.3f} eV (vs radicales separados)")
    print(f" -> Convergencia relajación libre:      {conv_libre} (F_max = {fmax_libre:.4f} eV/Å en {opt_libre.get_number_of_steps()} pasos)")

    info_extra = {
        "formula": dimero_unido.get_chemical_formula(),
        "natoms": len(dimero_unido),
        "idx1": int(idx1),
        "idx2": int(idx2),
        "e_infinito_eV": round(e_infinito, 6),
        "d_eq_libre_A": round(d_eq_libre, 6),
        "dE_enlace_eV": round(e_enlace_real, 6),
        "Ea_aparente_eV": round(ea_aparente, 6),
        "d_max_barrera_A": round(d_ts, 4),
        "fmax_libre_eV_A": round(fmax_libre, 6),
        "converged_libre": conv_libre,
        "frag1": frag1,
        "frag2": frag2,
        "registros_scan": registros_scan
    }

    return distancias, energias_rel, d_eq_libre, e_enlace_real, ea_aparente, dimero_unido, info_extra


res_cc = ejecutar_escaneo_relajado(None, "Intrínseco: 1,1'-Biadamantilo (C20H30)")
res_cb = ejecutar_escaneo_relajado('B', "Sustituido con Boro: Bora-biadamantilo neutro (C19BH29)")
res_cp = ejecutar_escaneo_relajado('P', "Sustituido con Fósforo: Fosfa-biadamantilo neutro (C19PH29)")

# ==============================================================================
# GENERACIÓN DE FIGURA 1 CON FÓRMULAS ESTEQUIOMÉTRICAS CORREGIDAS (C19BH29 / C19PH29)
# ==============================================================================
fig = plt.figure(figsize=(16, 10), dpi=150)
ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=3)

for (dists, e_rel, d_eq, e_bind, ea, _, _), color, marker, label in [
    (res_cc, '#1f77b4', 'o-', 'Intrínseco (C20H30)'),
    (res_cb, '#2ca02c', 's--', 'Bora-biadamantilo (C19BH29)'),
    (res_cp, '#d62728', '^-.', 'Fosfa-biadamantilo (C19PH29)')
]:
    ax1.plot(dists, e_rel, marker, color=color, lw=2.5, markersize=7,
             label=f"{label} | d_eq libre = {d_eq:.3f} Å | ΔE_enlace = {e_bind:+.2f} eV | Ea_app = {ea:.3f} eV")

ax1.axvline(1.578, color='purple', linestyle='--', lw=1.5, label='Enlace C–C Exp. 1,1\'-Biadamantilo (1.578 Å)')
ax1.axvline(1.540, color='gray', linestyle=':', lw=1.5, label='Enlace C–C Diamante Bulk (1.540 Å)')
ax1.axhline(0.0, color='black', lw=0.8, label='Cero Termodinámico: 2 Radicales Aislados Relajados')
ax1.invert_xaxis()
ax1.set_xlabel('Distancia C–C Restringida (Å) [Escaneo Relajado (FixBondLength) →]', fontsize=12, fontweight='bold')
ax1.set_ylabel('Energía de Interacción Relajada ΔE (eV)', fontsize=12, fontweight='bold')
ax1.set_title('Curva de Energía Potencial Relajada Auditada (C20H30, C19BH29 y C19PH29)', fontsize=13.5, fontweight='bold')
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, alpha=0.3)

for idx, (res, titulo) in enumerate([
    (res_cc, '1,1\'-Biadamantilo (C20H30)'),
    (res_cb, 'Bora-biadamantilo (C19BH29)'),
    (res_cp, 'Fosfa-biadamantilo (C19PH29)')
]):
    ax = plt.subplot2grid((2, 3), (1, idx))
    plot_atoms(res[5], ax, rotation='30x,45y,0z')
    ax.set_title(f"{titulo}\n(d_eq = {res[2]:.3f} Å, ΔE = {res[3]:+.2f} eV)", fontsize=11, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.savefig('figura1_relaxed_pes_auditada.png', dpi=300)
plt.show()

# ==============================================================================
# EXPORTACIÓN DE COORDENADAS .XYZ, TABLA CSV Y METADATOS JSON PARA AUDITORÍA
# ==============================================================================
guardar_xyz_puro(
    "monomer_adamantane_radical.xyz",
    res_cc[6]["frag1"],
    f"Formula={res_cc[6]['frag1'].get_chemical_formula()} | MACE-MP-0+D3 float64 relaxed"
)
guardar_xyz_puro(
    "monomer_bora_adamantane_radical.xyz",
    res_cb[6]["frag2"],
    f"Formula={res_cb[6]['frag2'].get_chemical_formula()} | MACE-MP-0+D3 float64 relaxed"
)
guardar_xyz_puro(
    "monomer_phospha_adamantane_radical.xyz",
    res_cp[6]["frag2"],
    f"Formula={res_cp[6]['frag2'].get_chemical_formula()} | MACE-MP-0+D3 float64 relaxed"
)

for nombre_xyz, res in [
    ("dimer_biadamantyl_relaxed.xyz", res_cc),
    ("dimer_bora_biadamantyl_relaxed.xyz", res_cb),
    ("dimer_phospha_biadamantyl_relaxed.xyz", res_cp)
]:
    info = res[6]
    comentario = (
        f"Formula={info['formula']} | idx_enlace=({info['idx1']},{info['idx2']}) | "
        f"d_eq_medida={info['d_eq_libre_A']:.4f}_A | dE_enlace={info['dE_enlace_eV']:+.4f}_eV | "
        f"Fmax={info['fmax_libre_eV_A']:.5f}_eV/A | converged={info['converged_libre']}"
    )
    guardar_xyz_puro(nombre_xyz, res[5], comentario)

# Guardar CSV con todos los puntos del barrido
csv_file = "datos_crudos_pes_auditoria.csv"
todos_registros = res_cc[6]["registros_scan"] + res_cb[6]["registros_scan"] + res_cp[6]["registros_scan"]
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(todos_registros[0].keys()))
    writer.writeheader()
    writer.writerows(todos_registros)

# Guardar resumen JSON
json_file = "resumen_metricas_auditoria.json"
resumen_json = {
    "entorno": {
        "torch_version": torch.__version__,
        "ase_version": ase.__version__,
        "mace_version": getattr(mace, "__version__", "installed"),
        "precision": "float64",
        "dispersion_d3": True
    },
    "sistemas": {
        "C20H30": {k: v for k, v in res_cc[6].items() if k not in ("frag1", "frag2", "registros_scan")},
        "C19BH29": {k: v for k, v in res_cb[6].items() if k not in ("frag1", "frag2", "registros_scan")},
        "C19PH29": {k: v for k, v in res_cp[6].items() if k not in ("frag1", "frag2", "registros_scan")},
    }
}
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(resumen_json, f, indent=2, ensure_ascii=False)

archivos_empaquetar = [
    "monomer_adamantane_radical.xyz",
    "monomer_bora_adamantane_radical.xyz",
    "monomer_phospha_adamantane_radical.xyz",
    "dimer_biadamantyl_relaxed.xyz",
    "dimer_bora_biadamantyl_relaxed.xyz",
    "dimer_phospha_biadamantyl_relaxed.xyz",
    csv_file,
    json_file,
    "figura1_relaxed_pes_auditada.png"
]

zip_filename = "paquete_auditoria_priones.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for f in archivos_empaquetar:
        if os.path.exists(f):
            zipf.write(f)

print(f"\n[+] Paquete completo generado: {zip_filename}")
try:
    from google.colab import files
    files.download(zip_filename)
except ImportError:
    pass
