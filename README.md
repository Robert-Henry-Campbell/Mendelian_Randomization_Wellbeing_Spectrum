# Mendelian Randomization Wellbeing Spectrum

This repository collects scripts and data used for exploring GWAS hits and eQTL effects within the wellbeing spectrum.

Raw data files are stored under `data/raw/` while generated results are written
to `data/processed/`. For example, the `GWAS_hits` and `GTEX_BRAIN_ONLY`
directories now live under `data/raw/`.

## Command line utilities

The `scripts/` directory contains small command line tools. Each script accepts arguments and can also read default locations from the `DATA_DIR` environment variable.

- **check_eqtl.py** – look up a GTEx formatted variant ID for an `rsID`.

  ```bash
  DATA_DIR=/path/to/data ./scripts/check_eqtl.py rs123 --gwas-file my_gwas.csv
  ```

- **lookup_vep.py** – query the Ensembl VEP API for a list of SNP IDs.

  ```bash
  ./scripts/lookup_vep.py snps.txt --output results.csv
  ```

Set `DATA_DIR` to control the default output/input directories.
