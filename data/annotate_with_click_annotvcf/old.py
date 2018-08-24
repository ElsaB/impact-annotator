from pysam import FastaFile
import pandas as pd

ref = FastaFile('/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta')

vcf = pd.read_csv("temp/small_impact.vcf", sep = "\t", comment = "#", header = None)
vcf.columns = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"]


is_insertion = vcf.REF == '-'


def get_precedent_base_insertion(chrom, start):
	return ref.fetch(reference = chrom, start = start - 1, end = start)

vcf.loc[is_insertion,'REF'] = vcf.loc[is_insertion,].apply(lambda x: get_precedent_base_insertion(x.CHROM, x.POS), axis = 1)
vcf.loc[is_insertion,'ALT'] = vcf.loc[is_insertion,].apply(lambda x: get_precedent_base_insertion(x.CHROM, x.POS) + x.ALT, axis = 1)

vcf.loc[is_insertion,]



is_deletion = vcf.ALT == '-'

def get_precedent_base_deletion(chrom, start):
	return ref.fetch(reference = chrom, start = start - 2, end = start - 1)

vcf.loc[is_deletion,'REF'] = vcf.loc[is_deletion,].apply(lambda x: get_precedent_base_deletion(x.CHROM, x.POS) + x.REF, axis = 1)
vcf.loc[is_deletion,'ALT'] = vcf.loc[is_deletion,].apply(lambda x: get_precedent_base_deletion(x.CHROM, x.POS), axis = 1)

vcf.loc[is_deletion,]



vcf.to_csv("temp/small_impact.vcf", sep = "\t", index = False, header = False)

