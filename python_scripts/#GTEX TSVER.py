#GTEX TSVER 
import os

os.chdir("C:\\Users\\username\\OneDrive - Imperial College London\\Documents\\0Oxford_main\\fergus paper\\code_main")
directory_path = 'GTEX_BRAIN_ONLY'


# Loop through each file in the directory
for filename in os.listdir(directory_path):
    # Construct full file path
    old_file = os.path.join(directory_path, filename)
    
    # Check if it's a file
    if os.path.isfile(old_file):
        # Create new file path with .tsv extension
        new_file = os.path.splitext(old_file)[0] + '.tsv'
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f"Renamed '{old_file}' to '{new_file}'")

print('applesauce')