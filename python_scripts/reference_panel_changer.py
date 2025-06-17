import argparse
import requests


def fetch_snp_info(rs_id: str) -> str:
    url = f"https://clinicaltables.nlm.nih.gov/api/snps/v3/search?terms={rs_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    chromosome = data[3][0][1]
    position = str(int(data[3][0][2]) + 1)
    allele_change = data[3][0][3]
    if len(allele_change) != 3:
        raise ValueError("Allele change is not of length 3")
    variant_id = f"chr{chromosome}_{position}_{allele_change[0]}_{allele_change[-1]}_b38"
    print(variant_id)
    return variant_id


def main(rs_id: str) -> None:
    fetch_snp_info(rs_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert rsID to b38 variant id")
    parser.add_argument("rs_id", help="rsID to query")
    args = parser.parse_args()
    main(args.rs_id)
