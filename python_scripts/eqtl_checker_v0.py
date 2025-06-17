import argparse
from pathlib import Path
import pandas as pd
import requests


def fetch_snp_info(rs_id: str, gwas_df: pd.DataFrame) -> str:
    url = f"https://clinicaltables.nlm.nih.gov/api/snps/v3/search?terms={rs_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    chromosome = data[3][0][1]
    position = str(int(data[3][0][2]) + 1)
    allele_change = data[3][0][3]

    if len(allele_change) != 3:
        mutations = [m.strip() for m in allele_change.split(',')]
        index = gwas_df.index[gwas_df['RS'] == rs_id].tolist()
        if len(index) != 1:
            raise ValueError("Unable to find unique index for rs_id")
        proposed = f"{gwas_df['A2'].loc[index[0]]}/{gwas_df['A1'].loc[index[0]]}"
        if proposed in mutations:
            allele_change = proposed
        else:
            raise ValueError("Proposed allele change not in returned mutations")

    return f"chr{chromosome}_{position}_{allele_change[0]}_{allele_change[-1]}_b38"


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
