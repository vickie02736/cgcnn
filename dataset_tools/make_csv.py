import os
import pandas as pd
from pymatgen.io.cif import CifParser
from pymatgen.core.structure import Structure

# Specify the directory path
directory_path = '/home/uceckz0/Scratch/CSD_non_disordered'

# List to hold file names without extensions
file_names = []

# Read all file names in the directory
for file_name in os.listdir(directory_path):
    if file_name.endswith(".cif"):
            name, _ = os.path.splitext(file_name)
            file_names.append(name)
    else:
        pass

# Convert the list to a DataFrame
df = pd.DataFrame(file_names)

df['Zero Column']=0.0

csv_file_path = '/home/uceckz0/Scratch/CSD_non_disordered/band_gap/test.csv'
df.to_csv(csv_file_path, index=False, header=False)