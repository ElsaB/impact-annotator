import numpy as np
import pandas as pd
from custom_tools import get_table

class Impact_Wrapper():

    original_categorical_features = ['Hugo_Symbol', 'Chromosome', 'Consequence', 'Variant_Type', 'Tumor_Sample_Barcode',
                                     'confidence_class', 'mut_key', 'VAG_VT', 'VAG_GENE', 'VAG_EFFECT', 'VEP_Consequence',
                                     'VEP_SYMBOL', 'VEP_Amino_acids', 'VEP_VARIANT_CLASS', 'VEP_EXON', 'VEP_INTRON',
                                     'VEP_IMPACT', 'VEP_CLIN_SIG', 'sample_mut_key', 'patient_key', 'VEP_SIFT_class', 'VEP_PolyPhen_class',
                                     'VEP_in_dbSNP', 'is_a_hotspot', 'is_a_3d_hotspot', 'oncogenic', 'gene_type']


    def __init__(self, path, label, shuffle=True):
        self.impact = pd.read_csv(path, sep='\t', low_memory=False)
        self.label = label

        # shuffle data
        if shuffle:
            rng = np.random.RandomState(42)
            permutation = rng.permutation(len(self.impact))
            self.impact = self.impact.iloc[permutation]
            self.impact.reset_index(drop=True, inplace=True)


    def process(self, features):
        self.impact_processed = self.impact.copy()

        # add 'is_artefact' label
        self.impact_processed['is_artefact'] = (self.impact_processed['confidence_class'] == "UNLIKELY")

        # keep only selected features
        self.impact_processed = self.impact_processed[features + [self.label]]

        # transform categorical features to dummy features
        categorical_features = [f for f in Impact_Wrapper.original_categorical_features if f in features]
        self.impact_processed = pd.get_dummies(self.impact_processed, columns=categorical_features, sparse=True)

        self.positive_class_number = self.impact_processed[ self.impact_processed[self.label]].shape[0]
        self.negative_class_number = self.impact_processed[~self.impact_processed[self.label]].shape[0]


    def get_X_and_y(self, positive_class_index, negative_class_index, shuffle=True):
        # get selected dataset
        if positive_class_index == 'all':
            positive_class_index = range(self.positive_class_number)
        if negative_class_index == 'all':
            negative_class_index = range(self.negative_class_number)

        self.impact_selected = pd.concat([self.impact_processed[ self.impact_processed[self.label]].iloc[positive_class_index],
                                          self.impact_processed[~self.impact_processed[self.label]].iloc[negative_class_index]],
                                          ignore_index=False)

        self.selected_indexes = self.impact_selected.index

        # shuffle again
        if shuffle:
            rng = np.random.RandomState(42)
            permutation = rng.permutation(len(self.impact_selected))
            self.impact_selected = self.impact_selected.iloc[permutation]
            self.second_permutation = permutation

        # get features matrix X (n_samples x n_features) and target array y (n_samples)
        X = self.impact_selected.drop(self.label, axis=1)
        X = X.astype(float)
        y = self.impact_selected[self.label]

        return X, y


    def get_original_impact(self):
        return self.impact.loc[self.selected_indexes[self.second_permutation]]



    def print_info(X, y):
        print('X: {} | y: {}'.format(X.shape, y.shape))
        display(get_table(y))




