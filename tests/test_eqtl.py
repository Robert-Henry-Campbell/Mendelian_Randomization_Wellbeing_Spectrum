import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
import pandas as pd
import pytest
from unittest.mock import patch, Mock

from gwas.eqtl_checker import fetch_snp_info
from gwas.vep_utils import parse_vep_results, filter_coding_variants


@patch('gwas.eqtl_checker.requests.get')
def test_fetch_snp_info_basic(mock_get):
    mock_get.return_value = Mock(
        json=lambda: [None, None, None, [["rs123", "1", "100", "A/T"]]],
        raise_for_status=lambda: None,
    )
    gwas_df = pd.DataFrame({'RS': ['rs123'], 'A1': ['A'], 'A2': ['T']})
    result = fetch_snp_info('rs123', gwas_df)
    assert result == 'chr1_101_A_T_b38'


@patch('gwas.eqtl_checker.requests.get')
def test_fetch_snp_info_multiple_alleles(mock_get):
    mock_get.return_value = Mock(
        json=lambda: [None, None, None, [["rs456", "2", "2000", "A/T,G/C"]]],
        raise_for_status=lambda: None,
    )
    gwas_df = pd.DataFrame({'RS': ['rs456'], 'A1': ['C'], 'A2': ['G']})
    result = fetch_snp_info('rs456', gwas_df)
    assert result == 'chr2_2001_G_C_b38'


def test_parse_vep_results():
    results = [
        {
            'id': 'rs1',
            'most_severe_consequence': 'missense_variant',
            'transcript_consequences': [
                {'consequence_terms': ['missense_variant'], 'gene_id': 'GENE1', 'gene_symbol': 'G1'}
            ],
        },
        {
            'id': 'rs2',
            'most_severe_consequence': 'intergenic_variant',
            'transcript_consequences': [],
        },
    ]
    df = parse_vep_results(results)
    assert list(df['SNP']) == ['rs1', 'rs2']
    assert df.loc[0, 'Gene_ID'] == 'GENE1'
    assert pd.isna(df.loc[1, "Gene_Name"])


def test_filter_coding_variants():
    results = [
        {
            'id': 'rs1',
            'transcript_consequences': [
                {'consequence_terms': ['missense_variant'], 'gene_id': 'GENE1', 'gene_symbol': 'G1'}
            ],
        },
        {
            'id': 'rs2',
            'transcript_consequences': [
                {'consequence_terms': ['synonymous_variant'], 'gene_id': 'GENE2', 'gene_symbol': 'G2'}
            ],
        },
        {
            'id': 'rs3',
            'transcript_consequences': [
                {'consequence_terms': ['nonsense_variant'], 'gene_id': 'GENE3', 'gene_symbol': 'G3'}
            ],
        },
    ]
    df = filter_coding_variants(results)
    assert list(df['SNP']) == ['rs1', 'rs3']
