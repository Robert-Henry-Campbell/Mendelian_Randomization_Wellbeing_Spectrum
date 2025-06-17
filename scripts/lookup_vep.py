#!/usr/bin/env python3
"""Query Ensembl VEP for a list of SNP IDs."""
import argparse
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "src"))

from gwas.vep_utils import get_vep_data, parse_vep_results


def main():
    parser = argparse.ArgumentParser(description="Query Ensembl VEP for SNPs")
    parser.add_argument("snp_file", help="File containing SNP IDs, one per line")
    parser.add_argument(
        "--output",
        help="Output CSV path (default: $DATA_DIR/vep_results.csv)",
        default=None,
    )
    args = parser.parse_args()

    with open(args.snp_file) as handle:
        snps = [line.strip() for line in handle if line.strip()]

    results = get_vep_data(snps)
    df = parse_vep_results(results)

    out_dir = Path(os.environ.get("DATA_DIR", BASE_DIR))
    output_path = Path(args.output) if args.output else out_dir / "vep_results.csv"

    df.to_csv(output_path, index=False)
    print(f"Results written to {output_path}")


if __name__ == "__main__":
    main()
