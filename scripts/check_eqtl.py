#!/usr/bin/env python3
"""Lookup a GTEx-style variant ID for a SNP."""
import argparse
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "src"))

import pandas as pd
from gwas.eqtl_checker import fetch_snp_info


def main():
    parser = argparse.ArgumentParser(description="Lookup GTEx-style variant ID for a given rsID")
    parser.add_argument("rsid", help="rsID to look up")
    parser.add_argument(
        "--gwas-file",
        help="Path to GWAS summary statistics (default: $DATA_DIR/gwas.csv)",
        default=None,
    )
    args = parser.parse_args()

    data_dir = Path(os.environ.get("DATA_DIR", BASE_DIR))
    gwas_path = Path(args.gwas_file) if args.gwas_file else data_dir / "gwas.csv"

    gwas_df = pd.read_csv(gwas_path)
    variant = fetch_snp_info(args.rsid, gwas_df)
    print(variant)


if __name__ == "__main__":
    main()
