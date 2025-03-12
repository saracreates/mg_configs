import os
import re

directory = "/afs/cern.ch/work/s/saaumill/public/MG5_aMC_v3_5_7/zha/Events"
output_file = "xsec-vs-energy.csv"
pattern = re.compile(r"#  Integrated weight \(pb\)  :\s+([\d.eE+-]+)")

results = []

for folder in sorted(os.listdir(directory)):
    if folder.startswith("run_") and folder.endswith("GeV"):
        energy = folder[4:-3]  # Extract energy from folder name
        file_path = os.path.join(directory, folder, f"run_{energy}GeV_tag_1_banner.txt")
        
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    match = pattern.search(line)
                    if match:
                        weight = match.group(1)
                        results.append(f"{energy}, {weight}")
                        break  # Stop after finding the first match

with open(output_file, "w") as out_file:
    out_file.write("Energy (GeV), Cross section (pb)\n")
    out_file.write("\n".join(results))

print(f"Extracted data saved to {output_file}")
