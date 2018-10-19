import numpy as np
import pandas as pd
from custom_tools import get_table

class Impact_Wrapper():

    original_categorical_features = ['Hugo_Symbol', 'Chromosome', 'Consequence', 'Variant_Type', 'Tumor_Sample_Barcode',
                                     'confidence_class', 'mut_key', 'VAG_VT', 'VAG_GENE', 'VAG_EFFECT', 'VEP_Consequence',
                                     'VEP_SYMBOL', 'VEP_Amino_acids', 'VEP_VARIANT_CLASS', 'VEP_EXON', 'VEP_INTRON',
                                     'VEP_IMPACT', 'VEP_CLIN_SIG', 'sample_mut_key', 'patient_key', 'VEP_SIFT_class', 'VEP_PolyPhen_class',
                                     'VEP_in_dbSNP', 'is_a_hotspot', 'is_a_3d_hotspot', 'oncogenic', 'gene_type']


    def __init__(self, path, label):
        self.impact = pd.read_csv(path, sep='\t', low_memory=False)

        # shuffle data
        rng = np.random.RandomState(42)
        permutation = rng.permutation(len(self.impact))
        self.impact = self.impact.iloc[permutation]
        self.impact.reset_index(drop=True, inplace=True)

        self.label = label


    def process(self, features):
        self.impact_processed = self.impact.copy()
        
        self.impact_processed['is_artefact'] = (self.impact_processed['confidence_class'] == "UNLIKELY")

        self.impact_processed = self.impact_processed[features + [self.label]]

        categorical_features = [f for f in Impact_Wrapper.original_categorical_features if f in features]
        self.impact_processed = pd.get_dummies(self.impact_processed, columns=categorical_features, sparse=True)


        self.positive_class_number = self.impact_processed[self.impact_processed[self.label]].shape[0]
        self.neegative_class_number = self.impact_processed[~self.impact_processed[self.label]].shape[0]


    def get_X_and_y(self, positive_class_index, negative_class_index):
        # get selected dataset
        if positive_class_index == 'all':
            positive_class_index = range(self.positive_class_number)
        if negative_class_index == 'all':
            negative_class_index = range(self.neegative_class_number)


        self.impact_selected = pd.concat([self.impact_processed[self.impact_processed[self.label]].iloc[positive_class_index],
                                          self.impact_processed[~self.impact_processed[self.label]].iloc[negative_class_index]],
                                          ignore_index=True)

        # get features matrix X (n_samples x n_features) and target array y (n_samples)
        X = self.impact_selected.drop(self.label, axis=1)
        X = X.astype(float)
        y = self.impact_selected[self.label]

        return X, y


    def print_info(X, y):
        print('X: {} | y: {}'.format(X.shape, y.shape))
        display(get_table(y))
