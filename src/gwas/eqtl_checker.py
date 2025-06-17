import requests
import pandas as pd


def fetch_snp_info(rs_id: str, gwas_df: pd.DataFrame) -> str:
    """Fetch the GTEx-style variant ID for an rsID using dbSNP.

    Parameters
    ----------
    rs_id : str
        The rsID to look up.
    gwas_df : pandas.DataFrame
        GWAS dataframe containing columns 'RS', 'A1', and 'A2'. This is used
        to determine the allele order when multiple alleles are returned.

    Returns
    -------
    str
        Variant ID string in the format expected by GTEx (e.g.
        ``chr1_12345_A_T_b38``).
    """
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
