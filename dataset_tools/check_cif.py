import os
import sys
import pandas as pd
from pymatgen.io.cif import CifParser
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_cif_file(directory, filename):
    if filename.endswith(".cif"):
        file_path = os.path.join(directory, filename)
        try:
            parser = CifParser(file_path)
            structures = parser.get_structures()
            if structures:
                return {'Filename': filename, 'Status': 'Valid with structures', 'Error Message': ''}
            else:
                return {'Filename': filename, 'Status': 'Valid but no structures', 'Error Message': ''}
        except Exception as e:
            return {'Filename': filename, 'Status': 'Invalid CIF file', 'Error Message': str(e)}

def check_cif_files_parallel(directory):
    results = []
    with ThreadPoolExecutor() as executor:
        # Create a future for each file
        futures = [executor.submit(process_cif_file, directory, filename) for filename in os.listdir(directory)]
        # Wait for the futures to complete
        for future in as_completed(futures):
            results.append(future.result())
    return results

# Specify the directory containing your CIF files
directory = '/home/uceckz0/Scratch/CSD_non_disordered'
results = check_cif_files_parallel(directory)

# Convert results to a DataFrame and save to CSV
df = pd.DataFrame(results)
df.to_csv("CSD_non_disordered_status.csv", index=False)

# Filter and print filenames of valid CIF files with structures
valid_files = df[df['Status'] == 'Valid with structures']['Filename']
valid_files.to_csv("CSD_non_disordered_valid_cif_files.csv", index=False)
print("Valid CIF files with structures:")
print(valid_files)

if __name__ == "__main__":
    file_index = sys.argv[1]
    process_cif_file(file_index)