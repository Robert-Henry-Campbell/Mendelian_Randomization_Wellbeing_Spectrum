import argparse
from pathlib import Path
import pandas as pd

from gwas.vep_utils import get_vep_data, parse_vep_results, filter_coding_variants


def main(base_dir: Path) -> None:
    df = pd.read_csv(base_dir / "Clustered_SNPS_for_gene_ontology_annotation.csv")
    snp_list = df["SNP"].tolist()

    vep_results = get_vep_data(snp_list)
    coding_variants_df = filter_coding_variants(vep_results)
    # coding_variants_df.to_csv(base_dir / "data" / "processed" / "VEP_output" / "Clustered_SNPS_for_gene_ontology_annotation_with_coding_variants.csv", index=False)

    vep_df = parse_vep_results(vep_results)
    print(vep_df)

    df = pd.merge(df, vep_df, on="SNP", how="left")
    df.to_csv(base_dir / "data" / "processed" / "VEP_output" / "Clustered_SNPS_for_gene_ontology_annotation_with_VEP.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate SNPs using Ensembl VEP")
    parser.add_argument("base_dir", type=Path, help="Base directory containing input files")
    args = parser.parse_args()
    main(args.base_dir)
