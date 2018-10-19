import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn
from sklearn.metrics import roc_curve, confusion_matrix, precision_recall_curve
from sklearn.model_selection import cross_validate, learning_curve
import time

# run_model_old() only
from sklearn.metrics import auc, roc_auc_score


# old run_model(), not safe to use, not commented, will be removed soon
# the whole cross-validation and metrics evaluation was done by hand without using cross_validate
def run_model_old(model, X, y, cv_strategy, grid_search=False):
    print('Run model')

    metrics = pd.DataFrame(index=range(cv_strategy.get_n_splits()),
                           columns=['fit_time', 'score_time',
                                    'train_accuracy', 'test_accuracy',
                                    'train_roc_auc', 'test_roc_auc',
                                    'test_fpr', 'test_tpr',
                                    'gs_best_parameters', 'gs_cv_results'])
    metrics.index.name = 'fold_number'
    
    i = 0
    
    # for each fold
    for train_index, test_index in cv_strategy.split(X, y):
        print('  - fold %d/%d...' % (i + 1, cv_strategy.get_n_splits()), end='')
        (X_train, X_test) = (X.iloc[train_index], X.iloc[test_index])
        (y_train, y_test) = (y.iloc[train_index], y.iloc[test_index])

        
        # Fit model
        start = time.time()
        model.fit(X_train, y_train)
        y_train_pred = model.predict_proba(X_train)[:, 1]
        y_test_pred  = model.predict_proba(X_test) [:, 1]        
        metrics.iloc[i].fit_time = time.time() - start
        
        # Get scores
        start = time.time()
        
        # accuracy
        metrics.iloc[i].train_accuracy = np.mean(model.predict(X_train) == y_train)
        metrics.iloc[i].test_accuracy  = np.mean(model.predict(X_test)  == y_test)

        # auc
        fpr, tpr, thresholds = roc_curve(y_train, y_train_pred) # fpr: false positive rate, tpr: true positive rate
        metrics.iloc[i].train_roc_auc = auc(fpr, tpr)

        fpr, tpr, thresholds = roc_curve(y_test , y_test_pred)
        metrics.iloc[i].test_roc_auc = auc(fpr, tpr)
        metrics.iloc[i].test_fpr = fpr
        metrics.iloc[i].test_tpr = tpr
    
        if grid_search:
            metrics.iloc[i].gs_best_parameters = model.best_params_
            metrics.iloc[i].gs_cv_results = model.cv_results_

        metrics.iloc[i].score_time = time.time() - start

        print(' done! (%.2fs)' % (metrics.iloc[i].fit_time + metrics.iloc[i].score_time))

        i += 1
        
    return metrics



# plot learning curves
# strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html
def plot_learning_curves(model, X, y, cv_strategy, figsize=(10, 10), n_jobs=1):
    print('Run learning curves computation...', end='')
    start = time.time()

    # set plot
    plt.figure(figsize=figsize)
    plt.title('Learning curves')
    plt.xlabel('Number of training examples')
    plt.ylabel('ROC AUC score')

    # get metrics
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, train_sizes=np.linspace(0.1, 1, 10), scoring='roc_auc', cv=cv_strategy, n_jobs=n_jobs, error_score='raise')
    train_scores_mean = np.mean(train_scores, axis=1)
    test_scores_mean  = np.mean(test_scores , axis=1)
    test_scores_std   = np.std(test_scores  , axis=1)
    train_scores_std  = np.std(train_scores , axis=1)

    # plot metrics and their standard deviations
    plt.plot(train_sizes, train_scores_mean, 'o-', color='r', markersize = 10, label='mean train score')
    plt.plot(train_sizes, test_scores_mean , 'o-', color='g', markersize = 10, label='mean test score')
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std,
                     alpha=0.1, color='r', label='mean train score $\pm$ 1 std. dev.')
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std,
                     alpha=0.1, color='g', label='mean test score  $\pm$ 1 std. dev.')
    
    plt.legend(loc='best', prop={'size': figsize[0] * 1.5})

    print(' done! (%.2fs)' % (time.time() - start))



# work in progress...
def plot_features_importance(model, X, y, random_forest=False, figsize=(20, 8)):
    model.fit(X, y)
    
    feature_importance = pd.DataFrame({'value': model.feature_importances_.tolist()}, index=X.columns.tolist())
    feature_importance.sort_values(by='value', axis=0, inplace=True)
    
    if random_forest:
        feature_importance['inter_tree_variability'] = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
    else:
        feature_importance['inter_tree_variability'] = 0
    
    plt.figure(figsize=figsize)
    
    plt.subplot(1, 2, 1)
    feature_importance.tail(15).value.plot.barh(width=0.85, xerr=feature_importance.tail(15).inter_tree_variability)
        
    plt.subplot(1, 2, 2)
    feature_importance.value.plot.barh(width=0.85, xerr=feature_importance.inter_tree_variability)
    plt.tight_layout()




# work in progress...
def get_impact_ready_for_classification(impact, label, features):
    # keep the selected features
    impact['is_artefact'] = impact.confidence_class == "UNLIKELY"
    impact = impact[features + [label]]

    # transform categorical features
    original_categorical_features = ['Hugo_Symbol', 'Chromosome', 'Consequence', 'Variant_Type', 'Tumor_Sample_Barcode',
                                     'confidence_class', 'mut_key', 'VAG_VT', 'VAG_GENE', 'VAG_EFFECT', 'VEP_Consequence',
                                     'VEP_SYMBOL', 'VEP_Amino_acids', 'VEP_VARIANT_CLASS', 'VEP_EXON', 'VEP_INTRON',
                                     'VEP_IMPACT', 'VEP_CLIN_SIG', 'sample_mut_key', 'patient_key', 'VEP_SIFT_class', 'VEP_PolyPhen_class',
                                     'VEP_in_dbSNP', 'is_a_hotspot', 'is_a_3d_hotspot', 'oncogenic', 'gene_type']
    categorical_features = [f for f in original_categorical_features if f in features]
    impact = pd.get_dummies(impact, columns=categorical_features, sparse=True)

    # shuffle data
    rng = np.random.RandomState(42)
    permutation = rng.permutation(len(impact))
    impact = impact.iloc[permutation]
    impact.reset_index(drop=True, inplace=True)

    return impact


# work in progress...
def get_X_and_y(impact, label, negative_class_index):
    # get selected dataset
    if negative_class_index == 'all':
        negative_class_index = range(impact[~impact[label]].shape[0])

    impact_selected = pd.concat([impact[impact[label]],
                                 impact[~impact[label]].iloc[negative_class_index]], ignore_index=True)

    # get features matrix X (n_samples x n_features) and target array y (n_samples)
    X = impact_selected.drop(label, axis=1)
    X = X.astype(float)
    y = impact_selected[label]
    
    return (X, y)







