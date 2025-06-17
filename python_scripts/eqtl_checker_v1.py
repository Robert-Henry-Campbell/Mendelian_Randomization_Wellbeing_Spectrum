import argparse
from pathlib import Path
import pandas as pd

from gwas.eqtl_checker import fetch_snp_info


def main(base_dir: Path) -> None:
    gtex_dir = base_dir / "data" / "raw" / "GTEX_BRAIN_ONLY"
    gwas_dir = base_dir / "data" / "raw" / "GWAS_hits"
    output_dir = base_dir / "data" / "processed" / "output"

    gtex_files = [f.name for f in gtex_dir.iterdir() if f.is_file()]
    gwas_files = [f.name for f in gwas_dir.iterdir() if f.is_file()]

    for gwas_file in gwas_files:
        for gtex_file in gtex_files:
            gtex_df = pd.read_csv(gtex_dir / gtex_file, sep="\t")
            gwas_df = pd.read_csv(gwas_dir / gwas_file, sep=",")

            gwas_df["variant_id"] = gwas_df["RS"].apply(lambda rs: fetch_snp_info(rs, gwas_df))

            gwas_eqtls = pd.merge(gwas_df, gtex_df, on="variant_id", how="inner")

            print(f"{gtex_file}|eQTLs_df size: {gwas_eqtls.shape[0]}")
            out_file = output_dir / f"{gwas_file} {gtex_file}eQTLs_.csv"
            gwas_eqtls.to_csv(out_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check eQTL overlap with GWAS hits")
    parser.add_argument("--base-dir", type=Path, default=Path.cwd(), help="Base directory containing data folders")
    args = parser.parse_args()
    main(args.base_dir)
