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

## R analysis

R scripts live in `src/r_scripts/`. They can be executed with `Rscript` and typically
expect the analysis directory as the first argument.

```bash
Rscript src/r_scripts/gene_ontology_mapper_v1.0.0.R /path/to/analysis_dir
```

A minimal package skeleton in the `R/` directory provides a place for shared
functions (`DESCRIPTION` and `NAMESPACE`).
