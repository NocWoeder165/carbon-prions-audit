import os
import math
from check_mace_vs_c3_geometry import read_xyz, write_xyz, align_monomer_c3
from generate_ts_inputs import make_frag2_from_frag1, combine_at_distance

base_dir = r"C:\Users\Leo\Desktop\Priones de carbono\dft_orca_validation"

# 1. Option B: C3-aligned coaxial geometries from UKS B97-3c optimized monomers
f1_b_cc = align_monomer_c3(read_xyz(os.path.join(base_dir, "audit_opt_mono_C10H15.xyz")), invert_z=False)
f2_b_cc = align_monomer_c3(read_xyz(os.path.join(base_dir, "audit_opt_mono_C10H15.xyz")), invert_z=True)
f2_b_cb = align_monomer_c3(read_xyz(os.path.join(base_dir, "audit_opt_mono_C9BH14.xyz")), invert_z=True)
f2_b_cp = align_monomer_c3(read_xyz(os.path.join(base_dir, "audit_opt_mono_C9PH14.xyz")), invert_z=True)

dists_B = [3.40, 2.92, 2.60, 2.44, 2.12]
for code, f2 in [("C20H30", f2_b_cc), ("C19H29B", f2_b_cb), ("C19H29P", f2_b_cp)]:
    for d in dists_B:
        tag = f"{int(round(d*100)):03d}"
        xyz_name = f"optB_{code}_{tag}.xyz"
        atoms = combine_at_distance(f1_b_cc, f2, d)
        write_xyz(os.path.join(base_dir, xyz_name), atoms, f"OptionB UKS-B97-3c C3 coaxial {code} d={d:.2f}A")
        inp_name = f"optB_{code}_{tag}.inp"
        with open(os.path.join(base_dir, inp_name), "w", encoding="utf-8") as f:
            f.write(f"""! UKS wB97X-D3 def2-SVP def2/J RIJCOSX TightSCF NoPop

%pal
  nprocs 12
end

%maxcore 2000

%scf
  BrokenSym 1,1
  MaxIter 200
end

* xyzfile 0 1 {xyz_name}
""")

# 2. Option A: Create .inp files for d = 2.92, 2.60, 2.44, 2.12 A (d=3.40 A is already in vdw_*.out!)
f1_a_cc = read_xyz(os.path.join(base_dir, "monomer_adamantane_radical.xyz"))
f2_a_cc = make_frag2_from_frag1(f1_a_cc)
f2_a_cb = read_xyz(os.path.join(base_dir, "monomer_bora_adamantane_radical.xyz"))
f2_a_cp = read_xyz(os.path.join(base_dir, "monomer_phospha_adamantane_radical.xyz"))

dists_A = [2.92, 2.60, 2.44, 2.12]
for code, f2 in [("C20H30", f2_a_cc), ("C19H29B", f2_a_cb), ("C19H29P", f2_a_cp)]:
    for d in dists_A:
        tag = f"{int(round(d*100)):03d}"
        xyz_name = f"optA_{code}_{tag}.xyz"
        xyz_path = os.path.join(base_dir, xyz_name)
        if not os.path.exists(xyz_path):
            atoms = combine_at_distance(f1_a_cc, f2, d)
            write_xyz(xyz_path, atoms, f"OptionA MACE coaxial {code} d={d:.2f}A")
        inp_name = f"optA_{code}_{tag}.inp"
        with open(os.path.join(base_dir, inp_name), "w", encoding="utf-8") as f:
            f.write(f"""! UKS wB97X-D3 def2-SVP def2/J RIJCOSX TightSCF NoPop

%pal
  nprocs 12
end

%maxcore 2000

%scf
  BrokenSym 1,1
  MaxIter 200
end

* xyzfile 0 1 {xyz_name}
""")

print("All Option A and Option B .xyz and .inp files ready.")
