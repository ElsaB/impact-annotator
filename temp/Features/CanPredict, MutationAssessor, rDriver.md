# CanDrA

* SIFT scores  
	* The SIFT algorithm uses similarity between closely related proteins to identify potentially deleterious changes
	* SIFT scores <0.05 are predicted to be deleterious and only SIFT scores with a median information content score <3.25 are included for predictions since higher values likely indicate unreliable SIFT scores

* Pfam-based lLogR.E-value
	* Predicts whether a change will alter protein function by determining the difference in fit of a wild-type version of the protein to a particular Pfam model 
	* These scores were derived from values provided by the HMMER 2.3.2 software and the ls mode was used to search against the Pfam protein family database
	* The LogR.E-value score was calculated as: log10(E-valuevariant/E-valuecanonical

* GOSS metrics
	* The GOSS metric uses the gene ontology to measure the similarity of the submitted RefSeq gene to other known cancer-causing genes

# MutationAssessor
Many mutations were tried in evolution in each sequence position sufficiently often such that the observed distributions of residues in aligned positions of homologous sequences reflect the functional constraints on these residues.", so possibility to convert the observed frequencies into a numerical estimate of the functional impact of a mutation

Phenomenological analysis that extracts information from protein family alignments of large numbers of homologous sequences grouped into aligned sets (families and subfamilies) and exploits 3D structures of sequence homologs.
Our use of evolutionary information for this purpose is novel in that it includes a refined class of evolutionarily conserved residues—specificity residues—which are determined by clustering multiple sequence alignments of homologous sequences into subfamilies to analyze functional specificity on the background of conservation of overall function. The specificity residues are predominantly located on protein surfaces in known or predicted binding interfaces and often directly linked to protein functional interactions.

# rDriver
Functional impact scores and genome-wide mRNA/protein expression levels