from pysam import FastaFile
import pandas as pd
import sys

ref = FastaFile('/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta')


impact = pd.read_csv(sys.argv[1], sep = '\t')
impact = impact[['Chromosome', 'Start_Position', 'Reference_Allele', 'Tumor_Seq_Allele2']]

impact['ID'] = '.'
impact['QUAL'] = '.'
impact['FILTER'] = '.'
impact['INFO'] = '.'
impact['FORMAT'] = '.'

impact = impact[['Chromosome', 'Start_Position', 'ID', 'Reference_Allele', 'Tumor_Seq_Allele2', 'QUAL', 'FILTER', 'INFO', 'FORMAT']]
impact.columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']



is_insertion = impact.REF == '-'

def get_precedent_base_insertion(chrom, start):
	return ref.fetch(reference = chrom, start = start - 1, end = start)

impact.loc[is_insertion,'REF'] = impact.loc[is_insertion,].apply(lambda x: get_precedent_base_insertion(x.CHROM, x.POS), axis = 1)
impact.loc[is_insertion,'ALT'] = impact.loc[is_insertion,].apply(lambda x: get_precedent_base_insertion(x.CHROM, x.POS) + x.ALT, axis = 1)

impact.loc[is_insertion,]



is_deletion = impact.ALT == '-'

def get_precedent_base_deletion(chrom, start):
	return ref.fetch(reference = chrom, start = start - 2, end = start - 1)

impact.loc[is_deletion,'REF'] = impact.loc[is_deletion,].apply(lambda x: get_precedent_base_deletion(x.CHROM, x.POS) + x.REF, axis = 1)
impact.loc[is_deletion,'ALT'] = impact.loc[is_deletion,].apply(lambda x: get_precedent_base_deletion(x.CHROM, x.POS), axis = 1)
impact.loc[is_deletion,'POS'] -= 1

impact.loc[is_deletion,]


impact.drop_duplicates(inplace = True)


impact.to_csv(sys.argv[2], sep = "\t", index = False, header = False)