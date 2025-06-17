import argparse
from pathlib import Path
import requests
import pandas as pd


def get_vep_data(snp_list):
    url = "https://rest.ensembl.org/vep/human/id"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"ids": snp_list}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data: {response.status_code}, {response.text}")
    return response.json()


def parse_vep_results(vep_results):
    parsed_data = []
    for result in vep_results:
        snp_id = result["id"]
        most_severe_consequence = result.get("most_severe_consequence", "N/A")
        gene_id = None
        gene_name = None
        for cons in result.get("transcript_consequences", []):
            if most_severe_consequence in cons.get("consequence_terms", []):
                gene_id = cons.get("gene_id", "")
                gene_name = cons.get("gene_symbol", "")
                break
        parsed_data.append({
            "SNP": snp_id,
            "Gene_ID": gene_id,
            "Gene_Name": gene_name,
            "Most_Severe_Consequence": most_severe_consequence,
        })
    return pd.DataFrame(parsed_data)


def main(base_dir: Path) -> None:
    df = pd.read_csv(base_dir / "Clustered_SNPS_for_gene_ontology_annotation.csv")
    snp_list = df["SNP"].tolist()
    vep_results = get_vep_data(snp_list)
    vep_df = parse_vep_results(vep_results)
    df = pd.merge(df, vep_df, on="SNP", how="left")
    output_path = base_dir / "data" / "processed" / "VEP_output" / "Clustered_SNPS_for_gene_ontology_annotation_with_VEP.csv"
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate SNPs using Ensembl VEP")
    parser.add_argument("base_dir", type=Path, help="Base directory containing input files")
    args = parser.parse_args()
    main(args.base_dir)
