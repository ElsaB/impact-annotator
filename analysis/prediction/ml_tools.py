import matplotlib.pyplot as plt
import numpy as np

def plot_cross_validation_ROC_curves(model, X, y, n_fold):
    # http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html

    from scipy import interp
    from sklearn.metrics import roc_curve, auc
    from sklearn.model_selection import StratifiedKFold

    # gives train/test indices to split data in train/test sets: returns 5 stratified fold (balanced: the percentage of samples foe each class is preserved)
    # see http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
    cv = StratifiedKFold(n_splits = n_fold)

    mean_fpr = np.linspace(0, 1, 100) # [0, 0.01, 0.02, ..., 0.09]
    tprs = [] # True Positive Rate for each fold
    aucs = [] # Area under ROC curve for each fold

    plt.figure(figsize = (2.5, 2.5))

    i = 0
    for train_index, test_index in cv.split(X, y):
        model.fit(X.iloc[train_index], y.iloc[train_index])
        y_pred = model.predict_proba(X.iloc[test_index])
        # y_pred: (n_samples, 2), 1st column = proba of 0, 2nd column = proba of 1
        # so y_pred[:, 1] is the probability of getting the output as 1
            
        # fpr: false positive rate
        # tpr: true positive rate
        # thresholds: probability thresholds (nunique(y_pred[:, 1]) + 1)
        fpr, tpr, thresholds = roc_curve(y.iloc[test_index], y_pred[:, 1])
        
        # because the length of fpr and tpr vary with the fold (number of thersholds  = nunique(y_pred[:, 1]) + 1), we can't just do
        # fprs.append(fpr) and tprs.append(tpr)
        
        tprs.append(interp(mean_fpr, fpr, tpr)) # linear interpolation to find the values for a 100 tpr
        tprs[-1][0] = 0.0 # threshold > 1 for the first point

        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        
        plt.plot(fpr, tpr, linewidth = 0.5, alpha = 0.4,
                 label = 'ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
        i += 1
        
    plt.plot([0, 1], [0, 1], '--r', linewidth = 0.5, alpha = 0.8, label = 'random')

    # mean ROC
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr, mean_tpr, 'b', linewidth = 1,
             label = 'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc))

    # mean std
    std_tprs = np.std(tprs, axis = 0)
    tprs_upper = mean_tpr + std_tprs # tprs_upper = np.minimum(mean_tpr + std_tprs, 1)
    tprs_lower = mean_tpr - std_tprs # tprs_lower = np.maximum(mean_tpr - std_tprs, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color = 'blue', alpha = 0.1,
                     label='$\pm$ 1 std. dev.')

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc = "lower right", prop = {'size': 4})
    
    return plt

