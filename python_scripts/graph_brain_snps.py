import pandas as pd
from pathlib import Path


brain_eqtl_directory = 'Mendelian_Randomization_Wellbeing_Spectrum\data\processed\output'

#gather filtered snps 
filtered_snps = pd.read_csv('Mendelian_Randomization_Wellbeing_Spectrum\data\processed\\filtered_SNPs\dep_brain_snps.csv')
print(filtered_snps.columns)
# gather brain region csvs

## gather up a list of all files startin with 'Indep. Signals AVG DS.*'
unfiltered_region_snps = {}
for file in Path(brain_eqtl_directory).glob('Indep. Signals AVG DS.*'):
    if file.is_file() and file.suffix == '.csv':
        print(f'found file {file.name}')
        unfiltered_region_snps[file.name] = pd.read_csv(file)

# for each region df, return filtered df of only filtered snps in that df
filtered_region_snps = {}
filtered_region_snps_for_df = {}
for idx,region in enumerate(unfiltered_region_snps.keys()):
    filtered_region_snps[f'{region}_filtered'] = set(unfiltered_region_snps[region]['RS']).intersection(set(filtered_snps['x']))
    filtered_region_snps_for_df[f'{region}_filtered'] = list(set(unfiltered_region_snps[region]['RS']).intersection(set(filtered_snps['x'])))

#pad the lists to make coherent df
max_len = max(len(lst) for lst in filtered_region_snps_for_df.values())
for key in filtered_region_snps_for_df:
    filtered_region_snps_for_df[key] += [None] * (max_len - len(filtered_region_snps_for_df[key]))

filtered_region_snps_df = pd.DataFrame(filtered_region_snps_for_df)
filtered_region_snps_df.to_csv('Mendelian_Randomization_Wellbeing_Spectrum\data\processed\\brain_region_filter\\filtered_region_SNPs.csv')


filtered_region_snps_count = {}
for idx,region in enumerate(filtered_region_snps.keys()):
    region_count = [len(filtered_region_snps[region])]
    filtered_region_snps_count[region] = region_count
filtered_count_df = pd.DataFrame(filtered_region_snps_count)
filtered_count_df.to_csv('Mendelian_Randomization_Wellbeing_Spectrum\data\processed\\brain_region_filter\\filtered_count.csv')

unfiltered_region_snps_count = {}
for idx, region in enumerate(unfiltered_region_snps.keys()):
    region_count = [len(unfiltered_region_snps[region]['RS'])]
    unfiltered_region_snps_count[region] = region_count
unfiltered_count_df = pd.DataFrame(unfiltered_region_snps_count)
unfiltered_count_df.to_csv('Mendelian_Randomization_Wellbeing_Spectrum\data\processed\\brain_region_filter\\unfiltered_count.csv')

#graph in blue a bar chart of filtered and unfiltered snp count by brain region
combined_df = pd.read_csv('Mendelian_Randomization_Wellbeing_Spectrum\data\processed\\brain_region_filter\\combined_count.csv')
combined_df.head()

import matplotlib.pyplot as plt
import numpy as np

# Set up positions
labels = combined_df['brain_region']
x = np.arange(len(labels))  # label positions
width = 0.35  # width of each bar

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Bar plots: before and after QC
bars1 = ax.bar(x - width/2, combined_df['snps_before_qc'], width, label='Before QC', color='steelblue')
bars2 = ax.bar(x + width/2, combined_df['snps_after_qc'], width, label='After QC', color='skyblue')

# Labels and formatting
ax.set_ylabel('SNP Count')
ax.set_xlabel('Brain Region')
ax.set_title('SNP Counts by Brain Region (Before and After QC)')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend()

# Improve layout
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# combined_df must already contain: brain_region / snps_before_qc / snps_after_qc
labels = combined_df["brain_region"]
x = np.arange(len(labels))          # X positions
width = 0.35                        # bar thickness

fig, ax = plt.subplots(figsize=(12, 6))

# Bars
ax.bar(x - width/2, combined_df["snps_before_qc"],
       width, label="Before QC", color="steelblue")
ax.bar(x + width/2, combined_df["snps_after_qc"],
       width, label="After QC",  color="skyblue")

# Axis formatting
ax.set_yscale("log")                # logarithmic Y-axis
ax.set_ylim(bottom=1)               # start at 1 so log scale is valid
ax.set_ylabel("SNP Count (log scale)")
ax.set_xlabel("Brain Region")
ax.set_title("SNP Counts by Brain Region (Before vs. After QC, Log Scale)")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.legend()

plt.tight_layout()
plt.show()



pass