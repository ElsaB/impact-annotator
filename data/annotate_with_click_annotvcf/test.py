import pandas as pd

impact = pd.read_csv('small_impact_1000.txt', sep = '\t')
impact = impact[['Chromosome', 'Start_Position', 'Reference_Allele', 'Tumor_Seq_Allele2']]

impact['ID'] = '.'
impact['QUAL'] = '.'
impact['FILTER'] = '.'
impact['INFO'] = '.'
impact['FORMAT'] = '.'

impact = impact[['Chromosome', 'ID', 'Start_Position', 'Reference_Allele', 'Tumor_Seq_Allele2', 'QUAL', 'FILTER', 'INFO', 'FORMAT']]
impact.columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
